import streamlit as st
from pathlib import Path
import math
import base64
import gspread
from google.oauth2.service_account import Credentials
import json

# ---------------- GOOGLE SHEETS BAĞLANTISI ----------------
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
service_account_info = json.loads(st.secrets["google"]["credentials"])
CREDS = Credentials.from_service_account_info(service_account_info, scopes=SCOPE)
client = gspread.authorize(CREDS)

SHEET_ID = "1BdB5_Bu_JFbCEy1ZYB3Dn1JCnCRqNaa7ncsdmGPMyNA"
sheet = client.open_by_key(SHEET_ID).sheet1

@st.cache_data(ttl=60)
def get_cd_list():
    return sheet.col_values(1)[1:]

cd_list = get_cd_list()

# ---------------- SAYFA YAPILANDIRMASI ----------------
st.set_page_config(
    page_title="Tuğgen'in DVD Koleksiyonu",
    page_icon="💿",
    layout="centered"
)

# ---------------- ARKA PLAN FOTOĞRAFI ----------------
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

image_base64 = get_base64_image("arka_plan.JPG")

# ---------------- CSS TASARIM ----------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Poppins:wght@400;600&display=swap');

/* --- GENEL TASARIM --- */
.stApp {{
    background: linear-gradient(rgba(0,0,0,0.35), rgba(0,0,0,0.75)),
                url("data:image/jpg;base64,{image_base64}");
    background-size: cover;
    background-position: left center; 
    background-attachment: fixed;
    color: #fff9e6;
    font-family: 'Poppins', sans-serif;
    overflow-x: hidden;
    padding-top: 100px !important;
}}

/* --- BAŞLIK --- */
.title {{
    text-align: center;
    font-family: 'Great Vibes', cursive;
    font-size: 64px;
    color: #ffebad;
    text-shadow: 0 0 18px rgba(255,220,120,0.9), 0 0 40px rgba(255,180,50,0.4);
    margin-bottom: 10px;
}}

/* --- ARAMA KUTUSU --- */
div[data-testid="stTextInputRoot"] > div:first-child {{
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
}}

input[type="text"] {{
    background-color: rgba(255,255,255,0.95) !important;
    border: 3px solid #ffb84c !important;
    border-radius: 18px !important;
    padding: 16px 22px !important;
    color: #3b2f2f !important;
    font-size: 20px !important;
    text-align: center !important;
    font-weight: 500 !important;
    box-shadow: 0 0 14px rgba(255,200,100,0.4);
}}

input[type="text"]::placeholder {{
    color: #6b4a12 !important;
    opacity: 0.85 !important;
    font-style: italic;
}}

/* --- BUTONLAR --- */
div.stButton > button:first-child {{
    background: linear-gradient(135deg, #ffb84c 0%, #ff8800 100%);
    color: #1b0e0e;
    font-weight: bold;
    font-size: 18px;
    border-radius: 50px;
    border: none;
    padding: 10px 25px;
    margin-top: 10px;
    box-shadow: 0 0 20px rgba(255,136,0,0.3);
    transition: all 0.25s ease-in-out;
}}
div.stButton > button:hover {{
    background: linear-gradient(135deg, #ffdd91, #ffb84c);
    transform: scale(1.05);
    box-shadow: 0 0 25px rgba(255,200,100,0.6);
}}

/* --- KOLEKSİYON GÖRÜNÜMÜ --- */
.cd-list {{
    background: rgba(0, 0, 0, 0.55);
    padding: 15px 20px;
    border-radius: 12px;
    border: 1px solid rgba(255, 216, 128, 0.4);
    margin-top: 10px;
    box-shadow: inset 0 0 10px rgba(255,255,255,0.05);
}}
.cd-item {{
    padding: 6px 0;
    font-size: 17px;
    border-bottom: 1px dashed rgba(255, 215, 128, 0.2);
}}
.cd-num {{
    color: #ffdd91;
    font-weight: bold;
}}
.collection-title {{
    font-size: 28px;
    color: #ffe6b3;
    font-weight: 600;
    text-align: center;
    margin-bottom: 20px;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- STREAMLIT MANTIK ----------------
DATA_FILE = Path("cd_listesi.txt")
if not DATA_FILE.exists():
    DATA_FILE.touch()

if "cd_yok" not in st.session_state:
    st.session_state.cd_yok = False
if "arama_sonucu" not in st.session_state:
    st.session_state.arama_sonucu = None
if "aranan_cd" not in st.session_state:
    st.session_state.aranan_cd = ""
if "eslesenler" not in st.session_state:
    st.session_state.eslesenler = []

st.markdown("<div style='height:160px;'></div>", unsafe_allow_html=True)

# --- BAŞLIK ---
st.markdown("<h1 class='title'>Tuğgen’in DVD Koleksiyonu 💿</h1>", unsafe_allow_html=True)

# --- LABEL ---
st.markdown("""
<div style='text-align:left; margin-left:10px; margin-top:0px; margin-bottom:-200px;'>
    <label style='font-size:20px; font-weight:700; color:#ffec9e;
    text-shadow:0 0 6px rgba(255,230,150,0.6);
    letter-spacing:0.3px; display:block;'>
        CD ismini gir:
    </label>
</div>
""", unsafe_allow_html=True)

# --- GİRİŞ ALANI ---
query = st.text_input("", placeholder="örnek: Matrix, Titanic, Harry Potter...")

# --- ARAMA BUTONU ---
if st.button("CD Ara"):
    if not query.strip():
        st.warning("CD ismi girsene slk krdsm!!!")
    else:
        st.session_state.aranan_cd = query.strip()
        query_lower = query.lower()
        matches = [cd for cd in cd_list if query_lower in cd.lower()]

        if matches:
            st.session_state.cd_yok = False
            st.session_state.eslesenler = matches
            st.session_state.arama_sonucu = ("Bu CD zaten var krdsm", "success")  # 🟢
        else:
            st.session_state.cd_yok = True
            st.session_state.eslesenler = []
            st.session_state.arama_sonucu = ("Bu CD yok al hemen go go go!!!", "error")  # 🔴

# --- SONUÇ GÖRÜNÜMÜ ---
if st.session_state.arama_sonucu:
    msg, status = st.session_state.arama_sonucu

    if st.session_state.cd_yok:
        if status == "error":
            st.error(msg)
        else:
            st.success(msg)

        if st.button("Koleksiyona Ekle ➕"):
            sheet.append_row([st.session_state.aranan_cd])
            st.success(f"✅ {st.session_state.aranan_cd} başarıyla eklendi! 🎞️")
            st.session_state.cd_yok = False
            st.session_state.arama_sonucu = None
    else:
        st.success(msg)
        st.markdown("<div class='cd-list'>", unsafe_allow_html=True)
        for cd in st.session_state.eslesenler:
            st.markdown(f"<div class='cd-item'>• <b>{cd}</b></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# --- TÜM KOLEKSİYONU GÖSTER BUTONU ---
if st.button("Tüm Koleksiyonu Göster"):
    if cd_list:
        sorted_cds = sorted(cd_list, key=lambda x: x.lower())
        total = len(sorted_cds)
        st.markdown(f"<div class='collection-title'>{total} CD</div>", unsafe_allow_html=True)
        midpoint = math.ceil(total / 2)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='cd-list'>", unsafe_allow_html=True)
            for i, cd in enumerate(sorted_cds[:midpoint], 1):
                st.markdown(f"<div class='cd-item'><span class='cd-num'>{i}.</span> {cd}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='cd-list'>", unsafe_allow_html=True)
            for i, cd in enumerate(sorted_cds[midpoint:], midpoint + 1):
                st.markdown(f"<div class='cd-item'><span class='cd-num'>{i}.</span> {cd}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
