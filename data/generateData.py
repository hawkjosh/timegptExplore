import pandas as pd
import numpy as np


def generate_basic_data(start_date, end_date, low_val, high_val, filename):

    dates = pd.date_range(start=start_date, end=end_date)

    np.random.seed(1)
    vals = np.random.uniform(low_val, high_val, size=len(dates))

    data = pd.DataFrame({"timestamp": dates, "value": vals})

    data.to_csv(f"../../data/generated/{filename}", index=False)

    return data


def generate_data_with_ex_vars(
    start_date,
    end_date,
    low_val,
    high_val,
    num_ex_vars,
    low_ex_var,
    high_ex_var,
    filename,
):
    dates = pd.date_range(start=start_date, end=end_date)

    np.random.seed(1)
    vals = np.random.uniform(low=low_val, high=high_val, size=len(dates))

    data = pd.DataFrame({"timestamp": dates, "value": vals})

    for i in range(num_ex_vars):
        ex_var_data = np.random.uniform(
            low=low_ex_var, high=high_ex_var, size=len(dates)
        )
        data[f"ex_var_{i+1}"] = ex_var_data

    data.to_csv(f"../../data/generated/{filename}", index=False)

    return data

# if __name__ == "__main__":
#     generate_basic_data("2021-01-01", "2021-12-31", 0, 100, "basic_data.csv")
#     generate_data_with_ex_vars(
#         "2021-01-01", "2021-12-31", 0, 100, 3, 0, 100, "data_with_ex_vars.csv"
#     )
