"""Aplikasi Streamlit EcoSurface untuk pendukung pemantauan kualitas air permukaan.

Aplikasi ini memiliki tiga halaman utama:
1. Beranda
2. Panduan Sampling
3. Evaluasi Baku Mutu
4. Tentang Aplikasi

Semua data teknis dikelola di file data/parameter_data.py.
"""

import sys
from pathlib import Path

import streamlit as st

# Pastikan folder aplikasi ditambahkan ke path Python agar import relative bekerja.
ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

from data.parameter_data import baku_mutu, sampling_data

# -----------------------------------------------------------------------------
# Konfigurasi halaman utama Streamlit
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EcoSurface",
    page_icon="🌊",
    layout="wide"
)

# CSS kustom untuk tampilan modern dan responsif.
page_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    color: #1E3A5F;
}

body {
    background: linear-gradient(180deg, #F6FEFF 0%, #F0FAFF 100%);
}

.stApp {
    background-color: transparent;
}

/* Sidebar modern */
[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E5EFF7;
}

/* Card umum */
.custom-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 14px 30px rgba(46, 139, 87, 0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    border-left: 6px solid #2E8B57;
}

.custom-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 22px 40px rgba(46, 139, 87, 0.12);
}

.custom-card-blue {
    border-left-color: #1E90FF;
}

.custom-card-success {
    border-left-color: #2E8B57;
}

.custom-card-danger {
    border-left-color: #E63946;
}

.status-badge {
    display: inline-block;
    padding: 10px 16px;
    border-radius: 999px;
    color: #FFFFFF;
    font-weight: 600;
}

.status-success {
    background: #2E8B57;
}

.status-danger {
    background: #E63946;
}

.metric-label {
    font-size: 1rem !important;
}

.metric-value {
    font-size: 1.8rem !important;
}

/* Responsive small screen */
@media (max-width: 768px) {
    .custom-card {
        padding: 18px;
    }
}
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Fungsi bantu untuk menampilkan kartu status evaluasi
# -----------------------------------------------------------------------------

def render_status_card(title: str, message: str, status: str) -> None:
    """Tampilkan kartu hasil evaluasi dengan warna dan teks yang sesuai."""
    color_class = "status-success" if status == "success" else "status-danger"
    icon = "✅" if status == "success" else "❌"

    st.markdown(
        f"""
        <div class="custom-card {'custom-card-success' if status == 'success' else 'custom-card-danger'}">
            <h3>{icon} {title}</h3>
            <p class="status-badge {color_class}">{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_card(content: str) -> None:
    """Tampilkan kartu informasi umum dengan gaya modern."""
    st.markdown(
        f"""
        <div class="custom-card custom-card-blue">
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# Navigasi sidebar
# -----------------------------------------------------------------------------

st.sidebar.title("🌊 EcoSurface")
st.sidebar.markdown("Sistem Pendukung Pemantauan Kualitas Air")
st.sidebar.markdown("---")

menu_items = [
    "🏠 Beranda",
    "🧪 Panduan Sampling",
    "📊 Evaluasi Baku Mutu",
    "ℹ️ Tentang Aplikasi",
]
selection = st.sidebar.radio("Pilih Halaman", menu_items)

# -----------------------------------------------------------------------------
# Halaman Beranda
# -----------------------------------------------------------------------------
if selection == "🏠 Beranda":
    st.title("🌊 EcoSurface")
    st.markdown("### Sistem Pendukung Pemantauan Kualitas Air Permukaan")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="📋 Parameter Sampling", value=len(sampling_data), delta="Tersedia")
    with col2:
        st.metric(label="⚖️ Baku Mutu", value=len(baku_mutu), delta="Regulasi")
    with col3:
        st.metric(label="🔎 Fitur Utama", value="2", delta="Panduan + Evaluasi")

    st.markdown("---")
    render_info_card(
        """
        <h3>Selamat Datang di EcoSurface</h3>
        <p>EcoSurface membantu pengguna untuk menentukan proses sampling air permukaan,
        memilih bahan pengawet, menyimpan sampel dengan benar, dan mengevaluasi hasil
        analisis terhadap baku mutu yang berlaku.</p>
        <ul>
            <li><strong>Panduan Sampling</strong> untuk parameter air penting.</li>
            <li><strong>Evaluasi Baku Mutu</strong> untuk mengetahui apakah hasil
            memenuhi standar.</li>
        </ul>
        """
    )

    with st.expander("ℹ️ Cara Menggunakan EcoSurface"):
        st.write(
            "Pilih menu di sidebar untuk melihat panduan sampling atau evaluasi baku mutu. "
            "Aplikasi dirancang untuk pembelajaran mahasiswa dan profesional lingkungan."
        )

# -----------------------------------------------------------------------------
# Halaman Panduan Sampling
# -----------------------------------------------------------------------------
elif selection == "🧪 Panduan Sampling":
    st.title("🧪 Panduan Sampling Air Permukaan")
    st.markdown("Pilih parameter untuk melihat rekomendasi wadah, pengawet, dan penyimpanan.")
    st.markdown("---")

    parameter_list = sorted(sampling_data.keys())
    selected_param = st.selectbox("Pilih Parameter Sampling", parameter_list)

    if selected_param:
        info = sampling_data[selected_param]

        with st.container():
            st.markdown(
                f"""
                <div class="custom-card">
                    <h3>🔬 {selected_param}</h3>
                    <p><strong>📦 Jenis Wadah:</strong> {info['wadah']}</p>
                    <p><strong>🧴 Volume Minimum:</strong> {info['volume']}</p>
                    <p><strong>🧪 Bahan Pengawet:</strong> {info['pengawet']}</p>
                    <p><strong>❄️ Suhu Penyimpanan:</strong> {info['penyimpanan']}</p>
                    <p><strong>⏳ Holding Time:</strong> {info['holding_time']}</p>
                    <p><strong>📝 Catatan Tambahan:</strong> {info['catatan']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# -----------------------------------------------------------------------------
# Halaman Evaluasi Baku Mutu
# -----------------------------------------------------------------------------
elif selection == "📊 Evaluasi Baku Mutu":
    st.title("📊 Evaluasi Baku Mutu")
    st.markdown("Input parameter dan nilai analisis untuk mendapatkan status kepatuhan.")
    st.markdown("---")

    param_options = list(baku_mutu.keys())
    selected_param = st.selectbox("Pilih Parameter Evaluasi", param_options)
    input_value = st.number_input(
        "Nilai Hasil Analisis", min_value=0.0, format="%.3f", step=0.1
    )

    if st.button("Evaluasi"):
        standar = baku_mutu[selected_param]
        difference = abs(input_value - standar)

        if selected_param == "DO":
            meets = input_value >= standar
            logic_text = "Parameter minimum: nilai harus lebih besar atau sama dengan baku mutu."
        else:
            meets = input_value <= standar
            logic_text = "Parameter maksimum: nilai harus kurang atau sama dengan baku mutu."

        status_text = "MEMENUHI BAKU MUTU" if meets else "TIDAK MEMENUHI BAKU MUTU"
        status_type = "success" if meets else "danger"
        icon = "✅" if meets else "❌"

        render_status_card(status_text, status_text, status_type)

        with st.container():
            st.markdown(
                f"""
                <div class="custom-card custom-card-blue">
                    <h4>Hasil Evaluasi</h4>
                    <p><strong>Parameter:</strong> {selected_param}</p>
                    <p><strong>Hasil Analisis:</strong> {input_value}</p>
                    <p><strong>Nilai Baku Mutu:</strong> {standar}</p>
                    <p><strong>Selisih Nilai:</strong> {difference:.3f}</p>
                    <p><strong>Logika Evaluasi:</strong> {logic_text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if meets:
            st.success(f"{icon} {selected_param} {status_text}")
        else:
            st.error(f"{icon} {selected_param} {status_text}")

# -----------------------------------------------------------------------------
# Halaman Tentang Aplikasi
# -----------------------------------------------------------------------------
elif selection == "ℹ️ Tentang Aplikasi":
    st.title("ℹ️ Tentang Aplikasi")
    st.markdown("---")

    render_info_card(
        """
        <h3>EcoSurface</h3>
        <p>EcoSurface adalah aplikasi pendukung kegiatan pemantauan kualitas air permukaan yang membantu menentukan kebutuhan sampling,
        pengawetan sampel, penyimpanan, holding time, dan evaluasi hasil analisis berdasarkan baku mutu.</p>
        <p><strong>Teknologi:</strong> Python, Streamlit</p>
        <p><strong>Versi:</strong> 1.0</p>
        <p><strong>Developer:</strong> Mahasiswa Politeknik AKA Bogor</p>
        """
    )

    st.markdown(
        """
        ### Fitur Utama
        - Panduan Sampling untuk berbagai parameter kualitas air.
        - Evaluasi hasil analisis terhadap baku mutu.
        - Antarmuka yang modern, profesional, dan responsif.
        """
    )
