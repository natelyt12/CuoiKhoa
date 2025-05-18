# Import
import pandas as pd
import numpy as np
import streamlit as st

# Đọc file
main_data = pd.read_csv("diem_thi_thpt_2024.csv")

# Lọc NaN
main_data.fillna(0, inplace = True)
main_data.rename(columns = {'sbd': 'SBD', 'toan': 'Toán', 'ngu_van': 'Ngữ văn', 'ngoai_ngu': 'Ngoại ngữ', 'vat_li': 'Vật Lí', 'hoa_hoc': 'Hóa học', 'sinh_hoc': 'Sinh học', 'lich_su': 'Lịch sử', 'dia_li': 'Địa lí', 'gdcd': 'GDCD', 'ma_ngoai_ngu': 'Mã ngoại ngữ'}, inplace = True)
print(main_data.head(5))
