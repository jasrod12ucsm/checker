"""Página impresa de cada entrada de los índices, buscada en orden en el PDF de la primera pasada."""
import json, re, subprocess, sys

pdf, entradas, salida = sys.argv[1:4]
paginas = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout.split("\f")
norm = lambda s: re.sub(r"\s+", " ", s).strip()
def impresa(texto):
    """El número del pie de página: la última línea que es solo un número."""
    for l in reversed(texto.strip().split("\n")):
        if re.fullmatch(r"\s*\d+\s*", l): return l.strip()
    return ""
planas = [norm(p) for p in paginas]
# Los índices mismos repiten cada título: se empieza a buscar después del último índice.
inicio = max(k for k, p in enumerate(planas) if "Índice de figuras" in p) + 1
res, k = {}, inicio
for t in json.load(open(entradas)):
    clave = norm(t)[:60]
    j = k
    while j < len(planas) and clave not in planas[j]: j += 1
    if j < len(planas):
        res[t] = impresa(paginas[j]); k = j
json.dump(res, open(salida, "w"), ensure_ascii=False)
print(f"{len(res)} de {len(json.load(open(entradas)))} entradas con página")
