"""Genera articulo_intro_metodologia.tex: solo Introducción y Metodología.

Sin resumen, palabras clave, trabajos relacionados, resultados, discusión ni
conclusiones. Las referencias se reducen a las citadas y se renumeran.
Uso: python3 version_corta.py && python3 refs.py articulo_intro_metodologia.tex articulo_intro_metodologia.tex --solo-citadas
"""
import re

s = open("articulo.tex", encoding="utf-8").read()


def quitar(ini, fin):
    global s
    i, j = s.index(ini), s.index(fin)
    assert i < j, (ini, fin)
    s = s[:i] + s[j:]


quitar(r"\begin{abstract}", r"\section{Introducción}")
quitar(r"\section{Trabajos relacionados}", r"\begin{figure*}")
quitar(r"\section{Resultados}", r"\begin{thebibliography}")
org = re.search(r"La Sección~II revisa.*?concluye\.", s).group(0)
s = s.replace(org, "La Sección~II describe la metodología: el procedimiento general, "
                   "el desarrollo del checker y el diseño de la evaluación experimental.")
open("articulo_intro_metodologia.tex", "w", encoding="utf-8").write(s)
