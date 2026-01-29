import streamlit as st
import boto3
import google.generativeai as genai

# --- 1. TASARIM AYARLARI ---
st.set_page_config(page_title="Mistik Psikolog", page_icon="🧙‍♂️", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap');
    .stApp {
        background-image: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1519074069444-1ba4fff66d16?q=80&w=2574&auto=format&fit=crop');
        background-size: cover;
        color: #e0e0e0;
        font-family: 'Cinzel', serif;
    }
    h1 { color: #d4af37; text-align: center; text-shadow: 0 0 10px #d4af37; font-size: 3em; }
    .analiz-karti {
        background: rgba(40, 0, 60, 0.9);
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #d4af37;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
        margin-top: 30px;
        text-align: center;
    }
    .cadi { font-size: 50px; margin-bottom: 10px; display: block; }
</style>
""", unsafe_allow_html=True)

st.title("🧙‍♂️ Mistik Freud")
st.write("Yüzünü göster, ruhunu okuyalım...")

# --- 2. BAĞLANTILAR (AKILLI MODEL SEÇİCİ) ---
try:
    # A) AWS Bağlantısı
    rekognition = boto3.client(
        'rekognition',
        aws_access_key_id=st.secrets["aws"]["access_key"],
        aws_secret_access_key=st.secrets["aws"]["secret_key"],
        region_name='us-east-1' 
    )
    
    # B) Google Gemini Bağlantısı (OTOMATİK SEÇİM)
    genai.configure(api_key=st.secrets["google"]["api_key"])
    
    # Mevcut modelleri listele ve 'generateContent' yapabilen İLK modeli seç
    try:
        mevcut_modeller = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        secilen_model = mevcut_modeller[0] # Listeden ilk çalışanı al
        model = genai.GenerativeModel(secilen_model)
        # st.success(f"Bağlanan Beyin: {secilen_model}") # (Test için, sonra silinebilir)
    except:
        # Eğer liste alamazsa en garanti eski modele düş
        model = genai.GenerativeModel('gemini-1.0-pro')
    
except Exception as e:
    st.error(f"⚠️ Bağlantı Hatası: {e}")

# --- 3. İŞLEM ---
uploaded_file = st.file_uploader("", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Yansıma', width=300)
    
    with st.spinner("🔮 Küre ısınıyor..."):
        try:
            # AWS Yüz Analizi
            image_bytes = uploaded_file.getvalue()
            response = rekognition.detect_faces(Image={'Bytes': image_bytes}, Attributes=['ALL'])

            if len(response['FaceDetails']) > 0:
                yuz = response['FaceDetails'][0]
                
                # Verileri al
                yas = f"{yuz['AgeRange']['Low']}-{yuz['AgeRange']['High']}"
                duygu = max(yuz['Emotions'], key=lambda x: x['Confidence'])['Type']
                guven = int(max(yuz['Emotions'], key=lambda x: x['Confidence'])['Confidence'])
                gulumseme = "Var" if yuz['Smile']['Value'] else "Yok"
                
                # Gemini Yorumu
                prompt = f"""
                Sen karanlık, mistik bir kahinsin.
                Karşımdaki kişinin özellikleri: Yaş {yas}, Duygu {duygu} (%{guven}), Gülümseme {gulumseme}.
                Buna kısa, gizemli ve etkileyici bir fal bak.
                """
                ai_cevap = model.generate_content(prompt)
                
                # Sonuç
                st.markdown(f"""
                <div class="analiz-karti">
                    <span class="cadi">🔮</span>
                    <h3>Kehanet:</h3>
                    <p style="font-size:18px; font-style:italic;">"{ai_cevap.text}"</p>
                    <hr>
                    <p style="font-size:12px; color:#aaa;">Enerji: {duygu}</p>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.warning("Yüz göremedim!")

        except Exception as e:
            st.error(f"Hata: {e}")