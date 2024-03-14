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


def printColor(text, style=None, color=None):
    codes = []

    if style and style in styleCodes:
        codes.append(styleCodes[style])
    if color and color in colorCodes:
        codes.append(colorCodes[color])

    combinedCodes = "".join(codes) if codes else styleCodes[Style.RESET]
    resetCode = styleCodes[Style.RESET]

    return f"{combinedCodes}{text}{resetCode}"


def printSpecial(message, sleepTime=1, newLine=False, end=""):
    if not newLine:
        print(f"\r{message}", end=end, flush=True)
        time.sleep(sleepTime)
    else:
        print(f"\r{message}\n", end=end)


def getLocalData(update=False):
    if os.path.exists("localData.json"):
        with open("localData.json", "r") as file:
            localData = json.load(file)
            lCalls = len(localData)
            lTokens = sum(
                (item["input_tokens"] if item["input_tokens"] is not None else 0)
                + (item["output_tokens"] if item["output_tokens"] is not None else 0)
                for item in localData
            )
            lSpent = sum(item["price_of_request_in_cents"] for item in localData) / 100
            localUsage = {"calls": lCalls, "tokens": lTokens, "spent": round(lSpent, 2)}
    else:
        localData = []
        localUsage = {"calls": 0, "tokens": 0, "spent": 0.0}

    if update:
        startTime = time.time()
        tryCount = 1
        checkCount = 4
        while time.time() - startTime < 20:
            response = requests.get(os.getenv("USAGE_URL"))
            apiData = response.json()
            if len(apiData) > len(localData):
                localDataIds = set(item["created_at"] for item in localData)
                newData = [
                    item for item in apiData if item["created_at"] not in localDataIds
                ]

                updatedData = localData + newData
                uCalls = len(updatedData)
                uTokens = sum(
                    (item["input_tokens"] if item["input_tokens"] is not None else 0)
                    + (
                        item["output_tokens"]
                        if item["output_tokens"] is not None
                        else 0
                    )
                    for item in updatedData
                )
                uSpent = (
                    sum(item["price_of_request_in_cents"] for item in updatedData) / 100
                )
                updatedUsage = {
                    "calls": uCalls,
                    "tokens": uTokens,
                    "spent": round(uSpent, 2),
                }
                with open("localData.json", "w") as file:
                    json.dump(updatedData, file)
                printSpecial("Usage data successfully updated with:               ", newLine=True)
                return updatedUsage, updatedData
            printSpecial(
                f"Checking for new data || Attempt {tryCount} of {checkCount} .        "
            )
            printSpecial(
                f"Checking for new data || Attempt {tryCount} of {checkCount} . .      "
            )
            printSpecial(
                f"Checking for new data || Attempt {tryCount} of {checkCount} . . .    "
            )
            printSpecial(
                f"Checking for new data || Attempt {tryCount} of {checkCount} . . . .  "
            )
            printSpecial(
                f"Checking for new data || Attempt {tryCount} of {checkCount} . . . . ."
            )
            tryCount += 1

        printSpecial(
            "No new data detected.                               ",
            newLine=True,
            end="\n",
        )
        return localUsage, localData
    return localUsage, localData


def getShelfData():
    totals, _ = getLocalData()
    
    shelfData = {
        "calls": {"curr": 0, "diff": 0},
        "tokens": {"curr": 0, "diff": 0},
        "spent": {"curr": 0.0, "diff": 0.0},
    }
    
    with shelve.open("shelfData") as shelf:
        for key in ["calls", "tokens", "spent"]:
            if key not in shelf:
                shelf[key] = {"curr": 0, "diff": 0}
            else:
                currVal = shelf[key]["curr"]
                diffVal = totals[key] - currVal
                shelf[key] = {"curr": totals[key], "diff": diffVal}
            
            shelfData[key]["curr"] = shelf[key]["curr"]
            shelfData[key]["diff"] = shelf[key]["diff"]
            
    return shelfData


def showTotalUsage():
    tots = getShelfData()
    
    calls = tots["calls"]["curr"]
    tokens = tots["tokens"]["curr"]
    spent = tots["spent"]["curr"]

    callsTxt = printColor("API CALLS:  ", color=Color.BRIGHT_WHITE)
    callsVal = printColor(f"{calls}", style=Style.BOLD, color=Color.BRIGHT_RED)
    tokensTxt = printColor("TOKENS:  ", color=Color.BRIGHT_WHITE)
    tokensVal = printColor(f"{tokens}", style=Style.BOLD, color=Color.BRIGHT_RED)
    spentTxt = printColor("SPENT:  ", color=Color.BRIGHT_WHITE)
    spentVal = printColor(f"{spent:.2f}", style=Style.BOLD, color=Color.BRIGHT_RED)
    
    divider = printColor("   ||   ", style=Style.BOLD, color=Color.BRIGHT_WHITE)
    printStr = f"{callsTxt}{callsVal}{divider}{tokensTxt}{tokensVal}{divider}{spentTxt}{spentVal}"
    width = len(printStr) + 20
    border = printColor(f"{"= " * int(width // 4)}", color=Color.BRIGHT_WHITE)
    
    print(border)
    print(f"\n{printStr.center(width)}\n")
    print(border)


def showRunUsage():
    tots = getShelfData()
    
    calls = tots["calls"]["diff"]
    tokens = tots["tokens"]["diff"]
    spent = tots["spent"]["diff"]
    
    if calls == 0 and tokens == 0 and spent == 0.0:
        return
    
    callsVal = printColor(f"{calls}", style=Style.BOLD, color=Color.BRIGHT_BLUE)
    callsTxt = printColor(f" {"call" if calls == 1 else "calls"}", color=Color.BRIGHT_YELLOW)
    tokensVal = printColor(f"{tokens}", style=Style.BOLD, color=Color.BRIGHT_BLUE)
    tokensTxt = printColor(" tokens", color=Color.BRIGHT_YELLOW)
    spentVal = printColor(f"{spent:.2f}", style=Style.BOLD, color=Color.BRIGHT_BLUE)
    spentTxt = printColor(" spent", color=Color.BRIGHT_YELLOW)

    front = printColor("<<  ", color=Color.BRIGHT_YELLOW)
    back = printColor("  >>", color=Color.BRIGHT_YELLOW)
    divider = printColor("  •  ", style=Style.BOLD, color=Color.BRIGHT_YELLOW)

    printStr = f"\n{front}{callsVal}{callsTxt}{divider}{tokensVal}{tokensTxt}{divider}{spentVal}{spentTxt}{back}"

    printSpecial(printStr, newLine=True, end="\n")


def getUsage(update=False):
    
    if not update:
        printSpecial("Current usage data:", newLine=True, end="\n")
        showTotalUsage()
        return
    
    getLocalData(update=True)
    showRunUsage()
    showTotalUsage()
