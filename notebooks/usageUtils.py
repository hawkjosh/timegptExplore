import os
import json
import time
import shelve
from enum import Enum, auto
import requests
from dotenv import load_dotenv

load_dotenv()

class Style(Enum):
    BOLD = auto()
    RESET = auto()

class Color(Enum):
    BRIGHT_RED = auto()
    BRIGHT_YELLOW = auto()
    BRIGHT_BLUE = auto()
    BRIGHT_WHITE = auto()

styleCodes = {
    Style.BOLD: "\033[1m",
    Style.RESET: "\033[0m",
}

colorCodes = {
    Color.BRIGHT_RED: "\033[91m",
    Color.BRIGHT_YELLOW: "\033[93m",
    Color.BRIGHT_BLUE: "\033[94m",
    Color.BRIGHT_WHITE: "\033[97m",
}

def printSp(text, style=None, color=None):
    codes = []

    if style and style in styleCodes:
        codes.append(styleCodes[style])
    if color and color in colorCodes:
        codes.append(colorCodes[color])

    combinedCodes = "".join(codes) if codes else styleCodes[Style.RESET]
    resetCode = styleCodes[Style.RESET]

    return f"{combinedCodes}{text}{resetCode}"

def printAndClear(message, sleepTime=1, newLine=False):
    if not newLine:
        print(f"\r{message}", end="", flush=True)
        time.sleep(sleepTime)
    else:
        print(f"\r{message}\n\n", end="")

def borderPrint(text1, text2=None):
    padding = 10
    width = max(len(text1), len(text2) if text2 is not None else 0) + padding * 2

    topBorder = printSp(f"{"= " * int(width // 4)}\n", color=Color.BRIGHT_WHITE)
    botBorder = printSp(f"\n{"= " * int(width // 4)}", color=Color.BRIGHT_WHITE)

    print(topBorder)
    print(f"{text1.center(width)}")
    if text2 is not None:
        print(f"{text2.center(width)}")
    print(botBorder)

def fetchData():
    response = requests.get(os.getenv("USAGE_URL"))
    if response.status_code == 200:
        return response.json()
    return None

def readJsonData():
    with open("usage.json", "r") as file:
        data = json.load(file)
        return data

def updateJsonData():
    apiData = fetchData()
    oldData = readJsonData()

    oldDataIds = set(item["created_at"] for item in oldData)
    newData = [item for item in apiData if item["created_at"] not in oldDataIds]

    if newData or len(apiData) != len(oldData):
        updatedData = oldData + newData
        with open("usage.json", "w") as file:
            json.dump(updatedData, file)
        return updatedData
    return oldData

def getTotals():
    data = readJsonData()

    calls = len(data)
    tokens = sum(
        (item["input_tokens"] if item["input_tokens"] is not None else 0)
        + (item["output_tokens"] if item["output_tokens"] is not None else 0)
        for item in data
    )
    spent = sum(item["price_of_request_in_cents"] for item in data) / 100

    totalsData = {
        "calls": calls,
        "tokens": tokens,
        "spent": spent
    }

    return totalsData

def updateShelfData():
    totalsData = getTotals()

    shelfData = {
        "calls": {"curr": 0, "diff": 0},
        "tokens": {"curr": 0, "diff": 0},
        "spent": {"curr": 0, "diff": 0},
    }

    with shelve.open("usage") as shelf:
        for key in ["calls", "tokens", "spent"]:
            if key not in shelf:
                shelf[key] = {"curr": 0, "diff": 0}
            else:
                currVal = shelf[key]["curr"]
                diffVal = totalsData[key] - currVal
                shelf[key] = {"curr": totalsData[key], "diff": diffVal}

            shelfData[key]["curr"] = shelf[key]["curr"]
            shelfData[key]["diff"] = shelf[key]["diff"]

    return shelfData

def readTotals():
    totals = {}
    with shelve.open("usage") as shelf:
        for key in ["calls", "tokens", "spent"]:
            if key not in shelf:
                shelf[key] = {"curr": 0, "diff": 0}
            totals[f"tot{key.capitalize()}"] = shelf[key]["curr"]
            totals[f"run{key.capitalize()}"] = shelf[key]["diff"]

    return totals

def showTotalUsage():
    tots = readTotals()

    calls = tots["totCalls"]
    tokens = tots["totTokens"]
    spent = tots["totSpent"]

    callsTxt = printSp("API CALLS:  ", color=Color.BRIGHT_WHITE)
    callsVal = printSp(f"{calls}", style=Style.BOLD, color=Color.BRIGHT_RED)
    tokensTxt = printSp("TOKENS:  ", color=Color.BRIGHT_WHITE)
    tokensVal = printSp(f"{tokens}", style=Style.BOLD, color=Color.BRIGHT_RED)
    spentTxt = printSp("SPENT:  ", color=Color.BRIGHT_WHITE)
    spentVal = printSp(f"{spent:.2f}", style=Style.BOLD, color=Color.BRIGHT_RED)

    divider = printSp("   ||   ", style=Style.BOLD, color=Color.BRIGHT_WHITE)

    printStr = f"{callsTxt}{callsVal}{divider}{tokensTxt}{tokensVal}{divider}{spentTxt}{spentVal}"

    return printStr

def showRunUsage():
    tots = readTotals()

    calls = tots["runCalls"]
    tokens = tots["runTokens"]
    spent = tots["runSpent"]

    callsVal = printSp(f"{calls}", style=Style.BOLD, color=Color.BRIGHT_BLUE)
    callsTxt = printSp(f" {"call" if calls == 1 else "calls"}", color=Color.BRIGHT_YELLOW)
    tokensVal = printSp(f"{tokens}", style=Style.BOLD, color=Color.BRIGHT_BLUE)
    tokensTxt = printSp(" tokens", color=Color.BRIGHT_YELLOW)
    spentVal = printSp(f"{spent:.2f}", style=Style.BOLD, color=Color.BRIGHT_BLUE)
    spentTxt = printSp(" spent", color=Color.BRIGHT_YELLOW)

    front = printSp("<<  ", color=Color.BRIGHT_YELLOW)
    back = printSp("  >>", color=Color.BRIGHT_YELLOW)
    divider = printSp("  ••  ", style=Style.BOLD, color=Color.BRIGHT_YELLOW)

    printStr = f"{front}{callsVal}{callsTxt}{divider}{tokensVal}{tokensTxt}{divider}{spentVal}{spentTxt}{back}"

    return printStr

def showUsage(withRun=False):

    totsText = showTotalUsage()
    runText = showRunUsage()

    if withRun:
        borderPrint(text1=totsText, text2=runText)
    else:
        borderPrint(text1=totsText)

def refreshUsageData():
    startTime = time.time()
    tryCount = 1
    checkCount = 4
    localData = readJsonData()

    while time.time() - startTime < 20:
        newData = updateJsonData()
        totals = updateShelfData()
        if newData is not None:
            if len(newData) > len(localData):
                runCalls = totals["calls"]["diff"]
                printAndClear(f"Usage data successfully updated with {runCalls} {"call" if runCalls == 1 else "calls"}", newLine=True)
                showUsage(withRun=True)
                return
            printAndClear(
                f"Checking for new data || Attempt {tryCount} of {checkCount} .        "
            )
            printAndClear(
                f"Checking for new data || Attempt {tryCount} of {checkCount} . .      "
            )
            printAndClear(
                f"Checking for new data || Attempt {tryCount} of {checkCount} . . .    "
            )
            printAndClear(
                f"Checking for new data || Attempt {tryCount} of {checkCount} . . . .  "
            )
            printAndClear(
                f"Checking for new data || Attempt {tryCount} of {checkCount} . . . . ."
            )
            tryCount += 1
        else:
            printAndClear(
                "Failed to connect with usage API. Retrying...", 5,
            )
            checkCount -= 1

    printAndClear("No new data detected.                              ", newLine=True)
    showUsage()

if __name__ == "__main__":
    refreshUsageData()
