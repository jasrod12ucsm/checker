#include <list>
#include <map>
#include <vector>
void clang_analyzer_dump(const void *);
template <class T> void clang_analyzer_dump(T);
void clang_analyzer_warnIfReached();

void sink(int);

void f_vec(std::vector<int> &c) {
  auto it = c.begin();
  clang_analyzer_dump(&it); // región del objeto iterador
  const int &h = *it;
  clang_analyzer_dump(&h); // región del elemento
  const int &h2 = *it;
  clang_analyzer_dump(&h2); // ¿la misma?
  auto it2 = it;
  clang_analyzer_dump(&it2);
  int &r = c[0];
  clang_analyzer_dump(&r);
  auto &d = c;
  clang_analyzer_dump(&d);
  clang_analyzer_dump(&c);
  c.push_back(1);
  sink(h);
}

void f_list(std::list<int> &c) {
  auto it = c.begin();
  if (it == c.end())
    return;
  const int &h = *it;
  clang_analyzer_dump(&h);
  c.erase(c.begin());
  sink(h);
}

void f_map(std::map<int, int> &c) {
  auto it = c.begin();
  if (it == c.end())
    return;
  auto *p = &*it;
  clang_analyzer_dump(p);
  clang_analyzer_dump(&p->second);
}
