#!/usr/bin/env bash
# Arma el Word del proyecto en dos pasadas: la primera calcula en qué página cae cada título,
# tabla y figura (LibreOffice → PDF); la segunda llena los índices con esas páginas.
# Uso: bench/informe/generar.sh V2.docx salida.docx
set -euo pipefail
V2=$(realpath "$1"); SAL=$(realpath -m "$2"); AQUI=$(dirname "$(realpath "$0")")
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
armar() {
  rm -rf "$T/u" && mkdir -p "$T/u" && unzip -q "$V2" -d "$T/u" && find "$T/u" -type l -delete
  python3 "$AQUI/build_v4.py" "$T/u"
  rm -f "$1" && (cd "$T/u" && zip -qXr "$1" . -x entradas.json)
}
armar "$T/pasada1.docx"
cp "$T/u/entradas.json" "$T/entradas.json"
soffice --headless --convert-to pdf --outdir "$T" "$T/pasada1.docx" >/dev/null 2>&1
python3 "$AQUI/paginas.py" "$T/pasada1.pdf" "$T/entradas.json" "$T/paginas.json"
PAGINAS="$T/paginas.json" armar "$SAL"
echo "→ $SAL"
