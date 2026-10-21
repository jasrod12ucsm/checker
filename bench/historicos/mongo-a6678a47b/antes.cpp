// Extracto fiel de mongo src/mongo/s/cursors.cpp en a6678a47b^ (el commit con el error).
// Se conservan los tipos de contenedor y cada sentencia que toca _cursors,
// _cursorsMaxTimeMS o sus iteradores, en el mismo orden. Lo demás (log, auth,
// conexiones) se reemplaza por funciones opacas que no reciben los contenedores.
// boost::shared_ptr -> std::shared_ptr; scoped_lock -> std::lock_guard.
#include <map>
#include <memory>
#include <mutex>
#include <string>

struct ShardedClientCursor {
  long long getId() const;
  long long idleTime(long long now) const;
  std::string getNS() const;
};
typedef std::shared_ptr<ShardedClientCursor> ShardedClientCursorPtr;

bool isAuthorizedForNamespace(const std::string &ns);   // authSession->isAuthorizedForActionsOnNamespace
void logKillCursorsAuthzCheck(const std::string &ns, long long id, bool ok);
void logKilling(long long id, long long idleFor);        // log() << "killing old cursor " ...
long long getElapsedTimeMillis();
const long long TIMEOUT = 600000;

class CursorCache {
public:
  typedef std::map<long long, ShardedClientCursorPtr> MapSharded;
  typedef std::map<long long, int> MapShardedInt;
  void gotKillCursor(long long id);
  void doTimeouts();

private:
  mutable std::mutex _mutex;
  MapSharded _cursors;
  MapShardedInt _cursorsMaxTimeMS;
};

// Cuerpo del bucle de gotKillCursors, para un id.
void CursorCache::gotKillCursor(long long id) {
  std::lock_guard<std::mutex> lk(_mutex);
  MapSharded::iterator i = _cursors.find(id);
  if (i != _cursors.end()) {
    const bool isAuthorized = isAuthorizedForNamespace(i->second->getNS());
    logKillCursorsAuthzCheck(i->second->getNS(), id, isAuthorized);
    if (isAuthorized) {
      _cursors.erase(i);
      _cursorsMaxTimeMS.erase(i->second->getId());
    }
    return;
  }
}

void CursorCache::doTimeouts() {
  long long now = getElapsedTimeMillis();
  std::lock_guard<std::mutex> lk(_mutex);
  for (MapSharded::iterator i = _cursors.begin(); i != _cursors.end(); ++i) {
    long long idleFor = i->second->idleTime(now);
    if (idleFor < TIMEOUT) {
      continue;
    }
    logKilling(i->second->getId(), idleFor);
    _cursors.erase(i);
    _cursorsMaxTimeMS.erase(i->second->getId());
    i = _cursors.begin();
    if (i == _cursors.end())
      break;
  }
}
