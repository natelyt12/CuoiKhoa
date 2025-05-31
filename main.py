import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from itertools import islice

# Mấy cái xàm xí
from module.data_handler import load_data
from PIL import Image
# Load & xử lý dữ liệu -----------------------------------------------------------------------
df = load_data()
df_noMNN = df.drop(columns=['Mã ngoại ngữ'])
df_clean = df_noMNN.drop(columns=['SBD'])
mon_thi = ['Toán', 'Vật Lí', 'Hóa học', 'Sinh học', 'Lịch sử', 'Địa lí', 'GDCD', 'Ngoại ngữ', 'Ngữ văn']

# Sidebar + title
st.sidebar.title('Giới thiệu')
st.sidebar.write(
    'Ứng dụng này giúp bạn tra cứu điểm thi THPT Quốc Gia 2024.\n'
    'Ứng dụng được viết nhằm mục đích chuẩn bị cuối khóa CSA của MindX.\n\n'
    'Thành viên nhóm:\n- Nguyễn Như Hải Đăng\n- Lã Phúc Thanh\n- Lê Trung Kiên'
)
st.title('THPT Quốc Gia 2024')

# Phần chính -----------------------------------------------------------------------------------------------
table_of_contents = st.tabs(["Tổng quan", "Điểm trung bình", "Phổ điểm của từng môn học", "Thống kê"])
with table_of_contents[0]: # Tổng quan
    st.write('Tổng quan dữ liệu:')
    st.write(df.head(10))

    # Các môn từng tổ hợp
    khtn = ["Vật Lí", "Hóa học", "Sinh học"]
    khxh = ["Lịch sử", "Địa lí", "GDCD"]
    # Kiểm tra từng thí sinh có thi ít nhất 1 môn của từng tổ hợp hay không
    df_KH = df_clean.copy()
    df_KH['thi_KHTN'] = df_KH[khtn].notnull().any(axis=1)
    df_KH['thi_KHXH'] = df_KH[khxh].notnull().any(axis=1)
    # Đếm số học sinh thi từng tổ hợp
    so_luong_khtn = df_KH['thi_KHTN'].sum()
    so_luong_khxh = df_KH['thi_KHXH'].sum()

    # Card to đầu tiên
    st.markdown(f"""
    <div style='background-color: transparent; padding: 30px; text-align: center; margin-bottom: 30px;'>
        <div style='font-size: 20px; color: white;'>Số thí sinh thi THPTQG 2024</div>
        <div style='font-size: 60px; color: white;'>{df_clean.shape[0]:,}</div>
    </div>
    """, unsafe_allow_html=True)

    # Card nhỏ (danh sách key-value)
    cards = {
        "Số môn thi": df_clean.shape[1],
        "Số học sinh thi KHTN": so_luong_khtn,
        "Số học sinh thi KHXH": so_luong_khxh,
        "Số học sinh thi ngoại ngữ N1": df['Mã ngoại ngữ'].notnull().sum(),
        "Số bài thi bị điểm liệt": (df_clean[mon_thi] <= 1.0).sum().sum(),
        "Số bài thi 0 điểm": (df_clean[mon_thi] == 0.0).sum().sum()
    }

    def chunk_dict(d, n):
        it = iter(d.items())
        for _ in range(0, len(d), n):
            yield dict(islice(it, n))

    # Hiển thị theo dạng lưới
    for row in chunk_dict(cards, 3):  # 3 card mỗi dòng
        cols = st.columns(3)
        for col, (title, value) in zip(cols, row.items()):
            with col:
                st.markdown(f"""
                <div style='background-color: transparent; padding: 20px; border-radius: 12px;
                        margin-bottom: 20px; text-align: center;'>
                    <div style='font-size: 14px; color: white;'>{title}</div>
                    <div style='font-size: 30px; color: white;'>{value}</div>
                </div>
                """, unsafe_allow_html=True)

with table_of_contents[1]: # Điểm trung binh
    average_scores = df_clean.mean().round(2)
    # Tìm SBD
    with st.expander("🔍 Tìm số báo danh", expanded=False):
        sbd_input = st.text_input("Nhập SBD cần tìm (ví dụ: 1000010):")

        if sbd_input:
            result = df[df["SBD"].astype(str) == sbd_input.strip()]
            if not result.empty:
                st.success(f"Tìm thấy {len(result)} kết quả:")
                st.dataframe(result, use_container_width=True)
                if result['Hóa học'].sum() == 0:
                    st.write('Thí sinh này thi khoa học xã hội')
                else:
                    st.write('Thí sinh này thi khoa học tự nhiên')
            else:
                st.warning("Không tìm thấy thí sinh với SBD này.")

    # Trung bình
    st.subheader('Trung bình điểm thi các môn')
    average_scores = average_scores.rename('Điểm trung bình')
    st.dataframe(average_scores, use_container_width=True)
    
    fig = px.bar(
        average_scores,
        x=average_scores.index,
        y=average_scores.values,
        labels={'index': 'Môn thi', 'y': 'Điểm trung bình'},
        title='Biểu đồ điểm trung bình các môn thi',
        color_discrete_sequence=["#FFAEE0"],
        text_auto=True
    )

    # Thêm biểu đồ đường
    fig.add_trace(go.Scatter(
        x=average_scores.index,
        y=average_scores,  # Dữ liệu cho biểu đồ đường
        mode='lines',
        line_color="#FF8A86",
        line_width=2,
        name='Độ dốc'
    ))

    st.plotly_chart(fig, use_container_width=True)

    
    # Môn có điểm trung bình cao nhất
    max_avg_score = average_scores.idxmax()
    st.markdown(f"Môn có điểm trung bình cao nhất là **{max_avg_score}** với điểm trung bình **{average_scores[max_avg_score]}**")
    # Môn có điểm trung bình thấp nhất
    min_avg_score = average_scores.idxmin()
    st.markdown(f"Môn có điểm trung bình thấp nhất là **{min_avg_score}** với điểm trung bình **{average_scores[min_avg_score]}**")
    

    st.subheader("Điểm trung bình của các môn tự nhiên và các môn xã hội")
    # Điểm trung bình của 4 môn tự nhiên
    tb_tu_nhiien = (average_scores['Toán'] + average_scores['Vật Lí'] + average_scores['Hóa học'] + average_scores['Sinh học']) / 4
    st.markdown(f'Điểm trung bình 4 môn tự nhiên: *{tb_tu_nhiien:.2f}*')
    # Điểm trung bình của 4 môn xã hội
    tb_xa_hoi = (average_scores['Ngữ văn'] + average_scores['Lịch sử'] + average_scores['Địa lí'] + average_scores['GDCD']) / 4
    st.markdown(f'Điểm trung bình 4 môn xã hội: *{tb_xa_hoi:.2f}*')

    if tb_xa_hoi > tb_tu_nhiien:
        st.info("Khối xã hội năm 2024 có điểm trung bình cao hơn khối tự nhiên.")
    else:
        st.info("Khối tự nhiên năm 2024 có điểm trung bình nhỉnh hơn khối xã hội.")

    # vẽ biểu đồ so sánh điểm trung bình 4 môn tự nhiên với 4 môn xã hội
    fig = px.bar(
        x=['4 môn tự nhiên', '4 môn xã hội'],
        y=[tb_tu_nhiien, tb_xa_hoi],
        labels={'x': 'Môn', 'y': 'Điểm trung bình'},
        title='Biểu đồ so sánh điểm trung bình 4 môn tự nhiên với 4 môn xã hội',
        color_discrete_sequence=["#AEF3FF"],
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

with table_of_contents[2]: # Phổ điểm và thông tin khác
    # Phổ điểm từng môn
    st.header("Thông tin chi tiết của môn học")
    mon_list = list(df_noMNN.columns)
    mon_list.remove("SBD")
    chon_mon = st.selectbox("Chọn môn học để bắt đầu xem thông tin chi tiết:", mon_list)

    if chon_mon:
        mon_data = df_clean[df_clean[chon_mon] > 0][chon_mon]
        st.success(f"Tìm thấy {len(mon_data)} học sinh có điểm môn {chon_mon}")
        fig = px.histogram(
            mon_data,
            x=chon_mon,
            nbins=20,
            title=f"Phân bố điểm môn {chon_mon}",
            color_discrete_sequence=["#5BBDFF"]
        )
        st.plotly_chart(fig, use_container_width=True)

with table_of_contents[3]: # Thống kê theo tổ hợp môn
    st.subheader("Phân tích theo tổ hợp môn")
    tohop_dict = {
        "A00": ["Toán", "Vật Lí", "Hóa học"],
        "A01": ["Toán", "Vật Lí", "Ngoại ngữ"],
        "B00": ["Toán", "Sinh học", "Hóa học"],
        "C00": ["Ngữ văn", "Lịch sử", "Địa lí"],
        "D01": ["Ngữ văn", "Toán", "Ngoại ngữ"],
        "D02": ["Ngữ văn", "Toán", "Lịch sử"],
        "D03": ["Ngữ văn", "Toán", "Sinh học"],
        "D04": ["Ngữ văn", "Toán", "Địa lí"],
        "D05": ["Ngữ văn", "Toán", "GDCD"]
    }
    
    chon = st.selectbox("Chọn tổ hợp môn:", list(tohop_dict.keys()))
    if chon:
        subjects = tohop_dict[chon]
        filtered_df = df.copy()
        for subj in subjects:
            filtered_df = filtered_df[filtered_df[subj] > 0]
        st.success(f"Tìm thấy {len(filtered_df)} học sinh thi tổ hợp {chon}")
        st.dataframe(filtered_df[["SBD"] + subjects], use_container_width=True)