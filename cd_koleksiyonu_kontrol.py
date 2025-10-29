import streamlit as st
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

# ---------------- GÖRSELLERİ BASE64’E ÇEVİRME ----------------
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_base64 = get_base64_image("arka_plan.JPG")
cd_base64 = get_base64_image("cd_disk.png")

# ---------------- CSS TASARIM ----------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');

/* --- GENEL TASARIM --- */
.stApp {{
  background: linear-gradient(rgba(0,0,0,0.35), rgba(0,0,0,0.75)),
              url("data:image/jpg;base64,{bg_base64}");
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  color: #fff9e6;
  font-family: 'Poppins', sans-serif;
  padding-top: 180px !important;   /* 🔽 ANA DÜZENİ AŞAĞI ÇEKİYORUZ */
  overflow: hidden;
}}

/* --- BAŞLIK --- */
.title {{
  text-align: center;
  font-size: 54px;
  font-weight: 700;
  background: linear-gradient(90deg, #fff8d6, #ffd700, #ffb84c, #fff6b0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
  animation: fadeInTitle 2s ease-out forwards;
  margin-bottom: -100px;   /* CD’ye biraz daha yakın */
}}

@keyframes fadeInTitle {{
  0% {{ opacity: 0; transform: translateY(-20px); }}
  100% {{ opacity: 1; transform: translateY(0); }}
}}

/* --- SAHNE --- */
.scene {{
  position: relative;
  width: 100%;
  height: 160px;
  margin: 100px auto 50px auto; /* 🔽 Aşağı doğru daha fazla boşluk */
  overflow: hidden;
}}

/* --- CD YUVARLANMA ANİMASYONU --- */
.cd {{
  position: absolute;
  bottom: 10px;
  left: -120px;
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: url("data:image/png;base64,{cd_base64}") no-repeat center/cover;
  animation: rollAcross 8s linear infinite;
  box-shadow: 0 0 20px rgba(255,255,255,0.5);
  z-index: 3;
}}

@keyframes rollAcross {{
  0% {{
    left: -150px;
    transform: rotate(0deg) translateY(0);
  }}
  25% {{
    transform: rotate(360deg) translateY(-8px);
  }}
  50% {{
    left: 50%;
    transform: rotate(720deg) translateY(0);
  }}
  75% {{
    transform: rotate(1080deg) translateY(-8px);
  }}
  100% {{
    left: 110%;
    transform: rotate(1440deg) translateY(0);
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
  padding: 14px 20px !important;
  color: #3b2f2f !important;
  font-size: 18px !important;
  text-align: center !important;
  font-weight: 500 !important;
  box-shadow: 0 0 12px rgba(255,200,100,0.4);
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
  font-size: 17px;
  border-radius: 40px;
  border: none;
  padding: 8px 22px;
  margin-top: 6px;
  box-shadow: 0 0 18px rgba(255,136,0,0.3);
  transition: all 0.25s ease-in-out;
}}
div.stButton > button:hover {{
  background: linear-gradient(135deg, #ffdd91, #ffb84c);
  transform: scale(1.05);
  box-shadow: 0 0 22px rgba(255,200,100,0.6);
}}

/* --- KOLEKSİYON --- */
.dvd-list {{
  background: rgba(0, 0, 0, 0.55);
  padding: 15px 20px;
  border-radius: 12px;
  border: 1px solid rgba(255, 216, 128, 0.4);
  margin-top: 10px;
  box-shadow: inset 0 0 10px rgba(255,255,255,0.05);
}}
.dvd-item {{
  padding: 5px 0;
  font-size: 16px;
  border-bottom: 1px dashed rgba(255, 215, 128, 0.2);
}}
.dvd-num {{
  color: #ffdd91;
  font-weight: bold;
}}
.collection-title {{
  font-size: 24px;
  color: #ffe6b3;
  font-weight: 600;
  text-align: center;
  margin-bottom: 15px;
}}
</style>
""", unsafe_allow_html=True)



# ---------------- BAŞLIK VE SAHNE ----------------
st.markdown("""
<div class='title'>Tuğgen’in DVD Koleksiyonu </div>
<div class='scene'>
  <div class='cd'></div>
</div>
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
