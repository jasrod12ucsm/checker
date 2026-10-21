"""Genera Proyecto_Fin_de_Carrera_V4 sobre la V2: capítulos 4, 5 y 7 desde el libro
(libro/diseno/cap4, cap5, libro/construccion) y las síntesis de los capítulos 1 y 2
(1.4.3, 1.11, 2.5.5) con los mismos códigos de requisitos y casos de uso."""
import os, re, struct, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
from split import split, text, style

REPO = os.path.expanduser("~/Documents/tesis/checker")
LIB = os.path.join(REPO, "libro")
PNG = os.path.join(LIB, "diagramas", "png")
U = sys.argv[1]                       # carpeta con el docx descomprimido

# ---------------------------------------------------------------- adaptaciones al informe
SUBS = [
    (r"CSA ya está construido como pide `modelado-funcional`:",
     "CSA ya está construido como pide el diseño funcional de dominio (Wlaschin, 2018):"),
    (r"Es la misma regla de la skill\s+`bodega-arquitectura` \(§2\.1\), con un \*target\* de CMake en el papel de un crate\s+de Cargo:",
     "Es la regla de dependencias del diseño guiado por el dominio (Evans, 2003), con un *target* de CMake como frontera:"),
    (r"Regla \(de `rust-trinity` y `modelado-funcional`, traducida a C\+\+\)", "Principio (Wlaschin, 2018), en C++"),
    (r"preferencia \(`bodega-arquitectura` §0\)\.", "preferencia."),
    (r"\| mdbook \+ PlantUML \| este libro \|", "| mdbook + PlantUML | libro del proyecto |"),
    (r"\(leyes, contradicción 2\)", "(sección 5.9.4)"),
    (r"Método: `modelado-funcional` §16–§18 \(Elliott y Maguire\)\.", "Método: primero el significado de cada pieza, después las leyes que se prueban, en la línea de Wlaschin (2018)."),
    (r" \(§18\.4\)", ""),
    (r"Procedimiento \(Maguire\):", "Procedimiento:"),
    (r"\[7\.1 d\)\]\(7-1-codigo\.md\)", "7.1.4"),
    (r"\(leyes, contradicciones 2 y 3\)", "(sección 5.9.4)"),
    (r"\[Dónde va cada cosa\]\([^)]*\)", "la estructura de paquetes de la sección 5.3"),
    (r"\[Decisiones\]\([^)]*\)", "la sección 5.8"),
    (r"(?<!!)\[([^\]]+)\]\(\.\./resultados/[^)]*\)", r"\1 (libro del proyecto)"),
    (r"(?<!!)\[([^\]]+)\]\(\.\./\.\./resultados/[^)]*\)", r"\1 (libro del proyecto)"),
    (r"(?<!!)\[([^\]]+)\]\(\.\./[^)]*dinamica[^)]*\)", r"\1 (libro del proyecto)"),
    (r"(?<!!)\[([^\]]+)\]\((?!http)[^)]*\)", r"\1"),          # el resto de enlaces: sólo el texto
]
def adaptar(md):
    for a, b in SUBS:
        md = re.sub(a, b, md)
    return md

# ---------------------------------------------------------------- XML de bajo nivel
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
LANG = '<w:lang w:val="es-PE"/>'
MONO = '<w:rFonts w:ascii="DejaVu Sans Mono" w:hAnsi="DejaVu Sans Mono"/>'

def runs(s, sz=None):
    """**negrita**, *cursiva*, `código` → w:r."""
    out, buf, b, i_, code = [], [], False, False, False
    def flush():
        if not buf: return
        t = "".join(buf); buf.clear()
        rpr = ("<w:b/>" if b else "") + ("<w:i/>" if i_ else "")
        if code: rpr = MONO + rpr + f'<w:sz w:val="{(sz or 22) - 3}"/>'
        elif sz: rpr += f'<w:sz w:val="{sz}"/>'
        out.append(f'<w:r><w:rPr>{rpr}{LANG}</w:rPr><w:t xml:space="preserve">{esc(t)}</w:t></w:r>')
    k = 0
    while k < len(s):
        c = s[k]
        if c == "`":
            flush(); code = not code; k += 1; continue
        if not code and s.startswith("**", k):
            flush(); b = not b; k += 2; continue
        if not code and c == "*" and (k + 1 < len(s) and s[k + 1] not in " ") and not i_ \
                and "*" in s[k + 1:]:
            flush(); i_ = True; k += 1; continue
        if not code and c == "*" and i_:
            flush(); i_ = False; k += 1; continue
        buf.append(c); k += 1
    flush()
    return "".join(out)

def par(inner, ppr='<w:jc w:val="both"/>', st=None):
    s = f'<w:pStyle w:val="{st}"/>' if st else ""
    return f'<w:p><w:pPr>{s}{ppr}<w:rPr>{LANG}</w:rPr></w:pPr>{inner}</w:p>'

def heading(st, t, extra=""):
    return f'<w:p><w:pPr><w:pStyle w:val="{st}"/>{extra}<w:rPr>{LANG}</w:rPr></w:pPr>{runs(t)}</w:p>'

def caption(t): return par(runs(t), "", "Descripcin").replace('<w:pPr><w:pStyle w:val="Descripcin"/>',
                                                              '<w:pPr><w:pStyle w:val="Descripcin"/><w:keepNext/>', 1)
def caption_fig(t): return par(runs(t), '<w:keepNext w:val="0"/>', "Descripcin")
SPACER = '<w:p><w:pPr><w:spacing w:after="40"/></w:pPr></w:p>'

def code_block(lines):
    out = []
    for n, l in enumerate(lines):
        after = "160" if n == len(lines) - 1 else "0"
        out.append(f'<w:p><w:pPr>{"" if n == len(lines)-1 else "<w:keepNext/>"}<w:keepLines/>'
                   f'<w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/>'
                   f'<w:spacing w:before="0" w:after="{after}" w:line="240" w:lineRule="auto"/></w:pPr>'
                   f'<w:r><w:rPr>{MONO}<w:sz w:val="16"/></w:rPr><w:t xml:space="preserve">{esc(l) or " "}</w:t></w:r></w:p>')
    return "".join(out)

BORD = ''.join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="D9D9D9"/>' for s in ("top", "left", "bottom", "right"))
MAR = ''.join(f'<w:{s} w:w="80" w:type="dxa"/>' for s in ("top", "left", "bottom", "right"))
TOTAL = 9071

def table(rows):
    ncol = len(rows[0])
    sz = 21 if ncol <= 3 else (19 if ncol == 4 else 17)
    plain = lambda c: re.sub(r"[*`]", "", c)
    cpw = 100 * sz / 21                                   # ancho aproximado de un carácter (dxa)
    word = lambda c: max((len(w) for w in plain(c).split()), default=1)
    minw = [max(word(r[j]) for r in rows if j < len(r)) * cpw + 220 for j in range(ncol)]
    peso = [max(6, min(60, max(len(plain(r[j])) for r in rows if j < len(r)))) for j in range(ncol)]
    if sum(minw) > TOTAL:
        minw = [m * TOTAL / sum(minw) for m in minw]
    libre = TOTAL - sum(minw)
    ws = [int(minw[j] + libre * peso[j] / sum(peso)) for j in range(ncol)]
    ws[-1] += TOTAL - sum(ws)
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in ws)
    trs = []
    for i, r in enumerate(rows):
        r = (r + [""] * ncol)[:ncol]
        hdr = i == 0
        trpr = '<w:trPr><w:cantSplit/>' + ('<w:tblHeader/>' if hdr else '') + '<w:jc w:val="center"/></w:trPr>'
        tcs = []
        for j, c in enumerate(r):
            fill = "DCE6F1" if hdr else "FFFFFF"
            c = f"**{c}**" if hdr and not c.startswith("**") else c
            tcs.append(f'<w:tc><w:tcPr><w:tcW w:w="{ws[j]}" w:type="dxa"/><w:tcBorders>{BORD}</w:tcBorders>'
                       f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/><w:tcMar>{MAR}</w:tcMar>'
                       f'<w:vAlign w:val="center"/></w:tcPr>'
                       f'<w:p><w:pPr><w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/>'
                       f'<w:rPr>{LANG}</w:rPr></w:pPr>{runs(c.strip(), sz)}</w:p></w:tc>')
        trs.append(f'<w:tr>{trpr}{"".join(tcs)}</w:tr>')
    return (f'<w:tbl><w:tblPr><w:tblW w:w="{TOTAL}" w:type="dxa"/><w:jc w:val="center"/><w:tblLayout w:type="fixed"/>'
            f'<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
            f'</w:tblPr><w:tblGrid>{grid}</w:tblGrid>{"".join(trs)}</w:tbl>') + SPACER

# ---------------------------------------------------------------- imágenes y numeración
RELS, NUMS = [], []
state = {"rid": 1000, "docpr": 5000, "num": 900}

def png_size(p):
    with open(p, "rb") as f:
        f.read(16); w, h = struct.unpack(">II", f.read(8))
    return w, h

def image(name):
    src = os.path.join(PNG, name + ".png")
    state["rid"] += 1; state["docpr"] += 1
    rid, dp = f"rId{state['rid']}", state["docpr"]
    shutil.copy(src, os.path.join(U, "word", "media", f"v4_{name}.png"))
    RELS.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/v4_{name}.png"/>')
    w, h = png_size(src)
    cx, cy = w * 9525, h * 9525
    k = min(1.0, 5760720 / cx, 7400000 / cy)
    cx, cy = int(cx * k), int(cy * k)
    return (f'<w:p><w:pPr><w:keepNext/><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:noProof/></w:rPr><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
            f'<wp:effectExtent l="0" t="0" r="0" b="0"/><wp:docPr id="{dp}" name="{name}"/>'
            f'<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
            f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="{dp}" name="{name}.png"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            f'</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')

def new_numbered():
    state["num"] += 1
    NUMS.append(f'<w:num w:numId="{state["num"]}"><w:abstractNumId w:val="7"/>'
                f'<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>')
    return state["num"]

# ---------------------------------------------------------------- markdown → OOXML
class Cap:
    def __init__(self, n): self.n, self.tab, self.fig, self.h2, self.h3 = n, 0, 0, 0, 0

def convert(md, cap, h1_as=None, skip_tables=()):
    """h1_as: texto del Ttulo2 que reemplaza al '# …' de la página (None = omitir)."""
    md = adaptar(md)
    L = md.split("\n"); i = 0; out = []; last_head = ""; pend = [None]
    def para_lines():
        nonlocal i
        buf = []
        while i < len(L) and L[i].strip() and not re.match(r"(#|\||```|!\[|>|\s*[-*] |\s*\d+\. )", L[i]):
            buf.append(L[i].strip()); i += 1
        return " ".join(buf)
    while i < len(L):
        l = L[i]
        if not l.strip(): i += 1; continue
        m = re.match(r"(#+) (.*)", l)
        if m:
            lvl, t = len(m.group(1)), m.group(2).strip(); i += 1
            if lvl == 3 and re.match(r"(RF|CU)-\d+ ", t):
                pend[0] = t; continue
            if lvl == 1:
                if h1_as:
                    cap.h2 += 1; cap.h3 = 0
                    out.append(heading("Ttulo2", h1_as)); last_head = h1_as
                continue
            if lvl == 2:
                cap.h3 += 1
                t = re.sub(r"^([a-z]\)|\d+\.)\s*", "", t)
                t = f"{cap.n}.{cap.h2}.{cap.h3} {t}"
                out.append(heading("Ttulo3", t))
            else:
                out.append(heading("Ttulo4", t))
            last_head = re.sub(r"^[\d.]+ ", "", t)
            continue
        if l.startswith("```"):
            i += 1; buf = []
            while i < len(L) and not L[i].startswith("```"): buf.append(L[i]); i += 1
            i += 1; out.append(code_block(buf)); continue
        if l.startswith("|"):
            rows = []
            while i < len(L) and L[i].startswith("|"):
                cells = [c.strip() for c in re.split(r"(?<!\\)\|", L[i].strip())[1:-1]]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells): rows.append(cells)
                i += 1
            if rows[0][0] in skip_tables: continue
            cap.tab += 1
            tit = pend[0] or TITULOS.get(rows[0][0] + '|' + rows[0][1], last_head); pend[0] = None
            out.append(caption(f"Tabla {cap.n}.{cap.tab} {tit}"))
            out.append(table(rows)); continue
        m = re.match(r"!\[([^\]]*)\]\(([^)]*)\)", l)
        if m:
            i += 1; cap.fig += 1
            out.append(image(os.path.splitext(os.path.basename(m.group(2)))[0]))
            out.append(caption_fig(f"Figura {cap.n}.{cap.fig} {m.group(1)}")); continue
        if l.startswith(">"):
            buf = []
            while i < len(L) and L[i].startswith(">"):
                buf.append(L[i].lstrip("> ").strip()); i += 1
            for chunk in " ".join(buf).split("  "):
                pass
            out.append(par(runs(" ".join(buf)), '<w:ind w:left="340"/><w:jc w:val="both"/>', "Cita")); continue
        m = re.match(r"(\s*)([-*]|\d+\.) (.*)", l)
        if m:
            numbered = m.group(2)[0].isdigit(); nid = new_numbered() if numbered else None
            while i < len(L):
                m = re.match(r"(\s*)([-*]|\d+\.) (.*)", L[i])
                if not m: break
                ind = len(m.group(1)); item = [m.group(3).strip()]; i += 1
                while i < len(L) and L[i].strip() and not re.match(r"\s*([-*]|\d+\.) ", L[i]) \
                        and L[i].startswith(" "):
                    item.append(L[i].strip()); i += 1
                t = " ".join(item)
                if numbered and ind == 0:
                    out.append(par(runs(t), f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{nid}"/></w:numPr><w:jc w:val="both"/>', "Listaconnmeros"))
                else:
                    out.append(par(runs(t), '<w:jc w:val="both"/>', "Listaconvietas2" if ind else "Listaconvietas"))
            continue
        out.append(par(runs(para_lines())))
    return "".join(out)

TITULOS = {
    "Contexto|Corre en": "Contextos de la arquitectura",
    "Caso|Actor": "Casos de uso, actores y requisitos",
    "Caso|Excepción": "Excepciones de los casos de uso",
    "Relación|Por qué": "Relaciones entre casos de uso",
    "Caso de uso|Criterio (dado, cuando, entonces)": "Criterios de aceptación de los casos de uso",
    "Componente|Qué es": "Componentes del sistema y usuarios",
    "Grupo|Requisitos": "Grupos funcionales",
    "Usuario|Qué hace con el sistema": "Usuarios del sistema",
    "Elemento|Especificación (fijada en la imagen `checker:llvm21`)": "Entorno operativo",
    "Requisito|Objetivo": "Trazabilidad requisito, objetivo, caso de uso y evidencia",
    "ID|Regla": "Reglas del producto y del experimento",
    "ID|Interfaz": "Interfaces",
    "Código|Característica": "Requerimientos de producto, criterio y medición",
    "Código|Descripción": "Requisitos organizacionales",
    "Referencia|Para qué": "Normas y estándares aplicables",
    "Categoría|Requisito": "Requerimientos externos",
    "Dato|Para qué": "Requisitos de datos",
    "Mensaje|De → a": "Mensajes de la colaboración y su API en CSA",
    "Paquete|Contiene": "Paquetes y dependencias",
    "Desde|Evento": "Transiciones del handle",
    "Capa|Sabe de": "Capas de la arquitectura lógica",
    "Nodo / artefacto|Qué es": "Nodos y artefactos del despliegue",
    "ID|Decisión": "Decisiones de diseño",
    "Riesgo|Señal temprana": "Riesgos y mitigaciones",
    "Pieza|Constructores": "Constructores y observaciones",
    "Ley|Prueba": "De las leyes a las pruebas",
    "Tema de la práctica|Sección": "Correspondencia con la práctica (Caso A)",
    "Herramienta|Versión": "Entorno de construcción",
    "Tema|Estándar": "Estándares de codificación",
    "Nivel|Qué prueba": "Pruebas durante la codificación",
    "Entidad|Archivo": "Diseño lógico: archivos, claves e integridad",
    "Prueba|Comprueba": "Pruebas de los datos",
    "Rama|Para": "Ramas del repositorio",
    "Tag|Cuándo": "Etiquetas de versión",
    "Característica|Práctica": "Características de calidad y controles",
    "Regla|Error que hace imposible": "Reglas de calidad y errores que evitan",
    "Componente|Responsabilidad única": "Componentes del sistema",
    "Inc.|Entrega": "Incrementos de construcción",
    "Pieza|Estado": "Estado actual del proyecto",
}

rd = lambda p: open(os.path.join(LIB, p)).read()

# ---------------------------------------------------------------- capítulo 5
c5 = Cap(5); x5 = []
intro = rd("diseno/cap5/index.md")
intro = re.sub(r"^> Versión rehecha.*?\n\n", "", intro, flags=re.S | re.M)
x5.append(convert(intro, c5, None, skip_tables=("Sección",)))
x5.append(par(runs("Esta versión reemplaza la propuesta anterior del capítulo. Aquella usaba clases conceptuales "
                   "con estados escritos como texto (`validez: String`), una capacidad guardada como entero y "
                   "métodos `void`, que no pueden existir dentro de CSA; y el prototipo `mi-linter` se apoyaba en "
                   "*AST matchers*, que no ven qué ocurrió antes en el mismo camino de ejecución. El corpus ya "
                   "ejecutado fija además el alcance: sobre el handle que cada caso sostiene, el analizador de referencia "
                   "detecta el 37.5 % de los usos inválidos de iteradores (48 de 128) y el 0 % de los de referencias "
                   "y punteros (0 de 200). Las decisiones se resumen en "
                   "la sección 5.8 y las leyes del modelo en la sección 5.9.")))
for f, t in [("5-1-casos-de-uso", "5.1 Diagramas de casos de uso"), ("5-2-colaboracion", "5.2 Diagrama de colaboración"),
             ("5-3-paquetes", "5.3 Diagramas de paquetes"), ("5-4-clases", "5.4 Diagramas de clases"),
             ("5-5-estados", "5.5 Diagramas de estado"), ("5-6-arquitectura-logica", "5.6 Arquitectura lógica"),
             ("5-7-arquitectura-fisica", "5.7 Arquitectura física")]:
    x5.append(convert(rd(f"diseno/cap5/{f}.md"), c5, t))
x5.append(convert(rd("diseno/decisiones.md"), c5, "5.8 Decisiones de diseño"))
x5.append(convert(rd("diseno/leyes.md"), c5, "5.9 Significado y leyes del modelo"))

# ---------------------------------------------------------------- capítulo 4
c4 = Cap(4); x4 = []
intro4 = re.sub(r"^> Versión rehecha.*?\n\n", "", rd("diseno/cap4/index.md"), flags=re.S | re.M)
# El enlace a la guía de uso es del libro, no del informe.
intro4 = re.sub(r"\n*Dónde se valida cada requerimiento en el código[^\n]*\n?", "\n", intro4)
intro4 = re.sub(r"\n- \[.*", "", intro4)
x4.append(convert(intro4, c4, None))
x4.append(convert(rd("diseno/cap4/4-1-funcionales.md"), c4, "4.1 Requerimientos funcionales"))
x4.append(convert(rd("diseno/cap4/4-2-no-funcionales.md"), c4, "4.2 Requerimientos no funcionales"))

# ---------------------------------------------------------------- síntesis de los capítulos 1 y 2
def md_table(md, primera):
    """Filas de la tabla del libro cuya cabecera empieza por `primera`."""
    L = md.split("\n"); k = next(j for j, l in enumerate(L) if l.startswith("| " + primera + " |"))
    rows = []
    while k < len(L) and L[k].startswith("|"):
        cells = [c.strip() for c in L[k].strip().split("|")[1:-1]]
        if not all(re.fullmatch(r":?-+:?", c) for c in cells): rows.append(cells)
        k += 1
    return rows
cu = rd("diseno/cap5/5-1-casos-de-uso.md")
nombres = {r[0].split("**")[1]: r[0].replace("**", "") for r in md_table(cu, "Caso")[1:]}
actores = {r[0].split("**")[1]: r[1] for r in md_table(cu, "Caso")[1:]}
reqs = {r[0].split("**")[1]: r[3] for r in md_table(cu, "Caso")[1:]}
crit = md_table(cu, "Caso de uso")
T110 = [["Caso de uso", "Actor", "Requisitos", "Criterio (dado, cuando, entonces)"]] + \
       [[nombres[r[0]], actores[r[0]], reqs[r[0]], r[1]] for r in crit[1:]]
S111 = ("Los requisitos completos se desarrollan en el capítulo 4 y los casos de uso en la sección 5.1. "
        "El sistema tiene tres partes: el checker ucsm.ContainerInvalidation, que se carga en clang como "
        "plugin; la norma de C++17 escrita como datos, de la que se generan el checker y las etiquetas; y el "
        "banco con su arnés, que mide al checker frente a Clang Static Analyzer. Los actores son el "
        "desarrollador de C++, el evaluador y el mantenedor. El docente y la asesoría supervisan el proyecto, "
        "pero no son actores del software. Cada caso de uso se ejecuta con una orden concreta y tiene un "
        "criterio de aceptación comprobado.")
grupos = md_table(rd("diseno/cap4/4-1-funcionales.md"), "Grupo")
OBJ = {"Analizar código": "OE2", "Seguir handles": "OE2", "Aplicar la norma": "OE2", "Diagnosticar": "OE2",
       "Medir": "OE1 y OE3", "Mantener": "OE1 y OE2"}
T212 = [["Necesidad", "Requisitos", "Casos de uso", "Objetivo"]] + [[g[0], g[1], g[2], OBJ[g[0]]] for g in grupos[1:]]
S255 = ("Los códigos RF-01 a RF-17, RNF-01 a RNF-08, RN-001 a RN-007 e INT-001 a INT-006 se definen una sola "
        "vez en el capítulo 4 y se reutilizan en los casos de uso (sección 5.1), en los componentes (sección 7.5) "
        "y en el plan de incrementos (sección 7.6). Cada requisito declara cómo se demuestra con el analizador "
        "estático y la evidencia registrada; un cambio de requisito sigue el procedimiento de 2.5.6 y se refleja "
        "en las pruebas lit, los gtests o el experimento que lo demuestran.")
T13 = [["Objetivo", "Resultado", "Capítulo que lo desarrolla"],
       ["OE1", "Banco de 750 casos etiquetado desde la norma, validado dinámicamente (852 ejecuciones, 0 contradicciones) y medición de referencia de CSA.",
        "2: metodología; 4: RF-13 a RF-15; 6: datos; 7: construcción del banco y del arnés."],
       ["OE2", "Checker ucsm.ContainerInvalidation construido como plugin de CSA (LLVM 21) y probado.",
        "4: RF-01 a RF-12, RF-16 y RF-17; 5: arquitectura; 7: construcción del código."],
       ["OE3", "Comparación en cuatro condiciones con cotejo por sitio y métricas reproducibles.",
        "2: protocolo; 4: RF-13, RF-14, RNF-01 a RNF-05; 7: estado y resultados."]]

# ---------------------------------------------------------------- capítulo 7
c7 = Cap(7); x7 = [heading("Ttulo1", "Capítulo 7 Construcción del software", "<w:pageBreakBefore/>")]
x7.append(convert(rd("construccion/index.md"), c7, None))
for f, t in [("7-1-codigo", "7.1 Construcción del código"), ("7-2-datos", "7.2 Construcción de la base de datos"),
             ("7-3-versiones", "7.3 Control de versiones"), ("7-4-calidad", "7.4 Calidad del código"),
             ("7-5-componentes", "7.5 Desarrollo de componentes"), ("7-6-incrementos", "7.6 Plan de incrementos"),
             ("7-7-estado", "7.7 Estado actual")]:
    x7.append(convert(rd(f"construccion/{f}.md"), c7, t))

# ---------------------------------------------------------------- ensamblar
doc = os.path.join(U, "word", "document.xml")
head, P, tail = split(open(doc).read())

def donde(st, empieza):
    return next(i for i, p in enumerate(P) if style(p) == st and text(p).startswith(empieza))
def sig(i, pred):
    return next(k for k in range(i + 1, len(P)) if pred(P[k]))
es_tabla = lambda p: p.startswith("<w:tbl")
es_cap = lambda p: style(p) == "Descripcin"
# Tabla 1.2: el banco real tiene un quinto eje, la garantía (D-20)
def fila_como(tr, celdas):
    out = tr
    for vieja, nueva in zip(re.findall(r"<w:tc>.*?</w:tc>", tr, re.S), celdas):
        ts = list(re.finditer(r"(<w:t[^>]*>)[^<]*(</w:t>)", vieja))
        c = vieja[:ts[0].start()] + ts[0].group(1) + esc(nueva) + ts[0].group(2) + "".join(
            vieja[a.end():b.start()] + b.group(1) + b.group(2) for a, b in zip(ts, ts[1:])) + vieja[ts[-1].end():]
        out = out.replace(vieja, c, 1)
    return out
k = next(i for i, p in enumerate(P) if es_cap(p) and text(p).startswith("Tabla 1.2 ")); t = sig(k, es_tabla)
ultima = re.findall(r"<w:tr[ >].*?</w:tr>", P[t], re.S)[-1]
P[t] = P[t].replace(ultima, ultima + fila_como(ultima, [
    "E", "Garantía previa: ninguna, reserve suficiente o handle devuelto por la mutación",
    "Medir falsas alarmas en el buen uso de operaciones que pueden invalidar."]))
# 1.4.3
k = donde("Ttulo3", "1.4.3"); P[sig(k, es_tabla)] = table(T13)
# 1.11
k = donde("Ttulo2", "1.11"); P[k + 1] = par(runs(S111))
P[sig(k, es_cap)] = caption("Tabla 1.10 Casos de uso y criterios de aceptación"); P[sig(k, es_tabla)] = table(T110)
# 2.5.5
k = donde("Ttulo3", "2.5.5"); P[k + 1] = par(runs(S255))
P[sig(k, es_cap)] = caption("Tabla 2.12 Requisitos por necesidad, caso de uso y objetivo"); P[sig(k, es_tabla)] = table(T212)
i4 = next(i for i, p in enumerate(P) if style(p) == "Ttulo1" and text(p).startswith("Capítulo 4"))
i5 = next(i for i, p in enumerate(P) if style(p) == "Ttulo1" and text(p).startswith("Capítulo 5"))
i6 = next(i for i, p in enumerate(P) if style(p) == "Ttulo1" and text(p).startswith("Capítulo 6"))
ig = next(i for i, p in enumerate(P) if style(p) == "Ttulo1" and text(p).startswith("Glosario"))
ir = next(i for i, p in enumerate(P) if style(p) == "Ttulo1" and text(p).startswith("Referencias"))

def ref(texto, cursiva):
    a, b = texto.split(cursiva)
    return (f'<w:p><w:pPr><w:keepLines/><w:spacing w:line="252" w:lineRule="auto"/><w:ind w:left="340" w:hanging="340"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{esc(a)}</w:t></w:r><w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">{esc(cursiva)}</w:t></w:r>'
            f'<w:r><w:t xml:space="preserve">{esc(b)}</w:t></w:r></w:p>')
EVANS = ref("Evans, E. (2003). Domain-driven design: Tackling complexity in the heart of software. Addison-Wesley.",
            "Domain-driven design: Tackling complexity in the heart of software")
WLAS = ref("Wlaschin, S. (2018). Domain modeling made functional: Tackle software complexity with domain-driven design and F#. Pragmatic Bookshelf.",
           "Domain modeling made functional: Tackle software complexity with domain-driven design and F#")
refs = P[ir + 1:]
pos_e = next(k for k, p in enumerate(refs) if text(p) > "Evans" and text(p).strip())
refs.insert(pos_e, EVANS)
pos_w = max(k for k, p in enumerate(refs) if text(p).strip() and text(p) < "Wlaschin") + 1
refs.insert(pos_w, WLAS)

nuevo = P[:i4 + 1] + ["".join(x4)] + P[i5:i5 + 1] + ["".join(x5)] + P[i6:ig] + ["".join(x7)] + P[ig:ir + 1] + refs
# El DOI de Kashyap et al. en la V2 apuntaba a otro artículo (Crossref: SCAM.2019.00019 es de
# Harrand et al.); el correcto es SCAM.2019.00020.
cuerpo = head + "".join(nuevo) + tail
assert cuerpo.count("10.1109/SCAM.2019.00019") == 1, "el DOI de Kashyap cambió de forma en la V2"
open(doc, "w").write(cuerpo.replace("10.1109/SCAM.2019.00019", "10.1109/SCAM.2019.00020"))

rels = os.path.join(U, "word", "_rels", "document.xml.rels")
s = open(rels).read(); open(rels, "w").write(s.replace("</Relationships>", "".join(RELS) + "</Relationships>"))
num = os.path.join(U, "word", "numbering.xml")
s = open(num).read()
k = s.rindex("</w:num>") + len("</w:num>")
open(num, "w").write(s[:k] + "".join(NUMS) + s[k:])
st = os.path.join(U, "word", "settings.xml")
s = open(st).read()
if "w:updateFields" not in s:
    m = re.search(r"<w:(hdrShapeDefaults|footnotePr|endnotePr|compat|docVars|rsids)\b", s)
    s = s[:m.start()] + '<w:updateFields w:val="true"/>' + s[m.start():]
    open(st, "w").write(s)
print(f"cap4: {c4.tab} tablas; cap5: {c5.tab} tablas, {c5.fig} figuras; cap7: {c7.tab} tablas, {c7.fig} figuras; imágenes {len(RELS)}")
