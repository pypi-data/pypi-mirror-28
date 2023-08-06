from collections import namedtuple
from colors import color


class Fr:
    def __init__(self, s, fg=None, bg=None, styles=None):
        self.s = s
        self.fg, self.bg, self.styles = fg, bg, styles
        self.width = len(s)

    def render(self, fg=None, bg=None, styles=None):
        style = self.styles or styles
        style = None if style == 'normal' else style
        return color(self.s, self.fg or fg, self.bg or bg, style)


class Line:
    def __init__(self, *fragments, fg=None, bg=None, styles=None):
        self.fragments = []
        self.fg, self.bg, self.styles = fg, bg, styles
        self.parent = None
        self.width = 0

        for fr in fragments:
            self.add(fr, recalc=False)
        self.recalc()

    def recalc(self):
        self.width = sum([f.width for f in self.fragments] or [0])
        if self.parent:
            self.parent.recalc()

    def add(self, fr, recalc=True):
        fr = Fr(fr) if isinstance(fr, str) else fr
        self.fragments.append(fr)
        if recalc:
            self.recalc()

    def lines(self):
        return [(self, 0)]

    def render(self, idx=0, fg=None, bg=None, styles=None, align=None):
        base = ''.join([f.render(
            fg=self.fg or fg,
            bg=self.bg or bg,
            styles=self.styles or styles
        ) for f in self.fragments])
        return base


LEFT, RIGHT, CENTER = (1, 2, 3)


class Cell:
    Padding = namedtuple('Padding', ['top', 'right', 'bottom', 'left'])

    def __init__(
        self, *elements,
        fg=None, bg=None, styles=None,
        padding=None, align=LEFT
    ):
        self._padding = padding
        self.fg, self.bg, self.styles = fg, bg, styles
        self.align = align
        self.parent = None
        self.elements = []
        self._lines = []
        self.width = 0
        self.height = 0

        for e in elements:
            self.add(e, recalc=False)
        self.recalc()

    def parse_padding(self):
        p = self._padding
        if p is None and self.parent:
            p = self.parent.padding
        if p is None:
            return self.Padding(0, 0, 0, 0)
        if isinstance(p, int):
            return self.Padding(p, p, p, p)
        if len(p) == 2:
            return self.Padding(p[0], p[1], p[0], p[1])
        return self.Padding(p[0], p[1], p[2], p[3])

    def adjust_child_cells(self):
        for c in [e for e in self.elements if isinstance(e, Cell)]:
            if c.width < self.width:
                c.width = self.width
                c.adjust_child_cells()

    def recalc(self):
        self.padding = self.parse_padding()
        self.width = max([e.width for e in self.elements] or [0])
        self.width += self.padding.left + self.padding.right
        self.adjust_child_cells()
        self._lines = []
        for el in self.elements:
            self._lines += el.lines()
        self.height = len(self._lines)
        self.height += self.padding.top + self.padding.bottom
        if self.parent:
            self.parent.recalc()

    def add(self, e, recalc=True):
        e = Line(e) if isinstance(e, str) else e
        e.parent = self
        self.elements.append(e)
        if recalc:
            self.recalc()

    def lines(self):
        return [(self, idx) for idx in range(self.height)]

    def render(
        self, idx, width=None,
        fg=None, bg=None, styles=None, align=LEFT
    ):
        bg = self.bg or bg
        align = self.align or align
        width = self.width if width is None else width
        idx -= self.padding.top
        if idx < len(self._lines) and idx >= 0:
            el, el_idx = self._lines[idx]
            base = el.render(
                el_idx, fg=self.fg or fg, bg=bg,
                styles=self.styles or styles,
                align=self.align or align
            )
            # how much to distribute?
            lpad, rpad = self.padding.left, self.padding.right
            distribute = width - el.width - lpad - rpad
            if align == LEFT:
                rpad += distribute
            elif align == RIGHT:
                lpad += distribute
            else:
                half = distribute // 2
                lpad += half
                rpad += distribute - half
            lpad = color(' ' * lpad, bg=bg)
            rpad = color(' ' * rpad, bg=bg)
            return lpad + base + rpad
        return color(' ' * width, bg=bg)


TOP, ROW, MID, BTM = range(4)
HALF = 1


class Table:
    def __init__(
        self, fg=None, bg=None, styles=None,
        padding=None, rowsepstyle=None, align=LEFT
    ):
        self.fg, self.bg, self.styles = fg, bg, styles
        self.align = align
        self.padding = padding
        self.rowsepstyle = rowsepstyle
        self.parent = None
        self.width = 0
        self.height = 0
        self.cells = {}
        self.row_heights = []
        self.col_widths = []
        # (typ, rowindex, lineinrow)
        # typ: TOP, ROW, MID, BTM
        self.idx_row_map = []

    def recalc(self):
        self.row_heights = []
        self.col_widths = []
        for (r, c), cell in self.cells.items():
            while c >= len(self.col_widths):
                self.col_widths.append(0)
            if cell.width > self.col_widths[c]:
                self.col_widths[c] = cell.width
            while r >= len(self.row_heights):
                self.row_heights.append(0)
            if cell.height > self.row_heights[r]:
                self.row_heights[r] = cell.height

        self.width = sum(self.col_widths or [0])
        # self.width += len(self.col_widths) + 1  # borders, not doing this

        self.idx_row_map = []
        if self.rowsepstyle == HALF:
            self.idx_row_map.append((TOP, 0, None))
        for row_idx, row_height in enumerate(self.row_heights):
            for i in range(row_height):
                self.idx_row_map.append((ROW, row_idx, i))
            if self.rowsepstyle == HALF:
                self.idx_row_map.append((MID, row_idx, None))
        # correct the separator after the last row
        if self.idx_row_map and self.idx_row_map[-1][0] == MID:
            last_row_idx = len(self.row_heights) - 1
            self.idx_row_map[-1] = (BTM, last_row_idx, None)

        self.height = len(self.idx_row_map)

        if self.parent:
            self.parent.recalc()

    def add(self, r, c, cell):
        cell = cell if isinstance(cell, Cell) else Cell(cell)
        cell.parent = self
        cell.recalc()
        self.cells[(r, c)] = cell
        self.recalc()

    def lines(self):
        return [(self, idx) for idx in range(self.height)]

    def render(self, idx, fg=None, bg=None, styles=None, align=LEFT):
        typ, row_idx, in_row_idx = self.idx_row_map[idx]
        ret = ''
        for col_idx, col_width in enumerate(self.col_widths):
            if not col_width:
                continue
            cell = None
            inherited_bg = self.bg or bg
            if (row_idx, col_idx) in self.cells:
                cell = self.cells[(row_idx, col_idx)]
                inherited_bg = cell.bg or self.bg or bg
            if typ == TOP:
                ret += color('▄' * col_width, bg=bg, fg=inherited_bg)
            elif typ == MID:
                _fg = inherited_bg
            elif typ == BTM:
                ret += color('▀' * col_width, bg=bg, fg=inherited_bg)
            else:
                if cell:
                    ret += cell.render(
                        in_row_idx,
                        width=col_width,
                        fg=self.fg or fg,
                        bg=inherited_bg,
                        styles=self.styles or styles,
                        align=self.align or align
                    )
                else:
                    ret += color(' ' * col_width, bg=inherited_bg)

            if typ == MID:
                if (row_idx + 1, col_idx) not in self.cells:
                    _bg = self.bg or bg
                else:
                    cell = self.cells[(row_idx + 1, col_idx)]
                    _bg = cell.bg or self.bg or bg
                ret += color('▀' * col_width, bg=_bg, fg=_fg)
        return ret

    def asstring(self, bg=None, fg=None, styles=None, align=LEFT):
        return '\n'.join([
            self.render(i, bg=bg, fg=fg, styles=styles, align=align)
            for i in range(self.height)
        ])
