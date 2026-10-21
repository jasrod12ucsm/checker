#!/usr/bin/env python3
"""Renderiza libro/diagramas/*.puml a SVG (libro) y PNG (Word).

PlantUML se busca en $PLANTUML_JAR o en ~/.local/share/plantuml/plantuml.jar.
No necesita Graphviz: los diagramas usan el motor interno «smetana».
"""
import os, subprocess, sys, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DIAG = RAIZ / "libro" / "diagramas"
JAR = os.environ.get("PLANTUML_JAR", str(pathlib.Path.home() / ".local/share/plantuml/plantuml.jar"))

if not pathlib.Path(JAR).is_file():
    sys.exit(f"no encuentro PlantUML en {JAR}: exporta PLANTUML_JAR o bájalo ahí")

fuentes = sorted(p for p in DIAG.glob("*.puml"))
for fmt, carpeta in (("svg", DIAG / "svg"), ("png", DIAG / "png")):
    carpeta.mkdir(exist_ok=True)
    r = subprocess.run(["java", "-jar", JAR, f"-t{fmt}", "-charset", "UTF-8",
                        "-o", str(carpeta), *map(str, fuentes)], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"PlantUML falló ({fmt}):\n{r.stdout}{r.stderr}")
print(f"{len(fuentes)} diagramas → {DIAG/'svg'} y {DIAG/'png'}")
