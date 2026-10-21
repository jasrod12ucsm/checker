#!/usr/bin/env python3
"""RNF-04 y RNF-05: el costo del checker, desde test/experimento/ejecucion.json.

  RNF-04  mediana del tiempo por caso con el checker frente a CSA solo: menos de 10 % más.
  RNF-05  memoria residente máxima por caso con el checker frente a CSA solo: menos de 5 % más.

Compara Reference con Experimental-Possibly sobre las ejecuciones completadas.
No corre clang: lee lo que dejó bench/experimento.py. Falla (código 1) si se pasa un umbral.

  python3 bench/rendimiento.py
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EJECUCION = RAIZ / "test" / "experimento" / "ejecucion.json"
BASE, CON = "Reference", "Experimental-Possibly"
UMBRAL_TIEMPO, UMBRAL_MEMORIA = 0.10, 0.05


def main() -> int:
    runs = json.loads(EJECUCION.read_text())["runs"]
    sel = lambda c: [r for r in runs if r["condicion"] == c and r["outcome"] == "Completed"]
    base, con = sel(BASE), sel(CON)
    t0 = statistics.median(r["segundos"] for r in base)
    t1 = statistics.median(r["segundos"] for r in con)
    m0 = max(r["max_rss_kb"] for r in base) / 1024
    m1 = max(r["max_rss_kb"] for r in con) / 1024
    dt, dm = t1 / t0 - 1, m1 / m0 - 1
    print(f"RNF-04 tiempo mediano por caso: {t0:.3f} s → {t1:.3f} s ({100 * dt:+.1f} %, umbral {100 * UMBRAL_TIEMPO:.0f} %)")
    print(f"RNF-05 memoria residente máxima: {m0:.1f} MB → {m1:.1f} MB ({100 * dm:+.1f} %, umbral {100 * UMBRAL_MEMORIA:.0f} %)")
    return 0 if dt < UMBRAL_TIEMPO and dm < UMBRAL_MEMORIA else 1


if __name__ == "__main__":
    sys.exit(main())
