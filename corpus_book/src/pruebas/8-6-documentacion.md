# 8.6 Documentación

La documentación de Centinela C++ se organiza por destinatario, siguiendo la
norma ISO/IEC/IEEE 26514:2022, que pide identificar a quién va dirigida cada
pieza de información, qué tarea le permite cumplir y en qué medio se entrega
(International Organization for Standardization et al., 2022b). Toda la documentación está en el repositorio
`github.com/jasrod12ucsm/checker` y se versiona con el código. Las cifras y
los fragmentos de código no se copian a mano: el libro los genera desde los
resultados y desde el código fuente (7.1.6).

## Documentos por destinatario

Tabla: Documentación del proyecto por destinatario

| Documento | Destinatario | Para qué sirve | Dónde está | Formato |
|---|---|---|---|---|
| Guía rápida | administrador que instala el servicio | construir la imagen, levantar la demostración y correr las pruebas | `README.md` | Markdown |
| Puesta en marcha con GitHub | administrador | crear el token, configurar las variables de `sistema/.env.ejemplo`, conectar el repositorio y exponer la URL del *webhook* | libro, *Sistema → Ponerlo en marcha con GitHub* | HTML (mdBook) |
| Manual del panel | desarrollador y administrador | ingresar, administrar usuarios y repositorios, consultar revisiones y clasificar hallazgos | libro, *Sistema → El panel web*, y capítulo 6 | HTML y Word |
| Referencia de la API | integrador | cada ruta HTTP con su método, cuerpo, respuesta y errores | libro, *Sistema → API HTTP*, y sección 6.7 | HTML y Word |
| Guía del checker | desarrollador de C++ | usar `ucsm.ContainerInvalidation` desde Clang, elegir la política `Silent` o `Possibly` y leer un aviso | libro, *Guía de uso* | HTML |
| Documentación técnica | equipo de mantenimiento | arquitectura, decisiones de diseño, leyes del modelo, base de datos y control de versiones | capítulos 5 a 7 y libro, *Sistema* | Word y HTML |
| Documentación del código | equipo de mantenimiento | comentarios de cada tipo, función pública y puerto | código del servicio (`/** … */`) y del motor (`///`) | en el código |
| Diagramas | equipo de mantenimiento | fuente editable de cada diagrama del informe | `libro/diagramas/*.puml` | PlantUML, SVG y PNG |
| Pruebas y evidencias | asesor y jurado | qué se probó, cómo se repite y con qué resultado | capítulo 8 y `sistema/no-funcionales/resultados/` | Word y JSON |
| Informe del proyecto | universidad | el presente documento | `bench/informe/generar.sh` | Word y PDF |
| Artículo IEEE | comunidad académica | el checker y el servicio en formato de congreso | `articulo/paper_centinela.tex` | LaTeX y PDF |
| Demostración | asesor y jurado | el flujo completo en pasos numerados | `video/demo.sh` | guion de consola |

## Cómo se mantiene al día

La documentación vive en el mismo repositorio que el código y pasa por el
mismo *pull request*, de modo que un cambio de funcionalidad y su
documentación se revisan juntos. El libro se regenera con
`python3 bench/gen_book.py`. Si un fragmento citado con
`{{codigo RUTA SÍMBOLO}}` deja de existir, el libro no se genera, y así la
documentación no puede quedar citando código que ya no está. El informe se
genera desde el libro con `bench/informe/generar.sh`, que también recalcula
las páginas de los índices. Por lo tanto, el libro, el informe y el código
no pueden divergir sin que la generación lo detecte.

## Documentos que se entregan en PDF

Tabla: Documentos entregados en PDF

| Archivo | Contenido |
|---|---|
| Informe del proyecto (Word y PDF) | capítulos 1 a 8, conclusiones, recomendaciones, referencias y apéndices |
| Manual de instalación y uso (PDF) | la presentación del sistema, la puesta en marcha con GitHub, el panel web, la API HTTP y la guía del checker, tomados del libro con `bench/informe/manual.py` |
| Artículo IEEE (PDF) | el artículo del proyecto completo |
