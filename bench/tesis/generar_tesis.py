#!/usr/bin/env python3
"""Plan de tesis V4: toma la V3 y le aplica los capítulos de bench/tesis/contenido_*.py.

No toca el documento de origen. Reemplaza el capítulo IV y la sección 3.5, inserta las
figuras y tablas de los capítulos I a III, renumera tablas y figuras y regenera los índices
con las páginas que da LibreOffice (dos pasadas).

  python3 bench/tesis/generar_tesis.py ORIGEN.docx SALIDA.docx
"""
from __future__ import annotations

import copy
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from lxml import etree

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
PIC = "http://schemas.openxmlformats.org/drawingml/2006/picture"
NS = {"w": W}
q = lambda t: f"{{{W}}}{t}"

ANCHO_MAX_IN, ALTO_MAX_IN, DPI = 6.25, 7.3, 170
MONO = "Courier New"


# ── lenguaje de los capítulos ───────────────────────────────────────────────
TTULO4 = ('<w:style w:type="paragraph" w:styleId="Ttulo4"><w:name w:val="heading 4"/><w:basedOn w:val="Heading"/>'
           '<w:uiPriority w:val="9"/><w:unhideWhenUsed/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:after="120"/><w:outlineLvl w:val="3"/></w:pPr>'
           '<w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
           '<w:i/><w:iCs/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>')


def H2(t): return ("h", 2, t)
def H3(t): return ("h", 3, t)
def H4(t): return ("h", 4, t)
def P(t): return ("p", t)
def F(id_, titulo, nota=""): return ("f", id_, titulo, nota)
def T(id_, titulo, anchos, filas, nota=""): return ("t", id_, titulo, anchos, filas, nota)
def L(id_, titulo, codigo, nota=""): return ("l", id_, titulo, codigo.strip("\n"), nota)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Doc:
    def __init__(self, raiz: Path):
        self.raiz = raiz
        self.tree = etree.parse(str(raiz / "word/document.xml"))
        self.body = self.tree.getroot().find(q("body"))
        self.els = list(self.body)  # los índices de la V3 siguen valiendo aunque se inserte
        self.rels_path = raiz / "word/_rels/document.xml.rels"
        self.rels = etree.parse(str(self.rels_path))
        self.imgs: dict[str, str] = {}
        self.dp = 2000
        self.bm = 9000
        self.nsdecl = " ".join(f'xmlns:{k}="{v}"' for k, v in self.tree.getroot().nsmap.items() if k)

    def xml(self, s: str):
        return etree.fromstring(f"<root {self.nsdecl}>{s}</root>")[0]

    # runs con *cursiva*, ~subíndice~ y `{T:id}`/`{F:id}` (los números se ponen al final)
    def runs(self, texto: str, base: str = "") -> str:
        out = []
        for i, trozo in enumerate(re.split(r"((?<!\\)\*(?:[^*\\]|\\.)+?(?<!\\)\*|~[^~]+~)", texto)):
            if not trozo:
                continue
            extra = ""
            if trozo[0] == "*" and trozo[-1] == "*" and len(trozo) > 2:
                trozo, extra = trozo[1:-1], "<w:i/>"
            elif trozo[0] == "~" and trozo[-1] == "~" and len(trozo) > 2:
                trozo, extra = trozo[1:-1], '<w:vertAlign w:val="subscript"/>'
            trozo = trozo.replace("\\*", "*")
            orden = extra if extra == "<w:i/>" else ""
            sub = extra if extra != "<w:i/>" else ""
            out.append(f'<w:r><w:rPr>{orden}{base}{sub}<w:lang w:val="es-PE"/></w:rPr>'
                       f'<w:t xml:space="preserve">{esc(trozo)}</w:t></w:r>')
        return "".join(out)

    def p(self, texto: str, after=120, first=709):
        return self.xml(f'<w:p><w:pPr><w:spacing w:after="{after}" w:line="360" w:lineRule="auto"/>'
                        f'<w:ind w:firstLine="{first}"/><w:jc w:val="both"/></w:pPr>{self.runs(texto)}</w:p>')

    def heading(self, nivel: int, texto: str):
        return self.xml(f'<w:p><w:pPr><w:pStyle w:val="Ttulo{nivel}"/></w:pPr>'
                        f'<w:r><w:rPr><w:lang w:val="es-PE"/></w:rPr><w:t>{esc(texto)}</w:t></w:r></w:p>')

    def caption(self, tipo: str, id_: str, titulo: str):
        ph = "{%s:%s}" % (tipo[0], id_)
        return [self.xml(f'<w:p><w:pPr><w:keepNext/><w:spacing w:before="120"/></w:pPr><w:r><w:rPr><w:b/>'
                         f'<w:lang w:val="es-PE"/></w:rPr><w:t xml:space="preserve">CAP{ph}</w:t></w:r></w:p>'),
                self.xml(f'<w:p><w:pPr><w:keepNext/><w:spacing w:after="120"/></w:pPr>'
                         f'{self.runs(titulo, "")}</w:p>')]

    def titulo_cursiva(self, el):
        for r in el.findall(q("r")):
            rp = r.find(q("rPr"))
            i = rp.find(q("i"))
            if i is None:
                rp.insert(0, etree.SubElement(rp, q("i")))
            else:  # lo que en el título ya iba en cursiva queda en redonda
                rp.remove(i)

    def nota(self, texto: str):
        t = f"Nota. {texto} Fuente: elaboración propia." if texto else "Nota. Fuente: elaboración propia."
        return self.xml(f'<w:p><w:pPr><w:spacing w:before="80" w:after="140"/></w:pPr>'
                        f'<w:r><w:rPr><w:i/><w:color w:val="000000"/><w:sz w:val="18"/><w:lang w:val="es-PE"/></w:rPr>'
                        f'<w:t xml:space="preserve">{esc(t)}</w:t></w:r></w:p>')

    def imagen(self, nombre: str):
        png = AQUI / "fig/png" / f"{nombre}.png"
        d = png.read_bytes()[:32]
        w, h = struct.unpack(">II", d[16:24])
        wi, hi = w / DPI, h / DPI
        k = min(1.0, ANCHO_MAX_IN / wi, ALTO_MAX_IN / hi)
        cx, cy = int(wi * k * 914400), int(hi * k * 914400)
        if nombre not in self.imgs:
            rid = f"rIdTesis{len(self.imgs) + 1}"
            self.imgs[nombre] = rid
            shutil.copy(png, self.raiz / "word/media" / f"tesis_{nombre}.png")
            rel = etree.SubElement(self.rels.getroot(),
                                   "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship")
            rel.set("Id", rid)
            rel.set("Type", f"{R}/image")
            rel.set("Target", f"media/tesis_{nombre}.png")
        rid = self.imgs[nombre]
        self.dp += 1
        return self.xml(
            f'<w:p><w:pPr><w:keepNext/><w:spacing w:before="60" w:after="60"/><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            f'<wp:inline xmlns:wp="{WP}" distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
            f'<wp:docPr id="{self.dp}" name="Figura {self.dp}" descr="Figura de la tesis: {nombre}"/>'
            f'<a:graphic xmlns:a="{A}"><a:graphicData uri="{PIC}"><pic:pic xmlns:pic="{PIC}">'
            f'<pic:nvPicPr><pic:cNvPr id="{self.dp}" name="{nombre}.png"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}" xmlns:r="{R}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
            f'</wp:inline></w:drawing></w:r></w:p>')

    def tabla(self, anchos: list[int], filas: list[list[str]]):
        assert sum(anchos) == 9000, (sum(anchos), filas[0])
        fr = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
        def celda(txt, ancho, cab):
            sombra = '<w:shd w:val="clear" w:color="auto" w:fill="1F4E78"/>' if cab else ""
            base = f'{fr}<w:b/><w:color w:val="FFFFFF"/><w:sz w:val="18"/>' if cab else f'{fr}<w:color w:val="000000"/><w:sz w:val="18"/>'
            parrafos = "".join(
                f'<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>{self.runs_tabla(l, base)}</w:p>'
                for l in str(txt).split("\n"))
            return (f'<w:tc><w:tcPr><w:tcW w:w="{ancho}" w:type="dxa"/>{sombra}'
                    f'<w:tcMar><w:top w:w="60" w:type="dxa"/><w:left w:w="100" w:type="dxa"/>'
                    f'<w:bottom w:w="60" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar></w:tcPr>{parrafos}</w:tc>')
        rows = []
        for i, fila in enumerate(filas):
            assert len(fila) == len(anchos), fila
            pr = "<w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>" if i == 0 else "<w:trPr><w:cantSplit/></w:trPr>"
            rows.append(f"<w:tr>{pr}{''.join(celda(c, a, i == 0) for c, a in zip(fila, anchos))}</w:tr>")
        grid = "".join(f'<w:gridCol w:w="{a}"/>' for a in anchos)
        return self.xml(f'<w:tbl><w:tblPr><w:tblStyle w:val="Tablaconcuadrcula"/><w:tblW w:w="9000" w:type="dxa"/>'
                        f'<w:jc w:val="center"/><w:tblLayout w:type="fixed"/>'
                        f'<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
                        f'</w:tblPr><w:tblGrid>{grid}</w:tblGrid>{"".join(rows)}</w:tbl>')

    def runs_tabla(self, texto: str, base: str) -> str:
        out = []
        for trozo in re.split(r"((?<!\\)\*(?:[^*\\]|\\.)+?(?<!\\)\*)", texto):
            if not trozo:
                continue
            ital = trozo[0] == "*" and trozo[-1] == "*" and len(trozo) > 2
            t = (trozo[1:-1] if ital else trozo).replace("\\*", "*")
            b = base
            if ital:  # el orden del esquema: rFonts, b, i, color, sz
                b = base.replace('<w:color', '<w:i/><w:color', 1)
            out.append(f'<w:r><w:rPr>{b}<w:lang w:val="es-PE"/></w:rPr><w:t xml:space="preserve">{esc(t)}</w:t></w:r>')
        return "".join(out)

    def listado(self, codigo: str):
        lineas = codigo.split("\n")
        assert max(map(len, lineas)) <= 90, max(lineas, key=len)
        rp = (f'<w:rPr><w:rFonts w:ascii="{MONO}" w:hAnsi="{MONO}" w:cs="{MONO}"/><w:noProof/>'
              f'<w:color w:val="000000"/><w:sz w:val="16"/><w:lang w:val="en-US"/></w:rPr>')
        cuerpo = []
        for i, l in enumerate(lineas):
            if i:
                cuerpo.append(f"<w:r>{rp}<w:br/></w:r>")
            cuerpo.append(f'<w:r>{rp}<w:t xml:space="preserve">{esc(l)}</w:t></w:r>')
        borde = '<w:{0} w:val="single" w:sz="4" w:space="4" w:color="A6A6A6"/>'
        return self.xml(f'<w:p><w:pPr><w:keepNext/><w:keepLines/><w:pBdr>{"".join(borde.format(x) for x in ("top", "left", "bottom", "right"))}</w:pBdr>'
                        f'<w:shd w:val="clear" w:color="auto" w:fill="F5F5F5"/><w:spacing w:before="60" w:after="60" w:line="240" w:lineRule="auto"/></w:pPr>'
                        f'{"".join(cuerpo)}</w:p>')

    def bloque(self, items: list, after=120, first=709) -> list:
        sal = []
        for it in items:
            k = it[0]
            if k == "h":
                sal.append(self.heading(it[1], it[2]))
            elif k == "p":
                sal.append(self.p(it[1], after, first))
            else:
                tipo = "Tabla" if k == "t" else "Figura"
                cap = self.caption(tipo, it[1], it[2])
                self.titulo_cursiva(cap[1])
                sal += cap
                if k == "f":
                    sal += [self.imagen(it[1]), self.nota(it[3])]
                elif k == "t":
                    sal += [self.tabla(it[3], it[4]), self.nota(it[5])]
                else:
                    sal += [self.listado(it[3]), self.nota(it[4])]
        return sal

    def tras(self, i: int, items: list, after=200, first=720):
        ancla = self.els[i]
        for e in reversed(self.bloque(items, after, first)):
            ancla.addnext(e)

    def quitar(self, desde: int, hasta: int, conservar=()):
        for i in range(desde, hasta + 1):
            if i in conservar:
                continue
            e = self.els[i]
            comentado = e.xpath(".//w:commentReference", namespaces=NS)
            assert not comentado, f"el elemento {i} tiene un comentario"
            self.body.remove(e)

    def cambiar(self, i: int, viejo: str, nuevo: str, celda=None):
        """Cambia un trozo de texto aunque cruce runs; respeta el formato del primer run."""
        raiz = self.els[i]
        hechos = 0
        for p in raiz.iter(q("p")):
            ts = list(p.iter(q("t")))
            texto = "".join(t.text or "" for t in ts)
            if viejo not in texto:
                continue
            ini = texto.index(viejo)
            fin = ini + len(viejo)
            pos = 0
            primero = True
            for t in ts:
                largo = len(t.text or "")
                a, b = max(ini, pos), min(fin, pos + largo)
                if a < b:
                    s = t.text
                    t.text = s[:a - pos] + (nuevo if primero else "") + s[b - pos:]
                    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                    primero = False
                pos += largo
            hechos += 1
        assert hechos, f"[{i}] no aparece: {viejo!r}"


# ── numeración e índices ────────────────────────────────────────────────────
def es_cap_vieja(p) -> str | None:
    t = "".join(x.text or "" for x in p.iter(q("t")))
    m = re.fullmatch(r"(Tabla|Figura) (\d+)", t)
    if m and p.find(f"{q('pPr')}/{q('keepNext')}") is not None:
        return t
    return None


def numerar(doc: Doc) -> list[dict]:
    """Numera por orden de aparición y reemplaza las marcas {T:id}/{F:id}."""
    n = {"T": 0, "F": 0}
    mapa: dict[str, str] = {}
    items = []
    hijos = list(doc.body)
    for i, e in enumerate(hijos):
        if e.tag != q("p"):
            continue
        ts = list(e.iter(q("t")))
        t = "".join(x.text or "" for x in ts)
        m = re.fullmatch(r"CAP\{([TF]):([\w-]+)\}", t)
        if not m:
            continue
        tipo, id_ = m.groups()
        n[tipo] += 1
        rotulo = f"{'Tabla' if tipo == 'T' else 'Figura'} {n[tipo]}"
        mapa[f"{{{tipo}:{id_}}}"] = rotulo
        ts[0].text = rotulo
        titulo = "".join(x.text or "" for x in hijos[i + 1].iter(q("t")))
        items.append({"tipo": tipo, "rotulo": rotulo, "titulo": titulo, "el": e})
    for t in doc.body.iter(q("t")):
        if t.text and "{" in t.text:
            t.text = re.sub(r"\{[TF]:[\w-]+\}", lambda m: mapa[m.group(0)], t.text)
            assert not re.search(r"\{[TF]:", t.text), t.text
    return items


def marcar(doc: Doc, el, nombre: str):
    doc.bm += 1
    s = etree.Element(q("bookmarkStart"))
    s.set(q("id"), str(doc.bm))
    s.set(q("name"), nombre)
    f = etree.Element(q("bookmarkEnd"))
    f.set(q("id"), str(doc.bm))
    ppr = el.find(q("pPr"))
    el.insert(1 if ppr is not None else 0, s)
    el.append(f)


def entrada(doc: Doc, estilo: str, ancla: str, texto: str, pagina: int, abre=False):
    prefijo = ('<w:r><w:fldChar w:fldCharType="begin"/><w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText>'
               '<w:fldChar w:fldCharType="separate"/></w:r>') if abre else ""
    return doc.xml(
        f'<w:p><w:pPr><w:pStyle w:val="{estilo}"/><w:rPr><w:noProof/></w:rPr></w:pPr>{prefijo}'
        f'<w:hyperlink w:anchor="{ancla}" w:history="1"><w:r><w:rPr><w:noProof/></w:rPr><w:t xml:space="preserve">{esc(texto)}</w:t></w:r>'
        f'<w:r><w:rPr><w:noProof/><w:webHidden/></w:rPr><w:tab/><w:fldChar w:fldCharType="begin"/>'
        f'<w:instrText xml:space="preserve"> PAGEREF {ancla} \\h </w:instrText><w:fldChar w:fldCharType="separate"/>'
        f'<w:t>{pagina}</w:t><w:fldChar w:fldCharType="end"/></w:r></w:hyperlink></w:p>')


def entrada_rotulo(doc: Doc, ancla: str, texto: str, pagina: int):
    """Índices de tablas y figuras: sin hipervínculo, porque LibreOffice los descarta fuera de un TOC."""
    return doc.xml(
        f'<w:p><w:pPr><w:pStyle w:val="TDC2"/><w:rPr><w:noProof/></w:rPr></w:pPr>'
        f'<w:r><w:rPr><w:noProof/></w:rPr><w:t xml:space="preserve">{esc(texto)}</w:t></w:r>'
        f'<w:r><w:rPr><w:noProof/></w:rPr><w:tab/><w:fldChar w:fldCharType="begin"/></w:r>'
        f'<w:r><w:rPr><w:noProof/></w:rPr><w:instrText xml:space="preserve"> PAGEREF {ancla} </w:instrText></w:r>'
        f'<w:r><w:rPr><w:noProof/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
        f'<w:r><w:rPr><w:noProof/></w:rPr><w:t>{pagina}</w:t></w:r>'
        f'<w:r><w:rPr><w:noProof/></w:rPr><w:fldChar w:fldCharType="end"/></w:r></w:p>')


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def paginas(raiz_docx: Path, tmp: Path) -> list[str]:
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(raiz_docx)],
                   check=True, capture_output=True, timeout=300)
    pdf = tmp / (raiz_docx.stem + ".pdf")
    out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], check=True, capture_output=True, text=True).stdout
    return out.split("\f")


def localizar(lista: list[dict], pags: list[str]) -> None:
    lineas = [[norm(l) for l in p.splitlines()] for p in pags]
    planos = [norm(p) for p in pags]
    # la primera aparición del capítulo I como línea exacta queda después de los índices
    i = next(k for k, ls in enumerate(lineas) if lista[0]["texto"] in ls)
    for it in lista:
        hallado = None
        for k in range(i, len(pags)):
            if it["exacta"] or " " not in it["texto"]:
                if it["texto"] in lineas[k]:
                    hallado = k
                    break
            elif it["texto"] in planos[k]:
                hallado = k
                break
        assert hallado is not None, it["texto"]
        it["pagina"] = hallado + 1
        i = hallado


def construir(origen: Path, salida: Path, pagina_de: dict[str, int] | None) -> tuple[dict, list[str]]:
    import contenido_cap1a3 as c1
    import contenido_cap4 as c4
    with tempfile.TemporaryDirectory() as td:
        raiz = Path(td) / "u"
        with zipfile.ZipFile(origen) as z:
            z.extractall(raiz)
        # cuarto nivel: subsecciones del capítulo IV, que no van a los índices
        estilos = raiz / "word/styles.xml"
        estilos.write_text(estilos.read_text(encoding="utf8").replace("</w:styles>", TTULO4 + "</w:styles>"), encoding="utf8")
        doc = Doc(raiz)
        c1.aplicar(doc, P, H2, H3, H4, F, T, L)
        # capítulo IV: del 360 al 481 (el título 359 se queda)
        c4_items = c4.capitulo(P, H2, H3, H4, F, T, L)
        doc.quitar(360, 481)
        ancla = doc.els[359]
        for e in reversed(doc.bloque(c4_items)):
            ancla.addnext(e)
        c1.temario(doc, c4_items)
        items = numerar(doc)

        # índices
        hijos = list(doc.body)
        entradas = []
        n = 0
        for e in hijos:
            if e.tag != q("p"):
                continue
            st = e.find(f"{q('pPr')}/{q('pStyle')}")
            nivel = {"Ttulo1": 1, "Ttulo2": 2, "Ttulo3": 3}.get(st.get(q("val")) if st is not None else "")
            if nivel:
                n += 1
                texto = "".join(x.text or "" for x in e.iter(q("t")))
                nombre = f"_TocV4{n:04d}"
                for b in e.findall(q("bookmarkStart")) + e.findall(q("bookmarkEnd")):
                    e.remove(b)
                marcar(doc, e, nombre)
                entradas.append({"clave": nombre, "texto": norm(texto), "nivel": nivel, "exacta": False})
        cap_items = []
        for it in items:
            n += 1
            nombre = f"_CapV4{n:04d}"
            marcar(doc, it["el"], nombre)
            cap_items.append({"clave": nombre, "texto": it["rotulo"], "titulo": it["titulo"], "tipo": it["tipo"], "exacta": True})

        pg = pagina_de or {}
        sdt = doc.els[17]
        cont = sdt.find(q("sdtContent"))
        viejos = list(cont)
        for e in viejos[1:-1]:
            cont.remove(e)
        fin = viejos[-1]
        for k, en in enumerate(entradas):
            fin.addprevious(entrada(doc, f"TDC{en['nivel']}", en["clave"], en["texto"], pg.get(en["clave"], 0), abre=k == 0))
        titulo_indice = doc.els[16]
        titulo_indice.find(q("pPr")).append(etree.Element(q("pageBreakBefore")))
        tras = sdt
        for tipo, nombre in (("T", "ÍNDICE DE TABLAS"), ("F", "ÍNDICE DE FIGURAS")):
            cab = copy.deepcopy(titulo_indice)
            ts = list(cab.iter(q("t")))
            ts[0].text = nombre
            for t in ts[1:]:
                t.text = ""
            for b in cab.xpath(".//w:bookmarkStart|.//w:bookmarkEnd", namespaces=NS):
                b.getparent().remove(b)
            tras.addnext(cab)
            tras = cab
            for it in (c for c in cap_items if c["tipo"] == tipo):
                e = entrada_rotulo(doc, it["clave"], f"{it['texto']}. {it['titulo']}", pg.get(it["clave"], 0))
                tras.addnext(e)
                tras = e

        doc.tree.write(str(raiz / "word/document.xml"), xml_declaration=True, encoding="UTF-8", standalone=True)
        doc.rels.write(str(doc.rels_path), xml_declaration=True, encoding="UTF-8", standalone=True)
        if salida.exists():
            salida.unlink()
        with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(raiz / "[Content_Types].xml", "[Content_Types].xml")
            for f in sorted(raiz.rglob("*")):
                if f.is_file() and f.name != "[Content_Types].xml":
                    z.write(f, f.relative_to(raiz).as_posix())
        return {"entradas": entradas, "caps": cap_items}, []


def main() -> int:
    origen, salida = Path(sys.argv[1]), Path(sys.argv[2])
    assert origen.resolve() != salida.resolve(), "el origen no se toca"
    pagina_de = None
    previo = None
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for vuelta in range(4):
            info, _ = construir(origen, salida, pagina_de)
            lista = info["entradas"] + info["caps"]
            lista_ord = list(info["entradas"])
            pags = paginas(salida, tmp)
            localizar_con_orden(info, pags)
            pagina_de = {x["clave"]: x["pagina"] for x in lista}
            if pagina_de == previo:
                break
            previo = dict(pagina_de)
        print(f"{vuelta + 1} pasadas, {len(pags) - 1} páginas")
        for e in info["entradas"]:
            if e["nivel"] == 1:
                print(f"  p. {e['pagina']:>3}  {e['texto']}")
        print(f"  {sum(c['tipo'] == 'T' for c in info['caps'])} tablas, {sum(c['tipo'] == 'F' for c in info['caps'])} figuras")
    return 0


def localizar_con_orden(info: dict, pags: list[str]) -> None:
    """Títulos y rótulos se buscan por separado: cada lista está en orden del documento."""
    localizar(info["entradas"], pags)
    i0 = info["entradas"][0]["pagina"] - 1
    lineas = [[norm(l) for l in p.splitlines()] for p in pags]
    for tipo in "TF":
        k = i0
        for c in (x for x in info["caps"] if x["tipo"] == tipo):
            while c["texto"] not in lineas[k]:
                k += 1
            c["pagina"] = k + 1


if __name__ == "__main__":
    sys.exit(main())
