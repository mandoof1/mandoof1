#!/usr/bin/env python3
"""Original profile artwork, in two themes and responsive sizes. No dependencies."""
from html import escape
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
SANS = 'Arial, Helvetica, sans-serif'
MONO = "'Courier New', monospace"
THEMES = {
    'dark': dict(bg='#111315', panel='#191c1f', fg='#f5f2ea', dim='#b1b2ae', line='#34383b', accent='#ffb454', violet='#b8a1ff', green='#98cdb5'),
    'light': dict(bg='#f5f2ea', panel='#eae7df', fg='#202321', dim='#5d625e', line='#cecfc6', accent='#9c4b0a', violet='#694eaa', green='#276853'),
}
# Kept as the shared palette for the optional, standalone statistics renderer.
BG, BORDER, WHITE, MUTED = (THEMES['dark'][key] for key in ('bg','line','fg','dim'))
LIME, CYAN = THEMES['dark']['accent'], THEMES['dark']['violet']


def text(x,y,value,size=20,color=WHITE,weight=400,mono=False,**attrs):
    extra=' '.join(f'{key.replace("_","-")}="{escape(str(value),quote=True)}"' for key,value in attrs.items())
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{MONO if mono else SANS}" font-size="{size}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def svg(width,height,title,description,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>\n{body}\n</svg>\n'


def save(name,w,h,title,description,items):
    (OUT/name).write_text(svg(w,h,title,description,'\n'.join(items)),encoding='utf-8')


def rect(x,y,w,h,fill,stroke='none',rx=0,**attrs):
    extra=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" {extra}/>'


def line(x1,y1,x2,y2,color,width=1,**attrs):
    extra=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" {extra}/>'


def arrow(x,y,color,scale=1):
    return f'<path transform="translate({x} {y}) scale({scale})" d="M0 0 H26 M17 -9 L26 0 L17 9" fill="none" stroke="{color}" stroke-width="2"/>'


def canvas(w,h,c):
    return [rect(0,0,w,h,c['bg'],rx=16),rect(1,1,w-2,h-2,'none',c['line'],16)]


def label(x,y,value,c,color=None,size=15):
    return text(x,y,value,size,color or c['dim'],mono=True,letter_spacing='1.3')


def field(cx,cy,r,c):
    """A deterministic toroidal field, drawn as curves rather than a bitmap."""
    parts=[]
    for i in range(32):
        phase=i*math.pi/16
        points=[]
        for j in range(121):
            t=j*2*math.pi/120
            radial=r*(.58+.32*math.cos(t))
            x=radial*math.cos(phase)
            z=radial*math.sin(phase)
            y=r*.50*math.sin(t)
            # Tilt the field to give the linework depth.
            px=cx+x*.88-z*.25
            py=cy+y*.84+z*.44+x*.12
            points.append(f'{px:.2f},{py:.2f}')
        parts.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{c["accent"]}" stroke-width="1.15" opacity=".6"/>')
    return '\n'.join(parts)


def hero(theme,mobile=False):
    c=THEMES[theme];w,h=(640,690) if mobile else (1200,550)
    p=canvas(w,h,c)
    if mobile:
        p += [label(34,48,'HADI ABDULRAHMAN',c,c['fg'],21),label(34,82,'@MANDOOF1 / SELECTED WORK',c,size=16),
              text(30,169,'I build systems',55,c['fg'],700,letter_spacing='-2.2'),
              text(30,234,'that investigate.',55,c['fg'],700,letter_spacing='-2.2'),
              text(34,283,'Cybersecurity engineering student.',24,c['dim']),field(320,447,175,c),
              line(34,598,606,598,c['line']),label(34,641,'SECURITY / APPLIED AI / SYSTEMS',c,c['accent'],18)]
    else:
        p += [label(42,51,'HADI ABDULRAHMAN',c,c['fg'],22),label(1158,51,'@MANDOOF1',c,size=16).replace('font-weight="400"','text-anchor="end" font-weight="400"'),
              line(42,79,1158,79,c['line']),
              text(37,204,'I build systems',70,c['fg'],700,letter_spacing='-3'),
              text(37,286,'that investigate.',70,c['fg'],700,letter_spacing='-3'),
              text(42,344,'Cybersecurity engineering student.',24,c['dim']),
              text(42,381,'Honeypots, security models, and AI infrastructure.',21,c['dim']),
              field(938,249,215,c),
              label(938,432,'CAPTURE → REASON → UNDERSTAND',c,c['accent'],12).replace('font-weight="400"','text-anchor="middle" font-weight="400"'),
              line(42,467,1158,467,c['line']),label(42,511,'SECURITY RESEARCH / APPLIED AI / SYSTEMS',c,c['accent'],16),
              text(1158,511,'BUILT END TO END',14,c['dim'],mono=True,text_anchor='end')]
    save(f'hero-{"mobile-" if mobile else ""}{theme}.svg',w,h,'Hadi Abdulrahman — I build systems that investigate.','Cybersecurity engineering student. Honeypots, security models, and AI infrastructure.',p)


def honey(theme,mobile=False):
    c=THEMES[theme];w,h=(640,650) if mobile else (1200,520)
    p=canvas(w,h,c)
    p += [label(34 if mobile else 42,48,'01 / FLAGSHIP SYSTEM',c,c['accent'],18 if mobile else 15)]
    if mobile:
        p += [text(30,124,'HoneySentinel',54,c['fg'],700,letter_spacing='-2'),text(34,169,'Capture. Analyze. Investigate.',25,c['dim']),
              line(34,201,606,201,c['line'])]
        rows=[('01','CAPTURE','SSH · Telnet · FTP · HTTP(S)'),('02','ANALYZE','Flow classifier · Rules · Local models'),('03','INVESTIGATE','Transcripts · ATT&CK · Indicators')]
        for i,(n,name,detail) in enumerate(rows):
            y=232+i*112
            p += [rect(34,y,572,94,c['panel'],rx=8),label(54,y+34,n,c,c['accent'],18),text(108,y+34,name,21,c['fg'],700),text(108,y+68,detail,20,c['dim'])]
        p += [label(34,612,'SELF-HOSTED / ENCRYPTED EVIDENCE',c,c['accent'],17)]
    else:
        p += [text(38,126,'HoneySentinel AI',59,c['fg'],700,letter_spacing='-2.5'),text(42,171,'A honeypot platform built around the investigation.',25,c['dim']),arrow(1118,116,c['accent'],1.2),line(42,203,1158,203,c['line'])]
        for i,(name,sub) in enumerate([('CAPTURE','Protocol emulation'),('ANALYZE','Layered local analysis'),('INVESTIGATE','Evidence you can follow')]):
            x=42+i*386
            p += [rect(x,233,344,198,c['panel'],rx=10),label(x+22,266,f'0{i+1} / {name}',c,c['accent']),text(x+22,303,sub,24,c['fg'],700)]
            if i==0:
                for j,(s,pw) in enumerate([('SSH',63),('TELNET',87),('FTP',63)]):
                    px=x+22+[0,75,174][j]
                    p += [rect(px,326,pw,32,c['bg'],c['line'],5),text(px+pw/2,348,s,14,c['dim'],mono=True,text_anchor='middle')]
                p += [text(x+22,397,'HTTP / HTTPS + decoy routing',17,c['dim'])]
            elif i==1:
                p += [text(x+22,343,'Random Forest + signatures',18,c['dim']),text(x+22,374,'Kev triage → Wolfram',21,c['fg']),text(x+22,405,'Local inference',15,c['accent'],mono=True)]
            else:
                p += [text(x+22,343,'Session transcripts + ATT&CK',18,c['dim']),text(x+22,374,'Indicators + encrypted evidence',17,c['dim']),text(x+22,405,'CSV / JSON / CEF / STIX',15,c['accent'],mono=True)]
            if i<2:p.append(arrow(x+352,333,c['accent'],.8))
        p += [label(42,480,'5 PROTOCOLS',c,c['accent']),label(427,480,'SELF-HOSTED INFERENCE',c),label(813,480,'FROM CAPTURE TO EXPORT',c)]
    save(f'honeysentinel-{"mobile-" if mobile else ""}{theme}.svg',w,h,'HoneySentinel AI — capture, analyze, investigate.','SSH, Telnet, FTP, HTTP and HTTPS honeypots. Local analysis with Wolfram, encrypted evidence, ATT&CK mapping, and investigation exports. Architecture schematic.',p)


def wolfram(theme,mobile=False):
    c=THEMES[theme];w,h=(640,650) if mobile else (1200,520)
    p=canvas(w,h,c)
    p += [label(34 if mobile else 42,48,'02 / SECURITY LANGUAGE MODEL',c,c['violet'],18 if mobile else 15)]
    if mobile:
        p += [text(28,146,'Wolfram',78,c['fg'],700,letter_spacing='-4'),text(34,196,'The final evolution of Chimera.',25,c['dim']),line(34,230,606,230,c['line']),
              text(30,335,'9B',90,c['violet'],700,letter_spacing='-4'),text(205,290,'MiMo-based security model',24,c['fg'],700),text(205,333,'QLoRA · GGUF · llama.cpp',20,c['dim']),
              rect(34,375,572,152,c['panel'],rx=10),label(56,410,'TRANSCRIPT → STRUCTURED ANALYSIS',c,c['violet'],16),text(56,453,'Intent · Objectives · ATT&CK',25,c['fg']),text(56,493,'Indicators grounded in the transcript',21,c['dim']),
              label(34,589,'CHIMERA → CHIMERA v2 → WOLFRAM',c,c['violet'],18),label(34,622,'LOCAL MODEL / HONEYSENTINEL INTEGRATION',c,size=14)]
    else:
        p += [text(36,150,'Wolfram',86,c['fg'],700,letter_spacing='-4'),text(42,199,'The final evolution of Chimera.',27,c['dim']),
              text(872,159,'9B',108,c['violet'],700,letter_spacing='-5'),label(873,196,'MiMo / QLoRA',c,c['violet'],16),line(42,240,1158,240,c['line'])]
        p += [label(42,280,'MODEL LINEAGE',c),text(42,331,'Chimera',25,c['dim']),arrow(164,323,c['dim'],.7),text(207,331,'Chimera v2',25,c['dim']),arrow(369,323,c['violet'],.7),text(415,331,'Wolfram',29,c['violet'],700),
              text(42,386,'Fine-tuned for the questions',26,c['fg']),text(42,424,'an investigator actually asks.',26,c['fg']),
              rect(653,265,505,185,c['panel'],rx=10),label(677,300,'TRANSCRIPT → STRUCTURED ANALYSIS',c,c['violet'],14)]
        for i,(key,val) in enumerate([('intent','what the attacker attempted'),('mitre_techniques','ATT&CK grounded in commands'),('iocs','hosts, URLs, and files')]):
            y=340+i*34
            p += [text(677,y,key,17,c['violet'],mono=True),text(865,y,val,14,c['dim'])]
        p += [label(42,483,'GGUF / llama.cpp',c,c['violet']),text(1158,483,'RUNS INSIDE HONEYSENTINEL’S ANALYSIS PIPELINE',14,c['dim'],mono=True,text_anchor='end')]
    save(f'wolfram-{"mobile-" if mobile else ""}{theme}.svg',w,h,'Wolfram — the final evolution of Chimera.','A MiMo 9B based security model, fine-tuned with QLoRA, deployed locally for structured analysis of honeypot transcripts. Chimera to Chimera v2 to Wolfram.',p)


def research(theme):
    c=THEMES[theme]
    projects=[
      ('amnis','03 / AGENT INFRASTRUCTURE','Amnis',c['green'],['Memory that survives','the next session.'],['Hybrid RAG + wiki compilation','MCP + a knowledge graph'],'MEMORY / RETRIEVAL / MCP'),
      ('aegis','04 / AGENT SECURITY','Aegis',c['accent'],['Test the attack.','Measure the defense.'],['Prompt injection + tool abuse','Layered guards + evaluation'],'ATTACKS / GUARDS / EVALS'),
      ('abliteration','05 / MODEL RESEARCH','Abliteration',c['violet'],['Understand the model.','Change the weights.'],['Hybrid-attention support','Training-free weight editing'],'EXTRACT / EDIT / EVALUATE'),
    ]
    for slug,category,title,accent,headline,detail,tags in projects:
        p=canvas(400,444,c)
        p += [label(26,37,category,c,accent,12),line(26,58,374,58,c['line'])]
        if slug=='amnis':
            nodes=[(42,108),(94,82),(144,122),(88,151),(194,89),(244,131),(300,87),(355,133)]
            for a,b in [(0,1),(0,3),(1,2),(2,3),(2,4),(4,5),(5,6),(5,7),(6,7)]:
                p.append(line(*nodes[a],*nodes[b],c['line'],2))
            for i,(x,y) in enumerate(nodes):p.append(f'<circle cx="{x}" cy="{y}" r="{7 if i in (2,5) else 4}" fill="{accent}" opacity="{1 if i in (2,5) else .55}"/>')
        elif slug=='aegis':
            for i in range(3):
                x=124+i*64
                p += [f'<path d="M{x} 79 L{x+29} 91 V120 Q{x+29} 143 {x} 159 Q{x-29} 143 {x-29} 120 V91 Z" fill="none" stroke="{accent}" stroke-width="1.5" opacity="{.35+.3*i}"/>']
            p.append(line(35,119,85,119,accent,2));p.append(arrow(286,119,accent,2))
        else:
            for i in range(15):
                x=30+i*24;y=119+math.sin(i*.65)*20
                p += [line(x,82,x,154,c['line']),rect(x-4,y-12,8,24,accent,rx=3)]
        p += [text(24,216,title,38,c['fg'],700,letter_spacing='-1.3')]
        for i,row in enumerate(headline):p.append(text(26,258+i*29,row,24,c['fg']))
        for i,row in enumerate(detail):p.append(text(26,335+i*26,row,18,c['dim']))
        p += [line(26,387,374,387,c['line']),label(26,419,tags,c,accent,11),arrow(345,414,accent,.7)]
        save(f'{slug}-{theme}.svg',400,444,title,' '.join(headline+detail),p)


def contact(theme,mobile=False):
    c=THEMES[theme];w,h=(640,310) if mobile else (1200,220)
    p=canvas(w,h,c)
    if mobile:
        p += [label(34,49,'RESEARCH / ENGINEERING / COLLABORATION',c,c['accent'],16),text(30,117,"Let's build something",44,c['fg'],700,letter_spacing='-1'),text(30,170,'worth investigating.',44,c['fg'],700,letter_spacing='-1'),line(34,208,606,208,c['line']),text(34,264,'haadii2005@gmail.com',27,c['fg']),arrow(558,254,c['accent'],1.1)]
    else:
        p += [label(42,48,'RESEARCH / ENGINEERING / COLLABORATION',c,c['accent'],15),text(38,110,"Let's build something",42,c['fg'],700,letter_spacing='-1.4'),text(38,160,'worth investigating.',42,c['fg'],700,letter_spacing='-1.4'),text(695,112,'haadii2005@gmail.com',27,c['fg']),text(695,151,'Open to internships & entry-level roles',18,c['dim']),arrow(1110,102,c['accent'],1.2)]
    save(f'contact-{"mobile-" if mobile else ""}{theme}.svg',w,h,"Let's build something worth investigating.",'Contact Hadi Abdulrahman at haadii2005@gmail.com. Open to cybersecurity internships and entry-level roles.',p)


if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    for theme in THEMES:
        for mobile in (False,True):
            hero(theme,mobile);honey(theme,mobile);wolfram(theme,mobile);contact(theme,mobile)
        research(theme)
    # Stable fallback retained for links to the old header location.
    (ROOT/'banner.svg').write_bytes((OUT/'hero-dark.svg').read_bytes())
    print('Rendered 22 theme-aware assets and banner.svg.')
