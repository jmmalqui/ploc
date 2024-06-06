TOPLEFT = "┏"
TOPRIGHT = "┓"
BOTTOMLEFT = "┗"
BOTTOMRIGHT = "┛"
HLINE = "━"
VLINE = "┃"
TRIBOTTOM = "┳"
TRIRIGHT = "┣"
TRILEFT = "┫"
TRITOP = "┻"
ALLDIR = "╋"


class Table:
    def __init__(
        self,
        dictionary_data: dict,
        primary_key: str,
        key_list: list[str],
        key_objects: list[callable],
    ) -> None:
        self.data = dictionary_data
        self.primary_key = primary_key
        self.key_list = key_list
        self.key_objects = key_objects
        self.widths = self.get_table_columns_width()

    def get_table_columns_width(self):
        columns_width = [len(self.primary_key)]
        for idx in range(len(self.key_list)):
            columns_width.append(len(self.key_list[idx]))
        for idx, (key, value) in enumerate(self.data.items()):
            if len(key) > columns_width[0]:
                columns_width[0] = len(key)
            for call_idx, call in enumerate(self.key_objects):
                if len(str(call(value))) >= columns_width[1 + call_idx]:
                    columns_width[1 + call_idx] = len(str(call(value)))
        return columns_width

    def draw_header(self):
        print(TOPLEFT, end="")
        for idx, width in enumerate(self.widths):
            print(HLINE * width, end="")
            if idx < len(self.widths) - 1:
                print(TRIBOTTOM, end="")
        print(TOPRIGHT)

        print(VLINE, end="")
        print(self.primary_key, end="")
        print(" " * (self.widths[0] - len(self.primary_key)), end="")

        for key_idx, key in enumerate(self.key_list):
            print(VLINE, end="")
            print(key, end="")
            print(" " * (self.widths[1 + key_idx] - len(key)), end="")
        print(VLINE)

        print(TRIRIGHT, end="")
        print(HLINE * self.widths[0], end="")
        for width in self.widths[1:]:
            print(ALLDIR, end="")
            print(HLINE * width, end="")
        print(TRILEFT)

    def draw_footer(self):
        print(BOTTOMLEFT, end="")
        for idx, width in enumerate(self.widths):
            print(HLINE * width, end="")
            if idx < len(self.widths) - 1:
                print(TRITOP, end="")
        print(BOTTOMRIGHT)

    def draw(self):
        self.draw_header()
        for key, value in self.data.items():
            print(VLINE, end="")
            print(key, end="")
            print(" " * (self.widths[0] - len(key)), end="")
            for call_idx, call in enumerate(self.key_objects):
                print(VLINE, end="")
                print(call(value), end="")
                print(" " * (self.widths[1 + call_idx] - len(str(call(value)))), end="")
            print(VLINE)
        self.draw_footer()
