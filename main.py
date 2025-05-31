import streamlit as st
from module.data_handler import load_data
from module.statistics import get_summary_stats, calculate_average_scores
from module.ui_components import show_sidebar_info, show_css_style, show_cards
import plotly.express as px
from PIL import Image

# logo team
logo = Image.open("logo.png")
st.sidebar.image(logo, caption="03 CSA Team", use_container_width=True)

# Load & xử lý dữ liệu
df = load_data()
df_noMNN = df.drop(columns=['Mã ngoại ngữ'])
df_clean = df_noMNN.drop(columns=['SBD'])

# Sidebar + title
show_sidebar_info()
st.title('THPT Quốc Gia 2024')

table_of_contents = st.tabs(["Tổng quan", "Điểm trung bình" , "Thống kê"])
with table_of_contents[0]:
    st.write('Tổng quan dữ liệu:')
    st.write(df.head(10))

    # Tìm SBD
    with st.expander("🔍 Tìm số báo danh", expanded=False):
        sbd_input = st.text_input("Nhập SBD cần tìm (ví dụ: 1000010):")

        if sbd_input:
            if not sbd_input.isdigit():
                st.error("❌ SBD chỉ được chứa chữ số.")
            else:
                sbd_input = sbd_input.strip()
                result = df[df["SBD"].astype(str) == sbd_input]

                if not result.empty:
                    st.success(f"✅ Tìm thấy {len(result)} thí sinh với SBD {sbd_input}:")
                    st.dataframe(result, use_container_width=True)

                    st.download_button(
                        label="📥 Tải kết quả thí sinh",
                        data=result.to_csv(index=False).encode("utf-8"),
                        file_name=f"thisinh_{sbd_input}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ Không tìm thấy thí sinh với SBD này.")



    # Tính thống kê
    so_thi_sinh, so_mon_thi, co_diem, khong_diem = get_summary_stats(df)
    show_css_style()
    show_cards(so_thi_sinh, so_mon_thi, co_diem, khong_diem)

with table_of_contents[2]:
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
        st.success(f"Tìm thấy {len(filtered_df)} học sinh có đủ điểm tổ hợp {chon}")
        st.dataframe(filtered_df[["SBD"] + subjects], use_container_width=True)
        # Biểu đồ điểm trung bình tổ hợp
        avg_combo = filtered_df[subjects].mean()
        fig = px.bar(
            x=subjects,
            y=avg_combo,
            labels={'x': 'Môn', 'y': 'Điểm trung bình'},
            title=f'Biểu đồ điểm trung bình tổ hợp {chon}',
            color_discrete_sequence=['#EF553B']
        )
        st.plotly_chart(fig, use_container_width=True)


with table_of_contents[1]:
    # Trung bình
    st.subheader('Trung bình điểm thi các môn')
    average_scores = calculate_average_scores(df_clean)
    st.dataframe(average_scores, use_container_width=True)
    
    fig = px.bar(
        average_scores,
        x=average_scores.index,
        y=average_scores.values,
        labels={'x': 'Môn thi', 'y': 'Điểm trung bình'},
        title='Biểu đồ điểm trung bình các môn thi',
        color_discrete_sequence=['#636EFA']
    )
    st.plotly_chart(fig, use_container_width=True)
