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
bench/informe/generar.sh bench/informe/base/Proyecto_Fin_de_Carrera_V2.docx Proyecto_Fin_de_Carrera.docx
```

`generar.sh` arma el Word del proyecto en dos pasadas. La primera ejecuta
`bench/informe/build_v4.py`, que toma la plantilla V2 de la universidad (no está en el
repositorio) y reemplaza portada, resumen, capítulos 1 a 7, glosario y referencias con el
contenido del libro: `libro/informe` (portada, capítulos 1 a 3, glosario y referencias),
`libro/diseno/cap4`, `cap5`, `cap6` y `libro/construccion`; los diagramas salen de
`libro/diagramas/png` y los *mockups* de `libro/mockups`. Luego convierte el documento a PDF
con LibreOffice y `bench/informe/paginas.py` lee en qué página cayó cada título, tabla y
figura; la segunda pasada vuelve a generar el Word con esos números en el índice general, el
índice de tablas y el índice de figuras. Después del capítulo 8 (que incluye 8.6 Documentación y 8.7
Soporte y mantenimiento) van las conclusiones (`libro/informe/conclusiones.md`), las recomendaciones
(`recomendaciones.md`), el glosario, las referencias y los apéndices (`apendices.md`: cronograma,
estándares y reproducción), como pide la guía de la Práctica 12. El sistema Centinela C++ es el centro del documento y
el checker es su motor. Es una herramienta de los autores: quien no tenga la V2 no la
necesita para usar el sistema ni el checker.

El manual de instalación y uso que se entrega en PDF junto al informe se arma con las páginas del
libro ya construidas (presentación del sistema, puesta en marcha con GitHub, panel, API y guía del
checker); necesita Google Chrome o Chromium:

```bash
python3 bench/gen_book.py && mdbook build corpus_book
python3 bench/informe/manual.py ~/Downloads/Centinela_Manual_Instalacion_y_Uso.pdf
```

## El plan de tesis

```bash
bench/tesis/render.sh                 # bench/tesis/fig/*.puml → fig/png; necesita Java y plantuml.jar
python3 bench/tesis/graficos.py       # figuras f5-*.png del capítulo V y test/experimento/costo.json; necesita matplotlib y scipy
python3 bench/tesis/generar_tesis.py bench/tesis/base/Plan_de_Tesis_Cap1_V3.docx Plan_de_Tesis.docx
```

Los documentos de partida están en el repositorio: `bench/tesis/base/Plan_de_Tesis_Cap1_V3.docx`
para la tesis y `bench/informe/base/Proyecto_Fin_de_Carrera_V2.docx` para el proyecto. Los
generadores no los modifican: trabajan sobre una copia y escriben el resultado en la ruta de salida.

La tesis trata solo del checker: no menciona Centinela C++ ni la revisión de *commits*
históricos. `generar_tesis.py` no toca el documento de origen. Sobre una copia cambia el título,
reemplaza el capítulo IV (`bench/tesis/contenido_cap4.py`), inserta las figuras y tablas de los
capítulos I a III y ordena el capítulo III según la rúbrica de los capítulos III y IV
(`bench/tesis/contenido_cap1a3.py`). Después renumera tablas y figuras y arma los índices con las
páginas que da LibreOffice. Los comentarios de revisión del documento se conservan. Las figuras de
la tesis están en `bench/tesis/fig/` y no son las del libro: estas últimas nombran el servicio. Los
valores obtenidos no van en el capítulo IV, sino en el V. El capítulo V (5.1 a 5.8), las
conclusiones y las recomendaciones salen de `bench/tesis/contenido_cap5.py` y se insertan antes del
cronograma. Las secciones 5.1 a 5.5 siguen los objetivos específicos OE1 a OE5, y la 5.6 presenta
el código real como complemento. Las conclusiones van una por objetivo, más una del objetivo
general. Cada cifra sale de un archivo de `test/`, que se nombra en la nota de su tabla. Las figuras del capítulo V las genera `bench/tesis/graficos.py` con matplotlib, en estilo APA:
sin título dentro de la imagen, ejes con su unidad, decimales con coma y la paleta validada para
daltonismo, con tramas para leerse en blanco y negro. El script comprueba con `assert` que cada
valor coincida con el que publica la tesis, y calcula la prueba de Wilcoxon y la de Shapiro-Wilk
del tiempo por caso. El análisis inferencial es no paramétrico: McNemar exacta, bootstrap y Wilcoxon,
justificados en 3.4.4.

El capítulo III queda con 3.1 Alcances y limitaciones, 3.2 Enfoque, tipo y nivel, 3.3 Universo,
población y muestra, 3.4 Metodología, técnicas e instrumentos (3.4.1 a 3.4.5) y 3.5 Consideraciones
éticas. El capítulo IV queda con 4.1 Generalidades y 4.2 Esquema de la solución y desarrollo del
prototipo, cuyas subsecciones 4.2.1 a 4.2.9 van del esquema de componentes al alcance previsto y su
avance. El cuarto nivel de títulos (por ejemplo, 4.2.3.2) usa un estilo que añade el generador y no
entra en los índices. Dentro de `contenido_cap1a3.py`, los textos de la V3 y los anteriores a
`renumerar` citan las secciones con la numeración antigua: esa función las convierte a la nueva. Lo
que se escribe después de ella, y todo `contenido_cap4.py`, ya usa la nueva.

## La demostración del video

La demostración del prototipo está en `video/`. Necesita git, Docker con Compose y Python 3, y corre
desde cualquier carpeta donde se haya clonado el repositorio:

```bash
git clone https://github.com/jasrod12ucsm/checker.git
cd checker
docker compose build     # una sola vez: descarga LLVM 21 (imagen de unos 2 GB)
./video/demo.sh 1        # compila el checker y corre sus pruebas; va antes que los demás pasos
./video/demo.sh 2        # Clang sin el checker sobre video/demo.cpp
./video/demo.sh 3        # con el checker, política Silent
./video/demo.sh ruta     # la ruta del primer aviso
./video/demo.sh 4        # con el checker, política Possibly
./video/demo.sh 5        # banco y experimento registrado
./video/demo.sh 6        # código real y defectos sembrados
./video/demo.sh 7        # verificación completa de los requerimientos
```

Los pasos 5 y 6 leen los resultados guardados en `test/`; no vuelven a ejecutar el experimento.

## El análisis estadístico

```bash
python3 bench/analisis_estadistico.py
```

Lee `test/experimento/cotejo.json` y `test/corpus_truth.json`, y solo usa la biblioteca estándar.
Escribe `test/experimento/contraste.json`, con la prueba exacta de McNemar por separado en los
casos `UB` y `SAFE` y el intervalo bootstrap del 95 % de ΔF1 (10 000 réplicas, semilla fija), y
`test/experimento/resultados.xlsx`, la hoja de resultados por condición, contenedor, operación,
clase de handle y forma, que se abre con Excel o LibreOffice Calc.

## La evaluación económica

```bash
python3 bench/informe/evaluacion_economica.py
```

Calcula la inversión, los flujos, el VAN, la TIR, la sensibilidad y el umbral de adopción del
capítulo 3 del informe. Cada parámetro del script lleva su fuente en un comentario, y la tabla
«Parámetros del análisis y sus fuentes» del capítulo 3 los reúne con su cita.

## El artículo

```bash
cd articulo
python3 refs.py articulo.tex articulo.tex          # referencias en orden de cita, formato IEEE
docker run --rm -u $(id -u):$(id -g) -v $PWD:/w -w /w texlive/texlive:latest-medium \
  sh -c 'pdflatex articulo.tex && pdflatex articulo.tex'
./word/generar.sh                                  # articulo.docx, articulo_intro_metodologia.docx y articulo_titulo_introduccion.docx
```

`version_titulo_intro.py` saca la versión con solo el título, los autores y la Introducción (con sus
referencias renumeradas), que se entregó como primer avance del artículo; se compila igual con
`articulo_titulo_introduccion.tex`.

Ver [Artículo: estructura y fuentes](../articulo/index.md) para las
decisiones de formato.

`articulo/paper_centinela.tex` es el artículo del proyecto completo, el
checker y el servicio Centinela C++, en el mismo formato de congreso IEEE.
Sus cifras salen de `articulo.tex`, de `test/experimento/contraste.json`
(McNemar y *bootstrap*) y del capítulo 8 (pruebas del servicio). Se compila
igual, con `paper_centinela.tex` en lugar de `articulo.tex`; sus referencias
están escritas en el propio archivo, en el orden de la primera cita.
