from enum import Enum, auto


class Style(Enum):
    BOLD = auto()
    DIM = auto()
    UNDERLINE = auto()
    BOLD_UNDERLINE = auto()
    RESET = auto()


class Color(Enum):
    BLACK = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    MAGENTA = auto()
    CYAN = auto()
    WHITE = auto()
    GRAY = auto()
    BRIGHT_RED = auto()
    BRIGHT_GREEN = auto()
    BRIGHT_YELLOW = auto()
    BRIGHT_BLUE = auto()
    BRIGHT_MAGENTA = auto()
    BRIGHT_CYAN = auto()
    BRIGHT_WHITE = auto()


class BgColor(Enum):
    BLACK = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    MAGENTA = auto()
    CYAN = auto()
    WHITE = auto()
    GRAY = auto()
    BRIGHT_RED = auto()
    BRIGHT_GREEN = auto()
    BRIGHT_YELLOW = auto()
    BRIGHT_BLUE = auto()
    BRIGHT_MAGENTA = auto()
    BRIGHT_CYAN = auto()
    BRIGHT_WHITE = auto()


styleCodes = {
    Style.BOLD: "\033[1m",
    Style.DIM: "\033[2m",
    Style.UNDERLINE: "\033[4m",
    Style.BOLD_UNDERLINE: "\033[1;4m",
    Style.RESET: "\033[0m",
}

colorCodes = {
    Color.BLACK: "\033[30m",
    Color.RED: "\033[31m",
    Color.GREEN: "\033[32m",
    Color.YELLOW: "\033[33m",
    Color.BLUE: "\033[34m",
    Color.MAGENTA: "\033[35m",
    Color.CYAN: "\033[36m",
    Color.WHITE: "\033[37m",
    Color.GRAY: "\033[90m",
    Color.BRIGHT_RED: "\033[91m",
    Color.BRIGHT_GREEN: "\033[92m",
    Color.BRIGHT_YELLOW: "\033[93m",
    Color.BRIGHT_BLUE: "\033[94m",
    Color.BRIGHT_MAGENTA: "\033[95m",
    Color.BRIGHT_CYAN: "\033[96m",
    Color.BRIGHT_WHITE: "\033[97m",
}

bgColorCodes = {
    BgColor.BLACK: "\033[40m",
    BgColor.RED: "\033[41m",
    BgColor.GREEN: "\033[42m",
    BgColor.YELLOW: "\033[43m",
    BgColor.BLUE: "\033[44m",
    BgColor.MAGENTA: "\033[45m",
    BgColor.CYAN: "\033[46m",
    BgColor.WHITE: "\033[47m",
    BgColor.GRAY: "\033[100m",
    BgColor.BRIGHT_RED: "\033[101m",
    BgColor.BRIGHT_GREEN: "\033[102m",
    BgColor.BRIGHT_YELLOW: "\033[103m",
    BgColor.BRIGHT_BLUE: "\033[104m",
    BgColor.BRIGHT_MAGENTA: "\033[105m",
    BgColor.BRIGHT_CYAN: "\033[106m",
    BgColor.BRIGHT_WHITE: "\033[107m",
}


def printSp(text, style=None, color=None, bgColor=None):
    codes = []

    if style and style in styleCodes:
        codes.append(styleCodes[style])
    if color and color in colorCodes:
        codes.append(colorCodes[color])
    if bgColor and bgColor in bgColorCodes:
        codes.append(bgColorCodes[bgColor])

    combinedCodes = "".join(codes) if codes else styleCodes[Style.RESET]
    resetCode = styleCodes[Style.RESET]

    return f"{combinedCodes}{text}{resetCode}"
