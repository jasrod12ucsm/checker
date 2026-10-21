# Artículo: estructura y fuentes

El artículo cuenta **Desarrollo y evaluación del checker**. En palabras de la
consigna: *explicar cómo se modeló la invalidación y comparar precisión,
exhaustividad y F1 entre CSA y CSA con el checker*. Esta sección del libro
reúne lo que el artículo necesita:

- [Trabajos relacionados y aporte](aportes.md): qué hacen las otras
  herramientas, con referencias, y qué hace este trabajo que ellas no. Incluye
  las amenazas a la validez.
- [El modelo en una figura](modelo.md): el diagrama único del apartado III.B.

## ¿Dónde va el diagrama único?

En **III.B (Desarrollo del checker)**. La figura no muestra las etapas del
proyecto, que van en III.A como texto o tabla. Muestra el **mecanismo**: cómo
la norma decide la validez de un handle en cada camino y cómo la misma norma
produce las etiquetas que miden al checker. Por eso tiene que ser una sola,
general y completa: norma → obtener → mutar → usar → evaluación.

## Estructura propuesta

| Apartado | Contenido | De dónde sale en el libro | Cifras y figuras |
|---|---|---|---|
| **I. Introducción** | problema (usar un handle invalidado es UB, CTR51-CPP) → dificultad (depende del contenedor, la categoría, la posición y a veces del estado) → enfoque técnico (plugin de CSA, norma como datos) → panorama → objetivo y aportes → organización | [Por qué se rehízo el diseño](../diseno/critica.md), [La lógica de la detección](../diseno/logica.md), [aportes §4](aportes.md#4-frase-de-aporte-para-el-artículo-borrador) | CSA: 0 de 200 referencias y punteros sostenidos |
| **II. Trabajos relacionados** | antecedentes específicos → comparación → necesidad | [aportes §1 y §2](aportes.md) | tabla comparativa (una tabla, con referencias) |
| **III.A Procedimiento general** | etapas: viabilidad, norma, banco y referencia, incrementos I1 a I5, evaluación; diseño de la comparación (misma plataforma y opciones, sólo cambia el checker) | [7.6 Plan de incrementos](../construccion/7-6-incrementos.md), [Metodología](../metodologia.md) | tabla de etapas |
| **III.B Desarrollo del checker** | alcance normativo (C++17, 10 contenedores, 3 categorías) → modelo de invalidación (**la figura**) → implementación (plugin, núcleo puro, `NoteTag`, garantías, escape) | [modelo](modelo.md), [5.5 Estados](../diseno/cap5/5-5-estados.md), [Significado y leyes](../diseno/leyes.md), [7.1 Código](../construccion/7-1-codigo.md) | **figura del modelo**; 101 mutaciones, 348 reglas |
| **III.C Evaluación experimental** | banco y etiquetas (750 casos, JOIN, validación dinámica) → entorno (LLVM 21.1.8, libstdc++ 13.3, Docker) → configuraciones (Reference, Silent, Possibly) → protocolo (una invocación por caso, SARIF, cotejo por sitio, incidentes aparte) → métricas (P, R, F1; tabla `POLICY` aparte) → pruebas complementarias (código real, defectos sembrados) | [Reglas y escenarios](../banco/reglas-escenarios.md), [Protocolo dinámico](../banco/protocolo-dinamico.md), [Experimento](../resultados/experimento.md), [Código real](../resultados/codigo-real.md) | 852 ejecuciones, 0 contradicciones; 3 000 ejecuciones, 0 incidentes |

La consigna pide comparar P, R y F1, así que el artículo necesita también los
apartados que siguen a la metodología:

| Apartado | Contenido | Fuente |
|---|---|---|
| **IV. Resultados** | tabla P/R/F1 por configuración; desglose por categoría de handle; `POLICY`; garantías; tiempo (+0.3 %) y memoria (+0.7 %); código real | [modelo, tabla final](modelo.md#resultado-que-la-figura-explica), [Experimento](../resultados/experimento.md) |
| **V. Discusión y amenazas** | por qué CSA no ve referencias y punteros; circularidad del banco; alcance | [aportes §3](aportes.md#3-lo-que-no-se-puede-afirmar-amenazas-a-la-validez) |
| **VI. Conclusiones y trabajo futuro** | correr cppcheck, Infer y Clang *Lifetime Safety* sobre el banco; `std::string`; C++20 | [7.7 Estado actual](../construccion/7-7-estado.md) |

## El artículo redactado

Fuentes en `articulo/` del repositorio:

| Archivo | Qué es |
|---|---|
| `articulo/articulo.tex` | el artículo, clase oficial `IEEEtran` v1.8b en modo `conference` |
| `articulo/refs.py` | escribe las referencias en el orden de su primera cita, con los formatos de la *IEEE Reference Guide* V 3.28.2025 |
| `articulo/IEEEtran.cls` | la clase, tal como se distribuye en CTAN |
| `articulo/stfloats.sty` | permite la Tabla I al pie de la página (generado desde `sttools` de CTAN; la imagen `texlive:latest-medium` no lo trae) |
| `articulo/version_corta.py` | genera `articulo_intro_metodologia.tex`: solo Introducción y Metodología (sin resumen, palabras clave, trabajos relacionados, resultados, discusión ni conclusiones) |
| `articulo/word/` | genera los dos Word con formato de congreso IEEE: `generar.sh`, `tex2json.py` (lee el `.tex`) y `build.js` (arma el `.docx` con la biblioteca `docx`) |

Compilar:

```bash
cd articulo
python3 refs.py articulo.tex articulo.tex
docker run --rm -u $(id -u):$(id -g) -v $PWD:/w -w /w texlive/texlive:latest-medium \
  sh -c 'pdflatex articulo.tex && pdflatex articulo.tex'
```

Decisiones de formato y por qué:

- **Citas sin rangos.** La guía V 3.28.2025 ya no admite «[1]–[4]»: exige
  «[1], [2], [3], [4]». Por eso `cite` se carga con `nocompress`.
- **`babel` con `es-nolayout`.** La maquetación española reemplaza la
  numeración de IEEE («III-A.» en vez de «A.», «1)»). Con `es-nolayout` se
  conservan la de IEEE, la separación silábica y los nombres en español.
- **Nombres de los componentes:** «Resumen», «Palabras clave», «Fig. 1.»,
  «TABLA I», «Referencias».
- **Referencias a mano** (no `IEEEtran.bst`, que es de 2015): cada una sigue el
  formato básico de su tipo en la guía vigente, con las abreviaturas de su
  lista oficial; las palabras que la lista no trae van completas.
- **La figura del modelo está en TikZ:** vectorial, en Times como el texto, en
  escala de grises para impresión. Es el mismo contenido que
  [el modelo en una figura](modelo.md).
- **Columnas equilibradas** en la última página con `\IEEEtriggeratref{23}`.
- **Texto de la figura en 8 pt como mínimo** (`\footnotesize`), el tamaño mínimo que IEEE pide para gráficos.
- **Métricas con dos decimales** (1.00, 0.23): con punto decimal en un texto en español, «1.000» se leería como mil.
- **Referencias de software con versión** (cppcheck v2.22.0, el *commit* del PR de Clang), como pide la guía siguiendo FORCE11.

## Los Word

`articulo/word/generar.sh` produce, desde los mismos `.tex`:

- `articulo.docx`: el artículo completo, 6 páginas.
- `articulo_intro_metodologia.docx`: solo I. Introducción y II. Metodología,
  4 páginas. Sus referencias son solo las citadas (22) y van renumeradas en
  orden de aparición (`refs.py ... --solo-citadas`). El párrafo que anuncia
  la organización del artículo se reescribe para las dos secciones.

Formato: carta; márgenes de 0.75 in arriba, 1 in abajo y 0.625 in a los
lados; dos columnas de 3.5 in separadas por 0.25 in; Times New Roman de
10 pt; título de 24 pt; resumen y palabras clave de 9 pt en negrita;
encabezados I. en versalitas centradas, A. en cursiva y 1) en cursiva
dentro del párrafo; figura, tablas y referencias de 8 pt. La Fig. 1 y la
Tabla I ocupan el ancho de la página, en una sección de una columna. La
figura y las ecuaciones son imágenes de 600 ppp compiladas desde el mismo
TikZ y las mismas ecuaciones del `.tex`, para que se vean igual que en el
PDF; para editarlas hay que cambiar el `.tex` y regenerar.

## Revisión de la metodología y de la introducción

- **La metodología no lleva resultados.** Salieron de III y de la Fig. 1, y
  ahora están al inicio de IV: el tamaño de la tabla normativa (101
  mutaciones, 348 reglas), las 40 pruebas unitarias con 92.5 % de cobertura
  y los 30 avisos esperados, las 852 ejecuciones sin contradicciones y las
  27 etiquetas corregidas. En III queda el procedimiento: qué se verifica,
  cómo, y qué se hace ante una contradicción. La composición del banco (750
  casos, 342/306/102) se queda en III porque es el diseño de la muestra.
- **Toda afirmación de la introducción lleva referencia.** La oración que
  cerraba el párrafo de CSA («ninguna de las fuentes revisadas separa…») no
  citaba nada. Ahora dice qué hace cada herramienta, con su cita: tratan como
  siempre invalidante una inserción que depende de la capacidad [12], [13],
  [14] o solo modelan `std::vector` [15]; la evaluación más cercana usa un
  banco hecho a mano [15], y los bancos generados toman sus etiquetas de
  defectos inyectados o de comparar analizadores [16], [17].

Pendiente de los autores: el bloque de autores de la plantilla admite un
correo u ORCID por autor; se agregan si el congreso lo pide. El papel es
carta (el de la plantilla); si el congreso pide A4, se cambia con la opción
`a4paper`.

Al verificar las referencias en Crossref apareció un error en la tesis: el DOI
de Kashyap et al. (2019) era `10.1109/SCAM.2019.00019`, que corresponde a
otro artículo. El correcto es `10.1109/SCAM.2019.00020`; quedó corregido en el
artículo y en el Word.
