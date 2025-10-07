import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ===============================
# ⚙️ KONFIGURASI HALAMAN
# ===============================
st.set_page_config(
    page_title="RGB Matrix Analyzer Pro",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# 🧩 CSS CUSTOM STYLE (MODERN GRADIENT THEME)
# ===============================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-title {
        color: #ffffff;
        font-weight: 700;
        font-size: 42px;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .sub-title {
        color: rgba(255,255,255,0.9);
        font-size: 16px;
        margin-top: 8px;
        font-weight: 300;
    }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        margin-bottom: 15px;
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    
    .stat-label {
        font-size: 13px;
        color: #666;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stat-value {
        font-size: 28px;
        color: #333;
        font-weight: 700;
        margin-top: 5px;
    }
    
    .rgb-preview {
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 3px solid #e0e0e0;
    }
    
    .rgb-value {
        font-size: 20px;
        font-weight: 600;
        margin: 8px 0;
        padding: 8px 12px;
        background: rgba(255,255,255,0.7);
        border-radius: 8px;
        display: inline-block;
    }
    
    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #333;
        margin: 25px 0 15px 0;
        border-left: 5px solid #667eea;
        padding-left: 15px;
    }
    
    .info-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #667eea;
    }
    
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    
    div[data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        border-radius: 12px;
        padding: 20px;
        border: 2px dashed #667eea;
    }
    
    .uploadedFile {
        background: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# ===============================
# 🎯 FUNGSI UTILITAS
# ===============================
def calculate_color_stats(rgb_array):
    """Menghitung statistik warna dari array RGB"""
    return {
        'mean_r': np.mean(rgb_array[:, :, 0]),
        'mean_g': np.mean(rgb_array[:, :, 1]),
        'mean_b': np.mean(rgb_array[:, :, 2]),
        'dominant_color': 'Red' if np.mean(rgb_array[:, :, 0]) > max(np.mean(rgb_array[:, :, 1]), np.mean(rgb_array[:, :, 2])) 
                         else 'Green' if np.mean(rgb_array[:, :, 1]) > np.mean(rgb_array[:, :, 2]) 
                         else 'Blue'
    }

def rgb_to_hex(r, g, b):
    """Konversi RGB ke HEX"""
    return f"#{r:02x}{g:02x}{b:02x}"

def create_color_histogram(rgb_array):
    """Membuat histogram distribusi warna"""
    fig = go.Figure()
    
    colors = ['Red', 'Green', 'Blue']
    for i, color in enumerate(colors):
        fig.add_trace(go.Histogram(
            x=rgb_array[:, :, i].flatten(),
            name=color,
            opacity=0.7,
            marker_color=color.lower()
        ))
    
    fig.update_layout(
        title="Distribusi Nilai RGB",
        xaxis_title="Nilai Pixel",
        yaxis_title="Frekuensi",
        barmode='overlay',
        height=350,
        template="plotly_white",
        hovermode='x unified'
    )
    
    return fig

# ===============================
# 🎨 HEADER
# ===============================
st.markdown("""
    <div class='main-header'>
        <h1 class='main-title'>🎨 Analisis Matrix RGB</h1>
        <p class='sub-title'>Pengolahan Citra | Muhammad Bukhori - 51422002</p>
    </div>
""", unsafe_allow_html=True)

# ===============================
# 📤 SIDEBAR - UPLOAD & SETTINGS
# ===============================
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan Analisis")
    
    uploaded_file = st.file_uploader(
        "📁 Upload Gambar",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
        help="Pilih gambar untuk dianalisis"
    )
    
    st.markdown("---")
    
    if uploaded_file:
        st.markdown("### 🎛️ Opsi Tampilan")
        show_histogram = st.checkbox("📊 Tampilkan Histogram", value=True)
        show_stats = st.checkbox("📈 Tampilkan Statistik", value=True)
        show_matrix = st.checkbox("🔢 Tampilkan Matrix RGB", value=True)
        
        st.markdown("---")
        st.markdown("### 📏 Ukuran Matrix")
        matrix_size = st.slider("Baris/Kolom Matrix", 10, 100, 50, 5)

# ===============================
# 📊 KONTEN UTAMA
# ===============================
if uploaded_file:
    # Memproses gambar
    image = Image.open(uploaded_file).convert("RGB")
    rgb_array = np.array(image)
    color_stats = calculate_color_stats(rgb_array)
    
    # ===============================
    # 📸 PREVIEW GAMBAR & INFO
    # ===============================
    col1, col2 = st.columns([1.2, 1], gap="medium")
    
    with col1:
        st.markdown("<div class='section-title'>🖼️ Preview Gambar</div>", unsafe_allow_html=True)
        st.image(image, use_container_width=True, caption=f"Dimensi: {image.width} × {image.height} pixels")
    
    with col2:
        st.markdown("<div class='section-title'>📊 Informasi Gambar</div>", unsafe_allow_html=True)
        
        # Metric cards
        st.markdown(f"""
            <div class='metric-card'>
                <div class='stat-label'>Lebar</div>
                <div class='stat-value'>{image.width} px</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='metric-card'>
                <div class='stat-label'>Tinggi</div>
                <div class='stat-value'>{image.height} px</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='metric-card'>
                <div class='stat-label'>Total Pixels</div>
                <div class='stat-value'>{image.width * image.height:,}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='metric-card'>
                <div class='stat-label'>Warna Dominan</div>
                <div class='stat-value' style='color: {color_stats["dominant_color"].lower()};'>
                    {color_stats["dominant_color"]}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # ===============================
    # 🎯 PIXEL SELECTOR & COLOR INFO
    # ===============================
    st.markdown("<div class='section-title'>🎯 Analisis Pixel Spesifik</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1.5], gap="medium")
    
    with col1:
        x_val = st.number_input(
            "📍 Koordinat X",
            min_value=0,
            max_value=image.width - 1,
            value=image.width // 2,
            step=1
        )
    
    with col2:
        y_val = st.number_input(
            "📍 Koordinat Y",
            min_value=0,
            max_value=image.height - 1,
            value=image.height // 2,
            step=1
        )
    
    with col3:
        selected_rgb = rgb_array[int(y_val), int(x_val)]
        r, g, b = selected_rgb
        hex_color = rgb_to_hex(r, g, b)
        
        st.markdown(f"""
            <div class='rgb-preview' style='background: linear-gradient(135deg, rgb({r},{g},{b}) 0%, rgba({r},{g},{b},0.3) 100%);'>
                <div style='text-align: center;'>
                    <div class='rgb-value' style='background: rgba(255,255,255,0.9);'>
                        🔴 R: <span style='color: red;'>{r}</span>
                    </div>
                    <div class='rgb-value' style='background: rgba(255,255,255,0.9);'>
                        🟢 G: <span style='color: green;'>{g}</span>
                    </div>
                    <div class='rgb-value' style='background: rgba(255,255,255,0.9);'>
                        🔵 B: <span style='color: blue;'>{b}</span>
                    </div>
                    <div class='rgb-value' style='background: rgba(255,255,255,0.9); margin-top: 10px;'>
                        🎨 HEX: <span style='color: {hex_color};'>{hex_color.upper()}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # ===============================
    # 📊 HISTOGRAM (OPSIONAL)
    # ===============================
    if show_histogram:
        st.markdown("<div class='section-title'>📊 Histogram Distribusi Warna</div>", unsafe_allow_html=True)
        fig = create_color_histogram(rgb_array)
        st.plotly_chart(fig, use_container_width=True)
    
    # ===============================
    # 📈 STATISTIK WARNA (OPSIONAL)
    # ===============================
    if show_stats:
        st.markdown("<div class='section-title'>📈 Statistik Warna</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class='info-box' style='background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);'>
                    <h3 style='color: #d63031; margin: 0;'>🔴 Red Channel</h3>
                    <p style='font-size: 24px; font-weight: 700; margin: 10px 0;'>{color_stats['mean_r']:.2f}</p>
                    <p style='margin: 0; color: #555;'>Rata-rata nilai Red</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class='info-box' style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);'>
                    <h3 style='color: #00b894; margin: 0;'>🟢 Green Channel</h3>
                    <p style='font-size: 24px; font-weight: 700; margin: 10px 0;'>{color_stats['mean_g']:.2f}</p>
                    <p style='margin: 0; color: #555;'>Rata-rata nilai Green</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class='info-box' style='background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);'>
                    <h3 style='color: #0984e3; margin: 0;'>🔵 Blue Channel</h3>
                    <p style='font-size: 24px; font-weight: 700; margin: 10px 0;'>{color_stats['mean_b']:.2f}</p>
                    <p style='margin: 0; color: #555;'>Rata-rata nilai Blue</p>
                </div>
            """, unsafe_allow_html=True)
    
    # ===============================
    # 🔢 RGB MATRIX TABLE (OPSIONAL)
    # ===============================
    if show_matrix:
        st.markdown("<div class='section-title'>🔢 RGB Matrix Data</div>", unsafe_allow_html=True)
        
        # Ambil sample sesuai slider
        sample_rgb = rgb_array[:matrix_size, :matrix_size, :]
        df_rgb = pd.DataFrame(
            [[f"({r},{g},{b})" for r, g, b in row] for row in sample_rgb],
            columns=[f"Col_{i}" for i in range(sample_rgb.shape[1])]
        )
        
        st.dataframe(
            df_rgb,
            use_container_width=True,
            height=400
        )
        
        # Tombol download
        csv = df_rgb.to_csv(index=False)
        st.download_button(
            label="📥 Download Matrix CSV",
            data=csv,
            file_name="rgb_matrix_data.csv",
            mime="text/csv",
        )

else:
    # ===============================
    # 💡 LANDING PAGE
    # ===============================
    st.markdown("""
        <div class='info-box' style='text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;'>
            <h2 style='color: white; margin-bottom: 20px;'>👋 Selamat Datang!</h2>
            <p style='font-size: 18px; margin-bottom: 10px;'>Upload gambar melalui sidebar untuk memulai analisis RGB</p>
            <p style='font-size: 14px; opacity: 0.9;'>✨ Fitur: Pixel Selector, Histogram, Statistik Warna, RGB Matrix Export</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Fitur info cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='metric-card'>
                <h3>🎯 Pixel Analysis</h3>
                <p>Pilih koordinat pixel tertentu dan lihat nilai RGB serta HEX-nya</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='metric-card'>
                <h3>📊 Color Distribution</h3>
                <p>Visualisasi histogram untuk setiap channel warna RGB</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='metric-card'>
                <h3>📥 Data Export</h3>
                <p>Download matrix RGB dalam format CSV untuk analisis lanjutan</p>
            </div>
        """, unsafe_allow_html=True)