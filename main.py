# Import
import pandas as pd
import streamlit as st

# Đọc file
def load_data():
    return pd.read_csv('diem_thi_thpt_2024.csv')

df = load_data()

# Clean data
# Thay NaN bằng 0 và đổi tên cột
df.fillna(0, inplace = True)
df.rename(columns = {'sbd': 'SBD', 'toan': 'Toán', 'ngu_van': 'Ngữ văn', 'ngoai_ngu': 'Ngoại ngữ', 'vat_li': 'Vật Lí', 'hoa_hoc': 'Hóa học', 'sinh_hoc': 'Sinh học', 'lich_su': 'Lịch sử', 'dia_li': 'Địa lí', 'gdcd': 'GDCD', 'ma_ngoai_ngu': 'Mã ngoại ngữ'}, inplace = True)
df_no_MaNgoaiNgu = df.drop(columns=['Mã ngoại ngữ'])

# Tổng quan -----------------------------------------------------------------
# Giới thiệu
st.sidebar.title('Giới thiệu')
st.sidebar.write('Ứng dụng này giúp bạn tra cứu điểm thi THPT Quốc Gia 2024.\nỨng dụng được viết nhằm mục đích chuẩn bị cuối khóa CSA của MindX.\n\nThành viên nhóm:\n- Nguyễn Như Hải Đăng\n- Lã Phúc Thanh\n- Lê Trung Kiên')

st.title('THPT Quốc Gia 2024')
st.write('Tổng quan dữ liệu:')
st.write(df.head(10))

# start ---------------------------------------------------------------------
with st.expander("Tìm số báo danh", expanded=False):
    sbd_input = st.text_input("Nhập SBD cần tìm (ví dụ: 1000010):")
    if sbd_input:
        result = df[df["SBD"].astype(str) == sbd_input.strip()]
        if not result.empty:
            st.success(f"Tìm thấy {len(result)} kết quả:")
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("Không tìm thấy thí sinh với SBD này.")

# 2. Biến số liệu
so_thi_sinh = df.shape[0]
so_mon_thi = df_no_MaNgoaiNgu.shape[1] - 1 
co_diem = df[df["Toán"] > 0].shape[0]
khong_diem = df[df["Toán"] == 0].shape[0]  

# define class for styling
st.markdown("""
<style>
    .main-box {
        text-align: center;
    }
    .main-title {
        font-size: 24px;
        font-weight: 600;
        color: #ffffff;
    }
    .big-number {
        display: inline-block;
        font-size: 4em;
        padding: 0px;
    }
    .small-label {
        font-size: 1rem;
        color: #cccccc;
        margin-bottom: 20px;
    }
    .card {
        text-align: center;
        color: #ffffff;
    }
    .card-title {
        font-size: 16px;
        color: #aaaaaa;
    }
    .card-value {
        font-size: 22px;
        font-weight: bold;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# create card layout
st.markdown(f"""
<div class='main-box'>
    <div class='main-title'>Số lượng thí sinh thi THPTQG 2024</div>
    <div class='big-number'>{so_thi_sinh:,}</div>
    <div class='small-label'>thí sinh</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class='card'>
        <div class='card-title'>Số môn thi</div>
        <div class='card-value'>{so_mon_thi:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='card'>
        <div class='card-title'>Thí sinh có điểm</div>
        <div class='card-value'>{co_diem:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='card'>
        <div class='card-title'>Không có điểm</div>
        <div class='card-value' style='color: #FF6961;'>{khong_diem:,}</div>
    </div>
    """, unsafe_allow_html=True)

# Trung bình -----------------------------------------------------------------
st.subheader('Trung bình điểm thi các môn')

# Tính trung bình điểm thi các môn
def calculate_average_scores(df):
    df = df.drop(columns=['SBD'])
    average_scores = df.mean().round(2)
    return average_scores
average_scores = calculate_average_scores(df_no_MaNgoaiNgu)
# Hiển thị trung bình điểm thi các môn
st.dataframe(average_scores, use_container_width=True)

st.bar_chart(average_scores, use_container_width=True, height=500)