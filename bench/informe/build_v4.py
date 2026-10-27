"""Genera el Word del proyecto sobre la V2 de la universidad: portada, resumen, índices, los capítulos 1 a 7, el glosario y las referencias salen del libro (libro/informe, libro/diseno/cap4 a cap6, libro/construccion).
De la V2 quedan solo el formato, la portada institucional y los títulos de capítulo."""
import json, os, re, struct, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from split import split, text, style
from fragmentos import fragmento

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
def codigo(m):
    "Una línea {{codigo RUTA SÍMBOLO}} del libro: en el informe va el fragmento, sin enlace."
    _, cuerpo = fragmento(os.path.join(REPO, m.group(1)), m.group(2).strip())
    return "```\n" + "\n".join(cuerpo) + "\n```"

def adaptar(md):
    md = re.sub(r"^\{\{codigo (\S+) (.+?)\}\}$", codigo, md, flags=re.M)
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

def caption(t): return par(runs(t), "<w:keepNext/>", "LeyendaTabla")
def caption_fig(t): return par(runs(t), '<w:keepNext w:val="0"/>', "LeyendaFigura")
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

MOCKUPS = os.path.join(LIB, "mockups")

def image(name):
    src = os.path.join(PNG, name + ".png")
    if not os.path.exists(src):
        src = os.path.join(MOCKUPS, name + ".png")
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
    def __init__(self, n): self.n, self.tab, self.fig, self.h2, self.h3, self.usados = n, 0, 0, 0, 0, set()
    def num(self, k): return "" if self.n is None else f"{self.n}.{k} "

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
        m = re.match(r"Tabla: (.*)", l)
        if m:
            pend[0] = m.group(1).strip(); i += 1; continue
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
            tit = re.sub(r"^([a-z]\)|[\d.]+) ", "", tit)
            if tit in cap.usados and last_head and last_head != tit:
                tit = f"{tit}: {re.sub(r'^([a-z]\)|[\d.]+) ', '', last_head)}"
            cap.usados.add(tit)
            out.append(caption(f"Tabla {cap.num(cap.tab)}{tit}" if cap.n is not None else tit))
            out.append(table(rows)); continue
        m = re.match(r"!\[([^\]]*)\]\(([^)]*)\)", l)
        if m:
            i += 1; cap.fig += 1
            out.append(image(os.path.splitext(os.path.basename(m.group(2)))[0]))
            out.append(caption_fig(f"Figura {cap.num(cap.fig)}{m.group(1)}")); continue
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

def convert_capitulo(md, cap):
    secciones = re.split(r"^## ", md, flags=re.M)
    out = [convert(re.sub(r"^# .*\n", "", secciones[0]), cap, None)]
    for sec in secciones[1:]:
        titulo, _, cuerpo = sec.partition("\n")
        out.append(convert("# x\n" + re.sub(r"^### ", "## ", cuerpo, flags=re.M), cap, titulo.strip()))
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
    "Usuario|Pantallas": "Usuarios, pantallas y casos de uso",
    "Elemento|Dónde": "Elementos de la interfaz y sus reglas",
    "Método y ruta|Cuerpo": "Rutas de la API HTTP y del webhook",
    "Evento|Respuesta": "Respuestas del webhook",
    "Servicio|Para qué": "Servicios consumidos por el sistema",
    "Tabla|Clave": "Tablas de la base de datos",
    "Regla|Cómo": "Reglas de integridad de la base de datos",
    "Nivel (servicio)|Qué prueba": "Pruebas del servicio",
    "Almacén|Para qué": "Almacenes de datos del proyecto",
    "Ruta|Método": "Rutas de la API y caso de uso que atienden",
    "Paso|Quién decide": "Pasos de la revisión de un pull request",
    "Nodo|Software": "Nodos del despliegue del servicio",
    "Decisión|Por qué": "Decisiones del diseño físico",
    "Casos|Antes": "Contradicción 6: antes y ahora",
    "Proyecto|*Commit*": "Proyectos reales analizados",
    "Síntoma en código real|Causa": "Errores que destapó el código real",
    "Id|Proyecto": "Defectos sembrados",
    "Nivel (motor)|Qué prueba": "Pruebas del motor",
    "Regla de codificación|Cómo se cumple": "Estándares de codificación del servicio",
    "Paso|Servicio": "Pasos de la integración continua",
    "Qué|Dónde": "Documentación del código",
    "Refactorización|Por qué": "Refactorizaciones",
    "Forma|Cómo se cumple": "Normalización del esquema",
    "Tipo de prueba|Qué se hizo": "Pruebas de rendimiento, recuperación y seguridad",
    "Carpeta|Contiene": "Estructura del repositorio",
    "Tag|Qué marca": "Etiquetas de versión",
    "Situación|Qué se hace": "Mantenimiento y gestión de incidentes",
    "Característica|Servicio Centinela C++": "Características de los componentes",
    "Condición|VP": "Precisión, exhaustividad y F1 por condición",
    "Condición|UB por caso": "Resultados del banco por condición",
    "Contexto|Leyes escritas": "Leyes y pruebas por contexto",
    "Estado|Significa": "Estados de una revisión y de un usuario",
}

rd = lambda p: open(os.path.join(LIB, p)).read()

# ---------------------------------------------------------------- capítulo 5
c5 = Cap(5); x5 = []
intro = rd("diseno/cap5/index.md")
intro = re.sub(r"^> Versión rehecha.*?\n\n", "", intro, flags=re.S | re.M)
x5.append(convert(intro, c5, None, skip_tables=("Sección",)))
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

# ---------------------------------------------------------------- capítulos 1 a 3, glosario y referencias
c1, c2, c3 = Cap(1), Cap(2), Cap(3)
x1 = convert_capitulo(rd("informe/cap1.md"), c1)
x2 = convert_capitulo(rd("informe/cap2.md"), c2)
x3 = convert_capitulo(rd("informe/cap3.md"), c3)
xg = convert(rd("informe/glosario.md"), Cap(None), None)
REFS = [l.strip() for l in rd("informe/referencias.md").split("\n") if l.strip() and not l.startswith("#")]
def referencia(t):
    return (f'<w:p><w:pPr><w:keepLines/><w:spacing w:line="252" w:lineRule="auto"/><w:ind w:left="340" w:hanging="340"/>'
            f'<w:rPr>{LANG}</w:rPr></w:pPr>{runs(t)}</w:p>')
portada = rd("informe/portada.md")
def bloque(titulo):
    return re.search(r"^## " + titulo + r"\n\n(.*?)(?=\n## |\Z)", portada, re.S | re.M).group(1).strip()

# ---------------------------------------------------------------- capítulo 6
c6 = Cap(6); x6 = []
x6.append(convert(rd("diseno/cap6/index.md"), c6, None, skip_tables=("Sección",)))
for f, t in [("6-1-interfaz", "6.1 Interfaz de usuario del sistema"), ("6-2-navegacion", "6.2 Diagrama de navegación del sistema"),
             ("6-3-mockups", "6.3 Esquemas de interfaz mockups y wireframes"), ("6-4-descripcion-ui", "6.4 Descripción de la interfaz de usuario"),
             ("6-5-servicios", "6.5 Interfaz de servicios del sistema"), ("6-6-diagrama-servicios", "6.6 Diagrama de interfaz de servicios"),
             ("6-7-descripcion-servicios", "6.7 Descripción de la interfaz de servicios"), ("6-8-consumidos", "6.8 Servicios consumidos por el sistema"),
             ("6-9-datos", "6.9 Modelo de base de datos")]:
    x6.append(convert(rd(f"diseno/cap6/{f}.md"), c6, t))

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

def con_texto(p, nuevo_runs):
    """El mismo párrafo (su pPr) con otro contenido."""
    m = re.match(r"(<w:p[ >].*?</w:pPr>)", p, re.S)
    return (m.group(1) if m else "<w:p>") + nuevo_runs + "</w:p>"
titulo1 = lambda empieza: next(i for i, p in enumerate(P) if style(p) == "Ttulo1" and text(p).startswith(empieza))
i1, i2, i3, i4, i5, i6 = (titulo1(f"Capítulo {n}") for n in range(1, 7))
ig, ir = titulo1("Glosario"), titulo1("Referencias")
it = next(i for i, p in enumerate(P) if style(p) == "Ttulo" and text(p).startswith("Implementacion"))
irs = next(i for i, p in enumerate(P) if style(p) == "Ttulo" and text(p) == "Resumen")
iab = next(i for i, p in enumerate(P) if style(p) == "Ttulo" and text(p) == "Abstract")
iix = next(i for i, p in enumerate(P) if style(p) == "Ttulo" and text(p).startswith("Índice"))

# portada, resumen y abstract
P[it] = con_texto(P[it], runs(bloque("Título")))
res, clave = bloque("Resumen").split("\n\n")
P[irs + 1] = con_texto(P[irs + 1], runs(res)); P[irs + 2] = con_texto(P[irs + 2], runs(clave))
abs_, key = bloque("Abstract").split("\n\n")
P[iab + 1] = con_texto(P[iab + 1], runs(abs_)); P[iab + 2] = con_texto(P[iab + 2], runs(key))

cuerpo = ([P[i1], x1, P[i2], x2, P[i3], x3, P[i4], "".join(x4), P[i5], "".join(x5), P[i6], "".join(x6), "".join(x7),
           P[ig], xg, P[ir]] + [referencia(r) for r in REFS])
assert "sectPr" in P[-1]

# índices: el general (Ttulo1 a Ttulo3), el de tablas y el de figuras, como campos TOC de Word.
# Se llenan con los números de página de una primera pasada (PAGINAS) y Word los actualiza al abrir.
PAG = json.load(open(os.environ["PAGINAS"])) if os.environ.get("PAGINAS") else {}
def entradas(estilos):
    out = []
    for m in re.finditer(r"<w:p[ >].*?</w:p>", "".join(cuerpo), re.S):
        st = style(m.group(0))
        if st in estilos: out.append((estilos[st], text(m.group(0)).strip()))
    return out
def indice(instr, items, estilo="TDC"):
    ps = []
    for k, (nivel, t) in enumerate(items):
        ini = (f'<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve">{instr}</w:instrText></w:r>'
               f'<w:r><w:fldChar w:fldCharType="separate"/></w:r>') if k == 0 else ""
        fin = '<w:r><w:fldChar w:fldCharType="end"/></w:r>' if k == len(items) - 1 else ""
        ps.append(f'<w:p><w:pPr><w:pStyle w:val="{estilo}{nivel}"/><w:rPr>{LANG}</w:rPr></w:pPr>{ini}'
                  f'<w:r><w:rPr>{LANG}</w:rPr><w:t xml:space="preserve">{esc(t)}</w:t></w:r>'
                  f'<w:r><w:tab/><w:t>{PAG.get(t, "")}</w:t></w:r>{fin}</w:p>')
    return "".join(ps)
SALTO = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
def titulo_indice(t): return con_texto(P[iix], f'<w:r><w:t>{t}</w:t></w:r>')
indices = (indice(' TOC \\o "1-3" \\h \\z \\u ', entradas({"Ttulo1": 1, "Ttulo2": 2, "Ttulo3": 3})) + SALTO
           + titulo_indice("Índice de tablas") + indice(' TOC \\o "8-8" \\h \\z \\u ', entradas({"LeyendaTabla": 1}), "IndiceIlustraciones") + SALTO
           + titulo_indice("Índice de figuras") + indice(' TOC \\o "9-9" \\h \\z \\u ', entradas({"LeyendaFigura": 1}), "IndiceIlustraciones"))
fin_indice = i1 - 1                       # el párrafo vacío (con el salto) antes del capítulo 1
nuevo = P[:iix + 1] + [indices] + P[fin_indice:i1] + cuerpo + [P[-1]]
open(doc, "w").write(head + "".join(nuevo) + tail)
open(os.path.join(U, "entradas.json"), "w").write(json.dumps(
    [t for _, t in entradas({"Ttulo1": 1, "Ttulo2": 2, "Ttulo3": 3, "LeyendaTabla": 1, "LeyendaFigura": 1})], ensure_ascii=False))

# estilos de las leyendas y de los índices
ESTILOS = (
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="LeyendaTabla"><w:name w:val="Leyenda de tabla"/><w:basedOn w:val="Descripcin"/>'
    '<w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:outlineLvl w:val="7"/></w:pPr></w:style>'
    '<w:style w:type="paragraph" w:customStyle="1" w:styleId="LeyendaFigura"><w:name w:val="Leyenda de figura"/><w:basedOn w:val="Descripcin"/>'
    '<w:next w:val="Normal"/><w:qFormat/><w:pPr><w:outlineLvl w:val="8"/></w:pPr></w:style>'
    + "".join(f'<w:style w:type="paragraph" w:styleId="TDC{n}"><w:name w:val="toc {n}"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>'
              f'<w:uiPriority w:val="39"/><w:unhideWhenUsed/><w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="8901"/></w:tabs>'
              f'<w:spacing w:after="40" w:line="240" w:lineRule="auto"/><w:ind w:left="{(n - 1) * 220}"/></w:pPr>'
              f'<w:rPr>{"<w:b/>" if n == 1 else ""}<w:sz w:val="19"/></w:rPr></w:style>' for n in (1, 2, 3))
    + '<w:style w:type="paragraph" w:customStyle="1" w:styleId="IndiceIlustraciones1"><w:name w:val="Índice de ilustraciones"/><w:basedOn w:val="Normal"/>'
      '<w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="8901"/></w:tabs><w:spacing w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>'
      '<w:rPr><w:sz w:val="19"/></w:rPr></w:style>')
sty = os.path.join(U, "word", "styles.xml")
s_ = open(sty).read()
if "LeyendaTabla" not in s_:
    open(sty, "w").write(s_.replace("</w:styles>", ESTILOS + "</w:styles>"))

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
print(f"cap1: {c1.tab} tablas, {c1.fig} figuras; cap2: {c2.tab}/{c2.fig}; cap3: {c3.tab}; cap6: {c6.tab} tablas, {c6.fig} figuras; cap4: {c4.tab} tablas; cap5: {c5.tab} tablas, {c5.fig} figuras; cap7: {c7.tab} tablas, {c7.fig} figuras; imágenes {len(RELS)}")
