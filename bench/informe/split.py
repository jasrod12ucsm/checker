import re
def split(xml):
    b0=xml.index('<w:body>')+len('<w:body>'); b1=xml.rindex('</w:body>')
    body=xml[b0:b1]; parts=[]; depth=0; start=None
    for m in re.finditer(r'<(/?)([\w:]+)[^>]*?(/?)>', body):
        close,name,selfc=m.group(1),m.group(2),m.group(3)
        if depth==0 and not close:
            start=m.start()
            if selfc: parts.append(body[start:m.end()]); continue
            depth=1; continue
        if close: depth-=1
        elif not selfc: depth+=1
        if depth==0: parts.append(body[start:m.end()])
    return xml[:b0], parts, xml[b1:]
def text(p): return ''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>',p))
def style(p):
    m=re.search(r'<w:pStyle w:val="([^"]+)"',p[:600]); return m.group(1) if m else ''
