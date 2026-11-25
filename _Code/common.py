"""Shared helpers: text, matrices, vectors, grid, and narration timing."""
import glob, json, os, subprocess
import numpy as np
from manim import *
from narration import NARRATION, WORDS_PER_SECOND

HERE = os.path.dirname(os.path.abspath(__file__))
VOICE_DIR = os.environ.get("VOICE_DIR", f"{HERE}/recordings")
AI_VOICE = "VOICE_DIR" in os.environ        # line lengths are known exactly
VOICE_CREDIT = os.environ.get("VOICE_CREDIT", "")
TEMP_VOICE = AI_VOICE and not VOICE_CREDIT   # preview only
BG, E1, E2, V, CA, CB = "#10141c", "#6fcf7c", "#ff6f61", "#ffd75e", "#58b7ff", "#c08bff"
config.background_color = BG
FONT = "STIX Two Text"

A = np.array([[0, -1], [1, 0]])   # quarter turn anticlockwise
B = np.array([[1, 1], [0, 1]])    # shear

def T(s, size=36, color=WHITE):
    return MarkupText(s, font=FONT, font_size=size, color=color)

def num(x):
    return str(x).replace("-", "−")

def mat(rows, col_colors=None, size=38):
    """Matrix drawn without LaTeX. result.cells[i][j] is the entry in row i, column j."""
    cells = [[T(num(x), size, col_colors[j] if col_colors else WHITE)
              for j, x in enumerate(r)] for r in rows]
    dx, dy = 0.021 * size, 0.0175 * size
    for i, r in enumerate(cells):
        for j, c in enumerate(r):
            c.move_to([j * dx, -i * dy, 0])
    w, h = (len(rows[0]) - 1) * dx / 2 + .0105 * size, (len(rows) - 1) * dy / 2 + .34
    mid = np.array([(len(rows[0]) - 1) * dx / 2, -(len(rows) - 1) * dy / 2, 0])
    def bracket(s):
        p = VMobject(stroke_width=3, color=WHITE)
        return p.set_points_as_corners([mid + [s*(w-.14), h, 0], mid + [s*w, h, 0],
                                        mid + [s*w, -h, 0], mid + [s*(w-.14), -h, 0]])
    g = VGroup(bracket(-1), *[c for r in cells for c in r], bracket(1))
    g.cells = cells
    return g

def row(*parts, buff=.2):
    return VGroup(*[T(p) if isinstance(p, str) else p for p in parts]).arrange(RIGHT, buff=buff)

def grid_lines(M, o, u, n, color=None, width=1.5, opacity=.8):
    """Grid lines from -n to n after applying matrix M, about origin o with unit u."""
    g = VGroup()
    for k in range(-n, n + 1):
        for q, (a, b) in enumerate((((k, -n), (k, n)), ((-n, k), (n, k)))):
            g.add(Line(*[to_screen(M @ np.array(p), o, u) for p in (a, b)],
                       color=WHITE if k == 0 else color or ("#3d7fd0", "#2aa9a0")[q],
                       stroke_width=width * (1.6 if k == 0 else 1), stroke_opacity=opacity))
    return g

def to_screen(p, o, u):
    return np.array([o[0] + u * p[0], o[1] + u * p[1], 0])

def arrow(p, o, u, color, start=(0, 0)):
    """Arrow with a soft glow: [0] and [1] are the glow, [2] is the arrow."""
    s, e = to_screen(start, o, u), to_screen(p, o, u)
    glow = [Line(s, e, color=color, stroke_width=w, stroke_opacity=k) for w, k in ((24, .10), (14, .16))]
    return VGroup(*glow, Arrow(s, e, buff=0, color=color, stroke_width=6,
                               max_tip_length_to_length_ratio=.22, tip_length=.22))

def grow(a):
    return GrowFromPoint(a, a[2].get_start())

def square(M, o, u):
    """Image of the unit square under M."""
    return Polygon(*[to_screen(M @ np.array(p), o, u) for p in ((0, 0), (1, 0), (1, 1), (0, 1))],
                   color=V, fill_color=V, fill_opacity=.22, stroke_width=1.5)

def stream(a, b, color, n=4, t=1.6):
    """Dots travelling from a to b, used for numbers moving through a machine."""
    return LaggedStart(*[MoveAlongPath(Dot(a, radius=.09, color=color), Line(a, b), remover=True, rate_func=linear)
                         for _ in range(n)], lag_ratio=.25, run_time=t)

CHAPTERS = ["The puzzle", "What is a matrix?", "Seeing it move", "Multiplying", "Solving the puzzle", "Summary"]

def clip_for(n):
    found = [f for f in glob.glob(f"{VOICE_DIR}/scene{n}.*")
             if f.lower().endswith((".m4a", ".mp3", ".wav", ".aac"))]
    return found[0] if found else None

def seconds(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                 "format=duration", "-of", "csv=p=0", path]))

class Narrated(Scene):
    """Each beat gets a share of the scene's time, in proportion to its word count."""
    number = 0
    def setup(self):
        words = [len(b.split()) for b in NARRATION[self.number]]
        clip = clip_for(self.number)
        total = seconds(clip) if clip else sum(words) / WORDS_PER_SECOND
        self.ends = np.cumsum(words) / sum(words) * total
        if AI_VOICE:      # exact beat times are known
            self.ends = json.load(open(f"{VOICE_DIR}/scene{self.number}.json"))
        self.i = 0
        # chapter label and six-part progress bar
        n, w = self.number, 14.2 / 6
        self.hud = VGroup()
        for k in range(6):
            x = -7.1 + k * w
            self.hud.add(Line([x + .04, -3.95, 0], [x + w - .04, -3.95, 0], stroke_width=4,
                              color=CA if k < n - 1 else GREY_D))
        fill = Line([-7.1 + (n-1)*w + .04, -3.95, 0], [-7.1 + (n-1)*w + .05, -3.95, 0], color=CA, stroke_width=4)
        def advance(m):
            x = -7.1 + (n - 1) * w
            f = max(.02, min(1, self.time / self.ends[-1]))
            m.put_start_and_end_on([x + .04, -3.95, 0], [x + .04 + (w - .08) * f, -3.95, 0])
        fill.add_updater(advance)
        label = T(f"{n}  {CHAPTERS[n-1]}", 20, GREY_B).to_corner(UL, buff=.25)
        label.add_background_rectangle(color=BG, opacity=.85, buff=.08)
        self.hud.add(fill, label).set_z_index(20)
        self.add(self.hud)
    def end_beat(self):
        left = self.ends[self.i] - self.time
        if left > .05:
            self.wait(left)
        elif left < -.3:
            print(f"!! scene {self.number} beat {self.i} overruns by {-left:.1f}s")
        self.i += 1
