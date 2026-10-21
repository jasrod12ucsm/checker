# Libro, informe y artículo

Estos pasos corren **fuera** de la imagen, con Python 3 en tu máquina.

## Este libro

```bash
python3 bench/render_diagramas.py   # libro/diagramas/*.puml → svg (libro) y png (Word); necesita Java y plantuml.jar
python3 bench/gen_book.py           # arma corpus_book/src desde test/ y libro/
mdbook serve corpus_book --open     # lo abre en http://localhost:3000
```

`gen_book.py` hace dos cosas. Escribe las páginas que salen de los datos (los
casos, los resultados, la matriz) y copia las páginas escritas a mano de
`libro/` a `corpus_book/src/`. **Se edita `libro/`, nunca `corpus_book/src/`**:
lo que escribas allí se pierde en la siguiente generación.

Al copiar, cada línea `{{codigo RUTA SÍMBOLO}}` se reemplaza por ese
fragmento del código fuente, con un enlace a la línea en GitHub. Así el
libro muestra siempre el código vigente, y si una función cambia de nombre el
libro deja de generarse. El símbolo puede ser una función, un
`TEST(Suite, Nombre)`, un texto entre comillas (la prueba `@prueba("…")`
que lo contiene) o un rango de líneas `10-20`:

[`bench/gen_book.py:1183`](https://github.com/jasrod12ucsm/checker/blob/main/bench/gen_book.py#L1183-L1219)

```python
def fragmento(ruta, simbolo):
    lineas = open(ruta, encoding="utf-8").read().split("\n")
    if re.fullmatch(r"\d+-\d+", simbolo):
        ini, fin = (int(x) for x in simbolo.split("-"))
        return ini, lineas[ini - 1:fin]
    if simbolo.startswith('"'):  # la línea que contiene ese texto, p. ej. @prueba("…")
        pat = re.compile(re.escape(simbolo))
    elif ruta.endswith(".py"):
        pat = re.compile(rf"^(\s*)(def|class) {re.escape(simbolo)}\b")
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
        if abierto and prof <= 0:
            return i + 1, lineas[i:j + 1]
    raise SystemExit(f"libro: llaves sin cerrar en {simbolo!r} de {ruta}")
```

PlantUML se busca en `$PLANTUML_JAR` o en `~/.local/share/plantuml/plantuml.jar`.
No necesita Graphviz.

## El Word del proyecto

`bench/informe/build_v4.py` arma `Proyecto_Fin_de_Carrera_V4.docx`.
Parte de la versión V2 del documento de la universidad, que no está en el
repositorio, y reemplaza los capítulos 4, 5 y 7 con el contenido de
`libro/diseno/cap4`, `libro/diseno/cap5` y `libro/construccion`, y los
diagramas con `libro/diagramas/png`. Es una herramienta de los autores:
quien no tenga la V2 no la necesita para usar el checker.

## El artículo

```bash
cd articulo
python3 refs.py articulo.tex articulo.tex          # referencias en orden de cita, formato IEEE
docker run --rm -u $(id -u):$(id -g) -v $PWD:/w -w /w texlive/texlive:latest-medium \
  sh -c 'pdflatex articulo.tex && pdflatex articulo.tex'
./word/generar.sh                                  # articulo.docx y articulo_intro_metodologia.docx
```

Ver [Artículo: estructura y fuentes](../articulo/index.md) para las
decisiones de formato.
