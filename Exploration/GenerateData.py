import pandas as pd
import numpy as np


def generate_basic_data(start_date, end_date, low_val, high_val):
    dates = pd.date_range(start=start_date, end=end_date)

    np.random.seed(1)
    vals = np.random.uniform(low_val, high_val, size=len(dates))

    data = pd.DataFrame({"timestamp": dates, "value": vals})

    return data


def generate_data_with_ex_vars(
    start_date, end_date, low_val, high_val, num_ex_vars, low_ex_var, high_ex_var
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

    return data
