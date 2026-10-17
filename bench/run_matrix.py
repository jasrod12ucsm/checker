#!/usr/bin/env python3
import json, re, subprocess, collections

truth = json.load(open("test/matrix_truth.json"))
src = open("test/matrix.cpp").read().splitlines()

# linea de inicio de cada funcion -> nombre
starts = []
for i, l in enumerate(src, 1):
    m = re.match(r'^void (it_|rf_)(\w+)\(', l)
    if m: starts.append((i, m.group(1) + m.group(2)))
def owner(line):
    best = None
    for ln, name in starts:
        if ln <= line: best = name
    return best

CHK = ("core,cplusplus,alpha.cplusplus.IteratorModeling,alpha.cplusplus.ContainerModeling,"
       "alpha.cplusplus.InvalidatedIterator,alpha.cplusplus.IteratorRange,"
       "alpha.cplusplus.MismatchedIterator")
cmd = ["clang++","--analyze","-std=c++17",
       "-Xclang", f"-analyzer-checker={CHK}",
       "-Xclang","-analyzer-config","-Xclang","aggressive-binary-operation-simplification=true",
       "test/matrix.cpp"]
err = subprocess.run(cmd, capture_output=True, text=True).stderr
warned = set()
for m in re.finditer(r'matrix\.cpp:(\d+):\d+: warning:', err):
    o = owner(int(m.group(1)))
    if o: warned.add(o)

rows = []
for fn, meta in truth.items():
    rows.append(dict(fn=fn, **meta, warned=fn in warned))

def bucket(r):
    e, w = r["expected"], r["warned"]
    if e == "UB":     return "detectado" if w else "FALSO NEGATIVO"
    if e == "SAFE":   return "FALSO POSITIVO" if w else "correcto"
    return "avisa (conservador)" if w else "silencio (optimista)"

for r in rows: r["bucket"] = bucket(r)

print("="*72)
print("COBERTURA DE LA MATRIZ NORMATIVA — clang 21.1.8, config por defecto")
print("="*72)
for dom in ("iterador","referencia"):
    sub=[r for r in rows if r["domain"]==dom]
    c=collections.Counter(r["bucket"] for r in sub)
    ub=[r for r in sub if r["expected"]=="UB"]; sf=[r for r in sub if r["expected"]=="SAFE"]
    po=[r for r in sub if r["expected"]=="POLICY"]
    det=sum(1 for r in ub if r["warned"])
    fp=sum(1 for r in sf if r["warned"])
    print(f"\nDOMINIO: {dom.upper()}   ({len(sub)} celdas)")
    print(f"  UB obligatorio ...... {len(ub):3d}   detectadas: {det:3d}   NO detectadas: {len(ub)-det:3d}")
    print(f"  Seguro obligatorio .. {len(sf):3d}   falsos positivos: {fp:3d}")
    print(f"  Dependiente de estado {len(po):3d}   avisa en: {sum(1 for r in po if r['warned']):3d}")
    if ub: print(f"  --> exhaustividad: {det}/{len(ub)} = {100*det//len(ub)}%")

print("\n" + "="*72)
print("DESGLOSE POR CONTENEDOR (solo celdas de UB obligatorio)")
print("="*72)
print(f"{'contenedor':11} {'dominio':11} {'UB':>4} {'detec':>6} {'huecos':>7}")
print("-"*46)
for cn in ["vector","deque","list","flist","set","map","uset","umap","string"]:
    for dom in ("iterador","referencia"):
        ub=[r for r in rows if r["container"]==cn and r["domain"]==dom and r["expected"]=="UB"]
        if not ub: continue
        d=sum(1 for r in ub if r["warned"])
        flag = "" if d==len(ub) else "  <<<"
        print(f"{cn:11} {dom:11} {len(ub):4d} {d:6d} {len(ub)-d:7d}{flag}")

print("\n" + "="*72)
print("TOTALES")
print("="*72)
ub=[r for r in rows if r["expected"]=="UB"]
det=[r for r in ub if r["warned"]]
sf=[r for r in rows if r["expected"]=="SAFE"]
fp=[r for r in sf if r["warned"]]
po=[r for r in rows if r["expected"]=="POLICY"]
print(f"  celdas totales evaluadas .......... {len(rows)}")
print(f"  celdas de UB obligatorio .......... {len(ub)}")
print(f"     detectadas ..................... {len(det)}")
print(f"     NO detectadas (huecos) ......... {len(ub)-len(det)}")
print(f"  celdas seguras .................... {len(sf)}   falsos positivos: {len(fp)}")
print(f"  celdas dependientes de estado ..... {len(po)}   avisa en: {sum(1 for r in po if r['warned'])}")
print(f"\n  EXHAUSTIVIDAD GLOBAL: {len(det)}/{len(ub)} = {100*len(det)/len(ub):.1f}%")
json.dump(rows, open("test/matrix_results.json","w"), indent=1)
