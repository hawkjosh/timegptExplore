import os
import time
import requests
from dotenv import load_dotenv
from UsageDb import initializeDb, insertData, fetchLastTimestamp
from UsageDisplayForDb import showTokenUsage

load_dotenv()

url = os.getenv("USAGE_URL")


def fetchData(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def updateUsageDb(newData):
    initializeDb()
    insertData(newData)
    printAndClear("Token usage successfully updated with new data.", newLine=True)
    showTokenUsage()


def refreshUsageData():
    initializeDb()
    tryCount = 1
    checkCount = 4
    while tryCount <= checkCount:
        newData = fetchData(url)
        if newData:
            lastTimestamp = fetchLastTimestamp()

            if any(
                item["created_at"] > lastTimestamp
                for item in newData
                if lastTimestamp is not None
            ):
                insertData(newData)
                printAndClear(
                    "Token usage successfully updated with new data.", newLine=True
                )
                showTokenUsage()
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
            checkCount -= 1
    printAndClear(
        "No new usage data detected. Token usage remains the same.", newLine=True
    )
    showTokenUsage()


def printAndClear(message, sleepTime=1, newLine=False):
    if not newLine:
        print(f"\r{message}", end="", flush=True)
        time.sleep(sleepTime)
    else:
        print(f"\r{message}\n\n", end="")


if __name__ == "__main__":
    refreshUsageData()
