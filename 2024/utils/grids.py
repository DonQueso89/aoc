_fmt_red = "\033[31m{}\033[0m"

def print_grid(
    grid: dict,
    xlim: int,
    ylim: int,
    default: str = " ",
    marked_chars: tuple | None = None,
):
    for y in range(ylim):
        line = ""
        for x in range(xlim):
            c = grid.get((x, y), default)
            if marked_chars and c in marked_chars:
                c = _fmt_red.format(c)
            line += c
        print(line)

caret_mapping = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}
