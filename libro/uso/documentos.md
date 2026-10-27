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

{{codigo bench/fragmentos.py fragmento}}

PlantUML se busca en `$PLANTUML_JAR` o en `~/.local/share/plantuml/plantuml.jar`.
No necesita Graphviz.

## El Word del proyecto

```bash
bench/informe/generar.sh ~/Downloads/Proyecto_Fin_de_Carrera_V2.docx ~/Downloads/Proyecto_Fin_de_Carrera_V6.docx
```

`generar.sh` arma el Word del proyecto en dos pasadas. La primera ejecuta
`bench/informe/build_v4.py`, que toma la plantilla V2 de la universidad (no está en el
repositorio) y reemplaza portada, resumen, capítulos 1 a 7, glosario y referencias con el
contenido del libro: `libro/informe` (portada, capítulos 1 a 3, glosario y referencias),
`libro/diseno/cap4`, `cap5`, `cap6` y `libro/construccion`; los diagramas salen de
`libro/diagramas/png` y los *mockups* de `libro/mockups`. Luego convierte el documento a PDF
con LibreOffice y `bench/informe/paginas.py` lee en qué página cayó cada título, tabla y
figura; la segunda pasada vuelve a generar el Word con esos números en el índice general, el
índice de tablas y el índice de figuras. El sistema Centinela C++ es el centro del documento y
el checker es su motor. Es una herramienta de los autores: quien no tenga la V2 no la
necesita para usar el sistema ni el checker.

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
