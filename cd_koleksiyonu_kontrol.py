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
def get_dvd_list():
    return sheet.col_values(1)[1:]

dvd_list = get_dvd_list()

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
  font-family: 'Poppins', sans-serif;
  font-weight: 700;
  font-size: 68px;
  background: linear-gradient(90deg, #fff8d6, #ffd700, #ffb84c, #fff6b0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
  animation: fadeInTitle 2s ease-out forwards;
  margin-bottom: 40px;
}}

@keyframes fadeInTitle {{
  from {{
    opacity: 0;
    transform: translateY(-30px);
  }}
  to {{
    opacity: 1;
    transform: translateY(0);
  }}
}}

/* --- SAHNE: GERÇEK GÖRSELLERLE CD + TRAY --- */
.scene {{
  position: relative;
  width: 400px;
  height: 250px;
  margin: 0 auto;
  margin-top: 40px;
}}

.cd {{
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%) translateY(0) rotate(0deg);
  width: 120px;
  height: 120px;
  background: url('cd_disk.png') no-repeat center/contain;
  animation: liftAndInsert 5s ease-in-out forwards;
  z-index: 3;
}}

.player {{
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  width: 300px;
  height: 120px;
  background: url('dvd_tray.png') no-repeat center/contain;
  background-size: contain;
  z-index: 1;
  animation: trayClose 5s ease-in-out forwards;
}}

@keyframes liftAndInsert {{
  0% {{
    transform: translateX(-50%) translateY(0) rotate(0deg);
    opacity: 0;
  }}
  10% {{
    opacity: 1;
  }}
  50% {{
    transform: translateX(-50%) translateY(-120px) rotate(720deg);
  }}
  70% {{
    transform: translateX(-50%) translateY(-140px) rotate(900deg);
  }}
  85% {{
    transform: translateX(-50%) translateY(-150px) scale(0.95);
  }}
  100% {{
    transform: translateX(-50%) translateY(-160px) scale(0.8);
    opacity: 0.8;
  }}
}}

@keyframes trayClose {{
  0%, 70% {{
    transform: translateX(-50%) scaleX(1);
  }}
  100% {{
    transform: translateX(-50%) scaleX(0.3);
    opacity: 0.7;
  }}
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

/* --- SİL BUTONU (Kırmızı) --- */
div.stButton > button:has(span:contains("Sil")) {{
    background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%) !important;
    color: #fff !important;
    font-weight: bold !important;
    border-radius: 20px !important;
    box-shadow: 0 0 15px rgba(255, 60, 60, 0.6);
    transition: all 0.2s ease-in-out;
}}
div.stButton > button:has(span:contains("Sil")):hover {{
    background: linear-gradient(135deg, #ff8888, #ff4444) !important;
    transform: scale(1.05);
}}

/* --- KOLEKSİYON GÖRÜNÜMÜ --- */
.dvd-list {{
    background: rgba(0, 0, 0, 0.55);
    padding: 15px 20px;
    border-radius: 12px;
    border: 1px solid rgba(255, 216, 128, 0.4);
    margin-top: 10px;
    box-shadow: inset 0 0 10px rgba(255,255,255,0.05);
}}
.dvd-item {{
    padding: 6px 0;
    font-size: 17px;
    border-bottom: 1px dashed rgba(255, 215, 128, 0.2);
}}
.dvd-num {{
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
if "dvd_yok" not in st.session_state:
    st.session_state.dvd_yok = False
if "arama_sonucu" not in st.session_state:
    st.session_state.arama_sonucu = None
if "aranan_dvd" not in st.session_state:
    st.session_state.aranan_dvd = ""
if "eslesenler" not in st.session_state:
    st.session_state.eslesenler = []

st.markdown("<div style='height:160px;'></div>", unsafe_allow_html=True)

st.markdown("""
<div class='title'>
  Tuğgen’in DVD Koleksiyonu 💿
</div>

<div class='scene'>
  <div class='player'></div>
  <div class='cd'></div>
</div>
""", unsafe_allow_html=True)






# --- GİRİŞ ALANI ---
query = st.text_input("")

# --- ARAMA BUTONU ---
if st.button("DVD Ara"):
    if not query.strip():
        st.warning("DVD ismi girsene slk krdsm!!!")
    else:
        st.session_state.aranan_dvd = query.strip()
        query_lower = query.lower()
        matches = [dvd for dvd in dvd_list if query_lower in dvd.lower()]

        if matches:
            st.session_state.dvd_yok = False
            st.session_state.eslesenler = matches
            st.session_state.arama_sonucu = ("Bu DVD zaten var krdsm", "success")
        else:
            st.session_state.dvd_yok = True
            st.session_state.eslesenler = []
            st.session_state.arama_sonucu = ("Bu DVD yok al hemen go go go!!!", "error")

# --- SONUÇ GÖRÜNÜMÜ ---
if st.session_state.arama_sonucu:
    msg, status = st.session_state.arama_sonucu

    if st.session_state.dvd_yok:
        st.error(msg)
        if st.button("Koleksiyona Ekle ➕"):
            sheet.append_row([st.session_state.aranan_dvd])
            st.success(f"✅ {st.session_state.aranan_dvd} başarıyla eklendi! 🎞️")
            st.session_state.dvd_yok = False
            st.session_state.arama_sonucu = None
            st.cache_data.clear()
            st.rerun()
    else:
        st.success(msg)
        st.markdown("<div class='dvd-list'>", unsafe_allow_html=True)
        for dvd in st.session_state.eslesenler:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"<div class='dvd-item'>• <b>{dvd}</b></div>", unsafe_allow_html=True)
            with col2:
                if st.button(f"Sil 🗑️", key=f"sil_{dvd}"):
                    rows = sheet.get_all_values()
                    for i, row in enumerate(rows[1:], start=2):
                        if row and row[0].strip().lower() == dvd.lower():
                            sheet.delete_rows(i)
                            st.success(f"✅ '{dvd}' koleksiyondan silindi!")
                            st.cache_data.clear()
                            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- TÜM KOLEKSİYONU GÖSTER BUTONU ---
if st.button("Tüm Koleksiyonu Göster"):
    if dvd_list:
        sorted_dvds = sorted(dvd_list, key=lambda x: x.lower())
        total = len(sorted_dvds)
        st.markdown(f"<div class='collection-title'>{total} DVD</div>", unsafe_allow_html=True)
        midpoint = math.ceil(total / 2)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='dvd-list'>", unsafe_allow_html=True)
            for i, dvd in enumerate(sorted_dvds[:midpoint], 1):
                st.markdown(f"<div class='dvd-item'><span class='dvd-num'>{i}.</span> {dvd}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='dvd-list'>", unsafe_allow_html=True)
            for i, dvd in enumerate(sorted_dvds[midpoint:], midpoint + 1):
                st.markdown(f"<div class='dvd-item'><span class='dvd-num'>{i}.</span> {dvd}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
