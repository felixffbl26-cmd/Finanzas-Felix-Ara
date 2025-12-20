import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os
import time
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Felix & Ara - Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FUNCIONES PARA EL FONDO DE IMAGEN ---
def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(image_name):
    if os.path.exists(image_name):
        img_b64 = get_img_as_base64(image_name)
        page_bg_img = f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(15, 23, 42, 0.90), rgba(6, 11, 25, 0.95)), url("data:image/jpeg;base64,{img_b64}");
            background-attachment: fixed;
            background-size: cover;
            background-position: center center;
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp { background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(6, 11, 25) 90%); }
        </style>
        """, unsafe_allow_html=True)

# Intentar cargar fondo
set_background("juntos.jpg")

# --- CSS GENERAL (GLASSMORPHISM) ---
st.markdown("""
    <style>
    .stApp { color: #e2e8f0; }
    
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
    
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Inputs y Tablas */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid #334155 !important;
        color: white !important;
        border-radius: 10px !important;
    }
    .stDataFrame { border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(45deg, #3b82f6, #8b5cf6);
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 12px;
        font-weight: bold;
        width: 100%;
    }
    .stTabs [aria-selected="true"] {
        background-color: #38bdf8 !important;
        color: #0f172a !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- INGENIERÍA DE DATOS (AUTO-FETCH) ---
@st.cache_data(ttl=120)
def obtener_datos_mercado():
    try:
        r_arg = requests.get("https://dolarapi.com/v1/dolares/blue", timeout=3)
        ars_blue = float(r_arg.json()['venta'])
    except: ars_blue = 1200.0

    try:
        r_pe = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=3)
        pen_venta = round(r_pe.json()['rates']['PEN'] * 1.004, 3)
    except: pen_venta = 3.78

    try: bob_paralelo = 14.40 
    except: bob_paralelo = 14.40

    return ars_blue, pen_venta, bob_paralelo

# --- GESTIÓN DE BASE DE DATOS (CSV) ---
ARCHIVO_DB = "ahorros_felix_ara.csv"

def cargar_db():
    if not os.path.exists(ARCHIVO_DB):
        return pd.DataFrame(columns=["Fecha", "Hora", "Usuario", "Monto", "Moneda", "Total_USD", "Motivo"])
    try:
        df = pd.read_csv(ARCHIVO_DB)
        # Asegurar tipos de datos correctos para que no falle el gráfico
        df['Total_USD'] = pd.to_numeric(df['Total_USD'], errors='coerce')
        return df
    except:
        return pd.DataFrame(columns=["Fecha", "Hora", "Usuario", "Monto", "Moneda", "Total_USD", "Motivo"])

def guardar_registro(usuario, monto, moneda, motivo, tasa_conversion):
    df = cargar_db()
    
    # Normalizar a USD para sumar peras con peras
    monto_usd = monto
    if moneda == "ARS": monto_usd = monto / tasa_conversion['ARS']
    elif moneda == "PEN": monto_usd = monto / tasa_conversion['PEN']
    elif moneda == "BOB": monto_usd = monto / tasa_conversion['BOB']
    
    nuevo = {
        "Fecha": datetime.now().strftime("%Y-%m-%d"),
        "Hora": datetime.now().strftime("%H:%M:%S"),
        "Usuario": usuario,
        "Monto": monto,
        "Moneda": moneda,
        "Total_USD": round(monto_usd, 2),
        "Motivo": motivo
    }
    
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv(ARCHIVO_DB, index=False)
    return True

def borrar_ultimo():
    df = cargar_db()
    if not df.empty:
        df = df[:-1] # Borra el último renglón
        df.to_csv(ARCHIVO_DB, index=False)
        return True
    return False

# --- VARIABLES GLOBALES ---
ars_val, pen_val, bob_val = obtener_datos_mercado()
TASAS = {"USD": 1.0, "ARS": ars_val, "PEN": pen_val, "BOB": bob_val}

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuración")
    fecha_meta = st.date_input("Fecha de Encuentro:", datetime(2026, 1, 15))
    if st.button("🗑️ RESETEAR TODO (Cuidado)"):
        if os.path.exists(ARCHIVO_DB):
            os.remove(ARCHIVO_DB)
            st.rerun()

# --- INTERFAZ PRINCIPAL ---

# 1. ENCABEZADO
col_head, col_count = st.columns([2, 1])
with col_head:
    st.markdown("### 🚀 Dashboard de Misión")
    st.markdown("# Felix & Ara")
    st.caption("Conectando Puno 🇵🇪 y Humahuaca 🇦🇷")

with col_count:
    dias = (fecha_meta - datetime.now().date()).days
    st.markdown(f"""
    <div class="glass-card" style="text-align:center; padding: 10px; background: rgba(56, 189, 248, 0.15);">
        <div style="font-size: 0.8rem; color: #ddd;">TIEMPO RESTANTE</div>
        <div style="font-size: 2.5rem; font-weight: 800; color: #fff;">{dias}</div>
        <div style="font-size: 0.8rem; color: #ddd;">DÍAS</div>
    </div>
    """, unsafe_allow_html=True)

# 2. COTIZACIONES
st.markdown("### 📡 Cotizaciones (Tiempo Real)")
c1, c2, c3 = st.columns(3)
def card(label, val, sym, flag):
    return f"""<div class="glass-card" style="padding:15px; text-align:center;">
    <div style="color:#aaa; font-size:0.9rem;">{flag} {label}</div>
    <div style="color:#fff; font-size:1.8rem; font-weight:bold;">{sym} {val}</div>
    </div>"""
c1.markdown(card("PERÚ Venta", f"{pen_val:.3f}", "S/", "🇵🇪"), unsafe_allow_html=True)
c2.markdown(card("BOLIVIA Blue", f"{bob_val:.2f}", "Bs", "🇧🇴"), unsafe_allow_html=True)
c3.markdown(card("ARGENTINA Blue", f"{ars_val:,.0f}", "$", "🇦🇷"), unsafe_allow_html=True)

# 3. CONVERSOR AVANZADO
st.markdown("### 🧮 Conversor Multidivisa")
tabs = st.tabs(["🌎 General", "🇦🇷 De Pesos Arg", "🇧🇴 De Bolivianos"])

with tabs[0]: # GENERAL
    k1, k2, k3 = st.columns([1,1,2])
    with k1: amt = st.number_input("Monto", 100.0, key="g_in")
    with k2: cur = st.selectbox("Moneda Base", ["USD", "PEN", "BOB", "ARS"], key="g_sel")
    base_usd = amt / TASAS[cur]
    with k3:
        st.info(f"""
        🇺🇸 **{base_usd:,.2f}** USD  |  🇵🇪 **{base_usd*TASAS['PEN']:,.2f}** PEN  |  🇧🇴 **{base_usd*TASAS['BOB']:,.2f}** BOB  |  🇦🇷 **{base_usd*TASAS['ARS']:,.0f}** ARS
        """)

with tabs[1]: # DESDE ARS
    a1, a2 = st.columns([1, 2])
    with a1: ars_in = st.number_input("🇦🇷 Pesos Argentinos", 10000.0, step=1000.0)
    usd_base = ars_in / TASAS["ARS"]
    with a2:
        st.markdown(f"""
        <div class="glass-card">
        🇵🇪 <b>{usd_base*TASAS['PEN']:,.2f}</b> Soles<br>
        🇧🇴 <b>{usd_base*TASAS['BOB']:,.2f}</b> Bolivianos<br>
        🇺🇸 <b style="color:#4ade80;">{usd_base:,.2f}</b> Dólares
        </div>
        """, unsafe_allow_html=True)

with tabs[2]: # DESDE BOB
    b1, b2 = st.columns([1, 2])
    with b1: bob_in = st.number_input("🇧🇴 Bolivianos", 100.0, step=10.0)
    usd_base = bob_in / TASAS["BOB"]
    with b2:
        st.markdown(f"""
        <div class="glass-card">
        🇵🇪 <b>{usd_base*TASAS['PEN']:,.2f}</b> Soles<br>
        🇦🇷 <b>{usd_base*TASAS['ARS']:,.0f}</b> Pesos Arg<br>
        🇺🇸 <b style="color:#4ade80;">{usd_base:,.2f}</b> Dólares
        </div>
        """, unsafe_allow_html=True)

# 4. BÓVEDA DE AHORROS (ARREGLADO)
st.markdown("### 💰 Bóveda de Ahorros")
df = cargar_db()
total_vault = df["Total_USD"].sum()

# SECCIÓN VISUAL (Métrica y Formulario)
col_input, col_viz = st.columns([1, 2])

with col_input:
    st.metric("Total Acumulado (USD)", f"${total_vault:,.2f}")
    with st.form("save_form"):
        st.write("📝 **Nuevo Registro**")
        u = st.radio("Usuario", ["Felix", "Ara"], horizontal=True)
        c = st.selectbox("Moneda", ["USD", "PEN", "ARS", "BOB"])
        m = st.number_input(f"Monto en {c}", min_value=1.0)
        r = st.text_input("Motivo", "Ahorro")
        if st.form_submit_button("💾 Guardar en Bóveda"):
            guardar_registro(u, m, c, r, TASAS)
            st.success("¡Guardado!")
            time.sleep(0.5)
            st.rerun()
    
    # Botón para borrar el último error
    if st.button("↩️ Deshacer último ingreso"):
        if borrar_ultimo():
            st.warning("Último registro borrado.")
            time.sleep(0.5)
            st.rerun()

with col_viz:
    if not df.empty:
        # PESTAÑAS: Gráfico y Tabla
        tab_graph, tab_data = st.tabs(["📈 Gráfico de Crecimiento", "📋 Historial Detallado"])
        
        with tab_graph:
            # Preparar datos para el gráfico
            df_chart = df.copy()
            # Convertir string fecha a objeto fecha real para ordenar
            df_chart['Fecha_Obj'] = pd.to_datetime(df_chart['Fecha'])
            # Agrupar por fecha y sumar montos
            daily_sum = df_chart.groupby('Fecha_Obj')['Total_USD'].sum().reset_index()
            # Ordenar cronológicamente
            daily_sum = daily_sum.sort_values('Fecha_Obj')
            # Calcular acumulado (Running Total)
            daily_sum['Acumulado'] = daily_sum['Total_USD'].cumsum()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_sum['Fecha_Obj'], 
                y=daily_sum['Acumulado'],
                mode='lines+markers',
                name='Ahorro',
                line=dict(color='#38bdf8', width=4),
                fill='tozeroy',
                fillcolor='rgba(56, 189, 248, 0.2)'
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'), margin=dict(l=10, r=10, t=10, b=10), height=250,
                xaxis_title="Fecha", yaxis_title="USD Acumulados"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with tab_data:
            # Mostrar tabla ordenada (lo último arriba)
            st.dataframe(
                df.sort_index(ascending=False), 
                use_container_width=True,
                height=250,
                column_config={
                    "Total_USD": st.column_config.NumberColumn("Valor en USD", format="$%.2f")
                }
            )
    else:
        st.info("La bóveda está vacía. Registra tu primer ahorro a la izquierda.")

# 5. GALERÍA FOTOS
st.markdown("### 📸 Archivos")
g1, g2 = st.columns(2)
with g1:
    if os.path.exists("felix.jpeg"): st.image("felix.jpeg", caption="PILOTO FELIX")
    else: st.warning("Falta felix.jpeg")
with g2:
    if os.path.exists("ara.jpeg"): st.image("ara.jpeg", caption="COPILOTO ARA")
    else: st.warning("Falta ara.jpeg")

st.write("---")
st.caption(f"Sistema v8.0 | Sync: {datetime.now().strftime('%H:%M:%S')}")
