// Arma el Word del artículo en formato de congreso IEEE (carta, dos columnas).
// Uso: ver generar.sh (node build.js art.json figuras_dir salida.docx)
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, WidthType,
  AlignmentType, BorderStyle, TabStopType, HeadingLevel, SectionType, LevelFormat, VerticalAlign,
} = require('docx');

const [, , jsonPath, figDir, outPath] = process.argv;
const art = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));

const FONT = 'Times New Roman';
const MONO = 'Courier New';
const PAGE = { width: 12240, height: 15840 };
const MARGIN = { top: 1080, bottom: 1440, left: 900, right: 900 };
const FULL = PAGE.width - MARGIN.left - MARGIN.right; // 10440
const GAP = 360;
const COL = (FULL - GAP) / 2; // 5040 = 3.5 in
const INDENT = 202; // 0.14 in

function runs(rs, base = {}) {
  return rs.map((r) => new TextRun({
    text: r.text,
    italics: !!(r.i || base.i),
    bold: !!(r.b || base.b),
    smallCaps: !!r.sc,
    font: r.code ? MONO : FONT,
    size: r.code ? (base.size || 20) - 2 : base.size,
  }));
}

function roman(n) {
  return ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'][n];
}

function png(file) {
  const buf = fs.readFileSync(file);
  return { buf, w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}

function image(file, dpi = 600) {
  const p = png(file);
  return new ImageRun({
    type: 'png', data: p.buf,
    transformation: { width: Math.round(p.w / dpi * 96), height: Math.round(p.h / dpi * 96) },
  });
}

const line = { style: BorderStyle.SINGLE, size: 6, color: '000000' };
const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };

function table(b) {
  const ncol = b.header[0].length;
  let widths;
  if (b.wide) {
    const w = [3.5, 2.8, 2.6, 3.0, 4.4];
    const t = w.reduce((a, x) => a + x, 0);
    widths = w.map((x) => Math.floor(FULL * x / t));
    widths[widths.length - 1] += FULL - widths.reduce((a, x) => a + x, 0);
  } else {
    widths = ncol === 8 ? [1560, 440, 400, 440, 420, 420, 420, 940] : [2640, 800, 800, 800];
    widths[0] += COL - widths.reduce((a, x) => a + x, 0);
  }
  const total = widths.reduce((a, x) => a + x, 0);
  const rows = [];
  const all = [{ rows: b.header, head: true }, ...b.groups.map((g) => ({ rows: g }))];
  all.forEach((g, gi) => {
    g.rows.forEach((cells, ri) => {
      const first = gi === 0 && ri === 0;
      const last = ri === g.rows.length - 1;
      rows.push(new TableRow({
        tableHeader: !!g.head,
        children: cells.map((c, ci) => new TableCell({
          width: { size: widths[ci], type: WidthType.DXA },
          verticalAlign: VerticalAlign.TOP,
          margins: { top: 20, bottom: 20, left: ci === 0 ? 0 : 60, right: 60 },
          borders: { top: first ? line : none, bottom: last ? line : none, left: none, right: none },
          children: [new Paragraph({
            alignment: !b.wide && ci > 0 ? AlignmentType.RIGHT : AlignmentType.LEFT,
            children: runs(c, { size: 16 }),
          })],
        })),
      }));
    });
  });
  const out = [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 160 }, keepNext: true,
      children: [new TextRun({ text: `TABLA ${roman(b.num)}`, size: 16, font: FONT })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, keepNext: true,
      children: runs(b.caption, { size: 16 }).map((r) => r) }),
    new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: widths, alignment: AlignmentType.CENTER, rows }),
  ];
  // El título de la tabla va en versalitas, como en la clase IEEEtran.
  out[1] = new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, keepNext: true,
    children: b.caption.map((r) => new TextRun({ text: r.text, smallCaps: true, size: 16, font: r.code ? MONO : FONT })) });
  if (b.note) {
    out.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { before: 40 }, children: runs(b.note, { size: 14 }) }));
  }
  out.push(new Paragraph({ spacing: { after: 80 }, children: [] }));
  return out;
}

// Contenido agrupado en secciones de 1 o 2 columnas.
const sections = [];
let cur = null;
function section(cols) {
  cur = { cols, children: [] };
  sections.push(cur);
}
const add = (...ps) => cur.children.push(...ps);

section(1);
add(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 },
  children: [new TextRun({ text: art.title, size: 48, font: FONT })] }));
const AUTORES = [
  'Jason Sebastián Rodríguez Chávez',
  'Mayerly Katrina Aranibar Zegovia',
];
const autorCelda = (n) => new TableCell({
  width: { size: FULL / 2, type: WidthType.DXA },
  borders: { top: none, bottom: none, left: none, right: none },
  children: [
    new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: n, size: 22, font: FONT })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: 'Escuela Profesional de Ingeniería de Sistemas', italics: true, size: 20, font: FONT })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: 'Universidad Católica de Santa María', italics: true, size: 20, font: FONT })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: 'Arequipa, Perú', size: 20, font: FONT })] }),
  ],
});
add(new Table({ width: { size: FULL, type: WidthType.DXA }, columnWidths: [FULL / 2, FULL / 2],
  rows: [new TableRow({ children: AUTORES.map(autorCelda) })] }));
add(new Paragraph({ spacing: { after: 320 }, children: [] }));
section(2);

let h1 = 0; let h2 = 0; let h3 = 0; let tnum = 0;
let prev = null;
let pendingRunIn = null;
// La figura del modelo va justo antes de «Modelo de invalidación», que la cita:
// así la página anterior se llena con texto y la figura queda arriba de la siguiente.
const blocks = art.blocks.slice();
{
  const fi = blocks.findIndex((x) => x.t === 'fig');
  const [fig] = blocks.splice(fi, 1);
  const hi = blocks.findIndex((x) => x.t === 'h3' && x.text === 'Modelo de invalidación');
  blocks.splice(hi, 0, fig);
}
for (let bi = 0; bi < blocks.length; bi++) {
  const b = blocks[bi];
  if (b.t === 'abstract') {
    add(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 120 }, children: [
      new TextRun({ text: 'Resumen', bold: true, italics: true, size: 18, font: FONT }),
      new TextRun({ text: '—', bold: true, size: 18, font: FONT }),
      ...runs(b.runs, { b: true, size: 18 })] }));
  } else if (b.t === 'keywords') {
    add(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 120 }, children: [
      new TextRun({ text: 'Palabras clave', bold: true, italics: true, size: 18, font: FONT }),
      new TextRun({ text: '—', bold: true, size: 18, font: FONT }),
      ...runs(b.runs, { b: true, size: 18 })] }));
  } else if (b.t === 'h1') {
    h1++; h2 = 0; h3 = 0;
    add(new Paragraph({ heading: HeadingLevel.HEADING_1, alignment: AlignmentType.CENTER, keepNext: true,
      spacing: { before: 160, after: 80 },
      children: [new TextRun({ text: `${roman(h1)}. ${b.text}`, smallCaps: true, size: 20, font: FONT, color: '000000' })] }));
  } else if (b.t === 'h2') {
    h2++; h3 = 0;
    add(new Paragraph({ heading: HeadingLevel.HEADING_2, keepNext: true, spacing: { before: 120, after: 60 },
      children: [new TextRun({ text: `${String.fromCharCode(64 + h2)}. ${b.text}`, italics: true, size: 20, font: FONT, color: '000000' })] }));
  } else if (b.t === 'h3') {
    h3++;
    pendingRunIn = new TextRun({ text: `${h3}) ${b.text}: `, italics: true, size: 20, font: FONT });
  } else if (b.t === 'p') {
    const children = runs(b.runs, { size: 20 });
    if (pendingRunIn) { children.unshift(pendingRunIn); pendingRunIn = null; }
    add(new Paragraph({ alignment: AlignmentType.JUSTIFIED,
      indent: { firstLine: prev && prev.t === 'eq' ? 0 : INDENT }, children }));
  } else if (b.t === 'list') {
    for (const it of b.items) {
      add(new Paragraph({ alignment: AlignmentType.JUSTIFIED, numbering: { reference: 'vinetas', level: 0 },
        children: runs(it, { size: 20 }) }));
    }
  } else if (b.t === 'eq') {
    add(new Paragraph({ spacing: { before: 80, after: 80 },
      tabStops: [{ type: TabStopType.CENTER, position: COL / 2 }, { type: TabStopType.RIGHT, position: COL }],
      children: [new TextRun({ text: '\t', size: 20 }), image(path.join(figDir, `eq${b.n}.png`)),
        new TextRun({ text: `\t(${b.n})`, size: 20, font: FONT })] }));
  } else if (b.t === 'fig') {
    section(1);
    add(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 80 }, keepNext: true,
      children: [image(path.join(figDir, 'fig.png'))] }));
    add(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 160 },
      children: [new TextRun({ text: 'Fig. 1. ', size: 16, font: FONT }), ...runs(b.caption, { size: 16 })] }));
    section(2);
  } else if (b.t === 'table') {
    tnum++;
    b.num = tnum;
    if (b.wide) {
      section(1);
      add(...table(b));
      section(2);
    } else {
      add(...table(b));
    }
  } else if (b.t === 'refs') {
    add(new Paragraph({ heading: HeadingLevel.HEADING_1, alignment: AlignmentType.CENTER, keepNext: true,
      spacing: { before: 160, after: 80 },
      children: [new TextRun({ text: 'Referencias', smallCaps: true, size: 20, font: FONT, color: '000000' })] }));
    b.items.forEach((it, i) => {
      add(new Paragraph({ alignment: AlignmentType.LEFT, indent: { left: 360, hanging: 360 },
        spacing: { after: 20 }, tabStops: [{ type: TabStopType.LEFT, position: 360 }],
        children: [new TextRun({ text: `[${i + 1}]\t`, size: 16, font: FONT }), ...runs(it.runs, { size: 16 })] }));
    });
  }
  prev = b;
}

// Sección final vacía de una columna: Word equilibra las dos columnas de la última página.
section(1);
add(new Paragraph({ children: [] }));

const doc = new Document({
  creator: 'Jason Sebastián Rodríguez Chávez; Mayerly Katrina Aranibar Zegovia',
  title: art.title,
  features: { updateFields: false },
  styles: {
    default: { document: { run: { font: FONT, size: 20, language: { value: 'es-PE' } } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 20, font: FONT, color: '000000' }, paragraph: { outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 20, font: FONT, italics: true, color: '000000' }, paragraph: { outlineLevel: 1 } },
    ],
  },
  numbering: { config: [{ reference: 'vinetas', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•',
    alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 200 } } } }] }] },
  sections: sections.filter((s) => s.children.length).map((s, i) => ({
    properties: {
      type: i === 0 ? undefined : SectionType.CONTINUOUS,
      page: { size: PAGE, margin: MARGIN },
      column: s.cols === 2 ? { count: 2, space: GAP, equalWidth: true } : { count: 1 },
    },
    children: s.children,
  })),
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(outPath, buf);
  console.log('escrito', outPath);
});
