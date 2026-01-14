
import pandas as pd
import seaborn as sns
import datetime
import numpy as np
from numpy import array
from numpy import argmax
import matplotlib.pyplot as plt
from matplotlib import pyplot
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

input_dataset = pd.read_csv("device_db.csv")

# 1.1 Doc du lieu co ban 
# print(input_dataset.head)  # doc 5 phan tu dau tien
# print(input_dataset.describe()) # doc so lieu thong ke
# print(input_dataset.dtypes) # Kieu du lieu cua cot 

# 1.2 Thống kê mô tả với describe()
# desc = input_dataset.describe()
# print(desc)

#1.3 Tạo Column Type DataFrame
# column_info = []
# for col in input_dataset.columns:
#     column_info.append({
#         'column_name': col,
#         'dtype': input_dataset[col].dtype,
#         'unique_count': input_dataset[col].nunique(),
#         'missing_count': input_dataset[col].isna().sum(),
#         'size': input_dataset[col].size
#     })

# column_type_df = pd.DataFrame(column_info)
# print(column_type_df)
 
 # Thong ke cot float64
float_cols  = input_dataset.select_dtypes(include=['float64']).columns
float_stats = []

for col in float_cols:
    float_stats.append({
        'column': col,
        'mean': np.nanmean(input_dataset[col]),
        'median': np.nanmedian(input_dataset[col])
    })

float_stats_df = pd.DataFrame(float_stats)
print(float_stats_df)
