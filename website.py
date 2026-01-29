import streamlit as st
import boto3

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Mistik Yapay Zeka Falcısı", page_icon="🔮", layout="centered")

# --- 2. MİSTİK TASARIM (CSS) ---
# Burası sitenin makyajı. Arka planı, renkleri ve kutuları ayarlıyor.
st.markdown("""
<style>
    /* Arka Plan: Koyu Mor ve Gece Mavisi Geçişli */
    .stApp {
        background: linear-gradient(to bottom, #1a0026, #0d001a, #000000);
        color: #ffffff;
    }
    
    /* Başlık Stili */
    h1 {
        text-align: center;
        color: #d4af37; /* Altın Sarısı */
        text-shadow: 2px 2px 4px #000000;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Yükleme Alanı Stili */
    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #d4af37;
    }

    /* Sonuç Kartları (Kutucuklar) */
    .mistik-kart {
        background-color: rgba(255, 255, 255, 0.1); /* Yarı saydam */
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #9b59b6; /* Mor Çizgi */
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Vurgulu Yazılar */
    .highlight {
        color: #f1c40f; /* Parlak Sarı */
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. BAŞLIK VE GİRİŞ ---
st.title("🔮 Mistik Falcı")
st.markdown("<p style='text-align: center; color: #b2bec3;'>Yüzünün fotoğrafını yükle, ruhunun derinliklerini okuyayım...</p>", unsafe_allow_html=True)

# --- 4. AWS BAĞLANTISI ---
try:
    rekognition = boto3.client(
        'rekognition',
        aws_access_key_id=st.secrets["aws"]["access_key"],
        aws_secret_access_key=st.secrets["aws"]["secret_key"],
        region_name='us-east-1'
    )
except:
    st.error("⚠️ Hata: Büyülü anahtarlar (API Key) eksik! Lütfen Secrets ayarlarını kontrol et.")

# --- 5. FOTOĞRAF YÜKLEME ---
uploaded_file = st.file_uploader("📸 Fotoğrafını Buraya Bırak", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    # Fotoğrafı Ortala ve Göster
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(uploaded_file, caption='Senin Yansıman', use_container_width=True)
    
    # Bekleme Efekti
    with st.spinner("🔮 Küreye bakılıyor... Yıldızlar hizalanıyor..."):
        try:
            image_bytes = uploaded_file.getvalue()
            response = rekognition.detect_faces(
                Image={'Bytes': image_bytes},
                Attributes=['ALL']
            )

            if len(response['FaceDetails']) > 0:
                yuz = response['FaceDetails'][0]
                
                # Verileri Çek
                yas_alt = yuz['AgeRange']['Low']
                yas_ust = yuz['AgeRange']['High']
                duygular = yuz['Emotions']
                baskin_duygu = max(duygular, key=lambda x: x['Confidence'])['Type']
                duygu_guven = int(max(duygular, key=lambda x: x['Confidence'])['Confidence'])

                st.markdown("---")
                
                # --- FAL YORUMLARI ---
                
                # 1. RUH HALİ KARTI
                st.markdown(f"""
                <div class="mistik-kart">
                    <h3>🌙 Ruh Hali Analizi</h3>
                    <p>Baskın Enerji: <span class="highlight">{baskin_duygu}</span> (%{duygu_guven})</p>
                </div>
                """, unsafe_allow_html=True)
                
                if baskin_duygu == 'HAPPY':
                    st.success("🌟 **Yorum:** Yüzünde güneş açmış! Pozitif enerjin o kadar yüksek ki, ekran bile parladı. Bu neşeni koru, etrafındakilere de şifa oluyorsun.")
                elif baskin_duygu == 'SAD':
                    st.info("🌑 **Yorum:** Gözlerinde hüzünlü bir şiir var. İçine attığın dertler yüzüne yansımış. Ama unutma, her gecenin bir sabahı vardır.")
                elif baskin_duygu == 'ANGRY':
                    st.error("🔥 **Yorum:** İçinde fırtınalar kopuyor! Bir şeye çok kızmışsın. Öfke ateştir, dikkat et seni yakmasın. Derin bir nefes al.")
                elif baskin_duygu == 'CALM':
                    st.info("🌊 **Yorum:** Durgun bir su gibisin. Olaylara bilgece bakıyorsun. Seni sinirlendirmek imkansız gibi.")
                else:
                    st.warning("🌪️ **Yorum:** Kafan karışık, duyguların arasında gidip geliyorsun. Biraz dinlenmeye ihtiyacın var.")

                # 2. KARAKTER VE FİZİKSEL KART
                gozluk = "Var" if yuz['Eyeglasses']['Value'] else "Yok"
                gulumseme = "Var" if yuz['Smile']['Value'] else "Yok"
                
                st.markdown(f"""
                <div class="mistik-kart">
                    <h3>🔮 Karakter ve Görünüm</h3>
                    <p>⏳ <b>Tahmini Yaş Aralığı:</b> <span class="highlight">{yas_alt} - {yas_ust}</span></p>
                    <p>👓 <b>Gözlük:</b> {gozluk} (Bilgelik göstergesi mi?)</p>
                    <p>😊 <b>Gülümseme:</b> {gulumseme}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if yuz['Eyeglasses']['Value']:
                    st.write("✒️ *Gözlüklerin sana entelektüel bir hava katmış. Detayları gören birisin.*")
                
                if not yuz['Smile']['Value']:
                    st.write("🛡️ *Ciddi duruşun, insanlara karşı bir kalkan oluşturduğunu gösteriyor. Güvenini kazanmak zor.*")

            else:
                st.error("🚫 Fotoğrafta yüz göremedim! Belki de çok gizemli birisin? (Lütfen yüzünün net olduğu bir foto yükle)")

        except Exception as e:
            st.error(f"Sihirli kürede bir çatlak oluştu: {e}")