import streamlit as st
import requests

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Finanzas Félix & Ara",
    page_icon="✈️",
    layout="centered"
)

# --- ESTILOS VISUALES (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: white;
    }
    .big-font {
        font-size: 45px !important;
        font-weight: bold;
        color: #bb86fc; /* Lila */
        text-shadow: 0px 0px 10px rgba(187, 134, 252, 0.3);
    }
    .sub-text {
        font-size: 18px;
        color: #03dac6; /* Verde agua */
    }
    div[data-testid="stMetricValue"] {
        font-size: 26px;
        color: #03dac6;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNCIONES PARA OBTENER DATOS REALES ---

def obtener_datos():
    """Conecta con APIs reales para sacar el precio del momento"""
    
    # 1. Dólar Blue Argentina (API: DolarApi.com)
    try:
        resp_arg = requests.get("https://dolarapi.com/v1/dolares/blue")
        data_arg = resp_arg.json()
        blue_compra = data_arg['compra'] # Cuánto pagan ellos si vendes dólares
    except:
        blue_compra = 1480 # Valor de respaldo si falla internet

    # 2. Dólar Perú (API: ExchangeRate)
    try:
        resp_pe = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data_pe = resp_pe.json()
        precio_base = data_pe['rates']['PEN']
        pen_venta = round(precio_base * 1.005, 3) 
    except:
        pen_venta = 3.39 # Valor de respaldo

    return blue_compra, pen_venta

# --- CARGAMOS LOS DATOS ---
with st.spinner('Consultando casas de cambio...'):
    blue_compra, pen_venta = obtener_datos()

# --- INTERFAZ GRÁFICA ---

st.title("🇵🇪 Félix  ❤️  Ara 🇦🇷")
st.markdown("### Calculadora en Tiempo Real")

# Mostrar las cotizaciones de hoy
col1, col2 = st.columns(2)
col1.metric("🇵🇪 Dólar Perú (Venta)", f"S/ {pen_venta}")
col2.metric("🇦🇷 Blue Arg (Compra)", f"$ {blue_compra}")

st.divider()

# CREAMOS LAS PESTAÑAS
tab1, tab2 = st.tabs(["👨 SOLES a PESOS (Félix)", "👩 PESOS a SOLES (Ara)"])

# --- PESTAÑA 1: TÚ (FÉLIX) ---
with tab1:
    st.write("¿Cuántos **Soles (S/)** quieres enviar o calcular?")
    soles = st.number_input("Ingresa monto en Soles:", min_value=0, value=100, step=10, key="input_felix")
    
    if soles > 0:
        # CÁLCULO: Soles / TasaPeru * TasaArg
        resultado_pesos = (soles / pen_venta) * blue_compra
        usd_bridge = soles / pen_venta
        
        st.markdown(f"""
            <div style="background-color:#1E1E1E; padding:20px; border-radius:15px; text-align:center; border: 1px solid #333;">
                <span style="color:#aaa;">En Argentina reciben:</span><br>
                <span class="big-font">$ {resultado_pesos:,.0f} ARS</span><br>
                <span class="sub-text">(Equivale a ${usd_bridge:.2f} USD puente)</span>
            </div>
        """, unsafe_allow_html=True)

# --- PESTAÑA 2: ELLA (ARA) ---
with tab2:
    st.write("¿Qué precio viste en **Pesos ($)** allá?")
    pesos = st.number_input("Ingresa precio en Pesos:", min_value=0, value=5000, step=500, key="input_ara")
    
    if pesos > 0:
        # CÁLCULO INVERSO: Pesos / TasaArg * TasaPeru
        resultado_soles = (pesos / blue_compra) * pen_venta
        
        st.markdown(f"""
            <div style="background-color:#1E1E1E; padding:20px; border-radius:15px; text-align:center; border: 1px solid #333;">
                <span style="color:#aaa;">Eso en Perú cuesta:</span><br>
                <span class="big-font">S/ {resultado_soles:.2f}</span>
            </div>
        """, unsafe_allow_html=True)

st.divider()
if st.button('🔄 Actualizar Cotizaciones'):
    st.rerun()