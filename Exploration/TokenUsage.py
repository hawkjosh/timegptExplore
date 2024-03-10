import os
import time
import requests

from dotenv import load_dotenv

from SpecialPrint import printSp, Style, Color, BgColor

load_dotenv()


def getData(waitForUpdate=False, timeout=20):
    startTime = time.time()
    prevCalls, prevTokens, prevSpent = readData()

    while True:
        url = os.getenv("USAGE_URL")
        response = requests.get(url)
        data = response.json()

        currCalls = len(data)
        runCalls = currCalls - prevCalls

        if not waitForUpdate or currCalls > prevCalls:
            currTokens = sum(
                (item["input_tokens"] if item["input_tokens"] is not None else 0)
                + (item["output_tokens"] if item["output_tokens"] is not None else 0)
                for item in data
            )
            currSpent = sum(item["price_of_request_in_cents"] for item in data) / 100
            runTokens = currTokens - prevTokens
            runSpent = currSpent - prevSpent

            writeData(currCalls, currTokens, currSpent)

            return currCalls, currTokens, currSpent, runCalls, runTokens, runSpent

        if time.time() - startTime > timeout:
            raise TimeoutError(
                "\nToken usage update timed out. There was either no update or the API is down."
            )

        time.sleep(4)


def readData():
    try:
        with open("usage.txt", "r") as file:
            data = file.read().strip().split(",")
            if len(data) == 3:
                calls, tokens, spent = data
                return int(calls), int(tokens), float(spent)
            raise ValueError("Invalid data in file.")
    except (FileNotFoundError, ValueError):
        return 0, 0, 0


def writeData(calls, tokens, spent):
    with open("usage.txt", "w") as file:
        file.write(f"{calls},{tokens},{spent}")


def prtCurrentRun(calls, tokens, spent):
    prtRunCalls = printSp(str(calls), style=Style.BOLD, color=Color.BRIGHT_RED)
    prtRunTokens = printSp(str(tokens), style=Style.BOLD, color=Color.BRIGHT_RED)
    runSpentFormat = f"{round(spent, 2):.2f}"
    prtRunSpent = printSp(runSpentFormat, style=Style.BOLD, color=Color.BRIGHT_RED)

    header = printSp("<< Current run: ", style=Style.BOLD, color=Color.YELLOW)
    footer = printSp(" spent >>", style=Style.BOLD, color=Color.YELLOW)

    callsText = " call made | " if calls == 1 else " calls made | "
    tokensText = " token used | " if tokens == 1 else " tokens used | "

    prtCallsText = printSp(callsText, style=Style.BOLD, color=Color.YELLOW)
    prtTokensText = printSp(tokensText, style=Style.BOLD, color=Color.YELLOW)

    prtStr = f"\n{header}{prtRunCalls}{prtCallsText}{prtRunTokens}{prtTokensText}{prtRunSpent}{footer}\n"

    return prtStr


def prtTotalUsage(calls, tokens, spent):
    prtCalls = printSp(str(calls), style=Style.BOLD, color=Color.BRIGHT_BLUE)
    prtTokens = printSp(str(tokens), style=Style.BOLD, color=Color.BRIGHT_BLUE)
    spentFormat = f"{round(spent, 2):.2f}"
    prtSpent = printSp(spentFormat, style=Style.BOLD, color=Color.BRIGHT_BLUE)

    header = printSp("TOTAL USAGE", style=Style.BOLD_UNDERLINE, color=Color.WHITE)

    prtStr = f"\n{header}: API Calls = {prtCalls} | Tokens = {prtTokens} | Spent = {prtSpent}\n"

    return prtStr


def showTokenUsage():
    try:
        calls, tokens, spent, runCalls, runTokens, runSpent = getData(
            waitForUpdate=True
        )

        prtStr = ""

        if runCalls > 0:
            prtStr += prtCurrentRun(runCalls, runTokens, runSpent)

        prtStr += prtTotalUsage(calls, tokens, spent)

        print(prtStr)

    except TimeoutError as e:
        calls, tokens, spent = readData()
        print(str(e))
        print(prtTotalUsage(calls, tokens, spent))


# if __name__ == "__main__":
#     showTokenUsage()
