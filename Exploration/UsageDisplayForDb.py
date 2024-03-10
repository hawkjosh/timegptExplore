from UsageDb import readData
from SpecialPrint import printSp, Style, Color


def showTokenUsage():
    calls, tokens, spent = readData()

    callsTxt = printSp("API CALLS:  ", color=Color.BRIGHT_WHITE)
    tokensTxt = printSp("TOKENS:  ", color=Color.BRIGHT_WHITE)
    spentTxt = printSp("SPENT:  ", color=Color.BRIGHT_WHITE)
    callsVal = printSp(f"{calls}", style=Style.BOLD, color=Color.BRIGHT_RED)
    tokensVal = printSp(f"{tokens}", style=Style.BOLD, color=Color.BRIGHT_RED)
    spentVal = printSp(f"{spent:.2f}", style=Style.BOLD, color=Color.BRIGHT_RED)

    divider = printSp("   ||   ", style=Style.BOLD, color=Color.BRIGHT_WHITE)

    usageString = f"{callsTxt}{callsVal}{divider}{tokensTxt}{tokensVal}{divider}{spentTxt}{spentVal}"

    borderPrint(usageString)


def borderPrint(text):
    padding = 10
    width = padding * 2 + len(text)

    border = printSp(f"{'= ' * int(width / 4)}", color=Color.BRIGHT_WHITE)

    print(border)
    print("\n" + text.center(width) + "\n")
    print(border)
