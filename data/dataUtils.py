import pandas as pd
import numpy as np
import pyperclip as pc


def generateBasicData(startDate, endDate, lowVal, highVal, filename):

    dates = pd.date_range(start=startDate, end=endDate)

    np.random.seed(1)
    vals = np.random.uniform(lowVal, highVal, size=len(dates))

    data = pd.DataFrame({"timestamp": dates, "value": vals})

    data.to_csv(f"../data/generated/{filename}", index=False)

    return data


# # Example Usage:
# generateBasicData(
#     startDate="2021-01-01",
#     endDate="2021-12-31",
#     lowVal=0,
#     highVal=100,
#     filename="basicData.csv",
# )


def generateDataWithExVars(
    startDate,
    endDate,
    lowVal,
    highVal,
    numExVars,
    lowExVar,
    highExVar,
    filename,
):
    dates = pd.date_range(start=startDate, end=endDate)

    np.random.seed(1)
    vals = np.random.uniform(low=lowVal, high=highVal, size=len(dates))

    data = pd.DataFrame({"timestamp": dates, "value": vals})

    for i in range(numExVars):
        exVarData = np.random.uniform(low=lowExVar, high=highExVar, size=len(dates))
        data[f"exVar{i+1}"] = exVarData

    data.to_csv(f"../data/generated/{filename}", index=False)

    return data


# # Example Usage:
# generateDataWithExVars(
#     startDate="2021-01-01",
#     endDate="2021-12-31",
#     lowVal=0,
#     highVal=100,
#     numExVars=3,
#     lowExVar=0,
#     highExVar=100,
#     filename="dataWithExVars.csv",
# )


def generateQuery(
    tenantId,
    daysAgo=None,
    startDate=None,
    endDate=None,
    envExlude="Test",
    meterNameExclude="StgBlockBlobArchivePriorityRetrievalOperationUnitsBilled",
):
    if daysAgo:
        timePeriod = f"""TimePeriod >= ago({daysAgo}d)
        and TimePeriod <= now()"""
    else:
        timePeriod = f"""TimePeriod >= datetime({startDate})
        and TimePeriod <= {"now()" if endDate is None else f"datetime({endDate})"}"""

    query = f"""XStoreAccountBillingDaily
    | where Tenant == "{tenantId}"
        and {timePeriod}
        and Environment != "{envExlude}"
        and isnotempty(MeterId)
    | where StgMeterName != "{meterNameExclude}"
    | summarize ProratedQuantity = sum(ProratedQuantity) by bin(TimePeriod,1d), Tenant
    | project TimePeriod, Tenant, ProratedQuantity"""

    pc.copy(query)
    print(query)


# # Example Usage 1:
# generateQuery(tenantId="MS-DSM06PrdStp04A", daysAgo=180)

# # Example Usage 2:
# generateQuery(tenantId="MS-CBN09PrdStf02C", startDate="2023-09-14", endDate="2024-03-10")

# # Example Usage 3:
# generateQuery(
#     tenantId="MS-CBN09PrdStf02C", startDate="2023-09-14", endDate="2024-03-10"
# )


def dataPrep(df, filename, timeCol, dropCols):
    df = pd.read_csv(f"../data/raw/{filename}.csv")
    df[timeCol] = pd.to_datetime(df[timeCol]).dt.tz_localize(None)
    df = df.drop(columns=dropCols)
    df.to_csv(f"../data/clean/{filename}.csv", index=False)
    df = pd.read_csv(f"../data/clean/{filename}.csv")
    return df


# # Example Usage:
# dataPrep(
#     df="df",
#     filename="billing1",
#     timeCol="TimePeriod",
#     dropCols=["Tenant"],
# )
