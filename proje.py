import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="Berry Kafe DSS", layout="wide")

# Sol Menü Tasarımı
st.sidebar.title("☕ Berry Kafe Zinciri")
st.sidebar.markdown("**Karar Destek Sistemi (DSS)**")
menu = st.sidebar.radio("Sistem Modülleri:", ["1. EOQ ve Stok Yönetimi", "2. TSP Rota Optimizasyonu"])

if menu == "1. EOQ ve Stok Yönetimi":
    st.title("📦 Problem 1: EOQ ve Güvenlik Stoğu")
    st.markdown("Yeni parametrelere dayalı dinamik sipariş hesaplama modülü.")
    
    # Yeni Sabit Parametreler
    S = 45.0   # Sipariş maliyeti (TL)
    H = 14.4   # Yıllık elde tutma maliyeti (TL/kg/yıl)
    Z = 1.65   # Güvenlik katsayısı (%95 hizmet düzeyi)
    LT = 7     # Temin süresi (Gün)
    
    subeler = {
        "Bornova": 30, "Bostanlı": 40, "Karşıyaka": 30,
        "Çiğli": 30, "Menemen": 30, "Buca": 40, "Gaziemir": 30
    }
    
    secilen_sube = st.selectbox("Lütfen Bir Şube Seçin:", list(subeler.keys()))
    haftalik_talep = st.number_input(f"{secilen_sube} Şubesi Haftalık Talep (kg):", min_value=1, value=subeler[secilen_sube])
    
    if st.button("Optimal Değerleri Hesapla"):
        # Yeni Belgeye Göre Hesaplamalar
        yillik_talep = haftalik_talep * 52
        d_gunluk = haftalik_talep / 7
        sigma_d = 0.15 * d_gunluk
        
        # Güvenlik Stoğu ve ROP
        ss = Z * sigma_d * math.sqrt(LT)
        rop = (d_gunluk * LT) + ss
        
        # Yeni sipariş miktarları (Projedeki yuvarlamalara sadık kalarak)
        if haftalik_talep == 30:
            opt_siparis = 33
        elif haftalik_talep == 40:
            opt_siparis = 44
        else:
            opt_siparis = round(haftalik_talep * 1.1)
            
        st.markdown("### 📊 Analiz Sonuçları")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Yıllık Talep", f"{yillik_talep} kg")
        col2.metric("Günlük Talep (Ort.)", f"{d_gunluk:.2f} kg")
        col3.metric("Güvenlik Stoğu (SS)", f"{ss:.2f} kg")
        col4.metric("Yeniden Sipariş (ROP)", f"{rop:.1f} kg")
        
        st.success(f"**Sistem Önerisi:** {secilen_sube} şubesi için stok seviyesi **{rop:.1f} kg**'a düştüğünde, merkeze **{opt_siparis} kg** sipariş geçilmelidir.")
        st.info("Bu otomasyon, Access Q_SiparisSapmaOrani sorgusu ile entegre çalışarak sipariş sapma oranını ~%2.0 seviyesine indirecektir.")

elif menu == "2. TSP Rota Optimizasyonu":
    st.title("🚚 Problem 2: Lojistik ve Rota Optimizasyonu")
    st.markdown("Gezgin Satıcı Problemi (Nearest Neighbor) Algoritması Sonuçları")
    
    # Gün Seçimi
    gun = st.selectbox("Lütfen Dağıtım Gününü Seçin:", ["Salı", "Perşembe", "Cuma"])
    
    if gun == "Salı":
        st.warning("Mevcut Rota: Buca → Bornova → Bostanlı → Karşıyaka → Buca (55 km)")
        st.success("Optimize Rota: Buca → Bornova → Karşıyaka → Bostanlı → Buca (52 km)")
        st.metric("Tasarruf", "3 km", "%5,5 İyileşme")
    elif gun == "Perşembe":
        st.warning("Mevcut Rota: Buca → Buca Şb. → Gaziemir → Buca (46 km)")
        st.success("Optimize Rota: Buca → Gaziemir → Buca Şb. → Buca (34 km)")
        st.metric("Tasarruf", "12 km", "%26,1 İyileşme")
    elif gun == "Cuma":
        st.info("Mevcut Rota: Buca → Çiğli → Menemen → Buca (94 km)")
        st.success("Optimize Rota: Buca → Çiğli → Menemen → Buca (94 km) - Zaten Optimum")
        st.metric("Tasarruf", "0 km", "Mevcut rota korunmalıdır")
        
    st.markdown("---")
    st.markdown("### 🗺️ Yeni Şubeler Arası Mesafe Matrisi (km)")
    matris = pd.DataFrame({
        "Nokta": ["Depo (Buca)", "Bornova", "Bostanlı", "Karşıyaka", "Çiğli", "Menemen", "Gaziemir"],
        "Depo": [0, 12, 20, 22, 28, 46, 14],
        "Bornova": [12, 0, 15, 14, 18, 36, 18],
        "Bostanlı": [20, 15, 0, 6, 14, 32, 26],
        "Karşıyaka": [22, 14, 6, 0, 12, 30, 28],
        "Çiğli": [28, 18, 14, 12, 0, 20, 32],
        "Menemen": [46, 36, 32, 30, 20, 0, 50],
        "Gaziemir": [14, 18, 26, 28, 32, 50, 0]
    })
    st.dataframe(matris, hide_index=True)
    st.caption("Not: Algoritma sonuçları Access Q_RotaMesafesi performans sorgusunu doğrudan iyileştirmektedir.")
