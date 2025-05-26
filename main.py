# Import
import pandas as pd
import streamlit as st

# Đọc file
def load_data():
    return pd.read_csv('diem_thi_thpt_2024.csv')

df = load_data()


# Clean data
st.title('THPT Quốc Gia 2024')

# Thay NaN bằng 0 và đổi tên cột
df.fillna(0, inplace = True)
df.rename(columns = {'sbd': 'SBD', 'toan': 'Toán', 'ngu_van': 'Ngữ văn', 'ngoai_ngu': 'Ngoại ngữ', 'vat_li': 'Vật Lí', 'hoa_hoc': 'Hóa học', 'sinh_hoc': 'Sinh học', 'lich_su': 'Lịch sử', 'dia_li': 'Địa lí', 'gdcd': 'GDCD', 'ma_ngoai_ngu': 'Mã ngoại ngữ'}, inplace = True)
df_no_MaNgoaiNgu = df.drop(columns=['Mã ngoại ngữ'], inplace=True)
st.write(df.head(10))

# start ---------------------------------------------------------------------
# Giới thiệu
st.sidebar.title('Giới thiệu')
st.sidebar.write('Ứng dụng này giúp bạn tra cứu điểm thi THPT Quốc Gia 2024.\nỨng dụng được viết nhằm mục đích chuẩn bị cuối khóa CSA của MindX.\n\nThành viên nhóm:\n- Nguyễn Như Hải Đăng\n- Lã Phúc Thanh\n- Lê Trung Kiên')

# Số lượng học sinh
st.markdown(f'### Số lượng học sinh thi THPTQG 2024: **_{df.shape[0]}_**')
# Số lượng môn thi
st.write(f'Số lượng môn thi: **_{df.shape[1] - 1}_**')  # -1 because 'SBD' is not a subject
# Số lượng học sinh có điểm thi
st.write(f'Số lượng học sinh có điểm thi: **_{df[df["Toán"] > 0].shape[0]}_**')
# Số lượng học sinh không có điểm thi
st.write(f'Số lượng học sinh không có điểm thi: **_{df[df["Toán"] == 0].shape[0]}_**')

sbd_input = st.text_input("Nhập SBD cần tìm (ví dụ: 1000010):")

if sbd_input:
    result = df[df["SBD"].astype(str) == sbd_input.strip()]
    if not result.empty:
        st.success(f"Tìm thấy {len(result)} kết quả:")
        st.dataframe(result, use_container_width=True)
    else:
        st.warning("Không tìm thấy thí sinh với SBD này.")
