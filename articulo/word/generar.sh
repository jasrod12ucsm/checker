#!/bin/sh
# Genera los dos Word del artículo desde los .tex, en formato de congreso IEEE.
#   articulo.docx                     el artículo completo
#   articulo_intro_metodologia.docx   solo Introducción y Metodología
# Requiere docker (texlive), poppler-utils, python3 con Pillow y node con el paquete docx 9.
set -e
cd "$(dirname "$0")"
mkdir -p build/fig
[ -d node_modules/docx ] || npm install --no-save docx@9 >/dev/null
(cd .. && python3 version_corta.py && python3 refs.py articulo_intro_metodologia.tex articulo_intro_metodologia.tex --solo-citadas)
# Figura y ecuaciones como imágenes de 600 ppp, en Times y con el mismo código TikZ del .tex.
python3 - <<'PY'
import re
s = open('../articulo.tex', encoding='utf-8').read()
pre = r"""\documentclass[10pt]{article}\usepackage[paperwidth=22cm,paperheight=12cm,margin=5mm]{geometry}\pagestyle{empty}
\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}
\usepackage[spanish,es-nolayout,es-noshorthands,es-nodecimaldot]{babel}
\usepackage{mathptmx}\usepackage{amsmath,amssymb}\usepackage{tikz}
\usetikzlibrary{positioning,arrows.meta,calc,fit}
\newcommand{\code}[1]{\texttt{#1}}
\begin{document}
"""
tik = re.search(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", s, re.S).group(0)
open('build/fig/fig.tex', 'w').write(pre + tik + "\n\\end{document}\n")
for i, e in enumerate(re.findall(r"\\begin\{equation\}(.*?)\\label", s, re.S), 1):
    open(f'build/fig/eq{i}.tex', 'w').write(pre + "$\\displaystyle " + e.strip() + "$\n\\end{document}\n")
PY
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD/build/fig:/w" -w /w texlive/texlive:latest-medium \
  sh -c 'for f in *.tex; do pdflatex -interaction=nonstopmode "$f" >/dev/null; done'
for f in build/fig/*.pdf; do pdftoppm -r 600 -png -singlefile "$f" "${f%.pdf}"; done
python3 - <<'PY'
import glob
from PIL import Image, ImageChops
for f in glob.glob('build/fig/*.png'):
    im = Image.open(f).convert('RGB')
    b = ImageChops.difference(im, Image.new('RGB', im.size, 'white')).getbbox()
    im.crop((b[0] - 12, b[1] - 12, b[2] + 12, b[3] + 12)).save(f, dpi=(600, 600))
PY
python3 tex2json.py ../articulo.tex build/articulo.json
python3 tex2json.py ../articulo_intro_metodologia.tex build/corto.json
node build.js build/articulo.json build/fig articulo.docx
node build.js build/corto.json build/fig articulo_intro_metodologia.docx
