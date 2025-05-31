def get_summary_stats(df):
    df_noMNN = df.drop(columns=['Mã ngoại ngữ'])
    so_thi_sinh = df.shape[0]
    so_mon_thi = df_noMNN.shape[1] - 1
    co_diem = df[df["Toán"] > 0].shape[0]
    khong_diem = df[df["Toán"] == 0].shape[0]
    return so_thi_sinh, so_mon_thi, co_diem, khong_diem

def calculate_average_scores(df):
    average_scores = df.mean().round(2)
    return average_scores
