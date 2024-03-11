import os
import json
import time
import shelve
import requests
from dotenv import load_dotenv

from UsageDisplay import showTokenUsage, readData

load_dotenv()


def fetchData(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def updateLocalData(jsonFilePath, newData=None):
    try:
        with open(jsonFilePath, "r") as file:
            try:
                localData = json.load(file)
            except json.JSONDecodeError:
                localData = []
    except FileNotFoundError:
        localData = []

    localDataCreatedAt = {item["created_at"]: item for item in localData}

    for item in newData:
        localDataCreatedAt[item["created_at"]] = item

    with open(jsonFilePath, "w") as file:
        json.dump(list(localDataCreatedAt.values()), file, indent=4)

    with shelve.open("usage") as shelf:
        usage = []
        for key in ["calls", "tokens", "spent"]:
            if key not in shelf:
                shelf[key] = {"curr": 0, "diff": 0}
                usage.append(shelf[key])
            else:
                currVal = shelf[key]["curr"]
                diffVal = newData[key] - currVal

                shelf[key]["curr"] = newData[key]
                shelf[key]["diff"] = diffVal

                if key == "spent":
                    usage.append(
                        {
                            key: {
                                "curr": round(shelf[key]["curr"], 2),
                                "diff": round(shelf[key]["diff"], 2),
                            }
                        }
                    )
                else:
                    usage.append(
                        {key: {"curr": shelf[key]["curr"], "diff": shelf[key]["diff"]}}
                    )
        if len(usage) == 0:
            shelfUsage = [
                {"calls": {"curr": 0, "diff": 0}},
                {"tokens": {"curr": 0, "diff": 0}},
                {"spent": {"curr": 0, "diff": 0}},
            ]
        else:
            shelfUsage = usage

    printAndClear("Token usage successfully updated with new data.", newLine=True)
    showTokenUsage()
    return shelfUsage


def printAndClear(message, sleepTime=1, newLine=False):
    if not newLine:
        print(f"\r{message}", end="", flush=True)
        time.sleep(sleepTime)
    else:
        print(f"\r{message}\n\n", end="")


def refreshUsageData():
    try:
        print("\033[?25l", end="")
        startTime = time.time()
        tryCount = 1
        checkCount = 4
        while time.time() - startTime < 20:
            newData = fetchData(os.getenv("USAGE_URL"))
            if newData is not None:
                try:
                    with open("./usage.json", "r") as file:
                        try:
                            localData = json.load(file)
                        except json.JSONDecodeError:
                            localData = []
                except FileNotFoundError:
                    localData = []

                if len(newData) > len(localData):
                    updateLocalData("./usage.json", newData)
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
                printAndClear("Failed to fetch new data. Retrying...", 5)
                tryCount += 1
                checkCount -= 1

        printAndClear(
            "No new usage data detected. Token usage remains the same.", newLine=True
        )
        showTokenUsage()
    finally:
        print("\033[?25h", end="")


if __name__ == "__main__":
    refreshUsageData()
