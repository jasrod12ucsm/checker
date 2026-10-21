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

{{codigo bench/gen_book.py fragmento}}

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
