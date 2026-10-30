"""Capítulo IV de la tesis: desarrollo de la propuesta. Sin valores de resultados (van al capítulo V)."""
from __future__ import annotations


def capitulo(P, H2, H3, H4, F, T, L):
    return [
        H2("4.1 Generalidades"),
        P("Este capítulo describe cómo se construyó la propuesta y cómo se preparó su evaluación. El problema de partida es que las reglas de invalidación de C++17 cambian según el contenedor, la operación, la clase de handle y el estado en ejecución, y que no se conocía el desempeño de Clang Static Analyzer frente a esas reglas. Los checkers de iteradores del analizador modelan la posición de los iteradores, pero el único que sigue punteros al almacenamiento, cplusplus.InnerPointer, se limita a std::string (sección 2.2.2)."),
        P("La propuesta es un checker, denominado ucsm.ContainerInvalidation, que se carga como complemento (plugin) de Clang Static Analyzer 21.1.8. El checker sigue cada iterador, referencia o puntero obtenido de un contenedor, es decir, cada handle (sección 2.3.3), a lo largo de cada camino de ejecución simbólica. Ante cada operación sobre el contenedor decide si el handle conserva su validez, y para ello aplica una matriz normativa con las reglas de C++17 para los diez contenedores del alcance. La matriz reúne 101 mutaciones, es decir, combinaciones de contenedor, operación y punto donde actúa, y 348 reglas. Las 163 reglas que invalidan o dependen del estado citan la cláusula de la norma que las respalda; las 185 que conservan la validez no citan cláusula en la matriz."),
        P("Para evaluarlo se construyó, a partir de esa misma matriz, un banco de 750 casos etiquetados, y las etiquetas se validaron por ejecución antes de medir. Un arnés analizó cada caso bajo cuatro condiciones y clasificó cada resultado según su etiqueta, de modo que la configuración de referencia y la que incorpora el checker pudieran compararse caso por caso. La evaluación se complementó con cuatro proyectos de código abierto y con defectos sembrados en ellos."),
        P("El prototipo se dirige a desarrolladores de C++ y a quienes revisan o mantienen código con análisis estático. Funciona durante el desarrollo, antes de ejecutar el programa, y no sustituye la revisión técnica del desarrollador. La {T:ficha} resume su propósito, sus usuarios, su contexto, sus condiciones de funcionamiento, sus entradas y sus resultados."),
        T("ficha", "Ficha de la propuesta", [2300, 6700], [
            ["Aspecto", "Descripción"],
            ["Propósito", "Avisar cuando un programa usa un iterador, una referencia o un puntero que una operación sobre un contenedor invalidó según las reglas de C++17"],
            ["Usuarios", "Desarrolladores de C++ que analizan su código; evaluadores que repiten el experimento; mantenedores que corrigen o amplían las reglas"],
            ["Contexto", "Programas en C++17 que usan alguno de los diez contenedores del alcance. El prototipo se evaluó en un entorno controlado y no se implantó en una organización"],
            ["Condiciones de funcionamiento", "Clang Static Analyzer 21.1.8 con libstdc++ 13.3.0, dentro de la imagen Docker del repositorio. El checker se carga con -load, sin recompilar el compilador, y solo analiza unidades de traducción que compilan"],
            ["Entradas", "Un archivo C++ o un proyecto con compile_commands.json, y la política elegida (Silent o Possibly). Para la evaluación, la matriz normativa y el banco de casos"],
            ["Resultados", "Avisos confirmados y posibles que nombran el handle, el contenedor, la operación y la línea, con notas de ruta. Para la evaluación, los registros de ejecución, el cotejo, las métricas y el contraste"],
            ["Evaluación", "750 casos bajo cuatro condiciones, con precisión, exhaustividad, F1, ΔF1, la prueba exacta de McNemar y un intervalo de confianza; como complemento, cuatro proyectos de código abierto y defectos sembrados"],
        ]),
        P("Frente a los trabajos del capítulo II, que compara la {T:enfoques}, la propuesta se diferencia en tres aspectos. Scasa (Li et al., 2024) atiende los contenedores secuenciales e IKOS4VecErr (Liu et al., 2025) se dirige a std::vector, mientras que el checker abarca diez contenedores de tres familias. Esos dos trabajos representan iteradores y tamaño del contenedor, y Teodorescu y Lucanu (2024) estudian punteros en tipos propietarios en general; el checker sigue iteradores, referencias y punteros, y aplica a cada uno la regla que corresponde a su contenedor, a la operación y a su clase. Además, la evaluación usó un banco derivado de las reglas de C++17, con etiquetas contrastadas por ejecución, y comparó caso por caso la misma configuración del analizador con y sin el checker."),
        P("Cada objetivo específico produjo un artefacto, como muestran la {F:f4-vision} y la {T:artefactos}. La sección 4.2 presenta el esquema de la solución y el desarrollo del prototipo: primero el esquema, luego la metodología de desarrollo y el diseño, después el procedimiento seguido para cada objetivo específico y, al final, el alcance previsto y su avance. El método, las técnicas y los instrumentos de cada paso se definieron en la sección 3.4 y no se repiten aquí. Los valores obtenidos se presentan en el capítulo V del informe final."),
        F("f4-vision", "Visión general de los artefactos de la propuesta"),
        T("artefactos", "Artefactos producidos por objetivo específico", [950, 3250, 3300, 1500], [
            ["Objetivo", "Artefacto", "Ubicación en el repositorio", "Sección"],
            ["OE1", "Matriz normativa, banco de 750 casos y registro de su validación dinámica", "norma/matriz.json; test/corpus.cpp; test/corpus_truth.json; test/runtime_validation_results.json", "4.2.4"],
            ["OE2", "Registro de la configuración de referencia y clasificación de sus omisiones por causa", "test/experimento/; test/corpus_fallos.json", "4.2.5"],
            ["OE3", "Checker como complemento del analizador, con sus pruebas", "plugin/", "4.2.6"],
            ["OE4", "Política Silent/Possibly, crédito de garantía y tratamiento del escape", "plugin/dominio/Decisions.cpp", "4.2.7"],
            ["OE5", "Arnés de ejecución y comparación y análisis estadístico; evaluación en código real (complemento)", "bench/experimento.py; bench/analisis_estadistico.py; bench/codigo_real.py; bench/inyeccion.py", "4.2.8"],
        ]),

        H2("4.2 Esquema de la Solución y Desarrollo del Prototipo"),
        P("Esta sección explica de qué partes se compone el prototipo y cómo se construyó. La sección 4.2.1 presenta sus componentes y sus relaciones; las secciones 4.2.2 y 4.2.3, la metodología de desarrollo, el diseño y la infraestructura; las secciones 4.2.4 a 4.2.8, el trabajo por objetivo específico; y la sección 4.2.9, el alcance previsto y lo que ya funciona."),
        H3("4.2.1 Esquema de la solución"),
        P("La solución tiene tres partes: la fuente normativa, el prototipo que funciona dentro de Clang y la evaluación. La {F:f4-esquema} muestra sus componentes y cómo se relacionan, y la {T:componentes} indica la función, la entrada y la salida de cada uno."),
        F("f4-esquema", "Esquema de la solución", "En amarillo, la fuente normativa; en azul, el prototipo dentro de Clang; en verde, la evaluación."),
        T("componentes", "Componentes de la solución", [1900, 2900, 2100, 2100], [
            ["Componente", "Función", "Entrada", "Salida"],
            ["Matriz normativa", "Reunir en un solo archivo las reglas de invalidación de C++17", "Cláusulas de la norma N4659", "norma/matriz.json"],
            ["Generador de la tabla", "Comprobar las leyes de la norma y convertirla en una tabla de C++", "Matriz normativa", "Tabla de reglas compilada en el núcleo"],
            ["Motor de Clang Static Analyzer", "Recorrer los caminos de ejecución del programa y avisar a los checkers de lo que ocurre", "Código C++ compilable", "Eventos del programa; informe SARIF"],
            ["Checker InvalidationChecker", "Recibir los eventos, guardar el estado de cada handle en cada camino y emitir los avisos", "Eventos del motor", "Estado y avisos con notas de ruta"],
            ["Reconocedor ClangRecognizer", "Traducir lo que ve el motor a operaciones y handles del dominio", "Llamada o acceso del programa", "Operación, contenedor y handle"],
            ["Núcleo de decisión", "Decidir, sin depender de Clang, cómo cambia un handle ante una operación y qué aviso corresponde", "Estado del handle, operación y crédito", "Nuevo estado y clase de aviso"],
            ["Banco de casos", "Representar cada combinación con un programa mínimo y su etiqueta", "Matriz normativa", "Casos y etiquetas sellados"],
            ["Validación dinámica", "Ejecutar los casos para contrastar las etiquetas con un criterio ajeno al analizador", "Casos y etiquetas", "Registro de cada ejecución"],
            ["Arnés", "Analizar cada caso en cada condición y clasificar el resultado", "Banco sellado y condiciones", "Registro de ejecución y cotejo"],
            ["Análisis estadístico", "Calcular las métricas y comparar las condiciones", "Cotejo y etiquetas", "Contraste y hoja de resultados"],
        ]),
        P("Los componentes interactúan en dos momentos. Al analizar un programa, el motor recorre cada camino y avisa al checker de cada llamada y de cada lectura de memoria. El checker pide al reconocedor que identifique la operación y el handle, y entrega ese evento y el estado actual al núcleo. El núcleo busca en la tabla la regla que corresponde y devuelve el nuevo estado del handle. Si después el programa usa un handle inválido, el checker emite un aviso, confirmado o posible según lo que el análisis haya podido determinar, con notas sobre dónde se obtuvo el handle y qué operación lo invalidó."),
        P("Al evaluar el prototipo, el banco sale de la misma matriz, pero sus etiquetas las calcula un script aparte, y la validación dinámica las contrasta ejecutando los casos. Con el banco sellado, el arnés invoca el analizador una vez por caso y condición, lee los avisos y los coteja con la etiqueta y el sitio de cada caso. El análisis estadístico toma ese cotejo y produce las métricas y el contraste."),
        P("La {T:coherencia} relaciona las causas y los efectos del árbol del problema ({F:f1-arbol}) con el componente que los atiende, el objetivo específico al que responde y el indicador con que se comprueba."),
        T("coherencia", "Relación entre el problema, los componentes y los indicadores", [3200, 2300, 800, 2700], [
            ["Causa o efecto del problema", "Componente que lo atiende", "OE", "Indicador"],
            ["Las reglas varían según el contenedor, la operación, la clase de acceso y el estado", "Matriz normativa, tabla de reglas y núcleo", "OE1, OE3", "Reglas modeladas; pruebas aprobadas"],
            ["No se encontró un banco público etiquetado por la norma para este dominio", "Banco de casos y validación dinámica", "OE1", "Ejecuciones que contradicen su etiqueta"],
            ["Las capacidades documentadas no determinan el desempeño en cada combinación", "Arnés aplicado a la configuración de referencia", "OE2", "VP, FP, FN, VN, precisión, exhaustividad y F1 de B"],
            ["Los checkers de iteradores son experimentales y el de punteros internos se limita a std::string", "Checker, reconocedor y núcleo", "OE3", "Exhaustividad; cobertura sobre el handle sostenido"],
            ["Falsas alarmas que reducen la utilidad de las herramientas", "Política Silent/Possibly y crédito de garantía", "OE4", "Avisos confirmados y posibles; FP en casos SAFE"],
            ["Decisiones sobre herramientas sin evidencia medida", "Arnés y análisis estadístico", "OE5", "ΔF1, pares discordantes, valor p e intervalo"],
        ]),
        H3("4.2.2 Metodología de desarrollo"),
        H4("4.2.2.1 Modelo incremental"),
        P("El checker se construyó con el modelo de desarrollo incremental (Sommerville, 2020), en el que el producto se entrega como una serie de versiones y cada una añade funcionalidad a la anterior, ya validada. El modelo se eligió porque el alcance podía dividirse por clase de handle y por grupo de operaciones, y cada parte podía medirse contra el banco antes de construir la siguiente. Así, una regresión podía atribuirse al incremento que la introdujo."),
        P("La {T:incrementos} resume los siete incrementos, el objetivo específico al que contribuyó cada uno y el criterio con el que se dio por terminado. La {F:f4-incrementos} muestra su secuencia. En los incrementos I2 a I4, el cierre exigió además que la medición sobre el banco no mostrara regresiones frente al incremento anterior. El banco, la validación dinámica y el arnés de medición se construyeron en paralelo con los incrementos I2 a I5, porque cada uno de ellos se midió con esos artefactos. Esta forma de trabajo tiene una consecuencia que se declaró como limitación en la sección 3.1.2: el checker se ajustó con los mismos casos con que después se evaluó."),
        T("incrementos", "Incrementos del desarrollo del checker", [1150, 3650, 800, 3400], [
            ["Incremento", "Contenido", "OE", "Criterio de cierre"],
            ["I0", "Entorno Docker con Clang 21.1.8; complemento vacío que se registra en el analizador", "OE3", "El analizador carga el complemento y una prueba lit lo confirma"],
            ["I1", "Matriz normativa, generador de la tabla de reglas, núcleo puro y pruebas de sus leyes", "OE1, OE3", "Las leyes del modelo se cumplen en las pruebas unitarias"],
            ["I2", "Referencias y punteros obtenidos con \\*it, c[i], front() y back(); detección del uso al leer la memoria", "OE3", "Pasan las pruebas del incremento y la medición sobre el banco no muestra regresiones"],
            ["I3", "Iteradores propios, posición designada, transporte entre variables y erase de rango", "OE3", "Pasan las pruebas del incremento y la medición sobre el banco no muestra regresiones"],
            ["I4", "Crédito de reserve, política Silent/Possibly y escape a código opaco", "OE4", "Pasan las pruebas del incremento, incluidas las de la política, y la medición sobre el banco no muestra regresiones"],
            ["I5", "Notas de ruta y mensajes que nombran la operación y la línea", "OE3", "Cada aviso indica dónde se obtuvo el handle y qué operación lo invalidó"],
            ["I6", "Banco congelado, experimento con las cuatro condiciones y evaluación en código real", "OE2, OE5", "Registro completo de las 3000 invocaciones y de los cuatro proyectos"],
        ], "El cierre de cada incremento está en libro/construccion/7-6-incrementos.md."),
        F("f4-incrementos", "Secuencia de los incrementos del desarrollo"),
        H4("4.2.2.2 Desarrollo guiado por pruebas"),
        P("Dentro de cada incremento se aplicó el desarrollo guiado por pruebas (Sommerville, 2020) en el núcleo de reglas: la prueba de cada ley del modelo se escribió antes que la función que debía cumplirla. En la capa que interactúa con el analizador esa práctica rinde menos, porque su comportamiento depende del motor de Clang. En ella se escribió primero un programa mínimo que reproducía la omisión o la falsa alarma, comprobado con lit, la herramienta de pruebas de LLVM, y después el código de reconocimiento que la corregía. La {F:f4-tdd} muestra el ciclo."),
        F("f4-tdd", "Ciclo de trabajo dentro de un incremento"),
        P("La {F:lst-ley} presenta una de las pruebas de ley del núcleo. La ley dice que un handle inválido no cambia con ninguna mutación. La prueba la verifica con todas las mutaciones de la tabla, las dos formas de guardar un handle (objeto iterador y elemento), un conjunto de posiciones representativas y los créditos posibles, en lugar de un solo ejemplo. La {F:lst-lit} presenta el formato de las pruebas lit: cada comentario expected-warning declara el aviso que el analizador debe emitir en esa línea, y una línea sin esa marca no debe producir ninguno."),
        L("lst-ley", "Prueba de la ley «inválido es absorbente»", """
TEST(Deteccion, InvalidoEsAbsorbente) {
  forAllMutations([](Mutation M) {
    for (HandleKind K : Kinds)
      for (Position P : positions())
        for (const HandleState &H : states(K, P, M))
          if (H.validity().kind() >= ValidityKind::Invalidated)
            for (Credit C : credits()) {
              ApplyResult R = apply(event(M, Position::first(0)), H, C);
              EXPECT_EQ(R.State, H);
              EXPECT_FALSE(R.Noted);
            }
  });
}""", "Tomado de plugin/tests/dominio/LeyesTest.cpp."),
        L("lst-lit", "Prueba con programas mínimos del crédito de reserve", """
void reserved(std::vector<int> &c) {
  c.reserve(c.size() + 2);
  const int &h = c[0];
  c.push_back(1);
  c.push_back(2);
  sink(h); // sin aviso: reserve garantiza dos inserciones
}

void reserved_too_little(std::vector<int> &c) {
  c.reserve(c.size() + 1);
  const int &h = c[0];
  c.push_back(1);
  c.push_back(2);
  sink(h); // expected-warning {{posiblemente invalidada: 'std::vector::push_back'
           //                     (línea 26)}}
}""", "Tomado de plugin/tests/lit/garantias.cpp; el comentario final ocupa una sola línea en el archivo."),
        H4("4.2.2.3 Registro de decisiones"),
        P("Las decisiones de diseño se registraron a medida que se tomaron, con la alternativa descartada y el problema que cada decisión evitaba. Ese registro reunió 25 decisiones, dos de ellas reemplazadas después por otras, y es la fuente de las justificaciones de este capítulo. La {T:decisiones} presenta las que más influyeron en el diseño."),
        T("decisiones", "Principales decisiones de diseño", [750, 2900, 2500, 2850], [
            ["ID", "Decisión", "Alternativa descartada", "Problema que evita"],
            ["D-01", "Checker sensible a caminos", "Patrones sobre el árbol de sintaxis", "Avisar sin saber qué ocurrió antes en el camino"],
            ["D-02", "Complemento cargado con -load", "Checker dentro del árbol de LLVM", "Recompilar Clang en cada cambio"],
            ["D-03", "Modelo propio de contenedores y handles", "Leer el estado de IteratorModeling", "Depender de cabeceras internas que no son una interfaz pública"],
            ["D-04", "Núcleo sin cabeceras de Clang", "Lógica dentro de las funciones que invoca el analizador", "Reglas imposibles de probar sin el analizador"],
            ["D-05", "Una sola fuente de reglas, de la que salen la tabla y las etiquetas", "Tabla y etiquetas escritas por separado", "Que el banco mida la diferencia entre dos copias de la norma"],
            ["D-06", "Handle identificado por la región del elemento", "Identificarlo por la variable", "Revivir un handle al reasignar; no ver que r y &r son el mismo elemento"],
            ["D-08", "Dos clases de aviso, confirmado y posible", "Un solo aviso", "Mezclar en la precisión lo que depende del estado"],
            ["D-13", "Un fallo de ejecución es una incidencia", "Contar «sin avisos»", "Que una caída mejore la precisión"],
            ["D-15, D-24", "Una invocación por caso y condición, con cotejo por sitio", "Un análisis del archivo completo", "Que un caso tape a otro, y contar un aviso sobre un handle válido"],
            ["D-19", "Crédito de garantía por contenedor", "Avisar en toda inserción sin garantía", "Avisos en código que sí reservó capacidad"],
            ["D-20", "Casos de buen uso con garantía", "Solo casos de la matriz", "Una precisión perfecta para un checker que avise en cada inserción"],
            ["D-21", "El escape olvida lo válido y lo no resuelto", "Marcarlo como no resuelto", "Avisos por llamadas opacas que no señalaban un defecto"],
            ["D-23", "Borrado de rango con relación semiabierta", "Reglas nuevas para rangos", "Una falsa alarma sobre el extremo final, que sobrevive"],
            ["D-25", "Cuarta condición sin alpha.cplusplus", "Medir el checker solo junto a ellos", "No ver el aporte del checker cuando otro corta el camino"],
        ], "El registro completo está en libro/diseno/decisiones.md, sección Motor de análisis."),

        H3("4.2.3 Diseño de la solución e infraestructura"),
        H4("4.2.3.1 Requerimientos del checker"),
        P("Antes de programar se fijaron los requerimientos, para que cada función tuviera una prueba que la demostrara, y las decisiones de la sección 4.2.2.3 los ajustaron durante el desarrollo; las tablas presentan su versión final. La {T:rf} presenta los 17 requerimientos funcionales, agrupados según lo que exigen al checker y al arnés, y la {T:rnf} los no funcionales, cada uno con el criterio que permite comprobarlo. Las reglas de la evaluación, que se aplicaron en todo el trabajo, se resumen en la {T:rn}."),
        T("rf", "Requerimientos funcionales", [800, 2500, 4700, 1000], [
            ["ID", "Requerimiento", "Qué exige", "OE"],
            ["RF-01", "Registrar el checker", "Cargarse como complemento y aparecer con el nombre ucsm.ContainerInvalidation y sus opciones PolicyMode y Debug", "OE3"],
            ["RF-02", "Activar y desactivar", "Activarse o quedar fuera con -analyzer-checker, sin recompilar Clang", "OE3"],
            ["RF-03", "Analizar un proyecto", "Analizar un proyecto desde su compile_commands.json, una unidad de traducción por invocación", "OE5"],
            ["RF-04", "Elegir la política", "Elegir PolicyMode=Silent (por omisión) o PolicyMode=Possibly", "OE4"],
            ["RF-05", "Seguir iteradores", "Seguir los obtenidos con begin, find, lower_bound, upper_bound, insert y emplace, sus copias y sus movimientos", "OE3"],
            ["RF-06", "Seguir referencias y punteros", "Seguir los obtenidos con \\*it, it->, c[i], at, front, back, data y &", "OE3"],
            ["RF-07", "No avisar en usos válidos", "No avisar en el iterador devuelto por la mutación, en uno obtenido de nuevo, en uno de otro contenedor ni al pasar un puntero por valor", "OE3"],
            ["RF-08", "Aplicar la regla de C++17", "Aplicar la regla según operación, contenedor, clase de handle y posición frente al punto de la mutación", "OE3"],
            ["RF-09", "Tratar lo que depende del estado", "No dar por confirmada una invalidación que depende de la capacidad o del factor de carga; reserve(c.size() + k) cubre k inserciones", "OE4"],
            ["RF-10", "Tratar las llamadas opacas", "Olvidar los handles válidos cuando el contenedor pasa a una llamada opaca; conservar los invalidados", "OE4"],
            ["RF-11", "Explicar la causa", "Indicar clase de handle, contenedor, operación, línea y tipo de aviso; el posible dice qué garantía falta", "OE3"],
            ["RF-12", "Mostrar la ruta", "Añadir una nota donde se obtuvo el handle y otra en la mutación", "OE3"],
            ["RF-13", "Ejecutar el experimento", "Ejecutar cada caso en cuatro condiciones, con una invocación por caso y condición", "OE5"],
            ["RF-14", "Cotejar por sitio", "Contar un acierto solo si el aviso cae sobre un handle que la norma da por inválido; separar confirmados, posibles e incidencias", "OE5"],
            ["RF-15", "Generar y validar el banco", "Generar el banco desde la norma y validar sus etiquetas ejecutando cada caso", "OE1"],
            ["RF-16", "Construir y verificar", "Construir y probar el complemento en la imagen fijada con una sola orden", "OE3"],
            ["RF-17", "Mantener la norma como datos", "Regenerar la tabla al corregir una regla; rechazar una norma que rompa sus leyes", "OE1, OE3"],
        ]),
        T("rnf", "Requerimientos no funcionales", [800, 1900, 4400, 1900], [
            ["ID", "Atributo", "Criterio", "Dónde se mide"],
            ["RNF-01", "Precisión", "Ningún aviso confirmado sobre casos SAFE ni avisos falsos confirmados en código real", "Experimento; código real"],
            ["RNF-02", "Exhaustividad", "Exhaustividad por caso y cobertura sobre el handle sostenido, como objetivo de diseño; el contraste de la sección 3.4.4 decide la comparación con la referencia", "Experimento"],
            ["RNF-03", "Robustez", "El checker no interrumpe a Clang; lo que no termina no se cuenta como analizado sin defectos", "Experimento; código real"],
            ["RNF-04", "Tiempo", "Sobrecosto mediano por caso frente a la referencia menor que 10 %", "Registro de ejecución"],
            ["RNF-05", "Memoria", "El mayor pico de memoria residente entre todos los casos supera en menos de 5 % al de la referencia", "Registro de ejecución"],
            ["RNF-06", "Claridad del diagnóstico", "Todo aviso nombra el handle, el contenedor, la operación y la línea; el posible dice qué falta", "Pruebas lit"],
            ["RNF-07", "Mantenibilidad", "El núcleo compila sin las cabeceras de Clang, y corregir una regla no toca código C++", "Sistema de compilación"],
            ["RNF-08", "Reproducibilidad", "Cada ejecución registra versiones y resúmenes sha256 del checker y del banco", "Registro de ejecución"],
        ]),
        T("rn", "Reglas de la evaluación", [800, 8200], [
            ["ID", "Regla"],
            ["RN-001", "La etiqueta de un caso sale de la norma: es el peor efecto que la norma da a cualquiera de sus handles"],
            ["RN-002", "Las condiciones de referencia y experimental difieren solo en el checker; la cuarta condición quita además los alpha.cplusplus y se informa aparte"],
            ["RN-003", "Nada que dependa del estado se informa como confirmado, y un handle no resuelto solo se da por válido con una garantía, salvo tras un escape a código opaco, donde el handle deja de seguirse (sección 4.2.7.4)"],
            ["RN-004", "Un aviso posible nunca cuenta como acierto ni como falso positivo"],
            ["RN-005", "Una compilación fallida, una caída o un tiempo agotado es una incidencia, nunca un verdadero negativo"],
            ["RN-006", "Un aviso acierta solo si cae sobre un handle que la norma da por inválido"],
            ["RN-007", "Cada resultado lleva la versión de Clang y de libstdc++ y el sha256 del checker y del banco"],
        ]),
        P("La {F:f4-casos-uso} presenta los casos de uso y la {T:cu} su flujo principal. Intervienen tres actores (desarrollador, evaluador y mantenedor), y el sistema se divide en tres partes: el analizador con el checker, el banco con el arnés, y la construcción con la norma. El checker no es un actor, porque forma parte del sistema."),
        F("f4-casos-uso", "Casos de uso del checker y de su evaluación"),
        T("cu", "Casos de uso", [1900, 1350, 4300, 1450], [
            ["Caso de uso", "Actor", "Flujo principal", "Requerimientos"],
            ["CU-01 Analizar un archivo", "Desarrollador", "Ejecuta clang++ --analyze con el complemento; el checker sigue los handles, aplica la norma y avisa", "RF-01, RF-02, RF-05 a RF-11"],
            ["CU-02 Analizar un proyecto", "Desarrollador", "Genera compile_commands.json e invoca CU-01 por cada unidad de traducción", "RF-03"],
            ["CU-03 Elegir la política", "Desarrollador", "Agrega PolicyMode=Possibly y recibe también avisos posibles", "RF-04, RF-09"],
            ["CU-04 Seguir la ruta de un aviso", "Desarrollador", "Lee las notas: obtención, mutación y uso", "RF-11, RF-12"],
            ["CU-05 Generar y validar el banco", "Evaluador", "Genera los casos desde la matriz y los ejecuta con libstdc++ Debug y con sanitizadores", "RF-15"],
            ["CU-06 Ejecutar el experimento", "Evaluador", "Verifica los sellos, ejecuta las cuatro condiciones, coteja y agrega", "RF-13, RF-14"],
            ["CU-07 Construir y verificar", "Mantenedor", "Genera la tabla, compila, y ejecuta las pruebas unitarias y lit", "RF-16"],
            ["CU-08 Corregir o ampliar la norma", "Mantenedor", "Edita una regla con su cláusula, regenera la tabla y repite CU-05 y CU-06", "RF-17"],
        ], "CU-02 incluye CU-01; CU-03 y CU-04 extienden CU-01; CU-06 incluye CU-01 y CU-05; CU-08 incluye CU-07."),

        H4("4.2.3.2 Modelo de invalidación"),
        P("El contenedor actúa como propietario y los handles como relaciones no propietarias (sección 2.3.6). El modelo parte de una pregunta: qué tiene que ser cierto para afirmar que un uso es inválido. La respuesta se expresó como seis premisas, que la {T:premisas} presenta. Un aviso confirmado exige las seis en un camino factible. Solo la cuarta procede de la norma; las otras cinco son hechos del programa que el checker debe reconocer, y evaluar mal cada una produce un error distinto."),
        T("premisas", "Premisas de un uso inválido", [1500, 4500, 3000], [
            ["Premisa", "Enunciado", "Si el checker la evalúa mal"],
            ["P1 Obtención", "El handle h queda ligado al elemento e del contenedor c, en la posición p", "Falso negativo: no se reconoce cómo se obtuvo"],
            ["P2 Mutación", "Después, una operación m actúa sobre ese mismo c, en el punto q", "Falso negativo: c tiene otro nombre y no se ve que es el mismo"],
            ["P3 Relación", "e está en la relación r con q: el mismo, antes, después o cualquiera", "Falso negativo o positivo: se calcula mal la posición"],
            ["P4 Norma", "El efecto de m para la clase de h y la relación r es invalidar", "Falso negativo o positivo: la tabla está mal"],
            ["P5 Identidad", "Entre P1 y P6, h no se volvió a ligar a otro elemento", "Falso positivo: un handle reasignado se confunde con el anterior"],
            ["P6 Uso", "h se desreferencia, se mueve o se compara", "Falso negativo: el uso ocurre en código que no se analiza"],
        ]),
        P("Las reglas de la norma, a su vez, responden a seis mecanismos de memoria, que la {T:mecanismos} resume. Conocerlos permitió explicar por qué la validación dinámica no observa todos los defectos: un corrimiento o una destrucción en el sitio no liberan memoria, de modo que AddressSanitizer no tiene nada que señalar. También permitió explicar por qué hay casos que dependen del estado: solo la realocación del búfer y el rehash están condicionadas."),
        T("mecanismos", "Mecanismos de memoria detrás de las reglas", [1800, 2600, 2100, 2500], [
            ["Mecanismo", "Operaciones", "Qué queda inválido", "Cómo se manifiesta al ejecutar"],
            ["M1 Realocación del búfer", "vector: inserción, resize o reserve que superan la capacidad", "Todo", "heap-use-after-free; iterador singular"],
            ["M2 Corrimiento", "vector y deque interior: insert y erase sin realocar", "vector: lo que está en el punto o después; deque interior: todo", "Casi siempre sin síntoma: se lee otro elemento"],
            ["M3 Destrucción en el sitio", "vector: pop_back, erase del elemento, clear, assign", "El elemento destruido y lo posterior", "Sin síntoma con int; AddressSanitizer no lo ve"],
            ["M4 Realocación del mapa de bloques", "deque: inserción en un extremo", "Solo iteradores", "Iterador singular; las referencias siguen bien"],
            ["M5 Liberación del nodo", "Nodos y no ordenados: erase, clear, pop; deque en los extremos", "El handle al nodo borrado", "Nodos: heap-use-after-free. deque: iterador singular; las referencias y los punteros, casi siempre sin síntoma"],
            ["M6 Rehash", "No ordenados: rehash, reserve o inserción que supera el factor de carga", "Solo iteradores", "Inserción con rehash: iterador singular. rehash y reserve explícitos: sin síntoma con estas herramientas. AddressSanitizer no lo ve"],
        ], "Un iterador singular es el que no está asociado a ninguna secuencia; heap-use-after-free es el informe de AddressSanitizer al acceder a memoria ya liberada."),
        P("A partir de las premisas de la {T:premisas}, el modelo describe la vida de un handle en tres momentos, que la {F:f4-modelo} resume: se obtiene, el contenedor se modifica y el handle se usa. Al obtenerse, el handle registra su contenedor, su clase, la posición que designa y su validez, cuyo valor inicial es «válido». La matriz normativa traduce cada modificación del mismo contenedor en uno de tres efectos: preserva, invalida o depende del estado. El efecto se determina por la clase del handle y la relación entre su posición y el punto de la operación. El tercero, «depende del estado», aparece cuando la norma condiciona la invalidación a la capacidad o al factor de carga, o cuando la operación es una solicitud que la implementación puede no atender."),
        F("f4-modelo", "Modelo de invalidación: de la norma al aviso"),
        P("La validez tiene tres niveles ordenados: válido, no resuelto e inválido. Al combinar efectos se conserva el peor nivel, de modo que la validez solo puede empeorar y un handle inválido no vuelve a ser válido. Obtener de nuevo un elemento crea otro handle, y una operación que devuelve un iterador, como it = c.erase(it), entrega uno nuevo y válido. Cuando el programa usa el handle, el modelo emite un aviso confirmado si es inválido y, según la política de la sección 4.2.7, un aviso posible si no está resuelto."),
        P("La implementación añade a los niveles no resuelto e inválido una marca de «ya avisado», lo que da los cinco estados de la {F:f4-estados}. La marca evita repetir el aviso en el mismo handle y camino. Un aviso posible no impide uno confirmado posterior: si una mutación invalida después ese handle, el uso siguiente se informa como confirmado. Cuando la región de memoria del handle deja de estar viva, su estado se descarta."),
        F("f4-estados", "Estados de un handle"),

        H4("4.2.3.3 Arquitectura lógica"),
        P("La solución mantiene las decisiones sobre la invalidación separadas del código que interactúa con el analizador. El checker se organizó en cuatro capas, que la {T:capas} describe y la {F:f4-arquitectura} ubica. Cada vez que el analizador notifica al checker un evento al que se aplica una regla, se sigue el mismo orden. Primero, la cáscara, que es la capa en contacto con el analizador, carga el estado del camino, y la capa de anticorrupción, que separa el modelo de los tipos de Clang, traduce el evento al vocabulario del modelo. Después, el núcleo decide con una función pura, es decir, una que solo depende de sus argumentos y no modifica nada, y la cáscara aplica el resultado, sea un estado nuevo o un aviso."),
        T("capas", "Capas del checker", [1500, 4100, 3400], [
            ["Capa", "Responsabilidad", "Restricción de diseño"],
            ["Cáscara", "Recibe los eventos del analizador, lee y escribe el estado del camino y emite los avisos", "Es la única capa que modifica el estado del analizador"],
            ["Anticorrupción", "Reconoce contenedores, operaciones, obtenciones y posiciones en las llamadas de Clang", "Concentra el reconocimiento de contenedores y operaciones"],
            ["Núcleo", "Decide el efecto de cada operación sobre cada handle y el veredicto de cada uso", "No incluye cabeceras de Clang; el objetivo de compilación no tiene sus rutas"],
            ["Tabla normativa", "Asigna un efecto a cada combinación de contenedor, operación, clase de handle y relación", "Se genera desde la matriz normativa; no se escribe a mano"],
        ]),
        P("La restricción del núcleo se hizo cumplir con el sistema de compilación: su biblioteca se compila sin las rutas de cabeceras de Clang, de modo que una inclusión de Clang en el núcleo no compila. Por eso el núcleo puede probarse sin el analizador. Por otra parte, la tabla normativa y las etiquetas del banco salen del mismo archivo, lo que impide que el checker y la verdad fundamental apliquen dos versiones distintas de la norma."),
        P("El arnés queda fuera del proceso de Clang: solo invoca el compilador y lee su salida, de modo que la medición no depende de la implementación medida."),
        F("f4-arquitectura", "Arquitectura lógica del checker y de la evaluación"),

        H4("4.2.3.4 Paquetes y clases"),
        P("La {F:f4-paquetes} presenta la organización del repositorio. La {F:f4-clases-dominio} muestra los tipos del núcleo. Todos son valores inmutables: una decisión no modifica un estado, sino que devuelve uno nuevo. Las funciones de decisión reciben esos valores y devuelven otros, sin leer nada del analizador. La {F:f4-clases-cascara} muestra la cáscara, que hereda de la plantilla Checker de Clang y declara en sus parámetros los eventos a los que se suscribe, y la {T:tipos} resume el vocabulario que comparten las capas."),
        F("f4-paquetes", "Paquetes del repositorio y sus dependencias"),
        F("f4-clases-dominio", "Clases del núcleo"),
        F("f4-clases-cascara", "Clases de la cáscara y de la capa de anticorrupción"),
        T("tipos", "Vocabulario del modelo", [1800, 3400, 3800], [
            ["Tipo", "Valores", "Qué representa"],
            ["HandleCategory", "Iterator, Reference, Pointer", "Clase del handle en la norma; el puntero sigue la regla de la referencia"],
            ["Relation", "Same, Before, After, Any", "El elemento frente al punto de la mutación"],
            ["EffectKind", "Preserves, Depends, Invalidates", "Efecto de una regla"],
            ["Condition", "None, CapacityReached, RehashTriggered, NonBinding", "De qué depende un efecto Depends"],
            ["Point", "Front, Back, Interior, Whole, ByKey", "Dónde actúa la mutación"],
            ["Growth", "One, None, Shrinks, Unknown, Reset", "Cuánto cambia size(); lo usa el crédito"],
            ["UnresolvedReason", "DependsOnState, RelationUnknown", "Por qué un handle no está resuelto"],
            ["PolicyMode", "Silent, Possibly", "Política ante lo no resuelto"],
        ], "El código conserva además la razón EscapedToOpaqueCode, de la primera versión del escape, que ya no se produce porque el escape olvida el handle (sección 4.2.7.4)."),

        H4("4.2.3.5 Colaboración con el motor de análisis"),
        P("El motor de ejecución simbólica conserva el control del recorrido: el checker no recorre el programa, sino que recibe eventos de cada camino y responde con un estado nuevo (LLVM Project, 2026c). El checker se suscribe a seis eventos, que la {F:f4-eventos} relaciona con lo que representan en el modelo."),
        F("f4-eventos", "Eventos del analizador y su significado en el modelo"),
        P("La {F:f4-secuencia} muestra la secuencia para el caso f_vector_erase_begin_ref_recto, en el que una referencia al primer elemento de un vector se usa después de borrar ese elemento. La obtención crea el handle; el borrado lo invalida y deja una nota en la ruta; la lectura posterior de la referencia produce el aviso. Este último paso no involucra ninguna llamada: el uso de una referencia es una lectura de memoria, y por eso un checker que solo observara llamadas no podría detectarlo."),
        F("f4-secuencia", "Secuencia de un caso del banco dentro del analizador"),

        H4("4.2.3.6 Datos de la evaluación"),
        P("El checker no guarda datos fuera del estado de cada camino. La evaluación, en cambio, produce archivos que se relacionan como muestra la {F:f4-datos}. Una mutación de la matriz da lugar a sus reglas y a los casos del banco; cada caso tiene sus ejecuciones de validación y una invocación del analizador por condición, y de cada invocación resulta un cotejo. Los conteos se suman desde los cotejos, y las métricas se calculan al final a partir de esos conteos, nunca promediando métricas de grupos."),
        F("f4-datos", "Modelo de datos de la evaluación"),

        H4("4.2.3.7 Infraestructura de ejecución"),
        P("El desarrollo y el experimento se ejecutaron en una computadora personal con procesador Intel Core i7-13620H, 16 GB de memoria y Ubuntu 24.04. Para que el entorno pudiera reproducirse, el compilador, la biblioteca estándar y las herramientas se definieron en un archivo Dockerfile (Ubuntu 24.04 y LLVM 21), con el que también construye su imagen el servicio de integración continua del repositorio. Ese archivo fija la versión principal de cada componente. La versión exacta de Clang y de libstdc++ queda en el registro de cada ejecución, y la de los demás componentes se consultó en la imagen. La {T:infra} lista los componentes de la infraestructura y la {F:f4-fisica} los ubica."),
        T("infra", "Componentes de la infraestructura de ejecución", [3000, 2000, 4000], [
            ["Componente", "Versión observada", "Función"],
            ["Clang y LLVM", "21.1.8", "Compilador y analizador estático que carga el checker"],
            ["g++", "13.3.0", "Compilación de los casos en la validación con libstdc++ Debug"],
            ["libstdc++", "13.3.0", "Biblioteca estándar analizada y usada en la validación dinámica"],
            ["Imagen Docker checker:llvm21", "Ubuntu 24.04", "Entorno fijo para compilar, analizar y medir"],
            ["CMake y Ninja", "3.28.3 y 1.11.1", "Compilación del checker y de sus pruebas"],
            ["GoogleTest", "Paquete de Ubuntu 24.04", "Pruebas unitarias del núcleo"],
            ["lit", "18.1.8", "Pruebas de programas mínimos con el analizador"],
            ["Python", "3.12", "Generación del banco, arnés de ejecución y procesamiento de resultados"],
            ["AddressSanitizer, UndefinedBehaviorSanitizer y libstdc++ Debug", "Los de Clang 21.1.8 y libstdc++ 13.3.0", "Validación dinámica de las etiquetas"],
            ["Git y GitHub Actions", "—", "Control de versiones, etiqueta del banco congelado e integración continua"],
        ]),
        F("f4-fisica", "Arquitectura física de la ejecución"),
        P("El arnés invoca el compilador como proceso, con los argumentos separados y sin pasar por una consola, y lee los diagnósticos en formato SARIF. Cada caso se analizó en una invocación propia del analizador, para que la caída de una invocación no afectara a los demás casos y para medir el tiempo y la memoria de cada uno."),
        P("La integración continua repite la verificación en cada cambio, con una imagen construida desde el mismo archivo, como muestra la {F:f4-ci}. Falla si el checker no compila, si una prueba falla, si no pasa la comprobación de formato o de tipos, si la cobertura de líneas del núcleo baja de 90 %, si un caso SAFE gana un aviso confirmado, si un caso UB que se detectaba deja de detectarse, si aparece una incidencia o si el costo supera sus umbrales."),
        F("f4-ci", "Integración continua del checker"),

        H3("4.2.4 Construcción y validación del banco de casos"),
        P("El primer objetivo específico requería un banco cuyas etiquetas procedieran de la norma y no del analizador. Se siguieron cinco actividades: registrar las reglas, generar los casos, añadir los casos con garantía, revisar la coherencia de las etiquetas y validarlas por ejecución. Al final el banco se congeló. Estas actividades no fueron estrictamente sucesivas: la revisión lógica empezó antes de escribir el checker, y los casos con garantía se añadieron cuando este ya existía, antes de sellar el banco."),
        H4("4.2.4.1 Registro de las reglas"),
        P("Las reglas de invalidación de la norma N4659 se registraron en un único archivo, la matriz normativa. Cada mutación indica el contenedor, la operación, el punto donde actúa y cuánto cambia el tamaño; cada una de sus reglas indica la clase de handle, la relación y el efecto y, si invalida o depende del estado, la cláusula de la norma, como muestra la {F:lst-matriz}. El puntero no tiene reglas propias, porque sigue la regla de la referencia. La {T:matriz} describe los campos."),
        L("lst-matriz", "Una mutación de la matriz normativa", """
{ "id": "vector.push_back.back",
  "contenedor": "vector", "operacion": "push_back",
  "punto": "back", "crecimiento": "one", "banco": ["push_back"],
  "reglas": [
    { "categoria": "iterator", "relacion": "before", "efecto": "depends",
      "condicion": "capacity_reached", "clausula": "[vector.modifiers] insert" },
    { "categoria": "reference", "relacion": "before", "efecto": "depends",
      "condicion": "capacity_reached", "clausula": "[vector.modifiers] insert" } ] }""",
          "Tomado de norma/matriz.json; se cambió solo el espaciado."),
        T("matriz", "Campos de la matriz normativa", [1700, 3900, 3400], [
            ["Campo", "Valores", "Significado"],
            ["contenedor", "Los diez del alcance", "Contenedor de la mutación"],
            ["operacion", "push_back, erase, clear y las demás", "Función miembro"],
            ["punto", "front, back, interior, whole, by_key", "Dónde actúa"],
            ["crecimiento", "one, none, shrinks, unknown, reset", "Cuánto cambia size()"],
            ["banco", "Lista de pares del banco", "Qué pares del banco se escriben con esta mutación"],
            ["categoria", "iterator, reference", "Clase de handle"],
            ["relacion", "same, before, after, any", "Elemento frente al punto"],
            ["efecto", "preserves, invalidates, depends", "Consecuencia para el handle"],
            ["condicion", "capacity_reached, rehash_triggered, non_binding", "De qué depende el efecto"],
            ["clausula", "Por ejemplo, [vector.modifiers] insert", "Respaldo en N4659; solo en reglas que invalidan o dependen del estado"],
        ]),
        P("Un script genera desde la matriz la tabla de reglas que se compila con el checker. Antes de generarla comprueba cuatro leyes del modelo, de modo que la construcción falla si una regla las contradice. Son las de la {T:leyes-norma}."),
        T("leyes-norma", "Leyes que se comprueban al generar la tabla", [4300, 4700], [
            ["Ley", "Qué evita"],
            ["Un iterador nunca está mejor que una referencia al mismo elemento", "Una regla que preserve el iterador e invalide la referencia"],
            ["Insertar en un contenedor de nodos no invalida nada", "Reglas de vector copiadas a list o map"],
            ["Lo que está antes del punto sobrevive en un vector si no se realoca", "Invalidar por error la parte anterior del búfer"],
            ["Una mutación de todo el contenedor no depende de la relación", "Reglas que distingan posiciones donde la norma no lo hace"],
        ]),
        H4("4.2.4.2 Generación de los casos"),
        P("Los casos se generaron por combinación de los 57 pares contenedor–operación de la {T:pares} con las tres clases de handle y cuatro formas sintácticas. Cada caso es una función mínima con un handle sostenido, una operación y un único punto de uso, y su nombre conserva la celda de la matriz de la que procede. La {F:lst-formas} presenta las cuatro formas con casos reales, y la {T:formas} indica qué pone a prueba cada una."),
        L("lst-formas", "Las cuatro formas sintácticas de los casos", """
void f_vector_erase_begin_ref_recto(std::vector<int>& c) {
  auto it = c.begin();
  const auto& h = *it;
  c.erase(c.begin());
  sink(h);
}
void f_vector_push_back_it_guarda(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  c.push_back(1);
  sink(*it);
}
void f_vector_erase_begin_ref_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3; ++it) {
    const auto& h = *it;
    c.erase(c.begin());
    sink(h);
  }
}
void f_vector_erase_begin_ref_llamada(std::vector<int>& c) {
  auto it = c.begin();
  if (it == c.end()) return;
  const auto& h = *it;
  mutar_vector_erase_begin(c);
  sink(h);
}""", "Tomado de test/corpus.cpp, que se genera con bench/gen_corpus.py."),
        T("formas", "Formas sintácticas del banco", [1200, 4300, 3500], [
            ["Forma", "Cómo se escribe", "Qué pone a prueba"],
            ["Recta", "El handle se usa justo después de la operación, sin comprobación previa", "El caso sin ayudas para el analizador"],
            ["Guarda", "Antes de obtener el handle se comprueba que el contenedor no esté vacío, con if (it == c.end()) return;", "Si una comparación con end() cambia el comportamiento de los checkers"],
            ["Bucle", "La operación ocurre dentro de un recorrido de tres rondas como máximo", "Que el iterador que controla el recorrido sea un segundo handle"],
            ["Llamada", "La operación ocurre en una función auxiliar", "El seguimiento a través de una llamada"],
        ]),
        P("La etiqueta se calcula desde la matriz con el procedimiento de la {F:f4-etiqueta}. En la forma de bucle con referencia o puntero intervienen dos handles, el sostenido y el iterador que controla el recorrido, y la etiqueta del caso es la peor de las dos, en el orden SAFE, POLICY y UB; cuando el handle sostenido es un iterador, es el mismo que controla el recorrido. Por eso el registro de cada caso guarda también la etiqueta de cada handle: el cotejo la necesita para saber si un aviso cayó sobre un handle inválido. La {F:f4-trazabilidad} muestra el recorrido completo de una regla: de la cláusula de la norma salen, por vías separadas, la etiqueta del caso y la decisión del checker, y una prueba compara ambas en 183 celdas (57 pares × 3 clases de handle, más 12 con reserva). La forma de bucle y el iterador devuelto quedan fuera de esa prueba y se comprueban con lit y con el banco."),
        F("f4-etiqueta", "Cálculo de la etiqueta de un caso"),
        F("f4-trazabilidad", "Trazabilidad de una regla hasta la etiqueta y la decisión"),
        H4("4.2.4.3 Casos con garantía"),
        P("A los 684 casos de la matriz se añadieron, cuando el checker ya existía y antes de sellar el banco, 66 casos de buen uso con garantía: 54 que reservan capacidad con reserve(size() + k) antes de insertar y 12 que usan el iterador devuelto por la operación. La {F:lst-garantia} presenta un ejemplo de cada grupo. Estos casos se incorporaron porque, sin ellos, un checker que avisara en cada inserción no tendría ninguna falsa alarma que medir. La {T:composicion} presenta la composición del banco."),
        L("lst-garantia", "Casos de buen uso con garantía", """
void f_vector_push_back_ref_recto_reserva(std::vector<int>& c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  const auto& h = *it;
  c.push_back(1);
  sink(h);
}
void f_vector_erase_ret_it_bucle(std::vector<int>& c) {
  int rondas = 0;
  for (auto it = c.begin(); it != c.end() && rondas++ < 3;) {
    it = c.erase(it);
    if (it != c.end()) sink(*it);
  }
}""", "Tomado de test/corpus.cpp."),
        T("composicion", "Composición del banco de casos por grupo y etiqueta", [5000, 1000, 1000, 1000, 1000], [
            ["Grupo", "Casos", "UB", "SAFE", "POLICY"],
            ["Matriz normativa (57 pares × 3 clases de handle × 4 formas)", "684", "342", "240", "102"],
            ["Buen uso con reserva previa de capacidad", "54", "0", "54", "0"],
            ["Buen uso del iterador devuelto", "12", "0", "12", "0"],
            ["Total", "750", "342", "306", "102"],
        ], "UB: el uso emplea un handle invalidado; SAFE: la norma conserva su validez; POLICY: la validez depende del estado del contenedor en ejecución."),
        H4("4.2.4.4 Revisión lógica de las etiquetas"),
        P("Antes de medir, se revisó la coherencia lógica de las reglas: una misma expresión pequeña del modelo se calculó de dos maneras y, cuando ambas daban resultados distintos, se registró una contradicción. Se encontraron seis, que la {T:contradicciones} resume. Las tres primeras cambiaron el diseño del checker antes de escribir su código, y las tres últimas corrigieron el banco antes de sellarlo. Dos de estas últimas mostraron que 27 etiquetas eran incompatibles con la norma: 21 casos etiquetados como UB y 6 como SAFE dependían en realidad del estado del contenedor. Todos pasaron a POLICY, y la corrección quedó registrada con su justificación."),
        T("contradicciones", "Contradicciones encontradas al revisar las reglas", [500, 2700, 3200, 2600], [
            ["N.º", "Contradicción", "Por qué era un error", "Resolución"],
            ["1", "Una posición guardada como «primero» deja de serlo", "Tras una inserción al frente, el elemento ya no es el primero y una regla posterior se aplicaría a otro", "Toda mutación transporta la posición de los handles"],
            ["2", "Reasignar una variable parecía revivir un handle", "Identificar el handle por la variable confunde dos elementos", "El handle se identifica por la región del elemento"],
            ["3", "Una referencia y el puntero al mismo elemento tenían dos estados", "r y &r designan el mismo elemento", "Comparten el estado de esa región"],
            ["4", "El bucle convertía «depende» en UB", "Si hay capacidad, las tres rondas no realocan: el defecto no ocurre con todas las entradas", "La etiqueta es el peor efecto de los handles; 21 casos pasan de UB a POLICY"],
            ["5", "El par insert_middle de deque insertaba en el frente", "El nombre y la sentencia decían cosas distintas: en un extremo, las referencias sobreviven", "La sentencia pasa a c.insert(c.begin() + 1, 1); la etiqueta no cambia"],
            ["6", "En contenedores no ordenados con referencia sostenida, el iterador de control no se tenía en cuenta", "La referencia se preserva, pero el iterador de control depende del rehash", "6 casos pasan de SAFE a POLICY"],
        ], "Las contradicciones están en libro/diseno/leyes.md y su corrección, en la decisión D-18 de libro/diseno/decisiones.md."),
        H4("4.2.4.5 Validación dinámica"),
        P("Cada caso se compiló y ejecutó con libstdc++ en modo de depuración (_GLIBCXX_DEBUG) y con AddressSanitizer y UndefinedBehaviorSanitizer, con un límite de 2 segundos por ejecución, según el flujo de la {F:f4-validacion}. Los casos UB y SAFE se ejecutaron en un solo estado inicial, el ordinario. Los casos POLICY se ejecutaron en sus dos estados: uno que fuerza la invalidación y otro que la evita, como detalla la {T:escenarios}. Por eso los 750 casos dieron lugar a 852 ejecuciones, entendidas como combinaciones de caso y estado, cada una con libstdc++ Debug y con los sanitizadores."),
        T("escenarios", "Estados de ejecución de los casos POLICY", [2400, 3300, 3300], [
            ["Contenedor u operación", "Estado que fuerza la invalidación", "Estado que la evita"],
            ["vector (en general)", "Capacidad agotada antes de la mutación", "Capacidad 512, con espacio para la mutación"],
            ["vector::reserve y resize con aumento", "Capacidad agotada antes de la mutación", "Capacidad 512, suficiente para size() + 100 tres veces"],
            ["vector::pop_back", "Un solo elemento: pop_back alcanza al elemento designado", "8 elementos: tres rondas no alcanzan al iterador"],
            ["vector::shrink_to_fit", "Con holgura de capacidad", "Capacidad ya ajustada al tamaño"],
            ["unordered_set, unordered_map", "Factor de carga alcanzado: la inserción dispara rehash", "reserve(256): sin rehash en la inserción evaluada"],
        ], "shrink_to_fit es una solicitud no vinculante, de modo que su resultado se registra y no se presupone. El registro rotula las 12 ejecuciones de pop_back con el texto genérico de vector; el estado real lo fija el ejecutor (test/runtime_runner.cpp)."),
        P("Se consideró contradicción toda detección dinámica en un caso SAFE o en un caso POLICY en el estado que preserva la validez. La ausencia de detección en un caso UB no se consideró contradicción, porque estas herramientas no detectan todos los usos inválidos, por las razones de la {T:mecanismos}. La etiqueta definitiva siguió siendo la que da la norma; la ejecución solo servía para detectar contradicciones con ella. Además de las contradicciones, se contabilizó en qué proporción de los casos UB, y de los casos POLICY en el estado que fuerza la invalidación, alguna herramienta observó el defecto. Esa proporción mide la concordancia que plantea la pregunta específica 1."),
        F("f4-validacion", "Flujo de la validación dinámica"),
        H4("4.2.4.6 Congelamiento"),
        P("Con las etiquetas corregidas y validadas, el banco se congeló como banco-1: su contenido se selló con un resumen sha256 antes de medir las condiciones del experimento. El sello, que muestra la {F:lst-sello}, permite comprobar que ningún caso ni etiqueta cambió después, y el arnés lo verifica antes de cada ejecución. La versión del repositorio (commit) que contiene el banco y los registros de ejecución y de cotejo se marcó después con la etiqueta de Git banco-1; el contraste estadístico se añadió en un commit posterior. Corregir el banco exige crear uno nuevo y repetir las mediciones."),
        L("lst-sello", "Sello del banco congelado", """
{
 "banco": "banco-1",
 "fecha": "2026-10-20",
 "casos": 750,
 "corpus.cpp": "efe9a7f0c3d473fec4f54f633ed8c25ef119b1eb8224549b86dd4806ec9a2ef5",
 "corpus_truth.json": "d0b680f1ab0e224441a0d0e7a79ae4fa94fdcc7d46af721251e6a6279500b9db",
 "nota": "Congelado con D-18 y D-20 aplicadas. Cambiar el banco exige un banco-2
          nuevo, no editar este."
}""", "Tomado de test/banco-1.json; la nota ocupa una sola línea en el archivo."),
        P("El producto del OE1 fue la matriz normativa, el banco congelado de 750 casos con sus etiquetas y el registro de las 852 ejecuciones de la validación dinámica."),

        H3("4.2.5 Caracterización de la línea base"),
        H4("4.2.5.1 Configuración de referencia"),
        P("La configuración B representa lo que ofrece Clang Static Analyzer 21.1.8 al activar los checkers pertinentes: core, cplusplus y los checkers experimentales alpha.cplusplus.IteratorModeling, ContainerModeling, InvalidatedIterator, IteratorRange y MismatchedIterator. Clang Lifetime Safety, descrito en la sección 2.2.2, no se incluyó porque es un análisis de flujo de datos del compilador y no un checker del analizador. Se activó además la opción aggressive-binary-operation-simplification, que el modelado de iteradores requiere para comparar posiciones. Las mismas opciones se aplicaron en las cuatro condiciones. La {F:lst-comando} presenta la orden."),
        L("lst-comando", "Orden de análisis de un caso en la configuración B", """
clang++ --analyze --analyzer-output sarif -std=c++17
  -Xclang -analyzer-checker=core,cplusplus,alpha.cplusplus.IteratorModeling,
          alpha.cplusplus.ContainerModeling,alpha.cplusplus.InvalidatedIterator,
          alpha.cplusplus.IteratorRange,alpha.cplusplus.MismatchedIterator
  -Xclang -analyzer-config -Xclang aggressive-binary-operation-simplification=true
  -Xclang -analyze-function=<firma del caso>
  -o caso.sarif test/corpus.cpp""",
          "Tomado del bloque meta del registro de ejecución; los dos últimos argumentos los añade por caso bench/experimento.py, y la lista de checkers es un solo argumento, partido aquí para que quepa."),
        H4("4.2.5.2 Procedimiento de medición"),
        P("La {F:f4-lineabase} muestra el procedimiento. Cada caso se analizó con una invocación limitada a su función y un límite de 120 segundos. El arnés leyó la salida SARIF y conservó cada aviso en el registro de ejecución, junto con el tiempo y la memoria máxima. El cotejo se hizo por sitio: un aviso cuenta como detección si recae sobre un handle que la norma da por inválido. Una caída, un error de compilación, un tiempo agotado o una salida ilegible se registraron como incidencia y no como ausencia de aviso, para que un fallo no pudiera mejorar la precisión."),
        F("f4-lineabase", "Medición de la línea base"),
        H4("4.2.5.3 Clasificación de las omisiones"),
        P("Para identificar las causas de las omisiones, cada caso UB sin aviso se clasificó en una de cuatro causas probables, propuestas a partir del funcionamiento de los checkers de Clang (sección 2.2.2) y de la forma del caso. La causa se asignó con una regla sobre los atributos del caso y no se verificó caso por caso, de modo que describe la explicación más probable. Cuando aplicaba más de una causa, se asignó la primera en el orden de la {F:f4-causas}. La {T:causas} indica la evidencia de cada una."),
                T("causas", "Causas de omisión de la configuración de referencia", [700, 3700, 4600], [
            ["Causa", "Enunciado", "Qué la identifica en el caso"],
            ["1", "El dominio de referencias y punteros no está modelado", "El handle sostenido es una referencia o un puntero"],
            ["2", "El modelado no se activa sin una comparación previa contra end()", "El iterador se usa en la forma recta"],
            ["3", "El modelado del borrado no alcanza la posición del iterador del caso", "La operación borra: erase, pop_front, pop_back o clear"],
            ["4", "El modelado de la inserción o la realocación no alcanza la posición del iterador del caso", "La operación inserta, redimensiona, reserva o hace rehash"],
        ], "La regla está en la función causa de bench/experimento.py, y su resultado, en test/corpus_fallos.json. La función prevé una quinta salida para otras operaciones, y los enunciados del archivo tienen otra redacción."),
        F("f4-causas", "Árbol de clasificación de las omisiones"),
        P("Cada falsa alarma que emitiera la configuración B se cotejaría con la regla de su caso en la ficha de resultados, y lo encontrado se informa en el capítulo V."),
        P("El producto del OE2 fue el registro de la configuración B sobre los 750 casos y el catálogo de omisiones por causa, junto con la revisión de las falsas alarmas, cuyos valores se presentan en el capítulo V."),

        H3("4.2.6 Diseño e implementación del checker"),
        P("El tercer objetivo específico se cumplió en los incrementos I0 a I3 y I5. Esta sección describe cómo el checker reconoce las operaciones, cómo representa el estado y las posiciones, cómo decide y avisa, y cómo se verificó."),
        H4("4.2.6.1 Reconocimiento de operaciones y handles"),
        P("La capa de anticorrupción reconoce los contenedores por su tipo y las llamadas por el nombre de la función miembro, y traduce cada llamada al vocabulario del modelo. La {T:reconocimiento} indica qué se reconoce y cómo se interpreta. Las mutaciones son las 101 de la matriz normativa. El iterador end() quedó fuera de las obtenciones, porque no designa un elemento."),
        T("reconocimiento", "Eventos del programa que reconoce el checker", [1900, 4300, 2800], [
            ["Evento del modelo", "Expresiones de C++", "Dónde se reconoce"],
            ["Obtención de un iterador", "begin, cbegin, find, lower_bound, upper_bound; iterador devuelto por insert, emplace o erase, también como .first de un par", "iteratorObtention, mutation; returnedPairFirst en la cáscara"],
            ["Obtención de un elemento", "\\*it, it->, c[i], at, front, back, data", "iteratorUse, elementAccess"],
            ["Mutación", "Las 101 de la matriz, con su punto y, en erase, su rango", "mutation"],
            ["Movimiento o copia de iterador", "++it, --it, it + k, std::next, std::advance; auto it2 = it", "iteratorUse, iteratorCopy"],
            ["Uso de iterador", "\\*it, it->, ++it, comparaciones, c.erase(it)", "iteratorUse, argumentIterator"],
            ["Uso de elemento", "Lectura o escritura de memoria, p->m(), f(p->campo) por referencia", "checkLocation y checkPreCall en la cáscara; categoryAtLoad decide la categoría"],
        ]),
        P("Pasar un puntero por valor no se trató como uso, porque en C++17 solo la indirección a través de un puntero inválido es comportamiento indefinido. La clase que nombra el mensaje se decide en el sitio de uso: la misma región puede usarse como referencia o como puntero, y el aviso nombra la forma que aparece en esa línea."),
        H4("4.2.6.2 Representación del estado"),
        P("El estado del checker se guarda en tres mapas inmutables dentro del estado de cada camino, como muestra la {F:lst-mapas}. El primero asocia la región del elemento con el estado de las referencias y los punteros que lo designan; el segundo, la región de cada objeto iterador con su estado; y el tercero, la región del contenedor con el crédito de garantía de la sección 4.2.7. El handle se identificó por la región del elemento y no por la variable, porque una referencia r y el puntero &r designan el mismo elemento y deben compartir su validez."),
        L("lst-mapas", "Registro de los mapas en el estado del camino", """
// Región del elemento -> estado; región del objeto iterador -> estado;
// región del contenedor -> crédito de reserve (ausente = Unknown).
REGISTER_MAP_WITH_PROGRAMSTATE(ElementMap, const MemRegion *, Stored)
REGISTER_MAP_WITH_PROGRAMSTATE(IteratorMap, const MemRegion *, Stored)
REGISTER_MAP_WITH_PROGRAMSTATE(CreditMap, const MemRegion *, unsigned)""", "Tomado de plugin/checker/InvalidationChecker.cpp."),
        P("Como el analizador no entra por defecto en el código de las funciones de los contenedores, cada obtención produce un símbolo y una región nuevos; esa región es el handle. Cuando una región deja de estar viva, el evento de muerte de símbolos retira su entrada de los tres mapas."),
        H4("4.2.6.3 Posiciones y relación con la mutación"),
        P("Para decidir qué regla aplica, el checker compara la posición del handle con el punto de la operación, como ilustra la {F:f4-relacion}. La posición se representa de forma simbólica, porque el analizador no conoce el tamaño del contenedor; la {T:posicion} presenta las cinco formas posibles. Si dos posiciones parten de la misma base, se comparan sus desplazamientos. Si no, como ocurre entre primero más a y último menos b, la relación no se conoce, y el checker considera todas las relaciones que la norma admite para esa mutación."),
        F("f4-relacion", "Relación de cinco elementos con el punto de una operación", "e2 es el elemento en el punto de la operación."),
        T("posicion", "Formas de la posición de un handle", [1900, 3800, 3300], [
            ["Forma", "Significado", "Ejemplo de obtención"],
            ["First + n", "n elementos después del primero", "c.begin(), c.front(), c[2]"],
            ["Last − n", "n elementos antes del último", "c.back()"],
            ["Anchor(id) + n", "n elementos después de un punto conocido solo por su identidad", "Una posición que no se puede expresar desde los extremos"],
            ["PastEnd", "El final de la secuencia", "Avanzar más allá del último elemento"],
            ["Unknown", "No se sabe", "Tras una mutación de todo el contenedor que puede reordenar"],
        ]),
        P("Toda mutación que preserva un handle también actualiza su posición, porque el elemento designado puede haberse desplazado: tras push_front, el que era primero queda en First + 1. El borrado de un rango se trató como la misma mutación que el borrado de un elemento, con la relación calculada frente al rango semiabierto, de modo que el extremo final del rango conserva su validez. Las constantes enteras que no caben en los tipos del modelo, como un índice de 64 bits, se tratan como desconocidas, para evitar interrumpir al compilador."),
        H4("4.2.6.4 Decisión"),
        P("Ante una mutación, la cáscara recorre los handles del mismo contenedor y pide al núcleo que aplique la mutación a cada uno. La {F:f4-apply} muestra esa decisión y la {F:lst-apply}, la parte final de su código. Primero se calculan las relaciones candidatas: las que permite la comparación de posiciones, restringidas a las que la norma contempla. Si esas relaciones dan efectos distintos, el handle queda no resuelto, con la razón de relación desconocida. Si coinciden, se aplica el efecto común. Como el checker no modela el tamaño ni la capacidad, de las tres situaciones de la sección 2.3.7 solo se presentan dos: la condición se descarta o queda no resuelta. La rama OnlyYes del listado no se alcanza en esta versión."),
        F("f4-apply", "Decisión del núcleo al aplicar una mutación a un handle"),
        L("lst-apply", "Aplicación del efecto común en el núcleo", """
switch (Common->Kind) {
case EffectKind::Preserves: return {Transported(H), false};
case EffectKind::Invalidates: return {H.withValidity(Validity::invalidated(E)), true};
case EffectKind::Depends:
  switch (answer(Common->Cond, G, C)) {
  case SolverAnswer::OnlyNo: return {Transported(H), false};
  case SolverAnswer::OnlyYes: return {H.withValidity(Validity::invalidated(E)), true};
  case SolverAnswer::Both: {
    Validity V = H.validity().join(Validity::dependsOn(Common->Cond, E));
    return {Transported(H).withValidity(V), V != H.validity()};
  }
  }
}""", "Tomado de plugin/dominio/Decisions.cpp. El segundo valor indica si corresponde una nota en la ruta."),
        H4("4.2.6.5 Emisión de avisos"),
        P("Ante un uso, el núcleo devuelve el veredicto y la cáscara emite el aviso como error no fatal, para que el análisis del camino continúe. El checker define dos tipos de aviso: uso de un handle invalidado, que es confirmado, y uso de un handle posiblemente invalidado, que depende de la política. El mensaje nombra la operación, la línea en que ocurrió y, en el caso posible, la garantía que falta."),
        P("La {F:lst-aviso} presenta la salida real del analizador sobre dos funciones de ejemplo, con la política Possibly. La primera borra el elemento y produce un aviso confirmado; la segunda inserta sin garantía y produce un aviso posible. Las notas forman la ruta del defecto: dónde se obtuvo el handle, qué operación lo afectó y dónde se usó."),
        L("lst-aviso", "Avisos del checker en la terminal", """
ejemplo.cpp:7:8: warning: Uso de una referencia invalidada: 'std::vector::erase'
                 (línea 6) lo invalidó [ucsm.ContainerInvalidation]
    7 |   sink(h);
ejemplo.cpp:5:12: note: El handle al elemento se obtiene de 'std::vector::front'
    5 |   int &h = c.front();
ejemplo.cpp:6:3: note: El handle al elemento queda invalidado por 'std::vector::erase'
    6 |   c.erase(c.begin());
ejemplo.cpp:13:8: warning: Uso de una referencia posiblemente invalidada:
                 'std::vector::push_back' (línea 12) si la capacidad está agotada
                 reubica los elementos; nada garantiza espacio: use reserve(size() + n)
                 antes, o vuelva a obtenerlo [ucsm.ContainerInvalidation]
   13 |   sink(h);
ejemplo.cpp:11:12: note: El handle al elemento se obtiene de 'std::vector::front'
   11 |   int &h = c.front();
ejemplo.cpp:12:3: note: El handle al elemento puede quedar invalidado por
                 'std::vector::push_back'
   12 |   c.push_back(1);""", "Salida de clang++ con -analyzer-output=text. Se partieron las líneas largas y se omitieron las marcas de columna y la repetición del mensaje como nota final."),
        H4("4.2.6.6 Verificación del checker"),
        P("El checker se verificó en cuatro niveles, que la {F:f4-piramide} ordena. Las pruebas unitarias del núcleo, escritas con GoogleTest, comprueban las leyes del modelo y las decisiones de la tabla; la {T:gtest} las agrupa. Las pruebas lit comprueban, en programas mínimos, que el analizador con el checker emite el aviso y la nota esperados; la {T:lit} presenta sus archivos. El banco actúa como prueba de regresión de los incrementos I2 a I4. El código real se usó para comprobar si el checker interrumpe al compilador en proyectos que no se escribieron para el estudio."),
        F("f4-piramide", "Niveles de verificación del checker"),
        T("gtest", "Pruebas unitarias del núcleo", [1400, 900, 6700], [
            ["Grupo", "Pruebas", "Qué comprueba"],
            ["Norma", "4", "Referencia y puntero siguen la misma regla; un iterador nunca está mejor que una referencia; la tabla es total; invalidar o depender cita su cláusula"],
            ["Posicion", "9", "Comparación de anclas, transporte, rango semiabierto, rango vacío, distancia y avance desde el final"],
            ["Deteccion", "24", "Obtener da un handle válido; inválido es absorbente; aplicar nunca mejora la validez; crédito, política, avisos únicos, movimiento y escape"],
            ["Lenguaje", "2", "Todo nombre del lenguaje tiene texto; toda mutación de la norma es conocida"],
            ["Banco", "1", "El veredicto del núcleo es la etiqueta del banco, en 183 celdas"],
            ["Total", "40", ""],
        ]),
        T("lit", "Archivos de pruebas lit", [1700, 1000, 900, 5400], [
            ["Archivo", "Avisos", "Notas", "Qué comprueba"],
            ["registro.cpp", "0", "0", "El analizador carga el complemento y lo registra"],
            ["referencias.cpp", "11", "0", "Referencias y punteros: obtención, mutación y uso"],
            ["iteradores.cpp", "10", "0", "Iteradores, copias, movimientos y erase de rango"],
            ["garantias.cpp", "6", "0", "Crédito de reserve, política y escape"],
            ["rutas.cpp", "3", "9", "Notas de obtención y de mutación en la ruta"],
            ["Total", "30", "9", ""],
        ], "Las cifras cuentan las marcas expected-warning y expected-note de cada archivo."),
        P("La calidad del código se controló con el formato de LLVM, la comprobación de tipos de los módulos del arnés con mypy, y un umbral de cobertura de líneas del núcleo de al menos 90 %. Además, el sistema de compilación trata como error un switch sobre un tipo del modelo que olvide un caso."),
        P("El producto del OE3 fue el checker compilado como complemento del analizador, con 40 pruebas unitarias y 5 archivos de pruebas lit."),

        H3("4.2.7 Política ante condiciones indeterminadas"),
        H4("4.2.7.1 Condiciones que dependen del estado"),
        P("Algunas reglas de la norma no dependen solo de la operación. Una inserción en un vector invalida siempre lo que está en el punto o después, pero lo que está antes solo si el tamaño alcanza la capacidad; una inserción en un contenedor no ordenado invalida los iteradores solo si provoca un rehash. En esos casos la matriz asigna el efecto «depende del estado», y el checker debe decidir con la información que el camino ofrece. Hay tres condiciones de ese tipo, que la {T:condiciones} presenta con las garantías capaces de descartarlas. También queda no resuelto un handle cuya relación con el punto no se conoce, si las relaciones posibles dan efectos distintos, como ocurre entre pop_back y el primer elemento."),
        T("condiciones", "Condiciones de estado y garantías", [2100, 3700, 3200], [
            ["Condición", "Garantía que la descarta", "Cómo la ve el checker"],
            ["CapacityReached (vector)", "reserve(size() + k) seguido de k inserciones como máximo", "Crédito por contenedor"],
            ["RehashTriggered (no ordenados)", "reserve(size() + k) seguido de k inserciones como máximo", "Crédito por contenedor"],
            ["NonBinding (vector::shrink_to_fit)", "Ninguna: la norma no obliga a la implementación", "Siempre queda no resuelto"],
            ["Relación desconocida", "Tamaño conocido de al menos dos elementos", "No se modeló el tamaño: queda no resuelto"],
        ]),
        H4("4.2.7.2 Crédito de garantía"),
        P("El checker no modela la capacidad ni el tamaño del contenedor, porque el analizador solo dispone de símbolos para ellos y asignarles un valor concreto sería inventar un dato. En su lugar lleva la cuenta de lo que el código garantiza, con un crédito de garantía por contenedor: la llamada reserve(size() + k) concede k inserciones que no realocan, cada llamada a una operación que añade un elemento consume una y cualquier operación no contada anula el crédito. La {F:f4-credito} muestra sus transiciones y la {T:credito}, el efecto de cada clase de operación."),
        F("f4-credito", "Transiciones del crédito de garantía de un contenedor"),
        T("credito", "Efecto de las operaciones sobre el crédito", [1500, 3900, 3600], [
            ["Crecimiento", "Operaciones", "Crédito después"],
            ["One", "Las que añaden un elemento, como push_back, emplace_back e insert", "Disminuye en 1 si era conocido y mayor que 0"],
            ["None, Shrinks", "Operaciones que no cambian o que reducen el tamaño", "Sin cambio"],
            ["Unknown, Reset", "Operaciones cuyo crecimiento no se cuenta, como resize, clear y assign", "Pasa a desconocido"],
        ]),
        P("Esta decisión tiene tres límites conocidos. Una comprobación explícita como if (v.size() < v.capacity()) antes de insertar no se reconoce como garantía, porque exigiría modelar esas dos llamadas; el resultado es un aviso posible, nunca uno confirmado. En sentido contrario, el reconocimiento no mira los argumentos de insert, de modo que un insert de rango consume un solo crédito, y tampoco comprueba que el size() de reserve sea del mismo contenedor. En estos dos casos el checker podría callar ante un defecto real. Ninguno de los dos aparece en el banco."),
        H4("4.2.7.3 Decisión y política"),
        P("La {F:f4-decision} resume la decisión. Si hay crédito suficiente, la condición se descarta y el handle conserva su validez. Si no lo hay, el handle queda no resuelto, con la razón que explica por qué. Lo que el checker hace con un handle no resuelto lo fija su política, que admite dos modos. Con Silent no emite aviso; con Possibly emite un aviso posible que nombra la garantía que falta. La {T:politica} presenta el veredicto de cada estado según el modo."),
        F("f4-decision", "Decisión ante una inserción que depende de la capacidad"),
        T("politica", "Veredicto de un uso según el estado y la política", [3000, 3000, 3000], [
            ["Estado del handle", "Silent", "Possibly"],
            ["Válido", "Sin aviso", "Sin aviso"],
            ["No resuelto", "Sin aviso", "Aviso posible; marca «ya avisado»"],
            ["No resuelto, ya avisado", "Sin aviso", "Sin aviso"],
            ["Inválido", "Aviso confirmado; marca «ya avisado»", "Aviso confirmado; marca «ya avisado»"],
            ["Inválido, ya avisado", "Sin aviso", "Sin aviso"],
        ]),
        P("Los avisos posibles se registran con un tipo propio y se contabilizan aparte de los confirmados, para que la política no altere la precisión ni la exhaustividad de la comparación principal. La {F:lst-politica} presenta dos pruebas de este comportamiento."),
        L("lst-politica", "Comportamiento de la política Possibly en programas mínimos", """
void no_guarantee(std::vector<int> &c) {
  const int &h = c[0];
  c.push_back(1);
  sink(h); // expected-warning {{Uso de una referencia posiblemente invalidada:
           //   'std::vector::push_back' (línea 10) si la capacidad está agotada
           //   reubica los elementos; nada garantiza espacio}}
}

void unordered_reserved(std::unordered_map<int, int> &c) {
  c.reserve(c.size() + 1);
  auto it = c.begin();
  if (it == c.end()) return;
  c.insert({42, 1});
  sink(it->second); // sin aviso
}""", "Tomado de plugin/tests/lit/garantias.cpp; el primer comentario ocupa una sola línea en el archivo."),
        H4("4.2.7.4 Escape a código opaco"),
        P("Se llama escape al paso del contenedor, o del objeto que lo contiene, a una función que el analizador no ve (código opaco); esa función pudo modificarlo. El checker olvida entonces los handles válidos y no resueltos de ese contenedor y su crédito, y conserva los inválidos, porque ninguna llamada revierte una invalidación. La primera versión pasaba esos handles a no resueltos, pero en código real producía avisos posibles por llamadas como printf, que no señalaban un defecto; por eso se optó por olvidarlos, aunque esa decisión puede omitir un defecto."),
        H4("4.2.7.5 Evaluación de la política"),
        P("El efecto de la política se evaluó comparando las condiciones C-Silent y C-Possibly sobre los 102 casos POLICY, y sobre los 306 casos SAFE para verificar que no aparecieran avisos posibles donde la norma conserva la validez. Los indicadores fueron el número de avisos posibles en los casos POLICY, el número de avisos posibles en los casos SAFE y la igualdad de los avisos confirmados entre ambos modos."),
        P("El producto del OE4 fue la política Silent/Possibly, el crédito de garantía y el tratamiento del escape implementados en el checker, con el procedimiento para medir su efecto."),

        H3("4.2.8 Protocolo de comparación y pruebas"),
        H4("4.2.8.1 Condiciones del experimento"),
        P("El quinto objetivo específico compara la configuración de referencia con la misma configuración más el checker. La {T:condiciones-exp} define las cuatro condiciones. Las cuatro comparten el banco, las etiquetas, el compilador y las opciones del analizador, y difieren solo en los checkers activos y en la política. Cada uno de los 750 casos se analizó bajo cada condición en una invocación propia, lo que suma 3000 invocaciones."),
        T("condiciones-exp", "Condiciones del experimento", [1100, 2100, 3000, 2800], [
            ["Condición", "Nombre en el arnés", "Checkers activos", "Función en el contraste"],
            ["B", "Reference", "core, cplusplus y alpha.cplusplus pertinentes", "Línea base principal"],
            ["C-Silent", "Experimental-Silent", "Los de B más el checker, política Silent", "Condición propuesta sin avisos posibles"],
            ["C-Possibly", "Experimental-Possibly", "Los de B más el checker, política Possibly", "Condición propuesta con avisos posibles"],
            ["D", "Plugin-Possibly", "core, cplusplus y el checker, política Possibly", "Aporte propio del checker, sin que InvalidatedIterator corte el camino"],
        ]),
        H4("4.2.8.2 Tubería de ejecución"),
        P("El arnés se organizó como una tubería de funciones, que muestra la {F:f4-tuberia} y describe la {T:tuberia}. Antes de medir, comprueba que el banco coincide con su sello y que el analizador carga el checker, y guarda las versiones y las opciones de cada condición en el registro. Por cada invocación registra los avisos, el resultado de la ejecución, el tiempo de reloj y la memoria residente máxima."),
        F("f4-tuberia", "Tubería del arnés de evaluación"),
        T("tuberia", "Etapas del arnés", [1400, 3800, 3800], [
            ["Etapa", "Qué hace", "Qué deja"],
            ["Verificar", "Comprueba el sello, las versiones y la carga del checker", "Bloque meta del registro de ejecución"],
            ["Ejecutar", "Lanza clang++ por caso y condición, con límite de 120 s", "Resultado, tiempo y memoria; el archivo SARIF se lee y se descarta"],
            ["Normalizar", "Convierte cada resultado del SARIF en un aviso con línea, columna, checker, clase y mensaje", "Avisos en ejecucion.json"],
            ["Atribuir", "Asigna el aviso al caso y a su sitio: handle sostenido o de control", "Avisos por sitio"],
            ["Cotejar", "Aplica la regla de clasificación", "cotejo.json"],
            ["Agregar", "Suma conteos por condición y grupo, y calcula las métricas al final", "metricas.json"],
            ["Contrastar", "Calcula McNemar y el intervalo bootstrap, y exporta la hoja", "contraste.json y resultados.xlsx"],
        ]),
        H4("4.2.8.3 Clasificación de cada caso"),
        P("Cada invocación termina con uno de cinco resultados: completada, error de compilación, caída, tiempo agotado o salida ilegible. Solo la primera se coteja; las otras cuatro son incidencias. La {T:clasificacion} define cómo se clasificó cada caso a partir de su etiqueta y de los avisos confirmados, y la {F:lst-cotejo} presenta la función que aplica esa regla."),
        T("clasificacion", "Regla de clasificación de cada caso", [1800, 3600, 3600], [
            ["Etiqueta", "Con aviso confirmado (sección 3.4.2)", "Sin aviso confirmado"],
            ["UB", "Verdadero positivo (VP)", "Falso negativo (FN)"],
            ["SAFE", "Falso positivo (FP)", "Verdadero negativo (VN)"],
            ["POLICY", "Se registra aparte; no entra en VP, FP, FN ni VN", "Se registra aparte"],
        ], "Los avisos posibles se cuentan aparte y no modifican VP, FP, FN ni VN; en POLICY separan los casos con aviso de los casos sin aviso. Las incidencias se informan por separado. En SAFE, cualquier aviso confirmado del caso cuenta como falso positivo, aunque no recaiga en el sitio de uso."),
        L("lst-cotejo", "Función de cotejo del arnés", """
def cotejar(case, caso, run, avisos):
    if run.outcome != "Completed":
        # Ley «un fallo nunca es un verdadero negativo».
        return Match(case, run.condicion, "Incident", [], False, 0, 0)
    conf = [(w, s) for w, s in avisos if w.clase == "Confirmed"]
    posibles = sum(w.clase == "Possible" for w, _ in avisos)
    etiqueta_de = {"sostenido": caso["handles"]["sostenido"],
                   "control": caso["handles"]["control"]}
    # Un aviso acierta en un caso UB sólo si cae sobre un handle
    # que la norma da por inválido.
    buenos = [s for _, s in conf if etiqueta_de.get(s) == "UB"]
    e = caso["esperado"]
    if e == "UB":
        v = "TP" if buenos else "FN"
    elif e == "SAFE":
        v = "FP" if conf else "TN"
    else:
        v = "PolicyWarned" if conf or posibles else "PolicySilent"
    ...""", "Tomado de bench/experimento.py; se omitieron las anotaciones de tipo y el final de la función."),
        H4("4.2.8.4 Métricas y contraste"),
        P("Con los conteos se calcularon la precisión, la exhaustividad y la medida F1 de cada condición (sección 2.3.8) y la diferencia ΔF1 entre C y B. F1 de C se calculó con los avisos confirmados, que por diseño de la política deben ser los mismos en C-Silent y en C-Possibly; la prueba de la política verifica esa igualdad. Como complemento, se calculó la cobertura sobre el handle sostenido, que exige que el aviso caiga sobre el handle que el caso mantiene y no sobre otro."),
        P("La hipótesis se contrastó con la prueba exacta de McNemar y el intervalo de ΔF1, según la regla de decisión de la sección 3.4.4. La {F:f4-mcnemar} presenta la tabla de pares: los casos en que ambas condiciones aciertan o ambas fallan no informan sobre la diferencia, de modo que la prueba se basa en los dos valores discordantes. El contraste se aplicó por separado a los casos UB y a los casos SAFE. La estabilidad de ΔF1 se estimó con un intervalo bootstrap del 95 %, por percentiles, remuestreando casos dentro de cada etiqueta, con 10 000 réplicas y una semilla fija para que el cálculo pueda repetirse."),
        F("f4-mcnemar", "Tabla de pares de la prueba de McNemar"),
        P("Como el arnés determina todas las cifras, también se probó. Las once leyes de la {T:leyes-arnes} se comprueban sin ejecutar Clang, nueve con datos escritos a mano, una con datos aleatorios generados con un valor inicial fijo y una sobre la matriz completa, y forman parte de la integración continua."),
        T("leyes-arnes", "Leyes del arnés de evaluación", [500, 5100, 3400], [
            ["N.º", "Ley", "Qué evita"],
            ["1", "Un fallo nunca es un verdadero negativo", "Que una caída mejore la precisión"],
            ["2", "El aviso sobre el control cuenta si el control es UB", "Perder una detección real en la forma de bucle"],
            ["3", "El aviso sobre un handle SAFE no es un acierto", "Contar un aviso que cae en otro handle"],
            ["4", "Un aviso posible no es un acierto ni un falso positivo", "Mezclar la política en la precisión"],
            ["5", "POLICY no entra en la precisión", "Clasificar lo que la norma no decide"],
            ["6", "Una métrica sin denominador no es cero", "Presentar un 0/0 como 0 %"],
            ["7", "Los conteos se suman por partes", "Promediar métricas de grupos"],
            ["8", "Los conteos se reconstruyen desde el cotejo", "Cifras sin respaldo por caso"],
            ["9", "Normalizar dos veces es normalizar una", "Duplicar avisos"],
            ["10", "Escribir y leer los resultados los conserva", "Perder datos al guardar"],
            ["11", "La etiqueta es la peor de sus handles, en toda la matriz", "Etiquetas que contradigan la regla"],
        ], "Las leyes están en bench/pruebas_evaluacion.py."),
        H4("4.2.8.5 Evaluación en código real"),
        P("La evaluación complementaria se realizó sobre cuatro proyectos de código abierto en versiones fijas, que la {T:proyectos} presenta, con 781 unidades de traducción. Los proyectos se analizaron con la política Possibly y con el modo de expansión que analiza cada función también como punto de partida, aunque ya se haya analizado dentro de otra (-analyzer-inlining-mode=all). Cada aviso se revisó manualmente. Una unidad que no compiló se registró como fallo y no como unidad sin defectos. Cada análisis tuvo un límite de 900 segundos; agotarlo detiene la corrida, de modo que una unidad sin terminar tampoco puede contarse como unidad sin defectos."),
        T("proyectos", "Proyectos de la evaluación en código real", [2500, 3500, 3000], [
            ["Proyecto", "Commit", "Unidades de traducción"],
            ["ninja", "2daa09ba270b", "29"],
            ["leveldb", "99b3c03b3284", "39"],
            ["yaml-cpp", "f7320141120f", "31"],
            ["rocksdb", "3c27a3dde099", "682"],
            ["Total", "", "781"],
        ]),
        P("Además, se sembraron ocho defectos y dos usos correctos en esos proyectos, según el flujo de la {F:f4-semillas}. Cada una de estas diez modificaciones, llamadas semillas, reemplaza un fragmento exacto del código, se analiza la unidad que lo contiene y se restaura el archivo. Para cada una se fijó de antemano el resultado esperado, como detalla la {T:semillas}. El modo de expansión all se adoptó después de comprobar que el modo por defecto no alcanzaba las semillas S7 y S8 (decisión D-22). Los proyectos se clonaron para el análisis y no forman parte del repositorio, que solo conserva el commit, los avisos y el resultado de cada semilla."),
        F("f4-semillas", "Evaluación en código real y con defectos sembrados"),
        T("semillas", "Semillas de la evaluación en código real", [600, 1000, 2000, 3900, 1500], [
            ["ID", "Proyecto", "Archivo", "Mecanismo", "Esperado"],
            ["S1", "ninja", "src/build.cc", "map::erase libera el nodo y luego se lee e->second (M5)", "Confirmado"],
            ["S2", "ninja", "src/build.cc", "map::erase y lectura posterior por el iterador (M5)", "Confirmado"],
            ["S3", "ninja", "src/missing_deps.cc", "unordered_map::clear y uso de un iterador obtenido con insert(...).first (M5)", "Confirmado"],
            ["S4", "ninja", "src/graph.cc", "Referencia al frente de un deque y pop_front (M5)", "Confirmado"],
            ["S5", "ninja", "src/build_log.cc", "unordered_map::erase dentro del recorrido y ++i (M5)", "Confirmado"],
            ["S6", "yaml-cpp", "src/node_data.cpp", "list::erase y ++it sobre el borrado (M5)", "Confirmado"],
            ["S7", "leveldb", "db/db_impl.cc", "Puntero a un elemento de vector y push_back sin reserve (M1)", "Posible"],
            ["S8", "ninja", "src/graph.cc", "Puntero a back() de un vector y pop_back (M3)", "Confirmado"],
            ["B1", "leveldb", "db/db_impl.cc", "La misma S7 con reserve(size() + 1) antes", "Sin aviso"],
            ["B2", "ninja", "src/build_log.cc", "i = erase(i): el iterador devuelto es válido", "Sin aviso"],
        ], "Las semillas están en bench/inyeccion.py."),
        H4("4.2.8.6 Pruebas definidas"),
        P("La {T:pruebas} reúne las pruebas definidas, con el objetivo, el indicador y el criterio de aceptación de cada una. Las marcadas como complemento no responden a un objetivo específico ni intervienen en la decisión sobre H0. Sus resultados se presentan en el capítulo V."),
        T("pruebas", "Pruebas definidas para la evaluación", [1450, 1350, 2300, 2000, 1900], [
            ["Prueba", "OE", "Indicador", "Procedimiento", "Criterio de aceptación"],
            ["Validación dinámica", "OE1", "Ejecuciones que contradicen su etiqueta; proporción de casos en que se observó el defecto", "852 ejecuciones con libstdc++ Debug y sanitizadores", "Ninguna contradicción"],
            ["Pruebas unitarias del núcleo", "OE3", "Pruebas aprobadas", "GoogleTest en la imagen Docker", "Todas aprobadas"],
            ["Pruebas lit", "OE3", "Programas mínimos con el aviso y la nota esperados", "lit de LLVM en la imagen Docker", "Todas aprobadas"],
            ["Leyes del arnés", "OE5", "Leyes cumplidas", "bench/pruebas_evaluacion.py", "Todas cumplidas"],
            ["Experimento sobre el banco", "OE2, OE5", "VP, FP, FN, precisión, exhaustividad, F1 y ΔF1", "750 casos × 4 condiciones, cotejo por sitio", "OE2: descriptivo; OE5: decisión sobre H0 según la regla de la sección 3.4.4"],
            ["Política", "OE4", "Avisos posibles en POLICY y en SAFE; avisos confirmados por modo", "C-Silent frente a C-Possibly", "Ningún aviso posible en SAFE; confirmados iguales en ambos modos"],
            ["Casos con garantía", "OE1, OE4", "FP en los 66 casos de buen uso", "Condiciones C-Silent y C-Possibly", "Ningún FP"],
            ["Código real", "Complemento", "Caídas y avisos revisados", "781 unidades de cuatro proyectos", "Ninguna caída; cada aviso revisado"],
            ["Defectos sembrados", "Complemento", "Semillas con el resultado esperado", "8 defectos y 2 usos correctos", "Resultado observado igual al esperado"],
            ["Costo", "Complemento", "Mediana del tiempo por caso y mayor pico de memoria", "B frente a C-Possibly", "Menos de 10 % de tiempo y 5 % de memoria adicionales"],
        ]),
        P("El producto del OE5 fue el arnés de ejecución y procesamiento, el registro de las 3000 invocaciones con su cotejo y el análisis estadístico. Junto con él se registraron, como complemento, las pruebas en código real."),
        P("La {T:trazabilidad} presenta la relación entre cada objetivo específico, el producto que lo cumple y la sección del capítulo V donde se presentan sus resultados."),
        T("trazabilidad", "Trazabilidad entre objetivos, productos y resultados", [950, 950, 3800, 1400, 1900], [
            ["Objetivo", "Pregunta", "Producto", "Desarrollo", "Resultados"],
            ["OE1", "PE1", "Matriz normativa, banco congelado y registro de validación", "Sección 4.2.4", "Sección 5.1"],
            ["OE2", "PE2", "Registro de B y catálogo de omisiones por causa", "Sección 4.2.5", "Sección 5.2"],
            ["OE3", "PE3", "Checker con sus pruebas", "Sección 4.2.6", "Sección 5.3"],
            ["OE4", "PE4", "Política, crédito y escape", "Sección 4.2.7", "Sección 5.4"],
            ["OE5", "PE5", "Arnés, registro de las 3000 invocaciones y contraste; pruebas en código real (complemento)", "Sección 4.2.8", "Secciones 5.5 y 5.6"],
        ]),
        H3("4.2.9 Alcance previsto y avance del prototipo"),
        P("Para seguir el avance del prototipo se fijó una línea base de su alcance, distinta de la línea base experimental del OE2, que es la configuración B. La {T:avance} divide el alcance total en diez componentes, con el peso de cada uno, que los autores estimaron según su esfuerzo, el criterio para darlo por terminado y su avance. El avance ponderado es de 97 %. El documento independiente que acompaña a este capítulo repite esa tabla e indica el minuto del video en que se demuestra cada componente funcionando."),
        T("avance", "Línea base del alcance y avance del prototipo", [550, 3100, 750, 3700, 900], [
            ["ID", "Componente o funcionalidad", "Peso", "Criterio para considerarlo terminado", "Avance"],
            ["C1", "Integración con Clang: el checker se carga como complemento sin recompilar el compilador", "5 %", "El analizador carga el complemento y la prueba registro.cpp pasa", "100 %"],
            ["C2", "Matriz normativa y tabla de reglas de C++17", "15 %", "101 mutaciones y 348 reglas; las 4 leyes pasan al generar la tabla", "100 %"],
            ["C3", "Núcleo de decisión independiente de Clang", "10 %", "40 pruebas GoogleTest aprobadas", "100 %"],
            ["C4", "Seguimiento de referencias y punteros", "15 %", "Pasa referencias.cpp y se avisa el uso inválido en la demostración", "100 %"],
            ["C5", "Seguimiento de iteradores y posiciones", "15 %", "Pasa iteradores.cpp y se avisa el uso inválido en la demostración", "100 %"],
            ["C6", "Política Silent/Possibly, garantía de reserve y escape a código opaco", "10 %", "Pasa garantias.cpp; un insert de rango consume un crédito por elemento, y reserve solo cuenta con el size() del mismo contenedor", "80 %"],
            ["C7", "Mensajes y ruta de cada aviso", "5 %", "Pasa rutas.cpp; el aviso nombra handle, operación y línea", "100 %"],
            ["C8", "Banco de 750 casos validado y sellado", "10 %", "852 ejecuciones sin contradicciones y sello sha256 verificado", "100 %"],
            ["C9", "Arnés de experimento y contraste estadístico", "10 %", "3000 invocaciones sin incidencias; McNemar e intervalo de ΔF1 calculados", "100 %"],
            ["C10", "Evaluación en código real y defectos sembrados", "5 %", "781 unidades analizadas y 10 de 10 semillas con el resultado esperado", "80 %"],
            ["", "Total", "100 %", "Avance ponderado: suma de peso × avance", "97 %"],
        ], "El avance de los ocho componentes terminados sale de comprobaciones que pasan o no pasan; el 80 % de C6 y de C10 es una estimación de los autores."),
        P("Ocho componentes están terminados y dos siguen en desarrollo. En C6, un insert de rango consume un solo crédito de reserve y no se comprueba que el size() de reserve(size() + k) sea del mismo contenedor, de modo que en esos casos el checker podría callar ante un defecto real; ninguno de los dos aparece en el banco. En C10, una unidad de ninja (src/browse.cc) no compiló por falta de un encabezado generado, de modo que se analizaron 780 de las 781 unidades, y un tiempo agotado detiene la corrida en lugar de registrarse como fallo."),
    ]
