# -*- coding: utf-8 -*-
"""
Created on Sun May 10 20:15:53 2026

@author: Yaren Akgül
"""

import streamlit as st
import math

st.set_page_config(page_title="Berry Kafe EOQ Otomasyonu", layout="centered")

st.title("☕ Berry Kafe Zinciri - Stok Yönetim Sistemi")
st.markdown("Kısım 3: EOQ ve Güvenlik Stoğu Otomasyon Paneli")

# Sabit Parametreler (Kısım 3'ten Alınmıştır)
S = 150  # Sipariş maliyeti (TL)
H = 24   # Yıllık elde tutma maliyeti (TL/kg/yıl)
z = 1.65 # Güvenlik katsayısı (%95)
sigma_d = 5 # Günlük talep standart sapması (kg)

# Şube Haftalık Talep Verileri
subeler = {
    "Bornova": 30,
    "Bostanlı": 40,
    "Karşıyaka": 30,
    "Çiğli": 30,
    "Menemen": 30,
    "Buca": 40,
    "Gaziemir": 30
}

st.header("1. Şube Seçimi ve Talep")
secilen_sube = st.selectbox("Lütfen Bir Şube Seçin:", list(subeler.keys()))

# Talep miktarını projeye göre otomatik getir ama hocanın denemesi için değiştirilebilir yap
haftalik_talep = st.number_input(
    f"{secilen_sube} Şubesi Haftalık Talep (kg):",
    min_value=1,
    value=subeler[secilen_sube]
)

if st.button("Optimal Değerleri Hesapla"):
    # Kısım 3 Hesaplamaları
    yillik_talep = haftalik_talep * 52
    eoq = math.sqrt((2 * yillik_talep * S) / H)
    
    # Güvenlik Stoğu ve Yeniden Sipariş Noktası (ROP)
    guvenlik_stogu = 8  # Projedeki sabit hesaplama (1.65 * 5 ≈ 8)
    rop = haftalik_talep + guvenlik_stogu
    
    st.header("📊 Analiz Sonuçları")
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Yıllık Talep (D)", f"{yillik_talep} kg")
    col2.metric("Sipariş Miktarı (EOQ)", f"{eoq:.0f} kg")
    col3.metric("Yeniden Sipariş (ROP)", f"{rop} kg")
    
    st.success(f"Sistem Önerisi: {secilen_sube} şubesi için stok seviyesi {rop} kg'a düştüğünde, merkeze {eoq:.0f} kg sipariş geçilmelidir.")
    st.info("Bu otomasyon sayesinde stok-out olayları elimine edilecek ve acil sipariş ihtiyacı ortadan kalkacaktır.")