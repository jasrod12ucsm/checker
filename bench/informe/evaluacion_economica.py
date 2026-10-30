#!/usr/bin/env python3
"""Evaluación económica de Centinela C++ (capítulo 3 del informe).

Modelo: licencia por suscripción, cobrada por desarrollador activo (committer) al mes;
cada organización despliega su instancia (single-tenant) en su propio servidor.
Cada parámetro lleva su fuente o se declara como supuesto en libro/informe/cap3.md.

  python3 bench/informe/evaluacion_economica.py
"""
from __future__ import annotations

# ------------------------------------------------------------------ parámetros con fuente
TIPO_CAMBIO = 3.44            # S/ por US$, interbancario venta, 12-14 oct 2026 (BCRP)
PRECIO_USD = 5.0              # US$ por committer al mes: 1/2 de GitHub Code Quality (10), 1/6 de Code Security (30)
TASA = 0.1659                 # TAMN, SBS, 9 jul 2026
TASA_SOCIAL = 0.08            # tasa social de descuento, MEF (Directiva 001-2019-EF/63.01, anexo 11)
FTAMN = 0.3239                # FTAMN, SBS, 9 jul 2026
SERVIDOR_USD = 24.0           # DigitalOcean Basic 4 GiB / 2 vCPU, US$ al mes
HORAS_PRODUCCION = 14.8       # NIST (2002), tabla 7-5: defecto de codificación hallado tras la entrega
HORAS_CODIFICACION = 3.2      # NIST (2002), tabla 7-5: el mismo defecto hallado al codificar
SUELDO_PROMEDIO = 2876.0      # Ponte en Carrera, Ing. de Sistemas y Cómputo (Andina, 2023)
SUELDO_MAXIMO = 5000.0
# costo empleador anual en sueldos: 12 + 2 gratificaciones con 9 % de bonificación + CTS (≈ 1,17) + EsSalud 9 % de 12
SUELDOS_ANUALES = 12 + 2 * 1.09 + 1.17 + 0.09 * 12
HORAS_ANUALES = 48 * 52 - 48 * 30 / 6 - 8 * 12  # 48 h/semana, 30 días de vacaciones, 12 feriados

# ------------------------------------------------------------------ costos del proyecto
TARIFA_EQUIPO = 35.0
INVERSION = {
    "Desarrollo del equipo (470 h × 35)": 470 * TARIFA_EQUIPO,
    "Reserva de contingencia (EMV, 2.5.3)": 2957.50,
    "Asesoría valorizada (24 h × 80)": 24 * 80.0,
    "Licencias": 0.0,
    "Depreciación del equipo de cómputo (3 meses)": 400.0,
    "Energía incremental (3 meses × 90)": 270.0,
    "Internet (3 meses × 120)": 360.0,
    "Servidor de pruebas y demostración (3 meses)": round(3 * SERVIDOR_USD * TIPO_CAMBIO, 2),
    "Dominio (1 año)": 60.0,
}
MANTENIMIENTO = 50 * TARIFA_EQUIPO + 60.0   # 50 h al año y el dominio del proveedor

ESCENARIOS = {
    #            committers por organización, organizaciones por año 2027..2031
    "Pesimista": (5, [1, 2, 3, 5, 7]),
    "Base": (10, [2, 5, 9, 14, 20]),
    "Optimista": (15, [3, 8, 15, 25, 40]),
}


def ingreso_por_org(committers: int, precio_usd: float = PRECIO_USD) -> float:
    return committers * precio_usd * 12 * TIPO_CAMBIO


def flujos(committers, orgs, precio_usd=PRECIO_USD, escala=1.0):
    i0 = sum(INVERSION.values())
    return [-i0] + [o * escala * ingreso_por_org(committers, precio_usd) - MANTENIMIENTO for o in orgs]


def van(fs, k):
    return sum(f / (1 + k) ** t for t, f in enumerate(fs))


def tir(fs, lo=-0.99, hi=10.0):
    if van(fs, lo) * van(fs, hi) > 0:
        return None
    for _ in range(200):
        m = (lo + hi) / 2
        if van(fs, lo) * van(fs, m) <= 0:
            hi = m
        else:
            lo = m
    return (lo + hi) / 2


def escala_critica(committers, orgs, k=TASA):
    lo, hi = 0.0, 1.0
    for _ in range(100):
        m = (lo + hi) / 2
        if van(flujos(committers, orgs, escala=m), k) < 0:
            lo = m
        else:
            hi = m
    return hi


def costo_hora(sueldo):
    return sueldo * SUELDOS_ANUALES / HORAS_ANUALES


def main():
    print(f"Inversión I0: {sum(INVERSION.values()):,.2f}")
    for k, v in INVERSION.items():
        print(f"  {k}: {v:,.2f}")
    print(f"Mantenimiento anual: {MANTENIMIENTO:,.2f}")
    print(f"Costo empleador por hora: promedio {costo_hora(SUELDO_PROMEDIO):.2f}, máximo {costo_hora(SUELDO_MAXIMO):.2f}"
          f" (sueldos/año {SUELDOS_ANUALES:.2f}, horas/año {HORAS_ANUALES:.0f})")
    for nombre, (c, orgs) in ESCENARIOS.items():
        fs = flujos(c, orgs)
        t = tir(fs)
        print(f"\n{nombre}: ingreso por org {ingreso_por_org(c):,.2f}")
        print("  flujos:", [round(f, 2) for f in fs])
        print(f"  VAN {TASA:.2%}: {van(fs, TASA):,.2f}  TIR: {('%.2f %%' % (100 * t)) if t is not None else 'no existe'}")
    c, orgs = ESCENARIOS["Base"]
    print("\nSensibilidad (base):")
    for k in (TASA_SOCIAL, TASA, FTAMN):
        print(f"  tasa {k:.2%}: {van(flujos(c, orgs), k):,.2f}")
    for p in (3.0, 5.0, 10.0):
        print(f"  precio US$ {p}: {van(flujos(c, orgs, p), TASA):,.2f}")
    for cc in (5, 10, 15):
        print(f"  committers {cc}: {van(flujos(cc, orgs), TASA):,.2f}")
    e = escala_critica(c, orgs)
    print(f"  proporción crítica de la senda base: {e:.1%} (≈ {e * orgs[-1]:.1f} organizaciones en 2031)")
    # comprobación del lado del cliente
    ahorro = (HORAS_PRODUCCION - HORAS_CODIFICACION)
    for nombre, s in (("promedio", SUELDO_PROMEDIO), ("máximo", SUELDO_MAXIMO)):
        valor = ahorro * costo_hora(s)
        costo_cliente = ingreso_por_org(c) + 12 * SERVIDOR_USD * TIPO_CAMBIO
        print(f"\nCliente ({nombre}): ahorro por defecto {ahorro:.1f} h = S/ {valor:,.2f}; "
              f"costo anual base (licencia + servidor) S/ {costo_cliente:,.2f} → "
              f"{costo_cliente / valor:.1f} defectos/año para recuperarlo")


if __name__ == "__main__":
    main()
