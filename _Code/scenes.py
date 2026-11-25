from common import *
from narration import NAME, STUDENT_ID

I = np.eye(2)
O, U = np.array([-3.2, -.6, 0]), .75       # origin and unit of the main grid
BIG = 1.35                                  # larger unit, used when vectors are short
PX = 4.25                                   # centre of the right-hand text panel

def set_unit(u):
    global U
    U = u

def panel():
    return Rectangle(width=5.6, height=8.2, fill_color=BG, fill_opacity=1,
                     stroke_width=0).move_to([4.3, 0, 0])

def base():
    """Faint fixed grid with labelled axes."""
    g = grid_lines(I, O, U, 10, GREY, 1, .22)
    labels = VGroup(*[T(str(k), 20, GREY_B).move_to(to_screen((k, -.35), O, U)) for k in (-4, -2, 2, 4)],
                    *[T(str(k), 20, GREY_B).move_to(to_screen((-.3, k), O, U)) for k in (-2, 2, 4)],
                    T("x", 24, GREY_B).move_to([1.1, O[1] + .28, 0]),
                    T("y", 24, GREY_B).move_to([O[0] + .28, 3.6, 0]))
    return VGroup(g, labels)

def vec(p, c, start=(0, 0)):
    return arrow(p, O, U, c, start)

def tag(s, p, c, d=(.45, .3)):
    t = T(s, 26, c).move_to(to_screen(np.array(p) + d, O, U))
    return t.add_background_rectangle(color=BG, opacity=.8, buff=.04)

def at(m, y):
    return m.move_to([PX, y, 0])

class S1(Narrated):
    number = 1
    def construct(self):
        title = VGroup(T("What does a matrix do?", 64), T("Matrices and matrix operations", 38, CA),
                       T(f"{NAME}  ·  {STUDENT_ID}", 30, GREY_B),
                       T("Linear Algebra and Calculus (M3)", 26, GREY_B)).arrange(DOWN, buff=.4)
        back = grid_lines(I, ORIGIN, .8, 10, None, 1.2, .28)
        title.set_z_index(5)
        self.add(back)
        self.play(Write(title[0]), FadeIn(title[1:], shift=UP * .2), run_time=1.6)
        self.play(Transform(back, grid_lines(B, ORIGIN, .8, 10, None, 1.2, .28)), run_time=1.8, rate_func=smooth)
        self.end_beat()
        self.play(FadeOut(title), FadeOut(back), run_time=.6)

        u, centers = .45, ([-3.5, -.3, 0], [3.5, -.3, 0])
        def figure(M, o):
            f = [(0, 0), (0, 2), (1.3, 2), (1.3, 1.6), (.4, 1.6), (.4, 1.2), (1, 1.2), (1, .8), (.4, .8), (.4, 0)]
            F = Polygon(*[to_screen(M @ np.array(p), o, u) for p in f], color=V,
                        fill_color=V, fill_opacity=.75, stroke_width=2)
            return VGroup(grid_lines(M, o, u, 3), F)
        L, R = (figure(I, c) for c in centers)
        ghosts = [figure(I, c).set_opacity(.1) for c in centers]      # where each grid started
        self.add(*ghosts)
        self.play(Create(L), Create(R), run_time=2)
        moves = VGroup(T("turn: 90° anticlockwise", 32, CA), T("shear: slide sideways", 32, CB)).arrange(RIGHT, buff=1.2).to_edge(UP)
        self.play(FadeIn(moves[0]), run_time=.8); self.wait(2)
        self.play(FadeIn(moves[1]), run_time=.8)
        self.end_beat()

        def shear(g, M, c):
            return Transform(g, figure(M, c))
        l1, l2 = T("1. turn", 32, CA), T("2. shear", 32, CB)
        VGroup(l1, l2).arrange(RIGHT, buff=.7).move_to([-3.5, -3.55, 0])
        r1, r2 = T("1. shear", 32, CB), T("2. turn", 32, CA)
        VGroup(r1, r2).arrange(RIGHT, buff=.7).move_to([3.5, -3.55, 0])
        self.play(FadeIn(l1), Rotate(L, PI/2, about_point=centers[0]), run_time=1.4)
        self.play(FadeIn(l2), shear(L, B @ A, centers[0]), run_time=1.4)
        self.play(FadeIn(r1), shear(R, B, centers[1]), run_time=1.4)
        self.play(FadeIn(r2), Rotate(R, PI/2, about_point=centers[1]), run_time=1.4)
        self.end_beat()
        ne = T("≠", 80, E2).move_to([0, -.4, 0])
        self.play(FadeIn(ne, scale=1.6)); self.play(Indicate(L[1]), Indicate(R[1]))
        self.end_beat()

class S2(Narrated):
    number = 2
    def construct(self):
        rows = [[2, 0, 1], [1, 3, 4]]
        M = mat(rows, size=60).move_to([0, .6, 0])
        name = T("C =", 48).next_to(M, LEFT, buff=.3)
        self.play(FadeIn(name), Create(M), run_time=1.5)
        rr = VGroup(*[SurroundingRectangle(VGroup(*M.cells[i]), color=CA, buff=.12) for i in range(2)])
        cc = VGroup(*[SurroundingRectangle(VGroup(M.cells[0][j], M.cells[1][j]), color=CB, buff=.12) for j in range(3)])
        size = T(f'<span foreground="{CA}">2 rows</span> × <span foreground="{CB}">3 columns</span>', 40).move_to([0, -1.3, 0])
        self.play(Create(rr)); self.play(FadeOut(rr), Create(cc)); self.play(FadeOut(cc), FadeIn(size))
        self.end_beat()
        box = SurroundingRectangle(M.cells[1][2], color=V, buff=.14)
        entry = T(f'c<sub><span foreground="{CA}">2</span><span foreground="{CB}">3</span></sub> = 4', 48, V).move_to([0, -2.3, 0])
        # row then column: entry c_ij
        gen = T("general entry: c<sub>ij</sub>  (row i, column j)", 32, GREY_B).move_to([0, -3.1, 0])
        r2 = SurroundingRectangle(VGroup(*M.cells[1]), color=CA, buff=.12)
        c3 = SurroundingRectangle(VGroup(M.cells[0][2], M.cells[1][2]), color=CB, buff=.12)
        self.play(Create(r2)); self.play(Create(c3)); self.play(FadeOut(r2, c3), Create(box), FadeIn(entry)); self.play(FadeIn(gen))
        self.end_beat()
        self.play(FadeOut(box, entry, gen, size), run_time=.5)
        mach = VGroup(Rectangle(width=2.6, height=1.3, color=CA), T("m × n", 40)).move_to([0, -2, 0])
        inn, out = T("n numbers in", 34, CB).move_to([-4.6, -2, 0]), T("m numbers out", 34, CA).move_to([4.8, -2, 0])
        a1 = Arrow([-2.9, -2, 0], [-1.4, -2, 0], buff=0); a2 = Arrow([1.4, -2, 0], [2.9, -2, 0], buff=0)
        self.play(FadeIn(mach)); self.play(FadeIn(inn), GrowArrow(a1)); self.play(GrowArrow(a2), FadeIn(out))
        for _ in range(2):
            self.play(stream([-2.9, -2, 0], [-1.3, -2, 0], CB, 3), run_time=.9)
            self.play(Indicate(mach, color=V, scale_factor=1.06), run_time=.5)
            self.play(stream([1.3, -2, 0], [2.9, -2, 0], CA, 2), run_time=.8)
        self.end_beat()
        self.play(FadeOut(M, name, mach, inn, out, a1, a2), run_time=.5)

        set_unit(BIG)
        bg, pl = base(), panel()
        g2, s2 = grid_lines(I, O, U, 10, None, 1.5, .55), square(I, O, U)
        e1, e2 = vec((1, 0), E1), vec((0, 1), E2)
        t1, t2 = tag("e₁ = (1, 0)", (1, 0), E1, (1, -.45)), tag("e₂ = (0, 1)", (0, 1), E2, (-1, .3))
        self.add(bg, g2, s2, pl)
        self.play(FadeIn(g2, s2), run_time=.6)
        self.add(pl)
        self.play(grow(e1), grow(e2), FadeIn(t1, t2))
        W = mat(B.tolist(), [E1, E2], 54); at(W, 1)
        c1 = at(T("column 1: where e₁ lands", 32, E1), -.6); c2 = at(T("column 2: where e₂ lands", 32, E2), -1.3)
        self.play(FadeIn(W))
        self.play(FadeIn(c1), Indicate(VGroup(W.cells[0][0], W.cells[1][0]), color=E1), Indicate(e1, color=E1))
        self.play(FadeIn(c2), Indicate(VGroup(W.cells[0][1], W.cells[1][1]), color=E2),
                  Transform(g2, grid_lines(B, O, U, 10, None, 1.5, .55)), Transform(s2, square(B, O, U)),
                  Transform(e2, vec((1, 1), E2)), Transform(t2, tag("e₂ lands", (1, 1), E2, (.2, .4))), run_time=2)
        # each column is read off from its arrow
        for a, j, c in ((e1, 0, E1), (e2, 1, E2)):
            d = Dot(a[2].get_end(), color=c, radius=.12)
            self.play(d.animate.move_to(VGroup(W.cells[0][j], W.cells[1][j])), run_time=1)
            self.play(Circumscribe(VGroup(W.cells[0][j], W.cells[1][j]), color=c), FadeOut(d), run_time=.8)
        self.end_beat()
        goal = at(VGroup(T("Goal: explain why matrices", 30, V), T("add, scale and multiply", 30, V),
                  T("the way they do", 30, V)).arrange(DOWN, buff=.15), -2.6)
        self.play(FadeIn(goal))
        self.end_beat()

class S3(Narrated):
    number = 3
    def construct(self):
        set_unit(.75)
        sq = square(I, O, U)
        bg, g, pl = base(), grid_lines(I, O, U, 10), panel()
        self.add(bg, g, sq, pl)
        e1, e2 = vec((1, 0), E1), vec((0, 1), E2)
        t1, t2 = tag("e₁", (1, 0), E1, (.3, -.4)), tag("e₂", (0, 1), E2, (-.5, .1))
        self.add(e1, e2, t1, t2)
        WB = mat(B.tolist(), [E1, E2], 44); eqB = at(row(T("B =", 40, CB), WB), 2.7)
        self.play(FadeIn(eqB)); self.wait(1)
        self.play(Transform(g, grid_lines(B, O, U, 10)), Transform(sq, square(B, O, U)), Transform(e2, vec((1, 1), E2)),
                  Transform(t2, tag("e₂ → (1, 1)", (1, 1), E2, (-.2, .4))),
                  Transform(t1, tag("e₁ → (1, 0)", (1, 0), E1, (.6, -.4))), run_time=3)
        self.end_beat()

        # back to the start, then send v through B
        self.play(Transform(g, grid_lines(I, O, U, 10)), FadeOut(sq), Transform(e2, vec((0, 1), E2)),
                  Transform(t2, tag("e₂", (0, 1), E2, (-.5, .1))),
                  Transform(t1, tag("e₁", (1, 0), E1, (.3, -.4))), run_time=1.2)
        v, tv = vec((1, 2), V), tag("v = (1, 2)", (1, 2), V, (.9, .3))
        r1 = at(T(f'v = 1<span foreground="{E1}">e₁</span> + 2<span foreground="{E2}">e₂</span>', 38), 1.4)
        steps = VGroup(vec((1, 0), E1), vec((1, 1), E2, (1, 0)), vec((1, 2), E2, (1, 1)))
        self.play(grow(v), FadeIn(tv))
        self.play(LaggedStart(*[grow(s) for s in steps], lag_ratio=.6), FadeIn(r1), run_time=2)
        self.wait(1)
        steps2 = VGroup(vec((1, 0), E1), vec((2, 1), E2, (1, 0)), vec((3, 2), E2, (2, 1)))
        self.play(Transform(g, grid_lines(B, O, U, 10)), Transform(e2, vec((1, 1), E2)),
                  Transform(steps, steps2), Transform(v, vec((3, 2), V)), FadeOut(t2),
                  Transform(tv, tag("Bv = (3, 2)", (3, 2), V, (1.1, .3))), run_time=3)
        r2 = at(row(T("Bv = 1", 34), mat([[1], [0]], [E1], 30), T("+ 2", 34), mat([[1], [1]], [E2], 30),
                    T("=", 34), mat([[3], [2]], [V], 30), buff=.1), -.1)
        self.play(FadeIn(r2))
        self.end_beat()

        self.play(FadeOut(r1, r2, eqB, steps, e1, e2, t1, tv, v), FadeOut(g), run_time=.8)
        Av, Bv = vec((-2, 1), CA), vec((3, 2), CB)
        tA, tB = tag("Av = (−2, 1)", (-2, 1), CA, (-1, -.4)), tag("Bv = (3, 2)", (3, 2), CB, (1, -.5))
        v0 = vec((1, 2), V); tv0 = tag("v", (1, 2), V, (.3, .2))
        eA = row(T("A =", 34, CA), mat(A.tolist(), None, 34)); eB = row(T("B =", 34, CB), mat(B.tolist(), None, 34))
        at(VGroup(eA, eB).arrange(RIGHT, buff=.45), 2.8)
        self.play(FadeIn(v0, tv0, eA)); self.play(Rotate(v0.copy(), PI/2, about_point=O, remover=True), run_time=1)
        self.play(FadeIn(Av, tA), run_time=.5)
        self.play(FadeIn(eB), FadeOut(v0, tv0), grow(Bv), FadeIn(tB))
        moved = vec((1, 3), CB, (-2, 1)); S = vec((1, 3), WHITE)
        self.play(TransformFromCopy(Bv, moved), run_time=1.5)
        tS = tag("(A + B)v = (1, 3)", (1, 3), WHITE, (.8, .45))
        self.play(grow(S), FadeIn(tS))
        self.end_beat()

        ma, mb, ms = mat(A.tolist(), None, 32), mat(B.tolist(), None, 32), mat((A + B).tolist(), None, 32)
        add = at(row(ma, "+", mb, "=", ms, buff=.14), .9)
        self.play(FadeIn(add[:4]))
        self.play(FadeIn(ms[0], ms[-1]), run_time=.3)
        for i in range(2):
            for j in range(2):
                self.play(Indicate(ma.cells[i][j], color=CA), Indicate(mb.cells[i][j], color=CB),
                          FadeIn(ms.cells[i][j]), *[x.cells[i][j].copy().animate(path_arc=-1.3 if i == 0 else 1.3, remover=True).move_to(ms.cells[i][j]).set_opacity(0) for x in (ma, mb)], run_time=1)
        same = at(T("same size needed", 30, GREY_B), -.4)
        chk = at(row(T("check:", 28), mat([[1, 0], [1, 1]], None, 28), mat([[1], [2]], [V], 28), T("=", 28), mat([[1], [3]], None, 28), buff=.12), -1.7)
        self.play(FadeIn(same)); self.play(FadeIn(chk))
        self.end_beat()
        self.play(FadeOut(Av, tA, moved, S, tS, add, same, chk, eA), run_time=.6)
        big = vec((6, 4), WHITE); tb = tag("2Bv = (6, 4)", (6, 4), WHITE, (-.9, .45))
        sc = at(row(T("2", 36), mat(B.tolist(), None, 34), "=", mat((2 * B).tolist(), None, 34), buff=.15), .9)
        self.play(TransformFromCopy(Bv, big), FadeIn(tb), run_time=1.8)
        self.play(FadeIn(sc))
        self.end_beat()

class S4(Narrated):
    number = 4
    def construct(self):
        set_unit(BIG)
        sq = square(I, O, U)
        bg, g, pl = base(), grid_lines(I, O, U, 10), panel()
        self.add(bg, g, sq, pl)
        head = at(T(f'(<span foreground="{CA}">A</span><span foreground="{CB}">B</span>)x = '
                    f'<span foreground="{CA}">A</span>(<span foreground="{CB}">B</span>x)', 44), 3.3)
        order = at(T(f'first <span foreground="{CB}">B</span>, then <span foreground="{CA}">A</span>', 34), 2.6)
        self.play(Write(head)); self.play(FadeIn(order))
        # preview of both moves, then reset
        self.play(Transform(g, grid_lines(B, O, U, 10)), Transform(sq, square(B, O, U)), run_time=2)
        self.play(Rotate(g, PI/2, about_point=O), Rotate(sq, PI/2, about_point=O), run_time=2)
        self.play(Transform(g, grid_lines(I, O, U, 10)), Transform(sq, square(I, O, U)), run_time=1)
        self.end_beat()
        e1, e2 = vec((1, 0), E1), vec((0, 1), E2)
        self.play(grow(e1), grow(e2))
        mA, mB, mP = mat(A.tolist(), None, 34), mat(B.tolist(), [E1, E2], 34), mat((A @ B).tolist(), [E1, E2], 34)
        eq = at(row(mA, mB, "=", mP, buff=.2), 1.05)
        la, lb = T("A", 28, CA).next_to(mA, UP, buff=.1), T("B", 28, CB).next_to(mB, UP, buff=.1)
        lp = T("AB", 28).next_to(mP, UP, buff=.1)
        self.play(Transform(g, grid_lines(B, O, U, 10)), Transform(sq, square(B, O, U)), Transform(e2, vec((1, 1), E2)), FadeIn(eq[:3], la, lb), run_time=2)
        self.play(FadeIn(mP[0], mP[-1], lp))
        self.end_beat()

        def push(col, w, out, y, c):
            return at(row(T(f"{w[0]}", 30), mat([[0], [1]], [WHITE], 28), T(f"+ {w[1]}", 30),
                          mat([[-1], [0]], [WHITE], 28), T("=", 30), mat(out, [c], 28), buff=.12), y)
        self.play(Indicate(VGroup(mB.cells[0][0], mB.cells[1][0]), color=E1))
        p1 = push(0, (1, 0), [[0], [1]], -.5, E1)
        self.play(FadeIn(p1))
        self.play(Rotate(e1, PI/2, about_point=O), run_time=1.6)
        t1 = tag("(0, 1)", (0, 1), E1, (.6, .25))
        self.play(FadeIn(t1, mP.cells[0][0], mP.cells[1][0]))
        self.end_beat()
        p2 = push(1, (1, 1), [[-1], [1]], -1.9, E2)
        self.play(Indicate(VGroup(mB.cells[0][1], mB.cells[1][1]), color=E2))
        self.play(FadeIn(p2))
        self.play(Rotate(e2, PI/2, about_point=O), Rotate(sq, PI/2, about_point=O), Rotate(g, PI/2, about_point=O), run_time=1.6)
        t2 = tag("(−1, 1)", (-1, 1), E2, (-.6, .35))
        self.play(FadeIn(t2, mP.cells[0][1], mP.cells[1][1]))
        self.end_beat()

        self.play(FadeOut(p1, p2), run_time=.4)
        lines = []
        for k, (i, j) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            a, b = A[i], B[:, j]
            s = f"row {i+1} · col {j+1}:  ({num(a[0])})({b[0]}) + ({num(a[1])})({b[1]}) = {num(a @ b)}"
            ln = at(T(s, 26, E1 if j == 0 else E2), -.4 - .7 * k)
            rb = SurroundingRectangle(VGroup(*mA.cells[i]), color=V, buff=.1)
            cb = SurroundingRectangle(VGroup(mB.cells[0][j], mB.cells[1][j]), color=V, buff=.1)
            pb = SurroundingRectangle(mP.cells[i][j], color=V, buff=.1)
            self.play(Create(rb), Create(cb), run_time=.9)
            # row and column entries fly into the calculation
            fly = [x.copy().set_color(V) for x in (mA.cells[i][0], mB.cells[0][j], mA.cells[i][1], mB.cells[1][j])]
            self.play(*[x.animate(path_arc=.6, remover=True).move_to(ln.get_left() + RIGHT * ln.width * f).set_opacity(0)
                        for x, f in zip(fly, (.45, .55, .7, .8))], FadeIn(ln), run_time=1.1)
            res = mP.cells[i][j].copy().set_color(V).move_to(ln.get_right(), aligned_edge=RIGHT)
            self.play(res.animate(remover=True).move_to(mP.cells[i][j]), Create(pb), run_time=.8)
            if k < 3:
                left = self.ends[self.i] - self.time - .4
                if left > .05: self.wait(left)
                self.play(FadeOut(rb, cb, pb), run_time=.4)
                self.i += 1
        end = at(T("row × column = move after move", 27, V), -3.4)
        self.play(FadeIn(end))
        self.end_beat()

class S5(Narrated):
    number = 5
    def construct(self):
        cs, u = ([-3.5, .2, 0], [3.5, .2, 0]), .42
        gs, arrows = [], []
        data = [(B @ A, "BA: turn, then shear", "BA ="), (A @ B, "AB: shear, then turn", "AB =")]
        for c in cs:
            gs.append(grid_lines(I, c, u, 3)); arrows.append([arrow((1, 0), c, u, E1), arrow((0, 1), c, u, E2)])
        self.play(*[FadeIn(g) for g in gs], *[FadeIn(a) for p in arrows for a in p])
        for k, (M, s, nm) in enumerate(data):
            c = cs[k]
            head = T(s, 32).move_to([c[0], 3.15, 0])
            m = row(T(nm, 34), mat(M.tolist(), [E1, E2], 34)).move_to([c[0], -3.1, 0])
            self.play(FadeIn(head), run_time=.5)
            first = A if k == 0 else B
            for N in (first, M):
                self.play(Transform(gs[k], grid_lines(N, c, u, 3)),
                          *[Transform(arrows[k][q], arrow(N[:, q], c, u, (E1, E2)[q])) for q in (0, 1)], run_time=1.4)
            self.play(FadeIn(m), run_time=.8)
        ne = T("≠", 70, V).move_to([0, -3.1, 0])
        self.play(FadeIn(ne))
        self.end_beat()
        for k in (1, 0):
            w = data[k][0] @ np.array([1, 2])
            start, end = arrow((1, 2), cs[k], u, V), arrow(w, cs[k], u, V)
            lab = T(f"{data[k][2][:2]}v = ({num(w[0])}, {w[1]})", 30, V).move_to([cs[k][0] + 2.1, 2.3, 0])
            lab.add_background_rectangle(color=BG, opacity=.85)
            lv = T("v = (1, 2)", 30, V).move_to(lab).add_background_rectangle(color=BG, opacity=.85)
            self.play(grow(start), FadeIn(lv), run_time=1)
            self.play(Transform(start, end), FadeOut(lv), FadeIn(lab), run_time=1.8)
        self.end_beat()
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in self.hud.get_family()], run_time=.6)
        rule = T(f'(m × <span foreground="{V}">n</span>) (<span foreground="{V}">n</span> × p) = m × p', 60).move_to([0, 2, 0])
        self.play(FadeIn(rule))
        def box(x, s, c): return VGroup(Rectangle(width=2.2, height=1.3, color=c), T(s, 36)).move_to([x, -.8, 0])
        def ar(a, b): return Arrow([a, -.8, 0], [b, -.8, 0], buff=0)
        names = [T(s, 34, c).move_to([x, -.8, 0]) for s, c, x in (("p in", WHITE, -5.9), ("n", V, 0), ("m out", WHITE, 5.9))]
        b1, b2 = box(-2.6, "n × p", CB), box(2.6, "m × n", CA)
        self.play(FadeIn(names[0]), GrowArrow(ar(-5.2, -3.8)), FadeIn(b1))
        self.play(GrowArrow(ar(-1.4, -.4)), FadeIn(names[1])); self.play(GrowArrow(ar(.4, 1.4)), FadeIn(b2))
        self.play(GrowArrow(ar(3.8, 5.1)), FadeIn(names[2]))
        for a, b, c in ((-5.2, -3.8, WHITE), (-1.4, 1.4, V), (3.8, 5.1, WHITE)):
            self.play(stream([a, -.8, 0], [b, -.8, 0], c, 4), run_time=1)
        self.play(FadeIn(T("the n outputs of the first machine feed the n inputs of the second", 30, GREY_B).move_to([0, -2.4, 0])))
        self.end_beat()

class S6(Narrated):
    number = 6
    def construct(self):
        items = VGroup(T("1.  Columns show where the basic arrows land.", 40, E1),
                       T("2.  Adding and scaling matrices adds and scales outputs.", 40, CA),
                       T("3.  Multiplying means move after move: order matters.", 40, V)).arrange(DOWN, buff=.6, aligned_edge=LEFT)
        for m in items:
            self.play(Write(m), run_time=1.6)
            self.play(Circumscribe(m, color=m.get_color(), time_width=.4), run_time=1.6)
        self.end_beat()
        self.play(FadeOut(items), run_time=.5)
        cr = VGroup(T("Summary and credits", 44),
            T("Columns = landing spots   ·   sums and scales of outputs   ·   products = move after move", 26, V),
            T(f"{NAME}  ·  {STUDENT_ID}", 30),
            T("Visual style inspired by 3Blue1Brown, Essence of Linear Algebra (YouTube)", 26, GREY_B),
            T("Made with Manim Community, Python and FFmpeg.", 26, GREY_B),
            T("Music: original instrumental, synthesised in Python (music.py).", 26, GREY_B),
            T("AI disclosure: script, storyboard, visuals, music and code generated with", 26, GREY_B),
            T("Claude (Anthropic), directed and reviewed by the student.", 26, GREY_B),
            T("PREVIEW: temporary computer voice" if TEMP_VOICE else VOICE_CREDIT or "Narration recorded by the student.", 26, GREY_B)).arrange(DOWN, buff=.35)
        self.play(FadeIn(cr)); self.wait(6)      # credits stay readable after the last word
