from typing import Self

class Object:
    ANCHOR_OPTIONS = ["tl", "tm", "tr", "ml", "mm", "mr", "bl", "bm", "br"]

    def __init__(self, children:list = None, x=0, y=0, height=0, width=0, anchor="tl"):
        if anchor in self.ANCHOR_OPTIONS:
            self.anchor = anchor
        elif len(anchor) == 2 and isinstance(anchor, (tuple, list)):
            self.anchor = anchor
        else:
            raise ValueError(
                f"anchor: {anchor} not in anchor options {self.ANCHOR_OPTIONS}"
            )

        self.anchor = anchor
        self.x = x
        self.y = y

        self.children = children

        self.data = [[" " for j in range(width)] for i in range(height)]

    @staticmethod
    def from_txt(path, encoding="utf-8"):
        obj = Object()

        with open(path, "r", encoding=encoding) as f:
            data = f.read().split("\n")
            data = list(map(list, data))

        obj.data = data
        return obj

    @property
    def width(self):
        return len(self.data[0])

    @property
    def height(self):
        return len(self.data)
    

    def get_anchor_point(self):
        if not isinstance(self.anchor, str):
            return self.anchor

        anchor_point = [0, 0]

        match self.anchor[0]:
            case "t":
                anchor_point[1] = 0
            case "m":
                anchor_point[1] = self.height // 2
            case "b":
                anchor_point[1] = self.height - 1

        match self.anchor[1]:
            case "l":
                anchor_point[0] = 0
            case "m":
                anchor_point[0] = self.width // 2
            case "r":
                anchor_point[0] = self.width - 1

        return anchor_point

    def compose(self, other: Self):
        other_anchor_x, other_anchor_y = other.get_anchor_point()
        for i in range(0, other.height):
            for j in range(0, other.width):

                pos_x = j + other.x - other_anchor_x
                pos_y = i + other.y - other_anchor_y
                if 0 <= pos_y < self.height and 0 <= pos_x < self.width:
                    self.data[pos_y][pos_x] = other.data[i][j]

    def __add__(self, o):
        self.compose(o)

    def __repr__(self):
        for child in self.children:
            self.compose(child)
        return "\n".join(map(lambda x: "".join(x), self.data))


class TextObject(Object):
    def __init__(self, text, children = None, x=0, y=0, height=0, width=0, anchor="tl"):
        super().__init__(children, x, y, height, width, anchor)
        self.data = [list(text)]

class ButtonObject(Object):
    def __init__(self, name, func, children = None, x=0, y=0, height=0, width=0, anchor="tl"):
        super().__init__(children, x, y, height, width, anchor)

        self.func = func
        self.data = [list(name)]

    def on_click(self):
        self.func()