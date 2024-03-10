import json
from SpecialPrint import printSp, Style, Color, BgColor


def readData():
    with open("usage.json", "r") as file:
        data = json.load(file)
        calls = len(data)
        tokens = sum(
            (item["input_tokens"] if item["input_tokens"] is not None else 0)
            + (item["output_tokens"] if item["output_tokens"] is not None else 0)
            for item in data
        )
        spent = sum(item["price_of_request_in_cents"] for item in data) / 100
        return calls, tokens, spent


def borderPrint(text):
    padding = 10
    width = padding * 2 + len(text)

    border = printSp(f"{'= ' * int(width / 4)}", color=Color.BRIGHT_WHITE)

    print(border)
    print("\n" + text.center(width) + "\n")
    print(border)


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


if __name__ == "__main__":
    showTokenUsage()
