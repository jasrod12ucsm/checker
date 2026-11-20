"""Arma el manual de instalación y uso en PDF con las páginas del libro ya construidas.

Antes: python3 bench/gen_book.py && mdbook build corpus_book.
Uso: python3 bench/informe/manual.py salida.pdf   (necesita Google Chrome o Chromium)
"""
import os, re, shutil, subprocess, sys, tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIBRO = os.path.join(RAIZ, "corpus_book", "book")
PAGINAS = ["sistema/index.html", "sistema/despliegue.html", "sistema/panel.html", "sistema/api.html", "uso/index.html", "uso/checker.html"]
CSS = """body{font-family:'Liberation Serif',serif;font-size:11pt;line-height:1.45;margin:0 1.5cm;color:#111}
h1{font-size:18pt;page-break-before:always;border-bottom:1px solid #999}h1.portada{page-break-before:avoid;font-size:24pt;border:0;margin-top:6cm}
h2{font-size:14pt}h3{font-size:12pt}table{border-collapse:collapse;font-size:9pt;margin:.6em 0;width:100%}
th,td{border:1px solid #bbb;padding:3px 5px;vertical-align:top}th{background:#e3e9f2}
pre{background:#f4f4f4;padding:6px;font-size:8pt;white-space:pre-wrap}code{font-size:9pt}img{max-width:100%;max-height:18cm;display:block;margin:auto;break-inside:avoid}
blockquote{border-left:3px solid #bbb;margin-left:0;padding-left:10px;color:#333}a{color:#111;text-decoration:none}
.buttons,.clip-button,.fa{display:none}"""

def main(salida):
    cuerpos = []
    for p in PAGINAS:
        html = open(os.path.join(LIBRO, p), encoding="utf-8").read()
        m = re.search(r"<main>(.*?)</main>", html, re.S)
        base = os.path.dirname(os.path.join(LIBRO, p))
        # el libro duplica cada imagen para el zoom (casilla + copia ampliada): se deja una
        cuerpo0 = re.sub(r'<label class="checkbox-label"><input[^>]*>(<img[^>]*>)<span class="img-wrapper"><img[^>]*></span></label>', r"\1", m.group(1))
        cuerpo = re.sub(r'(src)="(?!https?:|data:|/)([^"]+)"', lambda k: f'{k.group(1)}="file://{os.path.normpath(os.path.join(base, k.group(2)))}"', cuerpo0)
        cuerpos.append(cuerpo)
    portada = ('<h1 class="portada">Centinela C++<br>Manual de instalación y uso</h1>'
               '<p>Universidad Católica de Santa María. Escuela Profesional de Ingeniería de Sistemas.</p>'
               '<p>Proyecto de Fin de Carrera. Contenido tomado del libro del proyecto: '
               'puesta en marcha, panel web, API HTTP y guía del checker.</p>')
    doc = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{portada}{"".join(cuerpos)}</body></html>'
    t = tempfile.mkdtemp()
    try:
        f = os.path.join(t, "manual.html"); open(f, "w", encoding="utf-8").write(doc)
        chrome = shutil.which("google-chrome") or shutil.which("chromium-browser") or shutil.which("chromium")
        subprocess.run([chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={os.path.abspath(salida)}", "file://" + f],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        shutil.rmtree(t)
    print("→", salida)

if __name__ == "__main__":
    main(sys.argv[1])
