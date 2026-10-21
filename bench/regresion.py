"""Regla del CI (7.1 e): falla si un caso SAFE gana un aviso confirmado o si un UB
que se detectaba deja de detectarse. Compara test/experimento/metricas.json con el
mínimo registrado en bench/regresion.json.

Con --muestra <metricas.json> (la salida de experimento.py --muestra) la regla es
relativa a los casos de la muestra: con el checker, todo UB detectado, ningún falso
positivo, todo POLICY con aviso posible en Possibly y ninguno en Silent.

  python3 bench/regresion.py
  python3 bench/regresion.py --muestra build/verificacion/metricas.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CON_CHECKER = ("Experimental-Silent", "Experimental-Possibly", "Plugin-Possibly")


def banco_completo() -> list[str]:
    minimo = json.loads((RAIZ / "bench" / "regresion.json").read_text())
    medido = json.loads((RAIZ / "test" / "experimento" / "metricas.json").read_text())["metricas"]
    fallos = []
    for cond, umbral in minimo.items():
        m = medido[cond]["All"]
        if m["fp"] > umbral["fp_max"]:
            fallos.append(f"{cond}: {m['fp']} avisos confirmados sobre casos SAFE (máximo {umbral['fp_max']})")
        if m["tp"] < umbral["tp_min"]:
            fallos.append(f"{cond}: {m['tp']} UB detectados (antes {umbral['tp_min']})")
        if m["ubEnSostenido"] < umbral["sostenido_min"]:
            fallos.append(f"{cond}: {m['ubEnSostenido']} UB sobre el handle sostenido (antes {umbral['sostenido_min']})")
        if m["incidents"] > 0:
            fallos.append(f"{cond}: {m['incidents']} incidentes")
        print(f"{cond}: tp={m['tp']} fp={m['fp']} sostenido={m['ubEnSostenido']} incidentes={m['incidents']}")
    return fallos


def muestra(ruta: Path) -> list[str]:
    medido = json.loads(ruta.read_text())["metricas"]
    fallos = []
    for cond, todo in medido.items():
        m = todo["All"]
        print(f"{cond}: tp={m['tp']} fn={m['fn']} fp={m['fp']} "
              f"POLICY={m['policyWarned']}/{m['policyWarned'] + m['policySilent']} incidentes={m['incidents']}")
        if m["fp"] or m["incidents"]:
            fallos.append(f"{cond}: {m['fp']} falsos positivos, {m['incidents']} incidentes")
        if cond in CON_CHECKER and m["fn"]:
            fallos.append(f"{cond}: {m['fn']} UB sin detectar")
        if cond.endswith("Possibly") and m["policySilent"]:
            fallos.append(f"{cond}: {m['policySilent']} casos POLICY sin aviso posible")
        if cond == "Experimental-Silent" and m["policyWarned"]:
            fallos.append(f"{cond}: {m['policyWarned']} avisos posibles en modo Silent")
    return fallos


def main() -> int:
    fallos = muestra(Path(sys.argv[2])) if sys.argv[1:2] == ["--muestra"] else banco_completo()
    for f in fallos:
        print("REGRESIÓN:", f)
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
