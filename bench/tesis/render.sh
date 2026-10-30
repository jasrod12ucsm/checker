#!/usr/bin/env bash
# bench/tesis/fig/*.puml → bench/tesis/fig/png/*.png
set -euo pipefail
cd "$(dirname "$0")/fig"
java -Djava.awt.headless=true -jar "${PLANTUML_JAR:-$HOME/.local/share/plantuml/plantuml.jar}" -charset UTF-8 -tpng -Sdpi=170 -o png *.puml
