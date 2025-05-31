import streamlit as st

def show_sidebar_info():
    st.sidebar.title('Giới thiệu')
    st.sidebar.write(
        'Ứng dụng này giúp bạn tra cứu điểm thi THPT Quốc Gia 2024.\n'
        'Ứng dụng được viết nhằm mục đích chuẩn bị cuối khóa CSA của MindX.\n\n'
        'Thành viên nhóm:\n- Nguyễn Như Hải Đăng\n- Lã Phúc Thanh\n- Lê Trung Kiên'
    )

def show_css_style():
    st.markdown("""
    <style>
        .main-box { text-align: center; }
        .main-title { font-size: 24px; font-weight: 600; color: #ffffff; }
        .big-number { display: inline-block; font-size: 4em; padding: 0px; }
        .small-label { font-size: 1rem; color: #cccccc; margin-bottom: 20px; }
        .card { text-align: center; color: #ffffff; }
        .card-title { font-size: 16px; color: #aaaaaa; }
        .card-value { font-size: 22px; font-weight: bold; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

def show_cards(so_thi_sinh, so_mon_thi, co_diem, khong_diem):
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
