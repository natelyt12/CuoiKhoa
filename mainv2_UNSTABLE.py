# Import
import pandas as pd
import streamlit as st
import plotly.express as px

# Thiết lập màu nền trắng
st.set_page_config(page_title="Phân tích điểm thi THPT 2024", layout="wide")

# CSS tuỳ chỉnh màu nền trắng và chữ đen (trở lại mặc định)
st.markdown("""<style>body, .stApp { background-color: white; color: black; }</style>""", unsafe_allow_html=True)

# Đọc file
def load_data():
    return pd.read_csv('diem_thi_thpt_2024.csv')

df = load_data()
tohop_dict = {
    "KHTN (Tự nhiên)": ["Toán", "Vật Lí", "Hóa học", "Sinh học"],
    "KHXH (Xã hội)": ["Toán", "Lịch sử", "Địa lí", "GDCD"],
    "A00": ["Toán", "Vật Lí", "Hóa học"],
    "A01": ["Toán", "Vật Lí", "Ngoại ngữ"],
    "D01": ["Toán", "Ngữ văn", "Ngoại ngữ"],
    "C00": ["Ngữ văn", "Lịch sử", "Địa lí"]
}

# Clean data
df.fillna(0, inplace=True)
df.rename(columns={
    'sbd': 'SBD', 'toan': 'Toán', 'ngu_van': 'Ngữ văn', 'ngoai_ngu': 'Ngoại ngữ',
    'vat_li': 'Vật Lí', 'hoa_hoc': 'Hóa học', 'sinh_hoc': 'Sinh học',
    'lich_su': 'Lịch sử', 'dia_li': 'Địa lí', 'gdcd': 'GDCD', 'ma_ngoai_ngu': 'Mã ngoại ngữ'
}, inplace=True)
df_no_MaNgoaiNgu = df.drop(columns=['Mã ngoại ngữ'])

# Sidebar
st.sidebar.title('THPT Quốc Gia 2024')
st.sidebar.write('Ứng dụng này giúp bạn tra cứu điểm thi THPT Quốc Gia 2024.\nỨng dụng được viết nhằm mục đích chuẩn bị cuối khóa CSA của MindX.\n\nThành viên nhóm:\n- Nguyễn Như Hải Đăng\n- Lã Phúc Thanh\n- Lê Trung Kiên')

# Title
st.markdown("""
    <h1 style='text-align: center; color: #00AA66;'>📊 Phân tích điểm thi THPT Quốc Gia 2024</h1>
""", unsafe_allow_html=True)

# Tabs layout
tabs = st.tabs(["Tìm kiếm SBD", "Tổ hợp môn", "Phân tích môn", "Thống kê tổng quan"])

with tabs[0]:
    with st.expander("Tìm số báo danh", expanded=False):
        sbd_input = st.text_input("Nhập SBD cần tìm (ví dụ: 1000010):")
        if sbd_input:
            result = df[df["SBD"].astype(str) == sbd_input.strip()]
            if not result.empty:
                st.success(f"Tìm thấy {len(result)} kết quả:")
                st.dataframe(result, use_container_width=True)
            else:
                st.warning("Không tìm thấy thí sinh với SBD này.")

with tabs[1]:
    st.subheader("Phân tích theo tổ hợp môn")
    chon = st.selectbox("Chọn tổ hợp môn:", list(tohop_dict.keys()))
    if chon:
        subjects = tohop_dict[chon]
        filtered_df = df.copy()
        for subj in subjects:
            filtered_df = filtered_df[filtered_df[subj] > 0]
        st.success(f"Tìm thấy {len(filtered_df)} học sinh có đủ điểm tổ hợp {chon}")
        st.dataframe(filtered_df[["SBD"] + subjects], use_container_width=True)

        rows = (len(subjects) + 1) // 2
        for i in range(rows):
            cols = st.columns(2)
            for j in range(2):
                idx = i * 2 + j
                if idx < len(subjects):
                    subj = subjects[idx]
                    fig = px.histogram(filtered_df, x=subj, nbins=20, title=f"Phân bố điểm môn {subj}", color_discrete_sequence=['#00AA66'])
                    cols[j].plotly_chart(fig, use_container_width=True)

        filtered_df['Tổng tổ hợp'] = filtered_df[subjects].sum(axis=1)
        fig_total = px.histogram(filtered_df, x='Tổng tổ hợp', nbins=30,
                                 title=f"Phân bố tổng điểm tổ hợp {chon}", 
                                 color_discrete_sequence=['#FF6F61'])
        st.plotly_chart(fig_total, use_container_width=True)

with tabs[2]:
    st.subheader("Phân tích theo từng môn")
    mon_list = list(df_no_MaNgoaiNgu.columns)
    mon_list.remove("SBD")
    chon_mon = st.selectbox("Chọn môn để xem biểu đồ:", mon_list)

    if chon_mon:
        mon_data = df[df[chon_mon] > 0][chon_mon]
        st.success(f"Tìm thấy {len(mon_data)} học sinh có điểm môn {chon_mon}")
        fig = px.histogram(mon_data, x=chon_mon, nbins=20, title=f"Phân bố điểm môn {chon_mon}", color_discrete_sequence=['#007ACC'])
        st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    so_thi_sinh = df.shape[0]
    so_mon_thi = df_no_MaNgoaiNgu.shape[1] - 1 
    khong_diem = df[df["Toán"] == 0].shape[0]  

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tổng số thí sinh", f"{so_thi_sinh:,}")
    with col2:
        st.metric("Số môn thi", f"{so_mon_thi}")
    with col3:
        st.metric("Không có điểm Toán", f"{khong_diem}")

    st.subheader("Trung bình điểm các môn")
    def calculate_average_scores(df):
        df = df.drop(columns=['SBD'])
        average_scores = df.mean().round(2)
        return average_scores

    average_scores = calculate_average_scores(df_no_MaNgoaiNgu)
    st.dataframe(average_scores, use_container_width=True)
    st.bar_chart(average_scores, use_container_width=True, height=500)

    st.subheader("Biểu đồ hộp so sánh các môn")
    long_df = df_no_MaNgoaiNgu.melt(id_vars=['SBD'], var_name='Môn', value_name='Điểm')
    fig_box = px.box(long_df, x='Môn', y='Điểm', points='outliers', color='Môn', title='Boxplot điểm các môn')
    st.plotly_chart(fig_box, use_container_width=True)

    st.subheader("Top 10 thí sinh điểm cao nhất (tổng các môn)")
    df_no_MaNgoaiNgu['Tổng điểm'] = df_no_MaNgoaiNgu.drop(columns=['SBD']).sum(axis=1)
    top10 = df_no_MaNgoaiNgu.sort_values(by='Tổng điểm', ascending=False).head(10)
    st.dataframe(top10[['SBD', 'Tổng điểm']], use_container_width=True)
