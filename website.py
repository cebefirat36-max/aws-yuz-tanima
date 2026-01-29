import streamlit as st
import boto3

# Sayfa Başlığı
st.title("🕵️‍♂️ Fırat'ın Yapay Zeka Dedektifi")
st.write("İki fotoğraf yükleyin, Yapay Zeka (AWS) aynı kişi olup olmadıklarını söylesin!")

# 1. Kullanıcıdan Fotoğraf İsteme
col1, col2 = st.columns(2)
with col1:
    st.header("1. Fotoğraf")
    foto1 = st.file_uploader("Birinci resmi seç", type=['jpg', 'png', 'jpeg'], key="1")

with col2:
    st.header("2. Fotoğraf")
    foto2 = st.file_uploader("İkinci resmi seç", type=['jpg', 'png', 'jpeg'], key="2")

# 2. İşlemi Başlat
if foto1 is not None and foto2 is not None:
    st.success("✅ Fotoğraflar alındı! Analiz ediliyor...")

    try:
        # --- BURASI YENİLENDİ: ARTIK GİZLİ KASADAN OKUYORUZ ---
        # Kodun içine şifre yazmıyoruz, güvenli yöntem bu.
        rekognition = boto3.client(
            'rekognition',
            aws_access_key_id=st.secrets["aws"]["access_key"],
            aws_secret_access_key=st.secrets["aws"]["secret_key"],
            region_name='us-east-1'
        )
        
        # Analiz (Bytes yöntemi ile)
        response = rekognition.compare_faces(
            SourceImage={'Bytes': foto1.getvalue()},
            TargetImage={'Bytes': foto2.getvalue()},
            SimilarityThreshold=0
        )

        # Sonucu Ekrana Bas
        if len(response['FaceMatches']) > 0:
            oran = response['FaceMatches'][0]['Similarity']
            st.balloons()
            st.metric(label="Benzerlik Oranı", value=f"%{oran:.2f}")
            
            if oran > 90:
                st.info("Sonuç: KESİNLİKLE AYNI KİŞİ! ✅")
            elif oran > 70:
                st.warning("Sonuç: Büyük ihtimalle akraba veya aynı kişi. 🤔")
            else:
                st.warning("Sonuç: Biraz benziyor ama emin değilim.")
        else:
            st.error("Sonuç: BU İKİSİ FARKLI KİŞİ! ❌")
            st.metric(label="Benzerlik Oranı", value="%0")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
        st.info("İpucu: Eğer 'KeyError' alıyorsan, Buluttaki Secrets ayarlarını henüz yapmadın demektir.")