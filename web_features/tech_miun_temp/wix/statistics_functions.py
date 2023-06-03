import pandas as pd
import numpy as np

def no_func(data: pd.Series):
    return data

def mean(data: pd.Series):
    return data.mean()

def std(data: pd.Series):
   return data.std()

STATISTICS_FUNCTIONS = {
    'no_func': no_func,
    'mean': mean,
    'std': std,
}




