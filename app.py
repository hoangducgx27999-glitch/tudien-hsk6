import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(
    page_title="Từ Điển Quán Dụng Ngữ Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS LÀM ĐẸP (Giao diện Thẻ bài Flashcard)
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .idiom-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 6px solid #3498db;
        transition: transform 0.2s;
    }
    .idiom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.1);
    }
    .hanzi { font-size: 28px; font-weight: 800; color: #2c3e50; font-family: "Microsoft YaHei"; }
    .meaning { font-size: 18px; color: #34495e; margin-top: 5px; font-weight: 500; }
    .tag { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; color: white; margin-left: 5px; }
    .example-box { background-color: #f1f2f6; padding: 10px; border-radius: 8px; margin-top: 12px; font-size: 14px; font-style: italic; color: #57606f; }
</style>
""", unsafe_allow_html=True)

# 3. HÀM ĐỌC DỮ LIỆU
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("data.xlsx")
        df = df.fillna("Không có")
        # Chuyển đổi dữ liệu sang chuỗi
        cols = ['THÀNH NGỮ', 'ĐỘ THÔNG DỤNG', 'CẤU TRÚC', 'SẮC THÁI', 'NGHĨA', 'VÍ DỤ']
        for col in cols:
            if col in df.columns:
                df[col] = df[col].astype(str)
        return df
    except Exception:
        return None

df = load_data()

# 4. GIAO DIỆN CHÍNH
st.title("💎 TỪ ĐIỂN QUÁN DỤNG NGỮ (VISUAL)")
st.markdown("##### *Hệ thống tra cứu & Phân tích ngôn ngữ HSK 6*")

if df is not None:
    # --- BỘ LỌC BÊN TRÁI ---
    with st.sidebar:
        st.header("🎛 BỘ LỌC")
        if 'ĐỘ THÔNG DỤNG' in df.columns:
            all_td = df['ĐỘ THÔNG DỤNG'].unique().tolist()
            chon_td = st.multiselect("Độ thông dụng:", all_td, default=all_td)
        if 'SẮC THÁI' in df.columns:
            all_st = df['SẮC THÁI'].unique().tolist()
            chon_st = st.multiselect("Sắc thái:", all_st, default=all_st)
        st.divider()
        st.info(f"Tổng số từ: {len(df)}")

    # --- TÌM KIẾM ---
    tu_khoa = st.text_input("🔍 TRA CỨU NHANH:", placeholder="Nhập từ cần tìm...")

    # --- XỬ LÝ LỌC ---
    ket_qua = df.copy()
    if 'ĐỘ THÔNG DỤNG' in df.columns: ket_qua = ket_qua[ket_qua['ĐỘ THÔNG DỤNG'].isin(chon_td)]
    if 'SẮC THÁI' in df.columns: ket_qua = ket_qua[ket_qua['SẮC THÁI'].isin(chon_st)]
    
    if tu_khoa:
        ket_qua = ket_qua[
            ket_qua['THÀNH NGỮ'].str.contains(tu_khoa, case=False) |
            ket_qua['NGHĨA'].str.contains(tu_khoa, case=False) |
            ket_qua['VÍ DỤ'].str.contains(tu_khoa, case=False)
        ]

    # --- HIỂN THỊ KẾT QUẢ ---
    if not ket_qua.empty:
        st.success(f"📂 Tìm thấy {len(ket_qua)} kết quả")
        
        tab1, tab2, tab3 = st.tabs(["🎴 Xem dạng Thẻ (Đẹp)", "📋 Xem dạng Bảng", "📊 Biểu đồ"])
        
        # TAB 1: THẺ FLASHCARD
        with tab1:
            for index, row in ket_qua.iterrows():
                # Màu sắc tag
                st_color = "#e74c3c" if "Tiêu cực" in row['SẮC THÁI'] else "#27ae60"
                td_color = "#f39c12" if "Cao" in row['ĐỘ THÔNG DỤNG'] else "#3498db"
                
                st.markdown(f"""
                <div class="idiom-card">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <div class="hanzi">{row['THÀNH NGỮ']}</div>
                            <div class="meaning">👉 {row['NGHĨA']}</div>
                        </div>
                        <div style="text-align: right;">
                            <div class="tag" style="background-color: {td_color};">🔥 {row['ĐỘ THÔNG DỤNG']}</div>
                            <div style="margin-top:5px;"></div>
                            <div class="tag" style="background-color: {st_color};">{row['SẮC THÁI']}</div>
                        </div>
                    </div>
                    <hr style="margin: 10px 0; border: 0; border-top: 1px solid #eee;">
                    <div style="font-size: 13px; color: #7f8c8d;">🧬 Cấu trúc: <b>{row['CẤU TRÚC']}</b></div>
                    <div class="example-box">📝 <b>Ví dụ:</b> {row['VÍ DỤ']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # TAB 2: BẢNG
        with tab2:
            st.dataframe(ket_qua, use_container_width=True, hide_index=True)

        # TAB 3: BIỂU ĐỒ
        with tab3:
            col_a, col_b = st.columns(2)
            with col_a:
                fig1 = px.pie(ket_qua, names='SẮC THÁI', title='Tỷ lệ Sắc thái')
                st.plotly_chart(fig1, use_container_width=True)
            with col_b:
                fig2 = px.bar(ket_qua, x='ĐỘ THÔNG DỤNG', title='Mức độ phổ biến')
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Không tìm thấy kết quả nào!")
else:
    st.error("⚠️ Chưa có file data.xlsx trong thư mục này!")