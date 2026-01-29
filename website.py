import streamlit as st
import boto3
import google.generativeai as genai

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Mistik Psikolog Freud", page_icon="🧙‍♂️", layout="centered")

# --- 2. MİSTİK TASARIM (CSS BÜYÜSÜ) ---
st.markdown("""
<style>
    /* Büyülü Yazı Tipini İçe Aktar */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital@1&display=swap');

    /* Arka Plan Resmi - Mistik Orman ve Dolunay */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('https://images.unsplash.com/photo-1509515837298-2c67a3933321?q=80&w=2576&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #e0e0e0;
        font-family: 'Playfair Display', serif;
    }

    /* Ana Başlık Stili */
    h1 {
        color: #d4af37; /* Altın Sarısı */
        text-align: center;
        font-family: 'Cinzel', serif;
        text-shadow: 0 0 10px #d4af37, 0 0 20px #ff00ff; /* Büyülü parlama */
        font-size: 3em !important;
        margin-bottom: 0px;
    }
    
    /* Alt Başlık */
    .subtitle {
        text-align: center;
        color: #aba1c7;
        font-style: italic;
        margin-bottom: 30px;
    }

    /* Dosya Yükleme Alanı */
    .stFileUploader > div > div {
        background-color: rgba(20, 20, 40, 0.8);
        border: 2px dashed #9b59b6;
        border-radius: 15px;
    }

    /* Analiz Kartı (Cadı Kutusu) */
    .analiz-karti {
        background: rgba(44, 0, 62, 0.85); /* Yarı saydam mor */
        padding: 30px;
        border-radius: 20px;
        border: 3px solid #d4af37;
        box-shadow: 0 0 30px rgba(155, 89, 182, 0.6), inset 0 0 20px rgba(0, 0, 0, 0.5);
        position: relative;
        margin-top: 40px;
        text-align: left;
    }
    
    /* Kartın Tepesindeki Cadı Şapkası İkonu */
    .cadi-sapka {
        position: absolute;
        top: -40px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 60px;
        text-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }

    /* Kart Başlığı */
    .analiz-karti h3 {
        color: #ffcc00;
        font-family: 'Cinzel', serif;
        text-align: center;
        margin-top: 20px;
        border-bottom: 2px solid rgba(212, 175, 55, 0.3);
        padding-bottom: 15px;
    }

    /* Analiz Metni */
    .analiz-metni {
        font-size: 1.2em;
        line-height: 1.8;
        color: #fff;
        font-style: italic;
        padding: 20px;
        background: rgba(0,0,0,0.3);
        border-radius: 10px;
    }

    /* Alt Bilgi */
    .alt-bilgi { 
        color: #c7a1ff; 
        font-size: 12px; 
        text-align: center;
        margin-top: 15px; 
        letter-spacing: 1px;
    }
    
    /* --- UÇAN YARASALAR ANİMASYONU --- */
    @keyframes float {
        0% { transform: translateY(0px) translateX(0px) rotate(0deg); opacity: 0.6; }
        50% { transform: translateY(-20px) translateX(10px) rotate(5deg); opacity: 1; }
        100% { transform: translateY(0px) translateX(0px) rotate(0deg); opacity: 0.6; }
    }
    .floating-bat {
        position: fixed;
        font-size: 40px;
        z-index: 0; /* En arkada dursunlar */
        animation: float 6s ease-in-out infinite;
        filter: drop-shadow(0 0 5px #000);
    }
    .bat1 { top: 10%; left: 5%; animation-delay: 0s; font-size: 30px; }
    .bat2 { top: 20%; right: 10%; animation-delay: 2s; }
    .bat3 { bottom: 15%; left: 15%; animation-delay: 4s; font-size: 50px; }
    .bat4 { bottom: 30%; right: 5%; animation-delay: 1s; font-size: 25px;}

</style>

<div class="floating-bat bat1">🦇</div>
<div class="floating-bat bat2">🦇</div>
<div class="floating-bat bat3">🦇</div>
<div class="floating-bat bat4">🦇</div>

""", unsafe_allow_html=True)

# --- 3. BAŞLIK VE GİRİŞ ---
st.markdown("<h1>🧙‍♂️ Mistik Freud'un Odası 🔮</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Fotoğrafını karanlık küreye bırak, ruhunun derinliklerini okuyalım...</p>", unsafe_allow_html=True)


# --- 4. BAĞLANTILARI KUR ---
try:
    # AWS Bağlantısı (Gözler)
    rekognition = boto3.client(
        'rekognition',
        aws_access_key_id=st.secrets["aws"]["access_key"],
        aws_secret_access_key=st.secrets["aws"]["secret_key"],
        region_name=st.secrets["aws"]["region_name"]
    )
    
    # Google Gemini Bağlantısı (Beyin)
    genai.configure(api_key=st.secrets["google"]["api_key"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
except Exception as e:
    st.error(f"⚠️ Büyü bozuldu! Bağlantı hatası: {e}")

# --- 5. İŞLEM ---
uploaded_file = st.file_uploader("Ruhunun yansımasını (fotoğrafını) buraya yükle...", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    # Fotoğrafı ortala
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(uploaded_file, caption='Senin Yansıman', use_container_width=True)
    
    with st.spinner("🌙 Ay ışığı yüzüne vuruyor... Mistik güçler analiz ediyor..."):
        try:
            # A) AWS İLE GÖR
            image_bytes = uploaded_file.getvalue()
            response = rekognition.detect_faces(Image={'Bytes': image_bytes}, Attributes=['ALL'])

            if len(response['FaceDetails']) > 0:
                yuz = response['FaceDetails'][0]
                
                # AWS'den gelen teknik veriler
                yas = f"{yuz['AgeRange']['Low']}-{yuz['AgeRange']['High']}"
                duygu_ham = max(yuz['Emotions'], key=lambda x: x['Confidence'])['Type']
                guven = int(max(yuz['Emotions'], key=lambda x: x['Confidence'])['Confidence'])
                gulumseme = "Var" if yuz['Smile']['Value'] else "Yok"
                
                # B) GEMINI İLE YORUMLA (Prompt - Daha Mistik)
                prompt = f"""
                Sen, yüzyıllardır yaşayan, insan ruhunu okuyan mistik ve biraz karanlık bir kahin-psikologsun (Sigmund Freud'un büyücü versiyonu gibi).
                Karşındaki ruhun (fotoğraftaki kişinin) dünyevi verileri şunlar:
                - Biyolojik Yaş Aralığı: {yas}
                - Yüzüne Yansıyan Baskın Duygu: {duygu_ham} (Eminlik: %{guven})
                - Gülümseme Maskesi: {gulumseme}

                Lütfen bu verileri kullanarak bu kişiye "Sen" diliyle hitap eden, 3-4 cümlelik
                gizemli, edebi ve derin bir ruh analizi yap. Karanlık metaforlar kullan.
                Sadece teknik veriyi söyleme, bu maskenin ardındaki gerçek hisleri açığa çıkar.
                """
                
                ai_cevap = model.generate_content(prompt)
                
                # C) SONUCU GÖSTER (Mistik Kart)
                st.markdown(f"""
                <div class="analiz-karti">
                    <div class="cadi-sapka">🧙‍♀️</div>
                    <h3>🔮 Kahinin Kehaneti:</h3>
                    <p class="analiz-metni">"{ai_cevap.text}"</p>
                    <p class="alt-bilgi">🌙 Algılanan Enerji: {duygu_ham} (%{guven}) | Yaşam Döngüsü: {yas}</p>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.warning("🌑 Karanlıkta yüzünü seçemedim. Daha aydınlık bir yansıma gönder.")

        except Exception as e:
            st.error(f"Bir hata oluştu, kristal küre çatladı: {e}")