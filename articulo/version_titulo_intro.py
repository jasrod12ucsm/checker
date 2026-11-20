"""Genera articulo_titulo_introduccion.tex: solo el título, los autores y la Introducción.

Las referencias se reducen a las citadas y se renumeran.
Uso: python3 version_titulo_intro.py && python3 refs.py articulo_titulo_introduccion.tex articulo_titulo_introduccion.tex --solo-citadas
"""
s = open("articulo.tex", encoding="utf-8").read()


def quitar(ini, fin):
    global s
    i, j = s.index(ini), s.index(fin)
    assert i < j, (ini, fin)
    s = s[:i] + s[j:]


quitar(r"\begin{abstract}", r"\section{Introducción}")
quitar(r"\section{Trabajos relacionados}", r"\begin{thebibliography}")
open("articulo_titulo_introduccion.tex", "w", encoding="utf-8").write(s)
