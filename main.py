import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from itertools import islice

# Mấy cái xàm xí
from module.data_handler import load_data
from PIL import Image

st.set_page_config(
    page_title="03 CSA TEAM",
    page_icon="logo.png",  
)

st.title("TEAM NET PY")

# Load & xử lý dữ liệu -----------------------------------------------------------------------
df = load_data()
df_noMNN = df.drop(columns=['Mã ngoại ngữ'])
df_clean = df_noMNN.drop(columns=['SBD'])
mon_thi = ['Toán', 'Vật Lí', 'Hóa học', 'Sinh học', 'Lịch sử', 'Địa lí', 'GDCD', 'Ngoại ngữ', 'Ngữ văn']

# Sidebar + title
st.sidebar.title('Giới thiệu')

# logo team
logo = Image.open("logo.png")
st.sidebar.image(logo, caption="03 CSA Team", use_container_width=True)
st.sidebar.write(
    'Ứng dụng này giúp bạn tra cứu điểm thi THPT Quốc Gia 2024.\n'
    'Ứng dụng được viết nhằm mục đích chuẩn bị cuối khóa CSA của MindX.\n\n'
    'Thành viên nhóm:\n- Nguyễn Như Hải Đăng\n- Lã Phúc Thanh\n- Lê Trung Kiên'
)
st.title('THPT Quốc Gia 2024')

# Phần chính -----------------------------------------------------------------------------------------------
table_of_contents = st.tabs(["Tổng quan", "Điểm trung bình", "Thông tin chi tiết của từng môn học", "Tổ hợp"])
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
                    st.write('Thí sinh này thi KHTN')
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
    fig.update_layout(
        bargap=0.2,
        xaxis_title="Môn thi",
        yaxis_title="Điểm trung bình",
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
    st.markdown(f'*Số lượng học sinh tham gia thi KHTN và KHXH:*')
    fig = go.Figure(
        go.Pie(
            labels=["KHTN", "KHXH"],
            values=[so_luong_khtn, so_luong_khxh],
            textinfo="label+percent",
            textposition="inside",
            marker=dict(colors=["#FFAEE0", "#FF8A86"]),
        )    
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Điểm trung bình của các môn KHTN
    tb_tu_nhiien = (average_scores['Toán'] + average_scores['Vật Lí'] + average_scores['Hóa học'] + average_scores['Sinh học']) / 4
    st.markdown(f'Điểm trung bình các môn KHTN: *{tb_tu_nhiien:.2f}*')
    # Điểm trung bình của các môn KHXH
    tb_xa_hoi = (average_scores['Ngữ văn'] + average_scores['Lịch sử'] + average_scores['Địa lí'] + average_scores['GDCD']) / 4
    st.markdown(f'Điểm trung bình các môn KHXH: *{tb_xa_hoi:.2f}*')

    if tb_xa_hoi > tb_tu_nhiien:
        st.info("Khối xã hội năm 2024 có điểm trung bình cao hơn khối tự nhiên.")
    else:
        st.info("Khối tự nhiên năm 2024 có điểm trung bình nhỉnh hơn khối xã hội.")

with table_of_contents[2]: # Phổ điểm và thông tin khác
    # Phổ điểm từng môn
    chon_mon = st.selectbox("Chọn môn học để bắt đầu xem thông tin chi tiết:", mon_thi)

    if chon_mon:
        st.info(f"Thông tin chi tiết về môn {chon_mon}:")
        # Biểu đồ tròn biểu diễn phần trăm thí sinh tham gia thi môn so với tổng thí sinh
        fig = go.Figure(data=[go.Pie(
            labels=[f'Thí sinh tham gia thi {chon_mon}', f'Thí sinh không tham gia thi {chon_mon}'],
            values=[df_clean[chon_mon].notnull().sum(), df_clean[chon_mon].isnull().sum()],
            textinfo='percent+label',
            textposition='inside',
            insidetextorientation='radial',
            marker=dict(colors=['#AEF3FF', '#FFAEAE']),
        )])
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
        )
        st.plotly_chart(fig, use_container_width=True)


        # Card to đầu tiên
        st.markdown(f"""
        <div style='background-color: transparent; padding: 30px; text-align: center; margin-bottom: 30px;'>
            <div style='font-size: 20px; color: white;'>Số bài thi môn {chon_mon}</div>
            <div style='font-size: 60px; color: white;'>{df_clean[chon_mon].notnull().sum()}</div>
        </div>
        """, unsafe_allow_html=True)

        cards = {
            "Điểm trung bình": average_scores[chon_mon],
            "Số bài thi đạt 10 tuyệt đối": (df[chon_mon] == 10.0).sum(),
            "Số bài thi được 8 điểm trở lên": (df[chon_mon] >= 8.0).sum(),
            "Số bài thi bị điểm liệt": (df[chon_mon] <= 1.0).sum(),
            "Số bài thi 0 điểm": (df[chon_mon] == 0.0).sum(),
            "Trung vị": df[chon_mon].median(),
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

        mon_data = df_clean[df_clean[chon_mon] > 0][chon_mon]
        st.header(f"Phân bố điểm môn {chon_mon}")
        fig = px.histogram(
            mon_data,
            x=chon_mon,
            nbins=60,
            color_discrete_sequence=["#7BCAFF"],
            text_auto=True
        )
        fig.update_layout(
            bargap=0.05,
            xaxis_title="Điểm",
            yaxis_title="Số lượng thí sinh",
        )
        st.plotly_chart(fig, use_container_width=True, key=f"fig_{chon_mon}")

with table_of_contents[3]: # Thống kê theo tổ hợp môn
    st.subheader("Phân tích theo tổ hợp môn")
    tohop_dict = {
        "A00": ["Toán", "Vật Lí", "Hóa học"],
        "A01": ["Toán", "Vật Lí", "Ngoại ngữ"],
        "B00": ["Toán", "Sinh học", "Hóa học"],
        "C00": ["Ngữ văn", "Lịch sử", "Địa lí"],
        "D01": ["Ngữ văn", "Toán", "Ngoại ngữ"],
        "D02": ["Ngữ văn", "Toán", "Lịch sử"],
        "D03": ["Ngữ văn", "Toán", "Sinh học"],
        "D04": ["Ngữ văn", "Toán", "Địa lí"],
        "D05": ["Ngữ văn", "Toán", "GDCD"]
    }
    chon = st.selectbox("Chọn tổ hợp môn:", list(tohop_dict.keys()))
    if chon:
        subjects = tohop_dict[chon]
        filtered_df = df.copy()
        for subj in subjects:
            filtered_df = filtered_df[filtered_df[subj] >= 0]
        st.success(f"Có tất cả {len(filtered_df)} học sinh chọn thi tổ hợp {chon} ({', '.join(subjects)}) - chiếm {round(len(filtered_df) / df.shape[0] * 100, 2)}% tổng thí sinh")
        
        # Tính tổng điểm tổ hợp
        filtered_df["tong_diem"] = filtered_df[subjects].sum(axis=1)

        # Vẽ biểu đồ phổ điểm
        st.markdown("### Biểu đồ phổ điểm tổ hợp")
        st.bar_chart(
            filtered_df["tong_diem"]
            .round(1)  # làm tròn 1 chữ số thập phân để gom nhóm
            .value_counts()
            .sort_index()
        )

        st.markdown(f"""
        <div style='background-color: transparent; padding: 30px; text-align: center; margin-bottom: 30px;'>
            <div style='font-size: 20px; color: white;'>Điểm trung bình của tổ hợp {chon}</div>
            <div style='font-size: 60px; color: white;'>{filtered_df["tong_diem"].mean().round(2)}</div>
        </div>
        """, unsafe_allow_html=True)

        cards = {
            "Điểm tổ hợp cao nhất": filtered_df["tong_diem"].max(),
            "Điểm nhiều thí sinh đạt nhất": filtered_df["tong_diem"].mode().values[0],
            "Trung vị": filtered_df["tong_diem"].median()
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

