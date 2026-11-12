#!/usr/bin/env python3
"""Generate the formula SVGs of camera_obscura.adoc.

Matrices and vectors are drawn as bracketed blocks whose size is proportional
to their dimensions (3x3 rotation, 3x1 vector, 4x4 homogeneous matrix, ...).
Colors follow the browser light/dark theme.

usage: python3 make.py     (writes the .svg files next to this script)
"""
from pathlib import Path

OUT = Path(__file__).parent
SERIF = 'font-family="DejaVu Serif, Times New Roman, serif"'
SANS = 'font-family="DejaVu Sans, Arial, sans-serif"'
STYLE = ('<style>.f{fill:#222}.s{stroke:#222;fill:none}.g{fill:#777}.sep{stroke:#999}'
         '@media (prefers-color-scheme: dark){.f{fill:#e6e6e6}.s{stroke:#e6e6e6}'
         '.g{fill:#9a9a9a}.sep{stroke:#777}}</style>')


def text_width(s, size):
    """rough width estimate of an italic serif string"""
    w = 0
    for ch in s or '':
        if ch in 'tilj1':
            w += 0.40
        elif ch.isupper():
            w += 0.72
        elif ch in 'wm':
            w += 0.75
        else:
            w += 0.58
    return w * size


def label(cx, cy, base, sup=None, sub=None, size=28):
    """symbol with stacked superscript / subscript, centered on (cx, cy)"""
    small = size * 0.62
    bw = text_width(base, size)
    sw = max(text_width(sup, small), text_width(sub, small))
    x = cx - (bw + sw) / 2
    y = cy + size * 0.33
    o = [f'<text class="f" x="{x:.1f}" y="{y:.1f}" font-size="{size}" {SERIF} font-style="italic">{base}</text>']
    if sup:
        o.append(f'<text class="f" x="{x + bw:.1f}" y="{y - size * 0.38:.1f}" font-size="{small:.1f}" {SERIF} font-style="italic">{sup}</text>')
    if sub:
        o.append(f'<text class="f" x="{x + bw:.1f}" y="{y + size * 0.20:.1f}" font-size="{small:.1f}" {SERIF} font-style="italic">{sub}</text>')
    return o


def brackets(x, top, w, h):
    f = 7
    return [f'<path class="s" stroke-width="2" d="M{x + f:.1f},{top:.1f} H{x:.1f} V{top + h:.1f} H{x + f:.1f}"/>',
            f'<path class="s" stroke-width="2" d="M{x + w - f:.1f},{top:.1f} H{x + w:.1f} V{top + h:.1f} H{x + w - f:.1f}"/>']


# ---- elements: each returns (width, rows, draw(x, cy, u) -> [svg]) ----------

def block(base, sup=None, sub=None, rows=3, cols=3, transposed=False):
    """matrix / vector block of rows x cols units"""
    def width(u):
        return cols * u + (16 if transposed else 0)

    def draw(x, cy, u):
        w, h = cols * u, rows * u
        size = 28 if cols > 1 else 18
        o = brackets(x, cy - h / 2, w, h) + label(x + w / 2, cy, base, sup, sub, size)
        if transposed:
            o.append(f'<text class="f" x="{x + w + 3:.1f}" y="{cy - h / 2 + 12:.1f}" font-size="17" {SERIF} font-style="italic">T</text>')
        return o
    return width, rows, draw


def M(base, sup=None, sub=None, T=False):
    return block(base, sup, sub, 3, 3, T)


def V(base, sup=None, sub=None):
    return block(base, sup, sub, 3, 1)


def HV(sub):
    return block('Ṽ', None, sub, 4, 1)


def homogeneous(r, t, lab_r, lab_t):
    """4x4 matrix split into R (3x3), t (3x1), 0 (1x3), 1 (1x1)"""
    def width(u):
        return 4 * u

    def draw(x, cy, u):
        top = cy - 2 * u
        sx, sy = x + 3 * u, top + 3 * u
        o = brackets(x, top, 4 * u, 4 * u)
        o += [f'<line class="sep" stroke-width="1.4" x1="{sx}" y1="{top + 4}" x2="{sx}" y2="{top + 4 * u - 4}"/>',
              f'<line class="sep" stroke-width="1.4" x1="{x + 6}" y1="{sy}" x2="{x + 4 * u - 6}" y2="{sy}"/>']
        o += label(x + 1.5 * u, top + 1.5 * u, 'R', *r, size=30)
        o += label(sx + u / 2, top + 1.5 * u, 't', *t, size=22)
        o += label(x + 1.5 * u, sy + u / 2, '0', 'T', None, size=24)
        o += label(sx + u / 2 - 4, sy + u / 2 - 3, '1', size=22)
        for bx, by, dim in ((sx, sy, '3×3'), (x + 4 * u, sy, '3×1'), (sx, top + 4 * u, '1×3'), (x + 4 * u, top + 4 * u, '1×1')):
            o.append(f'<text class="g" x="{bx - 4}" y="{by - 4}" font-size="9" text-anchor="end" {SANS}>{dim}</text>')
        for lx, lab in ((x + 1.5 * u, lab_r), (sx + u / 2, lab_t)):
            o.append(f'<text class="g" x="{lx}" y="{top - 9}" font-size="12" text-anchor="middle" {SANS}>{lab}</text>')
        return o
    return width, 4, draw


def op(sym):
    def draw(x, cy, u):
        return [f'<text class="f" x="{x + 17}" y="{cy + 9}" font-size="26" text-anchor="middle" {SERIF}>{sym}</text>']
    return (lambda u: 34), 0, draw


EQ, PLUS, MINUS, TIMES = op('='), op('+'), op('−'), op('×')


def paren(opening):
    def draw(x, cy, u):
        h = 1.5 * u + 4
        a, b = (x + 11, x + 1) if opening else (x + 1, x + 11)
        return [f'<path class="s" stroke-width="1.8" d="M{a},{cy - h:.1f} Q{b - (a - b) * 0.6:.1f},{cy} {a},{cy + h:.1f}"/>']
    return (lambda u: 12), 0, draw


LP, RP = paren(True), paren(False)
GAP = 10  # between juxtaposed elements


def render(name, lines, number=None, u=36, top_margin=0):
    """lines: list of element lists; lines are aligned on their first '='"""
    pad, vgap = 16, 22
    widths, eq_pos = [], []
    for line in lines:
        x, eq = 0, 0
        for e in line:
            if e is EQ and not eq:
                eq = x
            x += e[0](u) + GAP
        widths.append(x - GAP)
        eq_pos.append(eq)
    shift = [max(eq_pos) - p for p in eq_pos]
    num_w = 60 if number else 0
    W = pad * 2 + max(w + s for w, s in zip(widths, shift)) + num_w
    body, y = [], pad + top_margin
    for line, s in zip(lines, shift):
        h = max(e[1] for e in line) * u
        cy = y + h / 2
        x = pad + s
        for e in line:
            body += e[2](x, cy, u)
            x += e[0](u) + GAP
        y += h + vgap
        last_cy = cy
    H = y - vgap + pad
    if number:
        body.append(f'<text class="f" x="{W - pad}" y="{last_cy + 7:.1f}" font-size="20" text-anchor="end" {SERIF}>({number})</text>')
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">', STYLE] + body + ['</svg>']
    (OUT / f'{name}.svg').write_text('\n'.join(svg) + '\n', encoding='utf-8')


# ---- formulas ----------------------------------------------------------------
Rwc, Rcw = ('R', 'w', 'c'), ('R', 'c', 'w')
twc, tcw = ('t', 'w', 'c'), ('t', 'c', 'w')
Vw, Vc = V('V', None, 'w'), V('V', None, 'c')

render('pose', [[Vw, EQ, M(*Rwc), Vc, PLUS, V(*twc)]], number=1)
render('transform', [[Vc, EQ, M(*Rcw), Vw, PLUS, V(*tcw)]], number=2)

render('homogeneous_transform', [[HV('c'), EQ, homogeneous(('c', 'w'), ('c', 'w'), 'rotation', 'translation'), TIMES, HV('w')]], u=46, top_margin=20)
render('homogeneous_pose', [[HV('w'), EQ, homogeneous(('w', 'c'), ('w', 'c'), 'orientation', 'position'), TIMES, HV('c')]], u=46, top_margin=20)

render('conversion_derivation', [
    [Vw, MINUS, V(*twc), EQ, M(*Rwc), Vc],
    [M(*Rwc, T=True), LP, Vw, MINUS, V(*twc), RP, EQ, Vc],
    [Vc, EQ, M(*Rwc, T=True), Vw, MINUS, M(*Rwc, T=True), V(*twc)],
], number=3)
render('conversion_transform', [
    [M(*Rcw), EQ, M(*Rwc, T=True)],
    [V(*tcw), EQ, MINUS, M(*Rwc, T=True), V(*twc)],
])
render('conversion_pose', [
    [M(*Rwc), EQ, M(*Rcw, T=True)],
    [V(*twc), EQ, MINUS, M(*Rcw, T=True), V(*tcw)],
])

Rab, Rba = ('R', 'α', 'β'), ('R', 'β', 'α')
Ra, ta = ('R', 'αw', 'αc'), ('t', 'αw', 'αc')
Rb, tb = ('R', 'βw', 'βc'), ('t', 'βw', 'βc')
Vaw, Vac, Vbw, Vbc = (V('V', None, s) for s in ('αw', 'αc', 'βw', 'βc'))

render('change_target', [[Vbw, EQ, M(*Rb), Vbc, PLUS, V(*tb)]])
render('change_rotation', [
    [V('V', None, 'β'), EQ, M(*Rba), V('V', None, 'α')],
    [V('V', None, 'α'), EQ, M(*Rab), V('V', None, 'β')],
], number=4)
render('change_derivation', [
    [Vaw, EQ, M(*Ra), Vac, PLUS, V(*ta)],
    [Vaw, EQ, M(*Ra), M(*Rab), Vbc, PLUS, V(*ta)],
    [M(*Rba), Vaw, EQ, M(*Rba), LP, M(*Ra), M(*Rab), Vbc, PLUS, V(*ta), RP],
    [Vbw, EQ, LP, M(*Rba), M(*Ra), M(*Rab), RP, Vbc, PLUS, M(*Rba), V(*ta)],
], number=5)
render('change_result', [
    [M(*Rb), EQ, M(*Rba), M(*Ra), M(*Rab)],
    [V(*tb), EQ, M(*Rba), V(*ta)],
])

render('tait_bryan', [[V('P', None, 'w'), EQ, M('R', None, 'yaw'), M('R', None, 'pitch'), M('R', None, 'roll'), V('P', None, 'c')]])
