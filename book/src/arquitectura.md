# Arquitectura

## Diagrama de Paquetes

```plantuml
@startuml
skinparam packageStyle rectangle
skinparam linetype ortho
skinparam nodesep 60
skinparam ranksep 60

' ═══════════════════════════════════════════════════════
'  Capa de Aplicación — orquesta el pipeline de análisis
' ═══════════════════════════════════════════════════════
package "Driver" as driver #E8F5E9 {
    [CLI]
    [Pipeline]
    note right of [Pipeline]
        Orquesta: parsear TU →
        construir modelo →
        aplicar reglas →
        emitir diagnósticos
    end note
}

' ═══════════════════════════════════════════════════════
'  Capa de Dominio — el conocimiento puro del problema
' ═══════════════════════════════════════════════════════
package "Modelo" as modelo #E3F2FD {
    [Contenedor]
    [HandleVivo]
    [OperaciónMutante]
    note right of [Contenedor]
        Abstracción de std::vector,
        std::map, std::deque, ...
        independiente de Clang
    end note
}

package "Semántica STL" as semantica #FFF3E0 {
    [TablaDeInvalidación]
    [CategoríaContenedor]
    [ReglaDeInvalidación]
    note right of [TablaDeInvalidación]
        Codifica las reglas del estándar:
        "vector::push_back invalida
        todos los iteradores si
        size() == capacity()"
    end note
}

package "Motor de Invalidación" as motor #FCE4EC {
    [Checker]
    [AnálisisDeFlujo]
    [DetectorDeConflicto]
    note right of [Checker]
        Recorre el CFG buscando pares
        (handle vivo, operación mutante)
        que violan las reglas
    end note
}

' ═══════════════════════════════════════════════════════
'  Capa Anti-Corrupción — aísla la dependencia de Clang
' ═══════════════════════════════════════════════════════
package "Adaptador Clang" as adaptador #F3E5F5 {
    [ExtractorAST]
    [MatcherFactory]
    [DiagnósticoEmitter]
    note right of [ExtractorAST]
        Traduce nodos del AST de Clang
        al Modelo de dominio propio
    end note
}

' ═══════════════════════════════════════════════════════
'  Capa de Infraestructura — testing y benchmarking
' ═══════════════════════════════════════════════════════
package "Harness" as harness #ECEFF1 {
    [Corpus]
    [Matriz]
    [Benchmark]
    note right of [Corpus]
        Generadores de casos de prueba
        y comparación con ground truth
    end note
}

' ═══════════════════════════════════════════════════════
'  Dependencias externas
' ═══════════════════════════════════════════════════════
package "Clang/LLVM" as clang #F5F5F5 {
    [LibTooling]
    [ASTMatchers]
    [DiagnosticsEngine]
}

' ═══════════════════════════════════════════════════════
'  Relaciones entre paquetes
' ═══════════════════════════════════════════════════════

' El driver orquesta todo
driver    ..>  motor          : «usa»
driver    ..>  adaptador      : «usa»

' El motor usa el modelo y consulta la semántica
motor     ..>  modelo         : «opera sobre»
motor     ..>  semantica      : «consulta reglas»

' La semántica solo conoce el modelo (no Clang)
semantica ..>  modelo         : «define sobre»

' El adaptador traduce Clang → Modelo (capa anti-corrupción)
adaptador ..>  modelo         : «produce»
adaptador ..>  clang          : «envuelve»

' El harness prueba el motor y usa el adaptador
harness   ..>  motor          : «valida»
harness   ..>  adaptador      : «alimenta»

@enduml
```

### Descripción de los paquetes

| Paquete | Responsabilidad | Principio DDD |
|---------|----------------|---------------|
| **Driver** | Punto de entrada CLI, orquesta el pipeline de análisis | Capa de Aplicación |
| **Modelo** | Value objects puros: `Contenedor`, `HandleVivo`, `OperaciónMutante` | Capa de Dominio — entidades y value objects |
| **Semántica STL** | Codifica las reglas del estándar C++ sobre invalidación | Capa de Dominio — servicio de dominio |
| **Motor de Invalidación** | Análisis de flujo + detección de conflictos handle/mutación | Capa de Dominio — lógica central |
| **Adaptador Clang** | Capa anti-corrupción: traduce AST de Clang al modelo propio | Anti-Corruption Layer |
| **Harness** | Corpus de pruebas, matrices de cobertura, benchmarks | Infraestructura de testing |
| **Clang/LLVM** | Dependencia externa: parsing, AST, diagnósticos | Externo |

### Principios de diseño

1. **El Modelo y la Semántica STL no dependen de Clang.** Esto permite probarlos unitariamente sin compilar C++ real.

2. **El Adaptador Clang es la única frontera con LibTooling.** Actúa como capa anti-corrupción: extrae nodos del AST y los traduce a los value objects del Modelo.

3. **El Motor de Invalidación es agnóstico a la fuente.** Recibe el modelo ya construido y aplica las reglas de la Semántica STL. Podría alimentarse desde otro frontend (no solo Clang).

4. **El Driver solo orquesta.** No contiene lógica de dominio; conecta las piezas y configura la CLI.

---

## Arquitectura Lógica

La arquitectura lógica organiza los mismos paquetes del diagrama anterior en **capas DDD**
con **puertos** (interfaces) que desacoplan los contextos. La regla de dependencia es
estricta: las capas internas definen los puertos, las externas los implementan.

```plantuml
@startuml
skinparam linetype ortho
skinparam nodesep 50
skinparam ranksep 40
skinparam componentStyle rectangle

' ═══════════════════════════════════════════════════════════
'  CAPA DE APLICACION
' ═══════════════════════════════════════════════════════════
rectangle "Capa de Aplicación" as app #E8F5E9 {
    component "Driver" as driver {
        [CLI]
        [Pipeline]
    }
}

' ═══════════════════════════════════════════════════════════
'  CAPA DE DOMINIO  (el nucleo, no depende de nada externo)
' ═══════════════════════════════════════════════════════════
rectangle "Capa de Dominio" as dominio #E3F2FD {

    component "Modelo" as modelo {
        [Contenedor]
        [HandleVivo]
        [OperacionMutante]
    }

    component "Semantica STL" as semantica {
        [TablaDeInvalidacion]
        [CategoriaContenedor]
        [ReglaDeInvalidacion]
    }

    component "Motor de Invalidacion" as motor {
        [Checker]
        [AnálisisDeFlujo]
        [DetectorDeConflicto]
    }

    ' --- Puertos (interfaces definidas por el dominio) ---
    portin "<<puerto entrada>>\nIFuenteModelo" as pFuente
    portin "<<puerto entrada>>\nIReglasInvalidacion" as pReglas
    portout "<<puerto salida>>\nIDiagnosticoEmitter" as pDiag
    portout "<<puerto salida>>\nIResultadoAnalisis" as pResult

    ' Conexiones internas del dominio
    motor --> modelo : opera sobre
    motor --> semantica : consulta
    semantica --> modelo : define sobre

    ' El motor consume y expone los puertos
    pFuente --> motor
    pReglas --> motor
    motor --> pDiag
    motor --> pResult
}

' ═══════════════════════════════════════════════════════════
'  CAPA DE INFRAESTRUCTURA  (implementa los puertos)
' ═══════════════════════════════════════════════════════════
rectangle "Capa de Infraestructura" as infra #F3E5F5 {

    component "Adaptador Clang" as adaptador {
        [ExtractorAST]
        [MatcherFactory]
        [DiagnosticoEmitter]
    }

    component "Clang/LLVM" as clang #F5F5F5 {
        [LibTooling]
        [ASTMatchers]
        [DiagnosticsEngine]
    }

    adaptador --> clang : envuelve
}

rectangle "Capa de Testing" as testing #ECEFF1 {
    component "Harness" as harness {
        [Corpus]
        [Matriz]
        [Benchmark]
    }
}

' ═══════════════════════════════════════════════════════════
'  CONEXIONES PUERTO <-> ADAPTADOR
'  (los adaptadores implementan los puertos del dominio)
' ═══════════════════════════════════════════════════════════

' El Driver orquesta el pipeline conectando puertos con adaptadores
driver --> pFuente : inyecta
driver --> pReglas : inyecta
pDiag --> adaptador : implementa
pResult --> harness : implementa

' Los adaptadores alimentan los puertos de entrada
adaptador --> pFuente : implementa\nIFuenteModelo
semantica .u.> pReglas : implementa\nIReglasInvalidacion

' El harness valida a traves del puerto de resultado
harness --> pFuente : alimenta con\ncasos de prueba

@enduml
```

### Puertos del dominio

| Puerto | Tipo | Definido en | Implementado por | Responsabilidad |
|--------|------|-------------|------------------|-----------------|
| **IFuenteModelo** | Entrada | Motor de Invalidación | Adaptador Clang, Harness | Proveer instancias de `Contenedor`, `HandleVivo` y `OperacionMutante` extraídas del código fuente |
| **IReglasInvalidacion** | Entrada | Motor de Invalidación | Semántica STL | Consultar si una operación mutante invalida un handle según el estándar C++ |
| **IDiagnosticoEmitter** | Salida | Motor de Invalidación | Adaptador Clang | Emitir warnings y fix-its al usuario a través del `DiagnosticsEngine` de Clang |
| **IResultadoAnalisis** | Salida | Motor de Invalidación | Harness | Exportar resultados estructurados para comparación con ground truth |

### Relación con el diagrama de paquetes

Los paquetes son los mismos en ambos diagramas. La diferencia es la perspectiva:

- El **diagrama de paquetes** muestra *qué* módulos existen y *qué* depende de *qué*.
- La **arquitectura lógica** muestra *por qué*: las capas DDD, los puertos que desacoplan, y la dirección de la regla de dependencia.

Los puertos garantizan que:

1. **El Motor de Invalidación nunca importa Clang.** Recibe datos a través de `IFuenteModelo` y emite resultados a través de `IDiagnosticoEmitter` — ambos son interfaces que él define.
2. **El Adaptador Clang es reemplazable.** Cualquier frontend que implemente `IFuenteModelo` puede alimentar el motor (útil para testing con el Harness).
3. **La Semántica STL es inyectable.** El motor consulta las reglas a través de `IReglasInvalidacion`, lo que permite intercambiar tablas de reglas sin tocar el análisis de flujo.

---

## Diagrama físico (despliegue)

Este diagrama muestra los artefactos y recursos que participan al ejecutar el
analizador. Representa la implementación actual: `mi-linter` se compila como
un ejecutable nativo, utiliza las bibliotecas de Clang/LLVM y analiza cada
unidad de traducción con sus mismas opciones de compilación. La regla de
captura de excepciones por valor es la primera regla instalada en el driver.

```plantuml
@startuml
skinparam componentStyle rectangle
skinparam linetype ortho
skinparam nodesep 45
skinparam ranksep 45

node "Entorno local de desarrollo" as host #E8F5E9 {
  artifact "Código C++\n*.cpp / *.h" as source
  artifact "Base de compilación\ncompile_commands.json\n(opcional)" as compdb

  component "Checker local\n(ejecutor)" as runner #FFF3E0

  component "mi-linter\n(ejecutable nativo)" as linter #E3F2FD {
    component "Driver / CLI" as driver
    component "CatchByValueCheck" as rule
  }

  folder "Salida de análisis" as output {
    artifact "Diagnósticos en consola\nwarning + fix-it" as diagnostics
    artifact "Código de salida\n0: sin hallazgos\n1: hay hallazgos" as exitcode
  }
}

node "Instalación LLVM/Clang" as clanghost #F5F5F5 {
  component "Clang LibTooling" as tooling
  component "ASTMatchers" as matchers
  component "DiagnosticsEngine" as de
}

source --> driver : archivos a analizar
compdb --> driver : flags y rutas
runner --> linter : ejecuta
driver --> tooling : crea ClangTool
tooling --> matchers : construye y recorre AST
matchers --> rule : callback por coincidencia
rule --> de : reporta warning y fix-it
de --> diagnostics
linter --> exitcode : devuelve resultado
exitcode --> runner

note bottom of compdb
También se admiten flags tras `--`,
por ejemplo: -- -std=c++17
end note
@enduml
```

El *checker local* interpreta el resultado de la ejecución y presenta los
diagnósticos al desarrollador. De ese modo, `mi-linter` permanece concentrado
en analizar el código y reportar sus hallazgos.

---

## Diagrama de casos de uso

El *checker local* es quien ejecuta el analizador. El desarrollador proporciona
el código y consulta los diagnósticos resultantes; ninguno interactúa
directamente con el AST ni con las reglas.

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle
skinparam actorStyle awesome

actor "Desarrollador C++" as developer
actor "Checker local\n(ejecutor)" as runner

rectangle "Analizador estático mi-linter" #E3F2FD {
  usecase "Ejecutar análisis\nde archivos C++" as analyze
  usecase "Emitir diagnóstico\ny fix-it" as report
  usecase "Devolver resultado\ndel análisis" as result

  report -[hidden]down-> result
}

developer --> report : consulta
runner --> analyze : ejecuta
runner --> result : recibe

analyze .> result : <<include>>
analyze .> report : <<include>>

note bottom of analyze
Regla actual:
catch (Excepción e)
end note
@enduml
```

El caso de uso central es ejecutar el análisis. Emitir el diagnóstico y
devolver el resultado son sus dos resultados obligatorios. La resolución de
opciones y la detección son detalles internos de implementación, por lo que no
se representan como casos de uso. Aplicar la corrección sugerida es una
decisión posterior del desarrollador y queda fuera de la frontera del
analizador.

---

## Diagrama de clases (preliminar)

El diseño de clases del analizador todavía está en definición. Por ello, este
diagrama no anticipa clases para reglas futuras: documenta únicamente las
clases y colaboraciones que ya existen en la primera regla implementada. Se
ampliará cuando se definan las abstracciones comunes para más *checks*.

```plantuml
@startuml
skinparam classAttributeIconSize 0
skinparam linetype ortho

class "MiLinter.cpp\n<<driver>>" as Driver {
  +main(argc, argv) : int
}

class "milinter::CatchByValueCheck" as Check {
  -Hallazgos : unsigned
  +registrar(Finder) : void
  +run(Result) : void
  +hallazgos() : unsigned
}

abstract class "clang::ast_matchers::\nMatchFinder::MatchCallback" as Callback <<externa>>
class "clang::ast_matchers::\nMatchFinder" as Finder <<externa>>
class "clang::tooling::ClangTool" as Tool <<externa>>
class "clang::DiagnosticsEngine" as Diagnostics <<externa>>

Check --|> Callback
Driver *-- Check : crea
Driver --> Finder : registra regla
Driver --> Tool : ejecuta
Finder --> Check : invoca run()
Check --> Diagnostics : emite warning / fix-it
@enduml
```

---

## Diagrama de estados: procesamiento de una coincidencia

Este es el flujo relevante de la regla `CatchByValueCheck`. Empieza cuando el
`MatchFinder` encuentra una variable de excepción capturada por valor y llama
a `run()`. Los filtros de contexto evitan reportar código en macros, *headers*
de terceros o ubicaciones inválidas; solo una coincidencia válida termina en
un hallazgo y su corrección sugerida.

```plantuml
@startuml
left to right direction
skinparam linetype ortho
skinparam shadowing false
skinparam nodesep 55
skinparam ranksep 35

state "Callback run()\ninvocado" as callback
[*] --> callback

state "Obtener VarDecl\nligado como exvar" as getVar
callback --> getVar
getVar --> noMatch : Var == nullptr
getVar --> validate : Var disponible

state "Validar ubicación\ndel nombre" as validate
state validLocation <<choice>>
validate --> validLocation
validLocation --> discard : ubicación inválida, macro\no fuera del archivo principal
validLocation --> buildFix : ubicación editable

state "Construir fix-it" as buildFix {
  [*] --> insertReference
  state "Insertar '&'\nantes del nombre" as insertReference
  insertReference --> isConst
  state isConst <<choice>>
  isConst --> insertConst : tipo no const
  isConst --> composeFix : tipo const
  state "Insertar 'const '\nantes del tipo" as insertConst
  insertConst --> composeFix
  state "Preparar corrección" as composeFix
  composeFix --> [*]
}

buildFix --> report
state "Emitir warning\ny fix-it" as report
report --> count
state "Incrementar Hallazgos" as count
count --> [*]

state "Descartar coincidencia\nsin diagnóstico" as discard
state "Sin coincidencia\nválida" as noMatch
discard --> [*]
noMatch --> [*]

note right of report
Mensaje:
"usa const Excepción &"
end note
@enduml
```

El estado final no detiene el recorrido global del AST: indica que terminó el
tratamiento de esa coincidencia. El `MatchFinder` continúa llamando a la regla
para las demás coincidencias encontradas en la unidad de traducción.

---

## Diagrama de colaboración

El diagrama de colaboración muestra qué objetos cooperan en una ejecución del
*checker local*. Los números indican el orden de los mensajes; la repetición
`4.*` ocurre por cada nodo del AST que coincide con el patrón de la regla.

```plantuml
@startuml
left to right direction
skinparam linetype ortho
skinparam shadowing false
skinparam nodesep 55
skinparam ranksep 35

actor "Checker local" as runner
rectangle "driver : MiLinter\n<<objeto>>" as objDriver #E8F5E9
rectangle "herramienta : ClangTool\n<<objeto>>" as objTool #E3F2FD
rectangle "buscador : MatchFinder\n<<objeto>>" as objFinder #FFF3E0
rectangle "regla : CatchByValueCheck\n<<objeto>>" as objCheck #FCE4EC
rectangle "diagnósticos : DiagnosticsEngine\n<<objeto>>" as objDiagnostics #F3E5F5

runner -> objDriver : 1. ejecutar(archivo, flags)
objDriver -> objTool : 3. run(FrontendAction)
objTool -> objFinder : 4. recorrerAST()
objFinder -> objCheck : 4.1 run(MatchResult)
objCheck -> objDiagnostics : 4.2 Report(warning, fix-it)

note top of objDriver
2. Antes de ejecutar, el driver
registra la regla en MatchFinder.
end note

note bottom of objCheck
4.3 Incrementa Hallazgos localmente.
Antes de 4.2, filtra macros y código
fuera del archivo principal.

Al finalizar, ClangTool retorna su estado
al driver; este entrega el total al checker.
end note
@enduml
```

La colaboración concentra la orquestación en el `driver`, delega el recorrido
del AST a Clang y mantiene la regla aislada como responsable de reconocer el
patrón y emitir el diagnóstico.
