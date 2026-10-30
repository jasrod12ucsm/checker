"""Cambios de la V4 en los capítulos I a III: figuras, tablas y la sección 3.5 completa."""
from __future__ import annotations

import copy
import re

from lxml import etree

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _reemplazar(doc, i, texto, first=0):
    nuevo = doc.p(texto, after=200, first=first)
    doc.els[i].addprevious(nuevo)
    doc.body.remove(doc.els[i])
    doc.els[i] = nuevo


def _rotulo(doc, i, id_):
    ts = list(doc.els[i].iter(W + "t"))
    ts[0].text = "CAP{T:%s}" % id_
    for t in ts[1:]:
        t.text = ""


def aplicar(doc, P, H2, H3, H4, F, T, L):
    c = doc.cambiar

    c(5, "mediante un checker para Clang Static Analyzer", "mediante un checker para el analizador de código de Clang")

    c(28, "La documentación de Clang Static Analyzer incluye", "Clang Static Analyzer es el analizador de código de Clang: examina un programa sin ejecutarlo y busca defectos mediante módulos llamados checkers o verificadores. Su documentación incluye")
    # ── marcas literales que quedaron en la V3 ──
    c(28, "`alpha.cplusplus.InvalidatedIterator`", "alpha.cplusplus.InvalidatedIterator")
    c(121, "*Standard Template Library*", "Standard Template Library")
    _reemplazar(doc, 56, "ΔF1 = F1~C~ − F1~B~")
    _reemplazar(doc, 58, "F1~B~ corresponde a la medida F1 de la configuración B, que constituye la línea base principal.")
    _reemplazar(doc, 59, "F1~C~ corresponde a la medida F1 de la configuración C, que incorpora el checker propuesto.")
    _reemplazar(doc, 61, "H~0~: ΔF1 = 0")
    _reemplazar(doc, 62, "H~1~: ΔF1 ≠ 0")

    # ── «instrumento» donde no es un instrumento de la investigación ──
    c(36, "con instrumentos dinámicos independientes", "con herramientas dinámicas independientes")
    c(45, "con instrumentos dinámicos", "con herramientas dinámicas")
    c(88, "con instrumentos independientes", "con herramientas independientes")
    c(98, "con dos instrumentos dinámicos independientes", "con dos herramientas dinámicas independientes")
    c(234, "bajo dos instrumentos dinámicos independientes", "bajo dos herramientas dinámicas independientes")
    c(234, "Estos instrumentos detectan", "Estas herramientas detectan")

    # ── la matriz de consistencia y la de operacionalización no llevan técnica ni instrumento ──
    c(109, "Método e instrumento", "Método")
    c(109, "Cuantitativo, aplicado, descriptivo-explicativo; diseño experimental intra-casos; banco de 750 casos",
      "Cuantitativo, aplicado, descriptivo-explicativo; diseño experimental intra-casos")
    c(109, "Matriz normativa; ficha de caso; validación dinámica", "Análisis documental (paso 1)")
    c(109, "Registro SARIF; ficha de resultados", "Experimental: medición de la línea base (paso 2)")
    c(109, "Código del checker; GoogleTest", "Desarrollo tecnológico incremental (paso 3)")
    c(109, "Ficha de resultados", "Experimental: comparación de políticas (paso 4)")
    c(109, "Arnés; scripts de análisis", "Experimental: contraste pareado (paso 5)")
    c(109, "p de McNemar", "valor p")
    c(110, "Fuente: elaboración propia.", "Los pasos se describen en la sección 3.5.1. Fuente: elaboración propia.")
    c(115, "Escala e instrumento", "Escala")
    c(115, "Nominal; protocolo experimental", "Nominal")
    c(115, "Razón; ficha de resultados y arnés", "Razón")
    c(115, "Razón; ficha de resultados", "Razón")
    _nota_op = doc.els[116]
    c(116, "Fuente: elaboración propia.", "Nota. El instrumento que registra cada indicador se indica en la sección 3.5.3. La robustez y el costo (caídas, avisos revisados, semillas, tiempo y memoria) se registran como indicadores secundarios y no intervienen en la decisión sobre H0. Fuente: elaboración propia.")

    # ── los SARIF se leen y se descartan: lo que se conserva son los avisos normalizados ──
    c(70, "Los registros conservan todos los avisos originales.", "Los registros conservan todos los avisos de cada ejecución.")
    c(269, "Los diagnósticos se almacenaron sin modificar, en formato SARIF (*Static Analysis Results Interchange Format*), asociados al identificador del caso.",
      "El analizador entregó sus diagnósticos en formato SARIF (Static Analysis Results Interchange Format), y cada aviso se registró completo, asociado al identificador del caso.")
    c(273, "los registros originales", "los registros de ejecución")
    c(358, "los registros originales", "los registros de ejecución")
    c(354, "Los cálculos se realizaron con scripts en Python sobre los registros SARIF originales, de modo que cualquier tabla del capítulo de resultados puede regenerarse a partir de los datos crudos.",
      "Los cálculos se realizaron con dos scripts en Python, bench/experimento.py y bench/analisis_estadistico.py, a partir de los registros de ejecución y de cotejo, de modo que cualquier tabla del capítulo de resultados puede regenerarse desde esos datos. El segundo script exporta los resultados a una hoja de cálculo.")

    # ── números de tabla ──
    for i, id_ in ((72, "var"), (107, "consistencia"), (113, "operacionalizacion"), (221, "pares"), (258, "contraste"), (484, "cronograma")):
        _rotulo(doc, i, id_)
    c(106, "La Tabla 2", "La {T:consistencia}")
    c(112, "La Tabla 3", "La {T:operacionalizacion}")
    c(220, "(Tabla 4)", "({T:pares})")
    c(225, "de la Tabla 4", "de la {T:pares}")
    c(483, "La Tabla 13", "La {T:cronograma}")

    # ── capítulo I ──
    doc.tras(23, [
        P("La {F:f1-realocacion} muestra el caso más conocido: un iterador que designa un elemento de un std::vector deja de ser válido cuando una inserción agota la capacidad y el contenedor traslada sus elementos a otro bloque de memoria."),
        F("f1-realocacion", "Invalidación de un iterador por la realocación de un std::vector",
          "Los valores son ilustrativos: la capacidad nueva depende de la implementación."),
    ])
    doc.tras(31, [
        P("La {F:f1-arbol} ordena el problema con sus causas y sus efectos. Las causas proceden de los párrafos anteriores, y los efectos se presentan como posibles, porque la investigación no midió incidentes en sistemas reales."),
        F("f1-arbol", "Árbol del problema"),
    ])
    doc.tras(71, [
        P("La {F:f1-variables} resume la relación entre las variables y las condiciones que se mantuvieron constantes."),
        F("f1-variables", "Modelo de variables del estudio"),
    ])
    doc.tras(93, [
        P("La {T:justificacion} resume cada dimensión de la justificación, lo que la investigación aporta en ella y lo que no se midió."),
        T("justificacion", "Dimensiones de la justificación", [1500, 3900, 3600], [
            ["Dimensión", "Aporte", "Lo que no se midió"],
            ["Teórica", "Reglas de invalidación organizadas y desempeño caracterizado de dos configuraciones", "Desempeño en construcciones de C++ fuera del alcance"],
            ["Social", "Información sobre qué escenarios se detectan y cuáles presentan dificultades", "Reducción de incidentes o de vulnerabilidades explotadas"],
            ["Metodológica", "Banco de 750 casos etiquetado, validado por ejecución y congelado, reutilizable con otros analizadores", "Revisión del banco por especialistas externos"],
            ["Económica", "Posible herramienta de apoyo para localizar accesos invalidados", "Costos de desarrollo, tiempos de depuración y productividad"],
            ["Tecnológica", "Checker para Clang Static Analyzer evaluado con un protocolo reproducible", "Experiencia de uso de los desarrolladores"],
        ]),
    ])
    doc.tras(100, [
        P("La {F:f1-solucion} presenta los componentes de la solución y su relación con la comparación principal. La norma alimenta por separado las etiquetas del banco y las reglas del checker, y las dos configuraciones se evalúan con los mismos casos."),
        F("f1-solucion", "Visión general de la solución"),
    ])
    doc.tras(104, [
        P("La {T:viabilidad} resume esas cuatro dimensiones."),
        T("viabilidad", "Viabilidad de la investigación", [1500, 7500], [
            ["Dimensión", "Condición que la sustenta"],
            ["Técnica", "Conocimientos de C++ y de Clang Static Analyzer; carga de checkers externos como complementos sin modificar el compilador"],
            ["Temporal", "Desarrollo por incrementos, con resultados medibles en cada etapa"],
            ["Material", "Computadora personal (Intel Core i7-13620H, 16 GB de memoria, Ubuntu 24.04) y contenedor Docker reproducible"],
            ["Económica", "Herramientas de software libre, sin costos de licencia"],
        ]),
    ])

    # ── capítulo II ──
    doc.tras(119, [
        P("La {F:f2-linea} ordena en el tiempo los antecedentes que se describen a continuación."),
        F("f2-linea", "Línea cronológica de los antecedentes"),
    ])
    doc.tras(132, [
        P("La {T:antecedentes} compara los antecedentes según su enfoque, la forma en que fueron evaluados y lo que aportan a esta investigación."),
        T("antecedentes", "Comparación de los antecedentes", [1750, 2450, 2500, 2300], [
            ["Trabajo", "Enfoque", "Evaluación informada", "Aporte a esta investigación"],
            ["Gregor y Schupp (2006)", "Analizador STLlint, dirigido a la STL y a bibliotecas genéricas", "No se usa como referencia cuantitativa", "Representar la semántica de la biblioteca dentro del analizador"],
            ["Pataki (2012)", "Iteradores que comprueban su validez durante la ejecución", "Ejemplos de código y discusión de limitaciones", "Conservar el vínculo entre iterador y contenedor"],
            ["Horváth et al. (2017)", "Metaprogramación, patrones sobre el árbol de sintaxis y GDB", "Implementaciones y ejemplos; sin precisión ni exhaustividad", "Distinguir los patrones del código de los cambios de estado"],
            ["Lipp et al. (2022)", "Estudio de seis analizadores estáticos para C", "27 proyectos y 192 vulnerabilidades; omisiones entre 47 % y 80 %", "Fijar la unidad con que se cuenta una detección"],
            ["Li et al. (2024)", "Scasa, sobre Clang Static Analyzer: tamaño de contenedores secuenciales y destino de iteradores", "2230 fragmentos y 8 proyectos; 72 de 125 reportes correctos", "Infraestructura y modelado cercanos a la propuesta"],
            ["Teodorescu y Lucanu (2024)", "Marco de flujo de datos para use-after-free, con tipos propietarios, punteros y valores", "102 pruebas en tres estilos de programación", "Efecto de la representación del tiempo de vida en los errores"],
            ["Liu et al. (2025)", "IKOS4VecErr: interpretación abstracta sobre std::vector", "503 de 505 defectos manuales; 16 errores nuevos en 5 proyectos", "Representar propiedades específicas del contenedor"],
        ], "Las cifras corresponden a conjuntos y condiciones diferentes y no son comparables entre sí."),
    ])
    doc.tras(147, [
        P("La {T:clang} reúne los mecanismos de Clang descritos en esta sección y el límite documentado de cada uno."),
        T("clang", "Mecanismos de Clang relacionados con el problema", [2500, 3300, 3200], [
            ["Mecanismo", "Qué atiende", "Límite documentado u observado"],
            ["InvalidatedIterator", "Usos de iteradores invalidados", "Pertenece al grupo experimental"],
            ["IteratorRange", "Accesos fuera del rango permitido", "Pertenece al grupo experimental"],
            ["MismatchedIterator", "Iteradores de contenedores diferentes", "Pertenece al grupo experimental"],
            ["ContainerModeling", "Modelado de assign, clear, push_back, pop_back, push_front, pop_front, insert, emplace, erase y erase_after", "handlePushBack no distingue allí la capacidad disponible"],
            ["cplusplus.InnerPointer", "Punteros al almacenamiento interno", "Se limita a std::string y no reconoce std::string_view"],
            ["Clang Lifetime Safety", "Punteros, referencias, vistas e iteradores, con análisis intraprocedural y contratos", "La invalidación es experimental; las llamadas sin contrato pueden tratarse de forma optimista"],
        ]),
    ])
    doc.tras(153, [
        P("La {T:enfoques} sitúa la propuesta frente a los tres enfoques especializados revisados."),
        T("enfoques", "Enfoques especializados frente a la propuesta", [1900, 2300, 2400, 2400], [
            ["Enfoque", "Técnica de análisis", "Contenedores", "Accesos que representa"],
            ["Scasa (Li et al., 2024)", "Ejecución simbólica sobre Clang Static Analyzer", "Secuenciales", "Iteradores y tamaño del contenedor"],
            ["IKOS4VecErr (Liu et al., 2025)", "Interpretación abstracta sobre IKOS", "std::vector", "Iteradores y tamaño del vector"],
            ["Teodorescu y Lucanu (2024)", "Flujo de datos sobre el grafo de flujo de control", "Tipos propietarios en general", "Punteros y su relación con el propietario"],
            ["Checker propuesto", "Ejecución simbólica sobre Clang Static Analyzer", "Diez contenedores de tres familias", "Iteradores, referencias y punteros a elementos"],
        ]),
    ])
    doc.tras(157, [
        P("La {F:f2-dimensiones} muestra las tres dimensiones que determinan la regla aplicable a un acceso retenido."),
        F("f2-dimensiones", "Dimensiones semánticas de la comparación"),
    ])
    doc.tras(162, [
        P("La {T:analisis} resume esas decisiones y su consecuencia."),
        T("analisis", "Decisiones de un análisis estático y su consecuencia", [2100, 2300, 2300, 2300], [
            ["Decisión", "Opción más económica", "Opción más precisa", "Consecuencia"],
            ["Alcance", "Intraprocedural: el cuerpo de una función", "Interprocedural: relaciones entre llamadas", "Cadenas más largas, con más estados"],
            ["Caminos", "Insensible: fusiona estados de ramas distintas", "Sensible: conserva restricciones por ruta", "Evita combinar estados incompatibles"],
        ], "Clang Static Analyzer pertenece a la categoría sensible a caminos."),
    ])
    doc.tras(165, [
        P("La {F:f2-simbolica} ilustra la bifurcación: cada condición divide el estado y cada camino acumula su restricción."),
        F("f2-simbolica", "Bifurcación de caminos en la ejecución simbólica", "Ejemplo elaborado para ilustrar el concepto."),
    ])
    doc.tras(169, [
        P("La {F:f2-csa} resume ese flujo y el lugar que ocupan los checkers: reciben eventos del motor y le devuelven estado."),
        F("f2-csa", "Flujo de análisis de Clang Static Analyzer"),
    ])
    doc.tras(174, [
        P("La {F:f2-familias} agrupa en tres familias los contenedores del alcance, y la {T:handles} distingue las tres clases de acceso que se estudian."),
        F("f2-familias", "Familias de contenedores del alcance"),
        T("handles", "Clases de acceso a un elemento", [1500, 3300, 4200], [
            ["Clase", "Qué representa", "Ejemplos de obtención"],
            ["Iterador", "Una posición; admite operaciones según su categoría y puede representar el final de la secuencia", "c.begin(), c.find(k)"],
            ["Referencia", "Un alias del elemento", "const auto& h = \\*it; c.front(); c[i]"],
            ["Puntero", "La dirección del elemento", "&\\*it; &c[i]; c.data()"],
        ]),
    ])
    doc.tras(183, [
        P("La {T:reglas} resume, por familia, las reglas de C++17 que se describieron en esta sección."),
        T("reglas", "Reglas de invalidación de C++17 por familia", [1800, 3700, 3500], [
            ["Contenedor", "Inserción", "Borrado"],
            ["std::vector", "Con realocación invalida iteradores, referencias y punteros; sin ella, solo los que están en el punto o después", "Invalida lo que está en el punto o después"],
            ["std::deque", "En un extremo invalida iteradores y conserva referencias; en el interior invalida todo", "En un extremo, solo lo borrado; en el interior, todo"],
            ["std::list, std::forward_list", "Conserva todo", "Solo lo borrado"],
            ["Asociativos ordenados", "Conserva todo", "Solo lo borrado"],
            ["Asociativos no ordenados", "Con rehash invalida iteradores y conserva referencias y punteros; sin rehash conserva todo", "Solo lo borrado"],
        ], "Síntesis de ISO/IEC JTC1/SC22/WG21 (2017), secciones [vector.modifiers], [deque.modifiers], [list.modifiers], [forwardlist.modifiers], [associative.reqmts] y [unord.req]."),
    ])
    doc.tras(188, [
        P("La {F:f2-owner} aplica esas categorías a un contenedor y sus handles."),
        F("f2-owner", "Relación Owner/Pointer en un contenedor", "Adaptación de las categorías de Sutter (2019) al dominio de esta investigación."),
    ])
    doc.tras(194, [
        P("La {F:f2-tres} presenta esas tres situaciones."),
        F("f2-tres", "Las tres situaciones de una regla que depende del estado"),
    ])
    doc.tras(200, [
        P("La {F:f2-confusion} presenta esos cuatro conteos con las etiquetas de esta investigación."),
        F("f2-confusion", "Matriz de confusión de un caso con etiqueta binaria", "VP: verdadero positivo; FN: falso negativo; FP: falso positivo; VN: verdadero negativo."),
    ])

    # ── capítulo III ──
    doc.tras(229, [
        P("La {F:f3-alcance} resume lo que se incluyó y lo que se dejó fuera."),
        F("f3-alcance", "Alcance de la investigación"),
    ])
    doc.tras(234, [
        P("Además, como el banco sirvió de prueba de regresión durante el desarrollo, el checker se ajustó con los mismos casos con que se evaluó. Por ello, los resultados sobre el banco no estiman su desempeño en programas no vistos. La evaluación en código real atiende esa limitación solo en parte, porque esos proyectos tampoco fueron del todo ajenos al desarrollo: avisos en rocksdb y en ninja motivaron cambios en el checker (decisiones D-21 y D-23), y dos semillas motivaron el modo de análisis empleado (D-22)."),
        P("Las etiquetas del banco y la tabla de reglas del checker salen, además, de la misma matriz normativa. Esto evita que apliquen dos versiones de la norma, pero un error de la matriz afectaría a ambas y no se reflejaría en las métricas. Por ello, el banco mide si el checker aplica las reglas en programas analizados y no si las reglas son correctas. Ese riesgo se atiende con la cláusula citada en las reglas que invalidan o dependen del estado y con la validación dinámica, que puede contradecir una etiqueta SAFE o POLICY, pero no confirma todos los casos UB."),
        P("La {T:limitaciones} reúne las limitaciones descritas y cómo se atendió cada una."),
        T("limitaciones", "Limitaciones y forma de atenderlas", [2900, 3000, 3100], [
            ["Limitación", "Efecto posible", "Cómo se atendió"],
            ["Exploración incompleta de caminos y código no disponible", "Defectos no detectados aunque la regla esté modelada", "Medición por forma sintáctica; incidencias registradas aparte"],
            ["Condiciones que dependen del estado", "Falsas alarmas u omisiones", "Política de aproximación y análisis aparte de los casos POLICY"],
            ["Versión de Clang y de C++", "Los resultados no se generalizan a otras versiones", "Entorno fijo y versiones registradas"],
            ["Casos mínimos", "No reproducen la complejidad de aplicaciones reales", "Evaluación complementaria en cuatro proyectos"],
            ["Sin revisión de especialistas externos", "Etiquetas sin juicio de terceros", "Trazabilidad a la norma y validación dinámica"],
            ["El banco sirvió de prueba de regresión durante el desarrollo", "Los resultados sobre el banco no estiman el desempeño en programas no vistos", "Etiquetas derivadas de la norma; evaluación complementaria en código real, que lo atiende solo en parte, porque también motivó ajustes del checker"],
            ["Etiquetas y checker salen de la misma matriz", "Un error de la matriz no se refleja en las métricas", "Cláusula en las reglas que invalidan o dependen del estado, y validación dinámica"],
            ["Posición del acceso frente al punto de la operación", "Antes, en y después se evaluaron solo en las posiciones de prueba de cada par", "Se informa por par contenedor–operación"],
        ]),
    ])
    doc.tras(254, [
        P("La {T:enfoque} resume estas elecciones y la razón de cada una."),
        T("enfoque", "Enfoque, tipo y nivel de la investigación", [1100, 1700, 3300, 2900], [
            ["Rasgo", "Elección", "Razón, según la pregunta y los objetivos", "Evidencia prevista"],
            ["Enfoque", "Cuantitativo", "La pregunta principal y el OE5 piden diferencias de precisión, exhaustividad y F1, que se expresan en números", "Conteos por caso y condición, métricas y valor p"],
            ["Tipo", "Aplicada", "El OE3 y el OE4 desarrollan y evalúan una solución para un problema concreto", "Checker verificado y su desempeño frente a la configuración de referencia"],
            ["Nivel", "Descriptivo y explicativo", "El OE2 caracteriza el desempeño del analizador, y el OE5 examina el cambio asociado con el checker", "Métricas y causas de omisión de B; pares discordantes entre B y C"],
            ["Diseño", "Experimental intra-casos", "Cada caso se analiza bajo todas las condiciones y es su propio control (sección 3.3.1)", "Resultado pareado de cada caso en cada condición"],
        ]),
        P("Los tres elementos son consistentes entre sí. Como el problema es de ingeniería y tiene solución verificable, la investigación es aplicada; como esa solución se juzga con mediciones, el enfoque es cuantitativo; y como primero se caracteriza la configuración de referencia y luego se compara con la que incorpora el checker, en condiciones controladas, el nivel es descriptivo y explicativo."),
    ])
    doc.tras(262, [
        P("La {F:f3-diseno} representa el diseño: el mismo banco pasa por todas las condiciones y el contraste se hace caso por caso."),
        F("f3-diseno", "Esquema del diseño intra-casos"),
    ])
    doc.tras(274, [
        P("La {F:f3-procedimiento} muestra el orden de las etapas."),
        F("f3-procedimiento", "Etapas del procedimiento experimental", "Las etapas 3 y 4 avanzaron en paralelo: los 66 casos de buen uso se añadieron cuando el checker ya existía, y la validación de los 750 casos terminó antes de la etapa 5."),
        P("La {T:fases} reúne la secuencia con las actividades, el producto y la orden que permite repetir cada fase dentro del entorno del repositorio. La evaluación de la propuesta corresponde a las fases 4 y 5."),
        T("fases", "Fases, actividades, productos y orden para repetirlas", [1500, 3050, 2050, 2400], [
            ["Fase", "Actividades", "Producto", "Orden para repetirla"],
            ["1. Banco", "Registrar las reglas, generar los casos, revisar las etiquetas y validarlas por ejecución", "Matriz, banco y registro de validación", "python3 bench/gen_corpus.py; python3 bench/run_runtime_validation.py"],
            ["2. Entorno", "Fijar versiones y checkers activos en la imagen", "Imagen checker:llvm21", "docker compose build"],
            ["3. Checker y política", "Desarrollar por incrementos, con pruebas en cada uno", "Complemento verificado", "docker compose run --rm plugin"],
            ["4. Medición", "Ejecutar las cuatro condiciones con el banco sellado y cotejar los avisos", "Registro de ejecución, cotejo y métricas", "docker compose run --rm experimento"],
            ["5. Contraste", "Calcular McNemar y el intervalo, y exportar la hoja", "contraste.json y resultados.xlsx", "python3 bench/analisis_estadistico.py"],
            ["6. Complemento", "Analizar cuatro proyectos y sembrar defectos", "Registro de código real", "python3 bench/codigo_real.py; python3 bench/inyeccion.py"],
        ], "Las órdenes se ejecutan desde la raíz del repositorio; bench/codigo_real.py y bench/inyeccion.py reciben además la carpeta de los proyectos y el archivo de salida."),
    ])
    doc.tras(288, [
        P("La {F:f3-poblacion} muestra cómo se pasa del universo al banco."),
        F("f3-poblacion", "Del universo al banco de casos"),
    ])

    # ── sección 3.5: un solo lugar para método, técnicas, instrumentos y herramientas ──
    doc.quitar(322, 327)
    doc.quitar(329, 333)
    doc.quitar(335, 349)
    doc.tras(321, [
        P("En esta sección se distinguen cuatro términos. El método es la ruta general con que se obtuvo el conocimiento; la técnica, el procedimiento concreto con que se recogieron los datos; el instrumento, el «recurso que utiliza el investigador para registrar información o datos sobre las variables» (Hernández-Sampieri y Mendoza, 2018, p. 228); y la herramienta, el programa que ejecuta o automatiza una técnica. El analizador evaluado no se trató como instrumento, sino como el objeto que se mide."),
        P("La investigación siguió la ruta cuantitativa y combinó tres métodos. El análisis documental estableció las condiciones esperadas conforme a las reglas del lenguaje. La especificación de C++17 fue la fuente normativa principal; la documentación de LLVM/Clang y la regla CTR51-CPP del estándar de codificación SEI CERT C++ (Software Engineering Institute, 2024) se utilizaron como apoyo para comprender las capacidades del analizador y contextualizar el problema, sin sustituir el criterio normativo. El desarrollo tecnológico incremental (Sommerville, 2020) produjo el checker. El método experimental permitió modificar de manera controlada la configuración del analizador y observar los resultados mediante indicadores cuantitativos, con las demás condiciones constantes."),
        P("Cada objetivo específico correspondió a un paso metodológico. Los pasos siguen el orden de los objetivos, pero los pasos 1 y 3 avanzaron en paralelo, porque el banco sirvió de prueba de regresión del checker; las mediciones definitivas de los pasos 2, 4 y 5 se hicieron con el banco ya sellado. La {F:f3-metodo} muestra la secuencia y la {T:metodo} indica el método, la técnica, el instrumento y la herramienta de cada paso."),
        P("El primer paso, que responde al OE1, aplicó el análisis documental. Se revisaron las reglas de invalidación de la norma N4659, se registraron en la matriz normativa y se derivaron de ella, por combinación, los casos del banco y sus etiquetas. Las etiquetas se contrastaron después con la ejecución de los casos."),
        P("El segundo paso, que responde al OE2, aplicó el método experimental para medir la línea base. La configuración B analizó el banco completo, cada caso se clasificó según su etiqueta y cada omisión se asignó a una causa."),
        P("El tercer paso, que responde al OE3, aplicó el desarrollo tecnológico incremental, con desarrollo guiado por pruebas en el núcleo de reglas. Cada incremento se cerró con su criterio de la {T:incrementos}; en los incrementos I2 a I4, ese criterio exigió además que la medición sobre el banco no mostrara regresiones. El proceso se detalla en la sección 4.2."),
        P("El cuarto paso, que responde al OE4, definió la política del checker ante las condiciones que el análisis no puede resolver y aplicó el método experimental para comparar sus dos modos sobre los mismos casos."),
        P("El quinto paso, que responde al OE5, aplicó el método experimental para contrastar las configuraciones B y C con un diseño pareado, y el plan de análisis de la sección 3.6 para decidir sobre la hipótesis. La evaluación en código real y la medición del costo son complementarias: se registraron junto con este paso, pero no responden al OE5 ni intervienen en la decisión sobre H~0~."),
        F("f3-metodo", "Pasos metodológicos por objetivo específico", "Los pasos 1 y 3 avanzaron en paralelo; las mediciones definitivas se hicieron con el banco sellado."),
        T("metodo", "Método, técnica, instrumento y herramienta por paso", [700, 1450, 1850, 1850, 1800, 1350], [
            ["Paso", "Método", "Técnica", "Instrumento", "Herramienta", "Producto"],
            ["1\nOE1", "Análisis documental", "Revisión documental estructurada; generación combinatoria; revisión lógica; validación dinámica", "Matriz normativa; ficha de caso; registro de validación dinámica", "Python; libstdc++ Debug; sanitizadores de Clang", "Banco validado y congelado"],
            ["2\nOE2", "Experimental", "Registro automatizado; observación estructurada", "Protocolo experimental; registro de ejecución; ficha de resultados", "Clang Static Analyzer; arnés", "Línea base y causas de omisión"],
            ["3\nOE3", "Desarrollo tecnológico incremental", "Prueba de leyes del modelo; programas mínimos", "Matriz normativa; registro de pruebas y decisiones", "CMake; GoogleTest; lit", "Checker verificado"],
            ["4\nOE4", "Experimental", "Registro automatizado; observación estructurada", "Protocolo experimental; registro de ejecución; ficha de resultados", "Clang Static Analyzer; arnés", "Política y su efecto medido"],
            ["5\nOE5", "Experimental", "Registro automatizado; observación estructurada; prueba de leyes del arnés; revisión manual en código real", "Protocolo experimental; registro de ejecución; ficha de resultados; hoja de resultados; registro de código real", "Arnés; scripts de análisis; hoja de cálculo", "Comparación y decisión sobre H0"],
        ]),
    ])
    doc.tras(328, [
        P("Se utilizaron ocho técnicas, que la {T:tecnicas} resume. La revisión documental estructurada examinó las reglas de invalidación de C++17 y organizó sus condiciones según el contenedor, la operación, el mecanismo de acceso y el estado relevante. También se revisó la documentación técnica de Clang Static Analyzer para establecer las características de las configuraciones."),
        P("La generación combinatoria produjo los casos a partir de la matriz normativa, con todas las combinaciones de par contenedor–operación, clase de handle y forma sintáctica, de modo que ningún caso de la matriz se eligió a mano. La validación dinámica ejecutó cada caso con herramientas que detectan el defecto al ejecutar el programa, para contrastar las etiquetas con un criterio ajeno al analizador. La revisión lógica calculó de dos maneras una misma expresión pequeña del modelo para encontrar contradicciones entre las reglas (sección 4.4.4)."),
        P("La prueba de leyes comprobó automáticamente las propiedades que el modelo debe cumplir para cualquier valor, y los programas mínimos comprobaron el comportamiento del checker dentro del analizador. Estos dos procedimientos, que la {T:tecnicas} agrupa, produjeron los datos de verificación del tercer paso."),
        P("El registro automatizado obtuvo los diagnósticos de cada condición sobre cada caso con parámetros fijados de antemano, lo que corresponde a la recolección mediante instrumentos electrónicos que describen Hernández-Sampieri y Mendoza (2018, p. 225). La observación estructurada contrastó después cada aviso con la etiqueta y el sitio de uso del caso: un diagnóstico se consideró pertinente cuando correspondía al caso, al defecto estudiado y al punto de uso esperado, según criterios definidos antes de la evaluación. Los avisos cuya correspondencia no pudo establecerse se conservaron aparte, sin clasificarlos como detecciones correctas. En los casos SAFE, cualquier aviso confirmado cuenta como falso positivo, porque ningún handle del caso es inválido."),
        P("La revisión manual se aplicó solo a los avisos en código real, donde no existe una etiqueta previa."),
        T("tecnicas", "Técnicas de recolección de datos", [1650, 2300, 1650, 1800, 1600], [
            ["Técnica", "Qué se hizo", "Dato que produce", "Fuente", "Momento"],
            ["Revisión documental estructurada", "Lectura de las cláusulas de N4659 por contenedor y operación", "Reglas con su cláusula", "Norma N4659; documentación de LLVM/Clang", "Paso 1, antes de generar el banco"],
            ["Generación combinatoria", "Combinación de 57 pares × 3 clases de handle × 4 formas", "Casos y etiquetas", "Matriz normativa", "Paso 1, al construir el banco"],
            ["Revisión lógica", "Una misma expresión del modelo calculada de dos maneras", "Contradicciones entre reglas y etiquetas", "Reglas de etiquetado y matriz", "Paso 1, antes de la validación dinámica"],
            ["Validación dinámica", "Ejecución de cada caso con libstdc++ Debug y con sanitizadores", "Estado de cada ejecución frente a su etiqueta", "Casos del banco en ejecución", "Paso 1, antes de congelar el banco"],
            ["Prueba de leyes y programas mínimos", "Pruebas automáticas del núcleo y del arnés, y del checker dentro del analizador", "Pruebas aprobadas o fallidas", "Código del checker y del arnés", "Paso 3, en cada incremento; las del arnés, en el paso 5"],
            ["Registro automatizado", "Una invocación del analizador por caso y condición", "Avisos, resultado, tiempo y memoria", "Salida de clang++ en SARIF y datos del proceso", "Pasos 2, 4 y 5, con el banco sellado"],
            ["Observación estructurada", "Cotejo de cada aviso con la etiqueta y el sitio de uso", "VP, FP, FN, VN e incidencias", "Registro de ejecución y ficha de caso", "Pasos 2, 4 y 5, después de cada ejecución"],
            ["Revisión manual", "Lectura de cada aviso en código real y comparación de cada semilla con su resultado esperado", "Avisos revisados y semillas con el resultado esperado", "Avisos en ninja, leveldb, yaml-cpp y rocksdb", "Paso 5, después de analizar los proyectos"],
        ]),
    ])
    doc.tras(334, [
        P("Los datos se registraron en nueve instrumentos, que la {T:instrumentos} relaciona con las variables e indicadores de las secciones 1.8 y 1.9. Todos son archivos versionados en el repositorio, generados o leídos por scripts, de modo que su contenido no se transcribió a mano, salvo la matriz normativa, que es el resultado de la revisión documental."),
        P("La matriz normativa es el registro de las reglas de invalidación: contenedor, operación, punto, clase de handle, relación, efecto, condición y cláusula de la norma. La ficha de caso contiene el identificador, el contenedor, la operación, la clase de handle, la forma, la garantía, la etiqueta del caso y la de cada uno de sus handles. El registro de validación dinámica guarda, por cada ejecución, el escenario, la etiqueta y lo que observó cada herramienta."),
        P("El protocolo experimental fija la versión de Clang y de la biblioteca, los checkers activos, las opciones de cada condición, el límite de tiempo y los criterios de cotejo; las opciones de cada condición y los sellos quedan guardados junto con los resultados. El registro de ejecución guarda, por caso y condición, el resultado de la invocación, el tiempo, la memoria máxima y todos los avisos. La ficha de resultados guarda el veredicto de cada caso en cada condición, los sitios de los avisos y los avisos posibles."),
        P("La hoja de resultados es un libro de hoja de cálculo con los conteos y las métricas por condición, contenedor, operación, clase de handle y forma, además de los contrastes pareados. El registro de pruebas y decisiones reúne la salida de las pruebas del checker y las decisiones de diseño con su alternativa descartada. El registro de código real guarda las unidades analizadas, sus avisos y el resultado de cada semilla."),
        T("instrumentos", "Instrumentos de registro de datos", [1500, 2000, 2300, 2500, 700], [
            ["Instrumento", "Archivo", "Variable o indicador que registra", "Aplicación", "Paso"],
            ["Matriz normativa", "norma/matriz.json", "Efecto de cada regla; base de las etiquetas", "Se completó durante la revisión documental; la leen el generador de la tabla y el del banco", "1, 3"],
            ["Ficha de caso", "test/corpus.cpp y test/corpus_truth.json", "Etiqueta normativa de cada caso", "La genera bench/gen_corpus.py desde la matriz, antes de medir", "1"],
            ["Registro de validación dinámica", "test/runtime_validation_results.json", "Concordancia de etiquetas", "Lo escribe bench/run_runtime_validation.py en cada ejecución", "1"],
            ["Protocolo experimental", "Sección 3.3.2 y bloque meta de test/experimento/ejecucion.json", "Configuración (B, C, D) y política (Silent, Possibly)", "Se fijó antes de medir; el arnés guarda sus valores al iniciar", "2, 4, 5"],
            ["Registro de ejecución", "test/experimento/ejecucion.json", "Avisos, incidencias, tiempo y memoria", "Lo escribe el arnés en cada invocación", "2, 4, 5"],
            ["Ficha de resultados", "test/experimento/cotejo.json, metricas.json y test/corpus_fallos.json", "VP, FP, FN, VN; avisos posibles; cobertura sobre el handle sostenido; causas de omisión", "La calcula el arnés al cotejar cada aviso con su caso", "2, 4, 5"],
            ["Hoja de resultados", "test/experimento/resultados.xlsx y contraste.json", "Precisión, exhaustividad, F1; ΔF1, pares discordantes, valor p e intervalo", "La exporta bench/analisis_estadistico.py después del cotejo", "5"],
            ["Registro de pruebas y decisiones", "Salida de GoogleTest y lit; libro/diseno/decisiones.md", "Reglas modeladas; pruebas aprobadas", "Las pruebas se ejecutan en cada incremento; las decisiones se anotan al tomarse", "3"],
            ["Registro de código real", "test/codigo_real/avisos.json e inyeccion.json", "Caídas, avisos revisados y semillas", "Lo escriben bench/codigo_real.py y bench/inyeccion.py; los avisos se revisan a mano", "5"],
        ]),
        P("Hernández-Sampieri y Mendoza (2018, p. 228) exigen a todo instrumento tres requisitos: confiabilidad, validez y objetividad. La {T:requisitos} indica cómo se atendió cada uno en la ficha de caso y en el banco que ella describe, de los que dependen todas las mediciones. Los demás instrumentos son registros automáticos, cuya confiabilidad procede de los sellos y del determinismo del análisis; la ficha de resultados se comprueba además con las leyes del arnés, que verifican, por ejemplo, que un fallo nunca cuente como verdadero negativo y que los conteos se reconstruyan desde el cotejo. La ausencia de una revisión por especialistas externos se declaró como limitación en la sección 3.1.2."),
        T("requisitos", "Confiabilidad, validez y objetividad del banco y del registro", [1500, 4300, 3200], [
            ["Requisito", "Cómo se atendió", "Evidencia"],
            ["Validez de contenido", "Los 684 casos de la matriz cubren todas las combinaciones del espacio delimitado, y cada etiqueta se remonta a una regla de la matriz; las reglas que invalidan o dependen del estado citan su cláusula", "norma/matriz.json; test/corpus_truth.json"],
            ["Validez de criterio", "Las etiquetas se contrastaron con la ejecución bajo dos herramientas independientes del analizador (sección 4.4.5)", "test/runtime_validation_results.json"],
            ["Confiabilidad", "El análisis es determinista, y el banco, el checker y la configuración quedan fijados por sus sellos. La integración continua vuelve a ejecutar el banco y falla si un resultado registrado empeora", "test/banco-1.json; bench/regresion.py"],
            ["Objetividad", "Las etiquetas y la clasificación salen de reglas ejecutadas por scripts, que no consultan la salida del analizador; ningún caso ni etiqueta cambió después del sello", "bench/etiquetar.py; bench/experimento.py; 11 leyes del arnés"],
        ]),
    ])

    # ── cronología real: banco y checker en paralelo; sello antes de la medición definitiva ──
    c(104, "en incrementos que entregaron primero el banco y la línea base y después el checker, de modo que cada etapa produjo resultados medibles", "en incrementos medidos contra el banco, que se congeló antes de la medición definitiva, de modo que cada etapa produjo resultados medibles")
    c(267, "lo que dio 852 ejecuciones, ninguna de las cuales contradijo la etiqueta asignada. El banco se congeló con un sello sha256 antes de medir.", "lo que dio 852 ejecuciones, cuyo resultado se presenta en la sección 5.1.")
    c(268, "El experimento se ejecutó dentro de una imagen Docker, y el banco y el checker se identificaron mediante su sello sha256.", "El experimento se ejecutó dentro de una imagen Docker. Antes de la medición definitiva, el banco se congeló con un sello sha256, y cada ejecución registra además el resumen sha256 del checker.")
    c(269, "El banco completo se ejecutó", "Con el banco sellado, el banco completo se ejecutó")
    c(270, "con un núcleo de reglas independiente de Clang generado desde la matriz normativa.", "con un núcleo independiente de Clang y una tabla de reglas generada desde la matriz normativa. El desarrollo avanzó por incrementos, en paralelo con el banco, que sirvió de prueba de regresión de cada uno.")
    c(28, "(LLVM Project, 2026)", "(LLVM Project, 2026a)")
    c(71, "de manera complementaria.", "de manera complementaria. La {T:var} resume las variables y sus indicadores.")
    c(257, "(diseño intra-casos).", "(diseño intra-casos), cuyas condiciones resume la {T:contraste}.")
    c(272, "Cada caso se clasificó como verdadero positivo, falso positivo, falso negativo o verdadero negativo, y después", "Cada caso UB o SAFE se clasificó como verdadero positivo, falso positivo, falso negativo o verdadero negativo, los casos POLICY se registraron aparte, y después")
    c(262, "Ambas producen los mismos avisos confirmados y difieren solo en los avisos posibles, que se contabilizan aparte;", "Por diseño, ambas deben producir los mismos avisos confirmados y diferir solo en los avisos posibles, que se contabilizan aparte, lo que se comprueba en la evaluación de la política (sección 4.7.5);")
    c(352, "bajo H0, b sigue una distribución binomial", "si ambas condiciones aciertan por igual, b sigue una distribución binomial")
    c(487, "La duración se expresa en semanas contadas desde la aprobación del plan.", "La duración corresponde a la planificación, en semanas; las actividades 2 a 5 se solapan porque el banco y el checker avanzaron en paralelo (sección 4.2.1).")
    c(486, "3–5", "3–11")
    c(486, "5–6", "5–11")
    c(486, "6–7", "6–11")
    c(486, "Banco de 750 casos", "684 casos de la matriz y 66 de buen uso")
    c(271, "Ningún caso ni etiqueta se modificó después de conocer la salida del analizador.", "Ningún caso ni etiqueta se modificó después del congelamiento.")
    doc.els[268].addprevious(doc.els[270])
    c(486, "Matriz de 57 pares contenedor–operación", "Matriz normativa de 101 mutaciones")
    c(486, "852 ejecuciones; banco congelado", "852 ejecuciones")
    c(486, "Medición de la línea base de Clang Static Analyzer", "Mediciones de la línea base durante el desarrollo")
    c(486, "Resultados de la configuración B", "Omisiones de la configuración B")
    c(486, "Medición experimental y evaluación en código real", "Congelamiento del banco, medición de las cuatro condiciones y evaluación en código real")
    c(486, "Resultados de C y D; código real", "Banco sellado; resultados de B, C y D; código real")

    # ── decisión sobre H0 ──
    c(63, "La hipótesis se contrastó con la prueba exacta de McNemar sobre los resultados pareados por caso, con un nivel de significación α = 0,05 (sección 3.6).", "La hipótesis se contrastó con la prueba exacta de McNemar sobre los resultados pareados por caso y con el intervalo de confianza de ΔF1, según la regla de decisión de la sección 3.6.")
    c(352, "Como los 684 casos de la matriz cubren por completo el espacio delimitado (sección 3.4.3), las métricas y la diferencia ΔF1 son valores exactos de ese espacio.", "Las métricas y la diferencia ΔF1 describen exactamente los 648 casos de etiqueta binaria (sección 3.4.3).")
    c(352, "Se fijó un nivel de significación α = 0,05, y la regla de decisión rechaza H0 cuando el valor p bilateral es menor que α. El contraste se aplicó por separado a los casos UB, que determinan la exhaustividad, y a los casos SAFE, que determinan las falsas alarmas.", "El contraste se aplicó por separado a los casos UB, que determinan la exhaustividad, y a los casos SAFE, que determinan las falsas alarmas. Como la prueba no opera sobre F1 y se aplica dos veces, H0 se decidió con ambos contrastes y con el intervalo de la diferencia: se rechaza si al menos un valor p bilateral es menor que 0,025, que corresponde a α = 0,05 con la corrección de Bonferroni para dos contrastes, y el intervalo de confianza del 95 % de ΔF1 excluye el cero. Este plan y su script se escribieron después de obtener los conteos, que no dependen de ellos porque el banco ya estaba sellado y el cotejo es automático.")
    c(353, "cuando un resultado no permite rechazar H0", "la tasa de falsos positivos y la cobertura sobre el handle sostenido se informan como indicadores complementarios, y el tiempo y la memoria se comparan con sus umbrales de 10 % y 5 % (sección 4.8.6), sin intervenir en la decisión; cuando un resultado no permite rechazar H0")

    # ── alcance: 101 mutaciones modeladas, 57 pares medidos, 648 casos en las métricas ──
    c(225, "La implementación se limitó a las operaciones de la {T:pares} y no abarca todos los comportamientos de la biblioteca estándar.", "El checker modela las 101 mutaciones de la matriz normativa: 57 corresponden a los pares de la {T:pares} y se miden en el banco, y las 44 restantes no se evaluaron con él. La implementación no abarca todos los comportamientos de la biblioteca estándar.")
    c(283, "las operaciones incluidas en la matriz normativa del proyecto", "las operaciones de la {T:pares}")
    c(288, "las métricas calculadas sobre la matriz son valores exactos del espacio delimitado y no estimaciones muestrales.", "las métricas describen exactamente los 648 casos de etiqueta binaria, 582 de la matriz y 66 de buen uso con garantía, y no son estimaciones muestrales. Los 102 casos POLICY se analizan aparte.")
    c(220, "Se excluyeron std::basic_string, std::unordered_multiset, swap,", "Quedaron fuera std::basic_string, std::unordered_multiset y std::unordered_multimap, que no se incorporaron a la matriz. También se excluyeron swap,")
    c(227, "La comparación principal se realizó entre B y C.", "La comparación principal se realizó entre B y C. Clang Lifetime Safety, descrito en la sección 2.2.2, no se incluyó en B porque es un análisis de flujo de datos del compilador y no un checker del analizador; su comparación queda fuera del alcance.")

    # ── los casos POLICY no fijan su estado en el código analizado ──
    c(171, "Cuando la regla depende del estado, el escenario incorpora la precondición correspondiente.", "Los casos cuya regla depende del estado no fijan ese estado en el código que se analiza; reciben la etiqueta POLICY, y sus dos estados se imponen solo al ejecutarlos (sección 4.4.5).")
    c(183, "los escenarios del corpus incorporan precondiciones como capacidad disponible, capacidad agotada o condiciones de carga relevantes para los contenedores no ordenados. La clasificación esperada se obtiene considerando conjuntamente la regla aplicable, el estado configurado y la clase de handle.", "los casos POLICY se ejecutan con precondiciones como capacidad disponible, capacidad agotada o condiciones de carga relevantes para los contenedores no ordenados, aunque el código que se analiza no las fija (sección 4.4.5). La clasificación esperada se obtiene considerando conjuntamente la regla aplicable, el estado y la clase de handle.")
    c(290, "se representaron mediante condiciones controladas que permitan distinguir situaciones válidas e inválidas.", "no fijan ese estado en el código analizado; sus dos estados se imponen solo al ejecutarlos en la validación dinámica.")
    c(304, ", siempre que el escenario permita establecer una clasificación normativa inequívoca.", "; estos casos reciben la etiqueta POLICY y se analizan aparte.")

    # ── términos ──
    c(70, "La unidad de evaluación es cada caso", "La unidad de análisis es cada caso")
    c(70, "La medida principal es la cobertura por caso: un caso", "El criterio principal de conteo es por caso: un caso")
    c(201, "la unidad de conteo es", "la unidad de análisis es")
    c(157, "Sin embargo, la evaluación sistemática de la primera requiere incorporar casos que distingan accesos retenidos antes, en y después de la posición afectada.", "El banco no distingue de forma sistemática los accesos retenidos antes, en y después de la posición afectada; esta dimensión se evaluó solo en las posiciones de prueba de cada par.")
    c(175, "las referencias y los punteros considerados son handles de elementos.", "se utiliza el término handle para designar un iterador, una referencia o un puntero, también llamados mecanismos de acceso. Las referencias y los punteros considerados son handles de elementos.")
    c(212, "Para esta investigación, si el denominador de una métrica es cero, se informó como no definida y se conservaron los conteos absolutos. F1 se calculó directamente mediante", "Si el denominador de una métrica es cero, la métrica no está definida y solo pueden informarse los conteos absolutos. F1 puede calcularse directamente mediante")
    c(213, "Las métricas se calcularon sobre los mismos casos para ambas configuraciones del analizador. También pueden desagregarse", "Las métricas pueden desagregarse")
    c(262, "La condición D, que retira de B los checkers experimentales alpha.cplusplus,", "La condición D, que retira de C-Possibly los checkers experimentales alpha.cplusplus,")
    c(260, "VP, FP, FN, precisión", "VP, FP, VN, FN, precisión")
    c(115, "Lista de checkers activos y opciones registradas en el protocolo", "Lista de checkers activos y opciones de la ejecución")
    c(115, "Indicadores complementarios", "Indicadores complementarios del desempeño (VD)")
    c(502, "Línea y sublínea", "Línea y sub-línea")
    c(543, "5.3 Desempeño del checker", "5.3 Implementación y verificación del checker")
    for i in range(117, 216):
        e = doc.els[i]
        texto = "".join(t.text or "" for t in e.iter(W + "t"))
        while "corpus" in texto:
            c(i, "corpus", "banco")
            texto = "".join(t.text or "" for t in e.iter(W + "t"))

    # ── plan de análisis ──
    doc.tras(354, [
        P("La {F:f3-analisis} muestra el orden del análisis y la {T:estadistica} relaciona cada pregunta con su procedimiento y su criterio de decisión."),
        F("f3-analisis", "Flujo del análisis de los datos"),
        T("estadistica", "Procedimientos de análisis por pregunta específica", [950, 2950, 2850, 2250], [
            ["Pregunta", "Indicador", "Procedimiento", "Decisión"],
            ["PE1", "Ejecuciones que contradicen su etiqueta; proporción de casos UB y POLICY en que una herramienta observó el defecto", "Conteo sobre el registro de validación", "Cero contradicciones; la proporción es descriptiva"],
            ["PE2", "VP, FP, FN, VN, P, R y F1 de B; omisiones y falsas alarmas por causa", "Estadística descriptiva", "Descriptiva, sin contraste"],
            ["PE3", "Pruebas aprobadas y reglas modeladas", "Conteo de pruebas", "Todas aprobadas"],
            ["PE4", "Avisos posibles y confirmados por política", "Comparación de C-Silent y C-Possibly", "Sin avisos posibles en SAFE; confirmados iguales"],
            ["PE5", "ΔF1, ΔR, pares discordantes, valor p e IC 95 %", "McNemar exacta y bootstrap estratificado", "Según la regla de la sección 3.6"],
        ], "P: precisión; R: exhaustividad; IC: intervalo de confianza. Hernández-Sampieri y Mendoza (2018, p. 372) ubican la prueba de McNemar entre las pruebas para datos nominales en dos muestras relacionadas."),
    ])

    # ── estructura de la rúbrica ──
    renumerar(doc)
    def tramo(a, b):
        sal, e = [], doc.els[a]
        while e is not doc.els[b]:
            sal.append(e)
            e = e.getnext()
        return sal

    def titulo(i, nivel, texto):
        e = doc.els[i]
        pp = e.find(W + "pPr")
        if pp is None:
            pp = etree.Element(W + "pPr")
            e.insert(0, pp)
        st = pp.find(W + "pStyle")
        if st is None:
            st = etree.Element(W + "pStyle")
            pp.insert(0, st)
        st.set(W + "val", "Ttulo%d" % nivel)
        for r in e.findall(W + "r"):
            rp = r.find(W + "rPr")
            if rp is not None:
                r.remove(rp)
        ts = list(e.iter(W + "t"))
        ts[0].text = texto
        for t in ts[1:]:
            t.text = ""

    # 3.1: contexto, periodo, unidades, componentes y resultados
    doc.tras(218, [
        P("El estudio se realizó en un entorno computacional controlado y no en una organización ni en un sistema en producción. Corresponde al año 2026: el banco se selló el 20 de octubre de 2026, y las mediciones definitivas se hicieron en ese mes, con el banco ya sellado. Las unidades de estudio fueron los casos de prueba del banco; los cuatro proyectos de código abierto se usaron solo en la evaluación complementaria. Los componentes del estudio fueron la matriz normativa, el banco de casos, el checker con su política y el arnés de evaluación, y sus resultados son el banco validado, la caracterización de la configuración de referencia, el checker verificado, el efecto medido de la política y la comparación entre las configuraciones."),
    ])
    # 3.2
    titulo(236, 2, "3.2 Enfoque, Tipo y Nivel de la Investigación")
    titulo(237, 3, "3.2.1 Enfoque de la Investigación")
    doc.body.remove(doc.els[238])
    titulo(243, 3, "3.2.2 Tipo de Investigación")
    titulo(249, 3, "3.2.3 Nivel de Investigación")
    # 3.3
    titulo(276, 2, "3.3 Universo, Población y Muestra")
    titulo(277, 3, "3.3.1 Universo")
    titulo(281, 3, "3.3.2 Población y Población Accesible")
    titulo(286, 3, "3.3.3 Muestra y Unidad de Análisis")
    titulo(294, 3, "3.3.4 Criterios de Inclusión y Exclusión")
    doc.tras(284, [
        P("La población accesible es la parte de esa población que pudo construirse y analizarse con los recursos del estudio: los escenarios de los 57 pares contenedor–operación de la {T:pares}, expresables en un programa mínimo y analizables con Clang 21.1.8 y libstdc++ 13.3.0. Quedaron fuera los escenarios de la población que dependen de dos contenedores, de la identidad del nodo transferido o de reglas que no se modelaron ni validaron (sección 3.1.1)."),
    ])
    doc.tras(291, [
        P("El tamaño de la muestra es de 750 casos. No se calculó con una fórmula de muestreo, porque el estudio no estima un parámetro de una población mayor: 684 casos salen de multiplicar 57 pares por 3 clases de handle y por 4 formas sintácticas, y los otros 66 corresponden a los usos correctos con garantía que se quiso medir, 54 con reserva previa y 12 con el iterador devuelto por la operación. El procedimiento de selección fue, por tanto, doble: censo por generación automática desde la matriz en el primer grupo y selección intencional en el segundo. La {T:muestra} resume cada elemento."),
        T("muestra", "Universo, población accesible, unidad de análisis y muestra", [1800, 4200, 1100, 1900], [
            ["Elemento", "Definición", "Tamaño", "Selección"],
            ["Universo", "Escenarios de C++ en los que una operación sobre la biblioteca estándar puede afectar la validez de un iterador, una referencia o un puntero", "No acotado", "—"],
            ["Población", "Escenarios de los diez contenedores del alcance, regidos por las reglas de C++17", "—", "Criterios de la sección 3.3.4"],
            ["Población accesible", "Escenarios de 57 pares contenedor–operación, expresables en un programa mínimo y analizables con Clang 21.1.8", "57 pares", "Regla de inclusión de la sección 3.1.1"],
            ["Unidad de análisis", "Caso de prueba: un programa mínimo con un handle conservado, una operación y un punto posterior de comprobación", "1 caso", "—"],
            ["Muestra", "Banco de casos: 342 UB, 306 SAFE y 102 POLICY", "750 casos", "Censo de 684 casos y selección intencional de 66"],
        ], "Las métricas se calculan sobre los 648 casos de etiqueta binaria; los 102 casos POLICY se analizan aparte."),
    ])
    # 3.4
    titulo(320, 2, "3.4 Metodología, Técnicas e Instrumentos")
    titulo(321, 3, "3.4.1 Metodología de la Investigación")
    titulo(328, 3, "3.4.2 Técnicas de Recolección de Datos")
    titulo(334, 3, "3.4.3 Instrumentos de Recolección de Datos")
    titulo(350, 3, "3.4.4 Técnicas de Procesamiento de Datos")
    titulo(355, 2, "3.5 Consideraciones Éticas")
    doc.tras(350, [
        P("Antes de calcular, los datos se prepararon en cuatro pasos, todos por script. Primero, cada resultado del archivo SARIF se normalizó en un aviso con línea, columna, checker, clase y mensaje. Segundo, cada aviso se atribuyó a su caso y a su sitio. Tercero, se cotejó con la etiqueta del caso. Cuarto, se separó lo que no entra en las métricas: las incidencias, que nunca cuentan como verdaderos negativos, los avisos posibles y los casos POLICY."),
    ])
    doc.tras(353, [
        P("La prueba de McNemar supone resultados dicotómicos pareados, condición que cumple el diseño porque cada caso se analiza en una invocación propia bajo cada condición, y no requiere normalidad. Como los casos no se extrajeron al azar, el valor p no se generaliza a otros programas. La lectura de los resultados sigue esta regla: un ΔF1 positivo favorece a C, el contraste UB indica si cambió la exhaustividad, el contraste SAFE si cambiaron las falsas alarmas, y H~0~ se decide con la regla descrita arriba."),
    ])
    # orden final
    a = tramo(276, 320)
    met = tramo(321, 328)
    dis = tramo(257, 263)
    pro = tramo(264, 276)
    tec = tramo(328, 334)
    ins = tramo(334, 350)
    proc = tramo(350, 355)
    h4m = doc.bloque([H4("3.4.1.1 Métodos y pasos")], 200, 720)
    h4d = doc.bloque([H4("3.4.1.2 Diseño de la investigación")], 200, 720)
    h4p = doc.bloque([H4("3.4.1.3 Procedimiento")], 200, 720)
    herr = doc.bloque([
        H3("3.4.5 Herramientas para el Procesamiento de Datos"),
        P("La {T:herramientas} indica cada herramienta y su función concreta. El procesamiento de los datos recae en los scripts en Python, que normalizan, cotejan, agregan y contrastan, y en la hoja de cálculo, con la que se consultan los resultados exportados y se elaboran las tablas; las demás herramientas producen o verifican los datos que esos scripts procesan."),
        T("herramientas", "Herramientas y función en el procesamiento de datos", [3000, 1500, 3700, 800], [
            ["Herramienta", "Versión", "Función concreta", "Paso"],
            ["Clang Static Analyzer y LLVM", "21.1.8", "Analiza los casos y emite los avisos; compila el checker", "2–5"],
            ["libstdc++", "13.3.0", "Biblioteca analizada", "1–5"],
            ["libstdc++ en modo de depuración", "13.3.0", "Validación dinámica", "1"],
            ["AddressSanitizer y UndefinedBehaviorSanitizer", "Los de Clang 21.1.8", "Validación dinámica", "1"],
            ["Python", "3.12", "bench/gen_corpus.py genera el banco; bench/experimento.py normaliza, coteja y agrega; bench/analisis_estadistico.py calcula McNemar y el intervalo, y exporta la hoja", "1, 2, 4, 5"],
            ["CMake y Ninja", "3.28.3 y 1.11.1", "Compilación del checker", "3"],
            ["GoogleTest", "Paquete de Ubuntu 24.04", "Pruebas unitarias del núcleo", "3"],
            ["lit", "18.1.8", "Pruebas con programas mínimos", "3"],
            ["clang-format, mypy y llvm-cov", "Los de la imagen", "Formato, tipos y cobertura", "3"],
            ["Docker", "Imagen checker:llvm21", "Entorno fijo", "1–5"],
            ["git y GitHub Actions", "—", "Versiones, etiqueta del banco e integración continua", "1–5"],
            ["SARIF", "Formato", "Formato de los diagnósticos que el arnés normaliza a avisos", "2, 4, 5"],
            ["Hoja de cálculo (Microsoft Excel o LibreOffice Calc)", "—", "Consulta de resultados.xlsx por condición, contenedor, operación, clase de handle y forma, y elaboración de tablas", "5"],
            ["PlantUML", "—", "Elaboración de los diagramas", "3"],
        ]),
        P("Los datos se conservaron junto con la identificación de las configuraciones y las condiciones de ejecución, con el propósito de permitir la revisión de los resultados y la reproducción del procedimiento."),
    ], 200, 720)
    orden = a + [doc.els[320], met[0]] + h4m + met[1:] + h4d + dis + h4p + pro + tec + ins + proc + herr
    ancla = doc.els[355]
    for i in (255, 256, 263):
        doc.body.remove(doc.els[i])
    for e in orden:
        if e.getparent() is not None:
            e.getparent().remove(e)
        ancla.addprevious(e)
    # temario
    c(517, "Tipo y nivel", "Enfoque, tipo y nivel")
    c(518, "Diseño de la investigación", "Universo, población y muestra")
    c(519, "3.4 Universo, población y muestra", "3.4 Metodología, técnicas e instrumentos")
    c(520, "3.5 Métodos, técnicas e instrumentos de recolección de datos", "3.5 Consideraciones éticas")
    doc.body.remove(doc.els[521])
    doc.body.remove(doc.els[522])


def _nuevo(n: str) -> str:
    fijos = {"3.2.1": "3.2.2", "3.2.2": "3.2.3", "3.3": "3.4.1", "3.3.1": "3.4.1.2", "3.3.2": "3.4.1.3", "3.4": "3.3",
             "3.5": "3.4", "3.5.1": "3.4.1", "3.5.2": "3.4.2", "3.5.3": "3.4.3", "3.6": "3.4.4", "3.7": "3.5"}
    if n in fijos:
        return fijos[n]
    p = n.split(".")
    if p[:2] == ["3", "4"] and len(p) == 3:
        return "3.3." + p[2]
    if p[0] == "4" and p[1] in "2345678":
        return "4.2." + ".".join(p[1:])
    return n


def renumerar(doc):
    """Las referencias de la V3 y de este archivo usan la numeración antigua; las de cap. IV ya vienen en la nueva."""
    num = r"\d\.\d+(?:\.\d+)?"
    pat = re.compile(r"([Ss]ecci(?:ón|ones)\s+)(" + num + r"(?:(?:\s+(?:a|y)\s+|,\s*)" + num + r")*)")
    for t in doc.body.iter(W + "t"):
        if t.text and "ecci" in t.text:
            t.text = pat.sub(lambda m: m.group(1) + re.sub(num, lambda k: _nuevo(k.group(0)), m.group(2)), t.text)


def temario(doc, items):
    """Reemplaza las entradas del capítulo IV en el posible temario (524 a 539)."""
    n2, n3 = doc.els[524], doc.els[527]
    ultimo = doc.els[523]
    nuevos = []
    for it in items:
        if it[0] != "h" or it[1] > 3:
            continue
        e = copy.deepcopy(n2 if it[1] == 2 else n3)
        ts = list(e.iter(W + "t"))
        ts[0].text = it[2]
        for t in ts[1:]:
            t.text = ""
        nuevos.append(e)
    for i in range(524, 540):
        doc.body.remove(doc.els[i])
    for e in reversed(nuevos):
        ultimo.addnext(e)
