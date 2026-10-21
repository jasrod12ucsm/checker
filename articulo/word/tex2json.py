"""Convierte articulo.tex en bloques JSON para armar el Word con docx-js."""
import json, re, sys

src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
body = s[s.index(r'\maketitle') + len(r'\maketitle'):s.index(r'\end{document}')]

URLS = {}
m = re.search(r'\\urldef\{\\(\w+)\}\\url\{(.*?)\}\n', s)
if m:
    URLS[m.group(1)] = m.group(2)

cites = re.findall(r'\\bibitem\{(\w+)\}', s)
CITE = {k: i + 1 for i, k in enumerate(cites)}
eqlabels = re.findall(r'\\begin\{equation\}.*?\\label\{(.*?)\}', s, re.S)
REF = {k: str(i + 1) for i, k in enumerate(eqlabels)}
REF['fig:modelo'] = '1'

MATH = {r'\gamma': 'γ', r'\kappa': 'κ', r'\geq': '≥', r'\in': '∈', r'\sqcup': '⊔',
        r'\sqsubseteq': '⊑', r'\leftarrow': '←', r'\{': '{', r'\}': '}', '{}': ''}


def run(text, **f):
    return dict(text=text, **{k: v for k, v in f.items() if v})


def math_runs(m, fmt):
    """Matemática en línea: letras latinas y griegas en cursiva, lo demás recto."""
    res = []
    i = 0
    while i < len(m):
        if m.startswith(r'\textsc{', i):
            j = match_brace(m, i + 7)
            res.append(run(m[i + 8:j], sc=True, **fmt))
            i = j + 1
            continue
        if m.startswith(r'\boldsymbol{', i):
            j = match_brace(m, i + 11)
            inner = m[i + 12:j].replace('_1', '₁')
            res.append(run(inner, i=True, b=True, **{k: v for k, v in fmt.items() if k != 'b'}))
            i = j + 1
            continue
        hit = next((k for k in MATH if m.startswith(k, i)), None)
        if hit:
            ch = MATH[hit]
            if ch:
                res.append(run(ch, i=ch in 'γκ', **fmt))
            i += len(hit)
            continue
        c = m[i]
        if c == ' ':
            i += 1
            continue
        if c.isalpha():
            res.append(run(c, i=True, **fmt))
        elif c in '=≥∈':
            res.append(run(c, **fmt))
        else:
            res.append(run(c, **fmt))
        i += 1
    # espacios alrededor de relaciones, como en la composición matemática
    out = []
    for r in res:
        if r['text'] in ('=', '∈', '≥', '⊔', '⊑', '←') :
            r = dict(r, text=f' {r["text"]} ')
        out.append(r)
    return out


def match_brace(t, i):
    assert t[i] == '{', t[i:i + 30]
    d = 0
    for j in range(i, len(t)):
        if t[j] == '{':
            d += 1
        elif t[j] == '}':
            d -= 1
            if d == 0:
                return j
    raise ValueError(t[i:i + 40])


def plain(t):
    t = t.replace('---', '—').replace('--', '–').replace('``', '“').replace("''", '”')
    t = t.replace('~', '\u00a0').replace(r'\_', '_').replace(r'\&', '&').replace(r'\%', '%')
    t = t.replace('C++', 'C\u2060+\u2060+')  # que no se corte en «C+ +»
    t = t.replace(r'\"{u}', 'ü').replace(r'\,', '\u202f').replace(r'\ ', ' ')
    return t


def inline(t, fmt=None):
    """Texto LaTeX en línea a lista de runs."""
    fmt = dict(fmt or {})
    res, buf, i = [], '', 0

    def flush():
        nonlocal buf
        if buf:
            res.append(run(plain(buf), **fmt))
            buf = ''
    while i < len(t):
        c = t[i]
        if c == '$':
            j = t.index('$', i + 1)
            flush()
            res += math_runs(t[i + 1:j], fmt)
            i = j + 1
            continue
        if c == '\\':
            acc = re.match(r'\\(["\'])\{?([A-Za-z])\}?', t[i:])
            if acc:  # acentos de LaTeX: \"{u}, \'A
                import unicodedata
                mark = {'"': '\u0308', "'": '\u0301'}[acc.group(1)]
                buf += unicodedata.normalize('NFC', acc.group(2) + mark)
                i += acc.end()
                continue
            m = re.match(r'\\([a-zA-Z]+)', t[i:])
            if not m:
                buf += t[i:i + 2]
                i += 2
                continue
            cmd = m.group(1)
            k = i + len(cmd) + 1
            styles = {'code': 'code', 'texttt': 'code', 'textit': 'i', 'textbf': 'b', 'textsc': 'sc', 'mathit': 'i'}
            if cmd in styles:
                j = match_brace(t, k)
                flush()
                res += inline(t[k + 1:j], {**fmt, styles[cmd]: True})
                i = j + 1
                continue
            if cmd == 'cite':
                j = match_brace(t, k)
                buf += '[' + str(CITE[t[k + 1:j]]) + ']'
                i = j + 1
                continue
            if cmd == 'ref':
                j = match_brace(t, k)
                buf += REF[t[k + 1:j]]
                i = j + 1
                continue
            if cmd == 'url':
                j = match_brace(t, k)
                flush()
                res.append(run(t[k + 1:j].replace(r'\%', '%'), url=True, **fmt))
                i = j + 1
                continue
            if cmd in URLS:
                flush()
                res.append(run(URLS[cmd], url=True, **fmt))
                i = k
                continue
            if cmd in ('footnotesize', 'scriptsize', 'centering', 'IEEEtriggeratref'):
                i = k
                if cmd == 'IEEEtriggeratref':
                    i = match_brace(t, k) + 1
                continue
            raise ValueError('comando no soportado: ' + cmd + ' en ' + t[i:i + 60])
        if c in '{}':
            i += 1
            continue
        if c == '\n':
            buf += ' '
            i += 1
            continue
        buf += c
        i += 1
    flush()
    # unir runs consecutivos con el mismo formato
    merged = []
    for r in res:
        if merged and {k: v for k, v in merged[-1].items() if k != 'text'} == {k: v for k, v in r.items() if k != 'text'}:
            merged[-1]['text'] += r['text']
        else:
            merged.append(r)
    return merged


def table(env, wide):
    cap = re.search(r'\\caption\{(.*?)\}\n', env).group(1)
    label = re.search(r'\\label\{(.*?)\}', env).group(1)
    tab = env[env.index(r'\begin{tabular}'):env.index(r'\end{tabular}')]
    tab = tab[tab.index('\n') + 1:]
    note = None
    if r'\multicolumn' in tab:
        k = tab.index(r'\multicolumn')
        j = match_brace(tab, k + 12)
        j = match_brace(tab, j + 1)
        e = match_brace(tab, j + 1)
        note = inline(tab[j + 2:e])
        tab = tab[:k]
    groups, cur = [], []
    for line in tab.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line == r'\hline':
            if cur:
                groups.append(cur)
                cur = []
            continue
        cells = [inline(c.strip()) for c in line.rstrip('\\').split('&')]
        cur.append(cells)
    if cur:
        groups.append(cur)
    return dict(t='table', label=label, caption=inline(cap), header=groups[0], groups=groups[1:], note=note,
                wide=wide)


blocks = []
abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', body, re.S)
keywords = re.search(r'\\begin\{IEEEkeywords\}(.*?)\\end\{IEEEkeywords\}', body, re.S)
rest = body
if abstract:  # la versión corta no tiene resumen ni palabras clave
    blocks.append(dict(t='abstract', runs=inline(abstract.group(1).strip())))
    blocks.append(dict(t='keywords', runs=inline(keywords.group(1).strip())))
    rest = body[keywords.end():]

ENV = re.compile(r'\\begin\{(equation|itemize|figure\*|table\*?|thebibliography)\}(.*?)\\end\{\1\}', re.S)
pos = 0
chunks = []
for m in ENV.finditer(rest):
    chunks.append(('text', rest[pos:m.start()]))
    chunks.append((m.group(1), m.group(2)))
    pos = m.end()
chunks.append(('text', rest[pos:]))

for kind, c in chunks:
    if kind == 'text':
        for para in re.split(r'\n\s*\n', c):
            para = para.strip()
            if not para:
                continue
            for line in para.split('\n'):
                pass
            m = re.match(r'\\(section|subsection|subsubsection)\{(.*?)\}\s*(.*)', para, re.S)
            if m:
                lvl = {'section': 'h1', 'subsection': 'h2', 'subsubsection': 'h3'}[m.group(1)]
                blocks.append(dict(t=lvl, text=plain(m.group(2))))
                para = m.group(3).strip()
                if not para:
                    continue
            if para.startswith(r'\IEEEtriggeratref'):
                continue
            blocks.append(dict(t='p', runs=inline(para)))
    elif kind == 'equation':
        label = re.search(r'\\label\{(.*?)\}', c).group(1)
        blocks.append(dict(t='eq', n=REF[label]))
    elif kind == 'itemize':
        items = [x.strip() for x in c.split(r'\item') if x.strip()]
        blocks.append(dict(t='list', items=[inline(x) for x in items]))
    elif kind == 'figure*':
        cap = c[c.index(r'\caption{') + 8:]
        cap = cap[1:match_brace(cap, 0)]
        blocks.append(dict(t='fig', caption=inline(cap)))
    elif kind.startswith('table'):
        blocks.append(table(c, kind == 'table*'))
    elif kind == 'thebibliography':
        items = re.findall(r'\\bibitem\{(\w+)\}\s*(.*?)(?=\\bibitem|\Z)', c, re.S)
        blocks.append(dict(t='refs', items=[dict(key=k, runs=inline(v.strip())) for k, v in items]))

title = re.search(r'\\title\{(.*?)\}', s).group(1)
json.dump(dict(title=plain(title), blocks=blocks, cites=cites), open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(blocks), 'bloques')
