#!/bin/bash
# Demostración del video. Uso: ./video/demo.sh 1   (o 2, 3, ruta, 4, 5, 6, 7), un paso cada vez que toque.
# El paso 1 compila el checker: hay que correrlo antes que 2, 3, ruta y 4.
cd "$(dirname "$0")/.." || exit 1
DC="docker compose run --rm -T shell bash -c"
B="-Xclang -analyzer-checker=core,cplusplus,alpha.cplusplus.IteratorModeling,alpha.cplusplus.ContainerModeling,alpha.cplusplus.InvalidatedIterator,alpha.cplusplus.IteratorRange,alpha.cplusplus.MismatchedIterator -Xclang -analyzer-config -Xclang aggressive-binary-operation-simplification=true"
L="-Xclang -load -Xclang build/plugin/libContainerInvalidation.so -Xclang -analyzer-checker=ucsm.ContainerInvalidation"
limpia() { grep -E "warning:|warnings? generated|^PASS|Passed|tests passed|FAILED" | sed 's#video/##'; }
case "$1" in
1) echo "== Matriz normativa, de la que sale la tabla de reglas"
   python3 -c "
import json;m=json.load(open('norma/matriz.json'));ms=m['mutaciones']
print(len(ms),'mutaciones,',sum(len(x['reglas']) for x in ms),'reglas,',len({x['contenedor'] for x in ms}),'contenedores')"
   echo "== Compilar el checker y correr sus pruebas (GoogleTest y lit)"
   docker compose run --rm -T plugin 2>&1 | grep -E "PASSED|^PASS|Passed:|FAILED";;
2) echo "== Clang sin el checker (configuración de referencia)"
   $DC "clang++ --analyze -std=c++17 -o /dev/null $B video/demo.cpp" 2>&1 | limpia
   echo "(fin de la salida)";;
3) echo "== Clang con el checker, política Silent: solo defectos seguros"
   $DC "clang++ --analyze -std=c++17 -o /dev/null $L video/demo.cpp" 2>&1 | limpia;;
4) echo "== Clang con el checker, política Possibly: también lo que depende del estado"
   $DC "clang++ --analyze -std=c++17 -o /dev/null $L -Xclang -analyzer-config -Xclang ucsm.ContainerInvalidation:PolicyMode=Possibly video/demo.cpp" 2>&1 | limpia;;
ruta) echo "== Ruta del primer aviso: dónde se obtuvo, qué lo invalidó y dónde se usó"
   $DC "clang++ --analyze -std=c++17 -o /dev/null $L -Xclang -analyzer-output=text video/demo.cpp" 2>&1 | grep -E "warning:|note:" | sed 's#video/##' | head -3;;
5) echo "== Banco de casos y experimento registrado"
   python3 - <<'P'
import json
c=list(json.load(open('test/corpus_truth.json')).values())
from collections import Counter
print('Casos del banco:',len(c),dict(Counter(x['esperado'] for x in c)))
r=json.load(open('test/runtime_validation_results.json'))
print('Validación dinámica:',r['ejecuciones'],'ejecuciones;',r['casos_base'],'casos')
print('Sello del banco:',json.load(open('test/banco-1.json'))['banco'],json.load(open('test/banco-1.json'))['fecha'])
m=json.load(open('test/experimento/metricas.json'));T=m['tiempos']
M=json.load(open('test/experimento/contraste.json'))['metricas']
print(f"\n{'Condición':24}{'VP':>5}{'FN':>5}{'FP':>5}{'VN':>5}{'Pos.':>6}{'F1':>7}{'seg':>8}")
for k in ('Reference','Experimental-Silent','Experimental-Possibly','Plugin-Possibly'):
    x=M[k];print(f"{k:24}{x['TP']:>5}{x['FN']:>5}{x['FP']:>5}{x['TN']:>5}{x['PolicyWarned']:>6}{x['f1']:>7.3f}{T[k]['segundos']:>8.1f}")
s=json.load(open('test/experimento/contraste.json'))
u,f,b=s['mcnemar']['UB'],s['mcnemar']['SAFE'],s['bootstrap']
print(f"\nMcNemar UB: b={u['b']} c={u['c']} p={u['p']:.1e}   McNemar SAFE: b={f['b']} c={f['c']} p={f['p']:.0f}")
print(f"Delta F1 = {b['dF1']:.3f}   IC 95 % [{b['ic95'][0]:.3f}, {b['ic95'][1]:.3f}]")
P
   ;;
6) echo "== Código real: cuatro proyectos y defectos sembrados"
   python3 - <<'P'
import json
a=json.load(open('test/codigo_real/avisos.json'))
for k,v in a['proyectos'].items():
    w=sum(len(r['avisos']) for r in v['resultados'])
    print(f"{k:10} unidades {v['unidades']:>4}  fallos {v['fallos']}  avisos {w}")
i=json.load(open('test/codigo_real/inyeccion.json'))
print()
for x in i: print(f"{x['id']} {x['proyecto']:9}{x['espera']:12}{x['obtenido']:12}{'correcto' if x['acierto'] else 'DISTINTO'}")
P
   ;;
7) echo "== Verificación completa de los requerimientos"
   docker compose run --rm -T verificar 2>&1 | tail -4;;
*) echo "Uso: ./video/demo.sh 1|2|3|ruta|4|5|6|7";;
esac
