import pandas as pd

def load_data():
    df = pd.read_csv('./diem_thi_thpt_2024.csv')
    df.fillna(0, inplace=True)
    df.rename(columns={
        'sbd': 'SBD',
        'toan': 'Toán',
        'ngu_van': 'Ngữ văn',
        'ngoai_ngu': 'Ngoại ngữ',
        'vat_li': 'Vật Lí',
        'hoa_hoc': 'Hóa học',
        'sinh_hoc': 'Sinh học',
        'lich_su': 'Lịch sử',
        'dia_li': 'Địa lí',
        'gdcd': 'GDCD',
        'ma_ngoai_ngu': 'Mã ngoại ngữ'
    }, inplace=True)
    return df
