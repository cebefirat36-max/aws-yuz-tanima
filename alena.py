import streamlit as st

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Для Алёны ❤️", page_icon="💌", layout="centered")

# --- 2. TASARIM VE KALP EFEKTLERİ (CSS) ---
st.markdown("""
<style>
    /* Arka Plan */
    .stApp {
        background: linear-gradient(to bottom, #ff9a9e, #fecfef);
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Kalp Animasyonu */
    @keyframes heart-fall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
    }
    
    .heart {
        position: fixed;
        top: -10vh;
        font-size: 2rem;
        color: #ff0000;
        animation: heart-fall linear infinite;
        z-index: 9999;
    }
    
    .heart:nth-child(1) { left: 10%; animation-duration: 5s; font-size: 3rem; }
    .heart:nth-child(2) { left: 20%; animation-duration: 7s; font-size: 2rem; }
    .heart:nth-child(3) { left: 35%; animation-duration: 4s; font-size: 2.5rem; }
    .heart:nth-child(4) { left: 50%; animation-duration: 6s; font-size: 3.5rem; }
    .heart:nth-child(5) { left: 65%; animation-duration: 5s; font-size: 2rem; }
    .heart:nth-child(6) { left: 80%; animation-duration: 8s; font-size: 4rem; }
    .heart:nth-child(7) { left: 90%; animation-duration: 4s; font-size: 2.5rem; }

    /* Başlıklar */
    h1 {
        color: #d63384;
        text-align: center;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
        margin-bottom: 30px;
    }
    h2 {
        color: #c84b31;
        text-align: center;
        font-style: italic;
    }
    
    /* Rusça Butonlar */
    .stButton>button {
        width: 100%;
        background-color: #ff4757;
        color: white;
        border-radius: 20px;
        height: 75px;
        font-size: 22px !important;
        font-weight: bold;
        border: 2px solid white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff6b81;
        transform: scale(1.05);
    }
    
    /* Final Kutusu */
    .final-box {
        background-color: rgba(255, 255, 255, 0.6);
        padding: 30px;
        border-radius: 20px;
        border: 4px solid #ff4757;
        text-align: center;
        margin-top: 20px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
</style>

<div class="heart">❤️</div><div class="heart">💖</div><div class="heart">💕</div>
<div class="heart">🥰</div><div class="heart">💓</div><div class="heart">😍</div>
<div class="heart">💘</div>
""", unsafe_allow_html=True)

# --- 3. UYGULAMA MANTIĞI ---
if 'adim' not in st.session_state:
    st.session_state.adim = 1

# --- ADIM 1: İLK SORU ---
if st.session_state.adim == 1:
    st.markdown("<h1>Привет, любимая... 🌸</h1>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<h2>У меня к тебе очень важный вопрос...</h2>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='color:#333;'>Ты меня любишь? 🥺</h2>", unsafe_allow_html=True)
        
        if st.button("ДА, КОНЕЧНО! ❤️"): 
            st.session_state.adim = 2
            st.rerun()

# --- ADIM 2: İKİNCİ SORU ---
elif st.session_state.adim == 2:
    st.markdown("<h1>Я так и знал! 🥰</h1>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<h2>А как сильно ты меня любишь? 🤔</h2>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Очень сильно! 🌍"): 
            st.session_state.adim = 3
            st.rerun()
    with col2:
        if st.button("Бесконечно! ♾️"): 
            st.session_state.adim = 3
            st.rerun()

# --- ADIM 3: FİNAL (SÜRPRİZ) ---
elif st.session_state.adim == 3:
    st.balloons()
    
    st.markdown("""
    <div class="final-box">
        <h1 style="font-size: 50px; margin:0;">НЕПРАВИЛЬНО! 😈</h1>
        <h2 style="font-size: 25px; color:#333; margin-top:10px;">Потому что...</h2>
        <h1 style="color:#ff0000; font-size: 35px; margin-top:20px;">Я ЛЮБЛЮ ТЕБЯ БОЛЬШЕ!!! ❤️❤️❤️</h1>
        <p style="font-size:18px; color:#555;">(Ты для меня всё, Алёна)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Aşk fotosu
    st.image("https://images.unsplash.com/photo-1518199266791-5375a83190b7?q=80&w=2600&auto=format&fit=crop", 
             use_container_width=True)
    
    st.write("")
    if st.button("Начать сначала 🔄"): 
        st.session_state.adim = 1
        st.rerun()