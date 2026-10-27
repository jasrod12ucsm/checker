"""Fragmentos de código para el libro y el Word: una función, prueba o rango de líneas de un archivo."""
import re


def fragmento(ruta, simbolo):
    lineas = open(ruta, encoding="utf-8").read().split("\n")
    if re.fullmatch(r"\d+-\d+", simbolo):
        ini, fin = (int(x) for x in simbolo.split("-"))
        return ini, lineas[ini - 1:fin]
    if simbolo.startswith('"'):  # la línea que contiene ese texto, p. ej. @prueba("…")
        pat = re.compile(re.escape(simbolo))
    elif ruta.endswith(".py"):
        pat = re.compile(rf"^(\s*)(def|class) {re.escape(simbolo)}\b")
    elif ruta.endswith(".ts"):  # función, método, clase, interfaz, tipo o constante con ese nombre
        pat = re.compile(rf"^\s*(export )?(async )?(function |class |interface |type |const |static )?{re.escape(simbolo)}\b\s*[(<:=]")
    elif "," in simbolo:
        pat = re.compile(rf"^TEST\({re.escape(simbolo)}\)")
    else:
        pat = re.compile(rf"^\S.*\b{re.escape(simbolo)}\s*\(.*[^;]\s*$")
    for i, l in enumerate(lineas):
        if pat.search(l) if simbolo.startswith('"') else pat.match(l):
            break
    else:
        raise SystemExit(f"libro: no encuentro {simbolo!r} en {ruta}")
    if ruta.endswith(".py"):
        d = i
        while lineas[d].lstrip().startswith("@"):  # decoradores: el bloque es el def que sigue
            d += 1
        sangria = len(lineas[d]) - len(lineas[d].lstrip())
        j = d + 1
        while j < len(lineas) and (not lineas[j].strip() or len(lineas[j]) - len(lineas[j].lstrip()) > sangria):
            j += 1
        while not lineas[j - 1].strip():
            j -= 1
        return i + 1, lineas[i:j]
    prof, abierto = 0, False
    for j in range(i, len(lineas)):
        sin_cadenas = re.sub(r'"(\\.|[^"\\])*"|\'(\\.|[^\'\\])*\'|//.*', "", lineas[j])
        prof += sin_cadenas.count("{") - sin_cadenas.count("}")
        abierto = abierto or "{" in sin_cadenas
        if not abierto and sin_cadenas.rstrip().endswith(";"):  # p. ej. `type X = A | B;`
            return i + 1, lineas[i:j + 1]
        if abierto and prof <= 0:
            return i + 1, lineas[i:j + 1]
    raise SystemExit(f"libro: llaves sin cerrar en {simbolo!r} de {ruta}")
