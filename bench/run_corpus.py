#!/usr/bin/env python3
import json, re, subprocess, collections, time

truth = json.load(open("test/corpus_truth.json"))
src = open("test/corpus.cpp").read().splitlines()
starts = [(i, m.group(1)) for i, l in enumerate(src,1)
          if (m := re.match(r'^void (f_\w+)\(', l))]
def owner(line):
    best=None
    for ln,name in starts:
        if ln<=line: best=name
    return best

CHK=("core,cplusplus,alpha.cplusplus.IteratorModeling,alpha.cplusplus.ContainerModeling,"
     "alpha.cplusplus.InvalidatedIterator,alpha.cplusplus.IteratorRange,"
     "alpha.cplusplus.MismatchedIterator")
cmd=["clang++","--analyze","-std=c++17","-Xclang",f"-analyzer-checker={CHK}",
     "-Xclang","-analyzer-config","-Xclang","aggressive-binary-operation-simplification=true",
     "test/corpus.cpp"]
t0=time.time(); err=subprocess.run(cmd,capture_output=True,text=True).stderr; dt=time.time()-t0
# ATRIBUCION LINEA A LINEA.
# Un aviso cuenta para el caso solo si cae sobre el uso de lo que se sostiene.
# En forma 'bucle' la cabecera del for tambien accede al ITERADOR: cuenta solo
# cuando sostiene=="it".  Sin esto, el iterador del bucle contamina la medicion
# del dominio de referencias.
warned=set()
for m in re.finditer(r'corpus\.cpp:(\d+):\d+: warning:', err):
    ln=int(m.group(1)); o=owner(ln)
    if not o: continue
    linea=src[ln-1].strip()
    en_cabecera = linea.startswith("for (")
    if en_cabecera and truth[o]["sostiene"] != "it":
        continue          # el aviso es sobre el iterador del bucle, no sobre la referencia
    warned.add(o)

rows=[dict(fn=k, avisa=k in warned, **v) for k,v in truth.items()]
json.dump(rows, open("test/corpus_results.json","w"), indent=1)

def tab(rows_, key, titulo):
    print(f"\n{titulo}")
    print(f"  {'valor':14} {'UB':>5} {'ve':>5} {'CALLA':>6} {'cobert':>8}   {'FP':>4}")
    print("  " + "-"*52)
    for v in sorted({r[key] for r in rows_}, key=str):
        sub=[r for r in rows_ if r[key]==v]
        ub=[r for r in sub if r["esperado"]=="UB"]
        sf=[r for r in sub if r["esperado"]=="SAFE"]
        d=sum(1 for r in ub if r["avisa"]); fp=sum(1 for r in sf if r["avisa"])
        pc=f"{100*d/len(ub):.0f}%" if ub else "—"
        print(f"  {str(v):14} {len(ub):5d} {d:5d} {len(ub)-d:6d} {pc:>8}   {fp:4d}")

ub=[r for r in rows if r["esperado"]=="UB"]
sf=[r for r in rows if r["esperado"]=="SAFE"]
po=[r for r in rows if r["esperado"]=="POLICY"]
det=[r for r in ub if r["avisa"]]; fp=[r for r in sf if r["avisa"]]

print("="*62)
print(f"CORPUS DE {len(rows)} CASOS — clang 21.1.8  ({dt:.1f}s de analisis)")
print("="*62)
print(f"  UB obligatorio ..... {len(ub):4d}   detecta {len(det):4d}   CALLA {len(ub)-len(det):4d}   cobertura {100*len(det)/len(ub):.1f}%")
print(f"  Seguro ............. {len(sf):4d}   falsos positivos: {len(fp)}")
print(f"  Depende del estado . {len(po):4d}   avisa en: {sum(1 for r in po if r['avisa'])}")

print("\n" + "="*62)
print("DONDE SE QUEDA CALLADO — eje D: la MISMA celda, cuatro escrituras")
print("="*62)
tab(rows,"forma","por forma sintactica")
tab(rows,"sostiene","por que se sostiene (eje C)")
tab(rows,"contenedor","por contenedor (eje A)")

print("\n" + "="*62)
print("CRUCE CON LOS CASOS DEL DOCUMENTO 01")
print("="*62)
mapa=[
 ("Caso 1  range-for + insertar", lambda r: r["forma"]=="bucle" and r["op"] in
    {"push_back","emplace_back","push_front","insert","insert_begin","insert_end",
     "insert_middle","insert_after","append","emplace","subscript","resize_grow","reserve","rehash"}),
 ("Caso 2/3 erase en el recorrido", lambda r: r["forma"]=="bucle" and "erase" in r["op"]),
 ("Caso 4  dominio de referencias", lambda r: r["sostiene"] in ("ref","ptr")),
 ("Caso 6  mutacion tras llamada", lambda r: r["forma"]=="llamada"),
 ("Caso 8  depende del estado",    lambda r: r["esperado"]=="POLICY"),
]
print(f"  {'caso':32} {'casos':>6} {'UB':>5} {'ve':>4} {'CALLA':>6} {'cobert':>8}")
print("  "+"-"*66)
for nombre,pred in mapa:
    sub=[r for r in rows if pred(r)]
    u=[r for r in sub if r["esperado"]=="UB"]; d=sum(1 for r in u if r["avisa"])
    pc=f"{100*d/len(u):.0f}%" if u else "n/a"
    print(f"  {nombre:32} {len(sub):6d} {len(u):5d} {d:4d} {len(u)-d:6d} {pc:>8}")

# ── CATALOGO DE FALLOS: por que calla, con precedencia ────────────────────
INS={"push_back","emplace_back","push_front","insert","insert_begin","insert_end",
     "insert_middle","insert_after","append","emplace","subscript","resize_grow",
     "reserve","rehash"}
def causa(r):
    if r["sostiene"] in ("ref","ptr"):
        return "1. El dominio de referencias y punteros no esta modelado"
    if r["forma"]=="recto":
        return "2. Sin comparacion previa contra end(), el modelado no se activa"
    if "erase" in r["op"] or r["op"] in ("pop_front","pop_back","clear"):
        return "3. Se invalida por identidad del iterador, no por posicion"
    if r["op"] in INS:
        return "4. La invalidacion por insercion/realojamiento no esta modelada"
    return "5. Operacion no modelada"

mudos=[r for r in rows if r["esperado"]=="UB" and not r["avisa"]]
cnt=collections.Counter(causa(r) for r in mudos)
print("\n"+"="*62)
print(f"POR QUE CALLA — catalogo causal de los {len(mudos)} falsos negativos")
print("="*62)
for c,n in sorted(cnt.items()):
    print(f"  {n:4d}  ({100*n/len(mudos):4.1f}%)  {c}")

print("\n  Ejemplos representativos por causa:")
vistos=set()
for r in mudos:
    c=causa(r)
    if c in vistos: continue
    vistos.add(c)
    print(f"\n    [{c[:2]}] {r['fn']}")
    print(f"         contenedor={r['contenedor']}  op={r['op']}  sostiene={r['sostiene']}  forma={r['forma']}")
json.dump([dict(r, causa=causa(r)) for r in mudos],
          open("test/corpus_fallos.json","w"), indent=1)
print(f"\n  -> catalogo completo en test/corpus_fallos.json ({len(mudos)} casos)")
