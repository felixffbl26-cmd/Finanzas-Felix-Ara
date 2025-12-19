import streamlit as st
import requests
import time

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="Nuestro Espacio - Félix & Ara",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS (Diseño Cálido) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Fondo degradado moderno */
    .stApp {
        background: linear-gradient(135deg, #2b1055 0%, #7597de 100%);
        color: white;
    }

    /* Títulos */
    h1 {
        color: #ffcc00 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Métricas (Cajitas de precio) */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    div[data-testid="stMetricValue"] {
        color: #ffcc00 !important;
        font-size: 2rem !important;
    }

    /* Tarjeta de Resultados */
    .result-card {
        background: rgba(0, 0, 0, 0.3);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        border: 2px solid #ffcc00;
        margin-top: 20px;
    }
    .big-font {
        font-size: 3rem !important;
        font-weight: bold;
        color: #fff;
        margin: 10px 0;
    }
    
    /* Botones */
    .stButton>button {
        background-color: #ffcc00;
        color: #2b1055;
        border-radius: 20px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ffe066;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNCIONES DE DATOS ---
@st.cache_data(ttl=3600)
def obtener_datos():
    # 1. Dólar Blue Argentina
    try:
        resp_arg = requests.get("https://dolarapi.com/v1/dolares/blue", timeout=5)
        data_arg = resp_arg.json()
        blue_compra = data_arg['compra']
        fecha_arg = data_arg['fechaActualizacion']
    except:
        blue_compra = 1480
        fecha_arg = "Sin conexión"

    # 2. Dólar Perú
    try:
        resp_pe = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        data_pe = resp_pe.json()
        precio_base = data_pe['rates']['PEN']
        pen_venta = round(precio_base * 1.005, 3) 
    except:
        pen_venta = 3.39

    return blue_compra, pen_venta, fecha_arg

# --- BARRA LATERAL (MENSAJE EDITADO) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2909/2909805.png", width=80)
    st.title("Conexión F&A")
    st.write("---")
    st.markdown("📍 **Félix:** Puno, Perú 🇵🇪")
    st.markdown("📍 **Ara:** Argentina 🇦🇷")
    
    st.write("---")
    st.subheader("💌 Nota para ti:")
    # AQUI CAMBIÉ EL MENSAJE:
    st.info("¡Hola! Espero que tengas un día lindo. Aquí actualicé la app para organizar nuestras cosas. Te quiero.")
    
    st.write("---")
    if st.button('🔄 Actualizar Datos'):
        st.cache_data.clear()
        st.rerun()

# --- CUERPO PRINCIPAL ---

st.markdown("<h1 style='text-align: center;'>✨ Construyendo Futuro ✨</h1>", unsafe_allow_html=True)

with st.spinner('Conectando fronteras...'):
    blue_compra, pen_venta, fecha_arg = obtener_datos()

# 1. PRECIOS ACTUALES
col1, col2, col3 = st.columns([1, 0.2, 1])
with col1:
    st.metric("🇵🇪 Dólar Perú", f"S/ {pen_venta:.2f}")
with col3:
    st.metric("🇦🇷 Blue Argentina", f"$ {blue_compra:,}")

st.divider()

# 2. NUEVA SECCIÓN DE AHORRO (EMPEZANDO DE CERO)
st.subheader("🌱 Nuestra Meta de Ahorro")
st.write("Registra aquí cuánto vamos juntando para ver nuestro progreso.")

# Definimos la meta (puedes cambiar este 1500 por lo que quieran)
META_USD = 1500 

col_input, col_bar = st.columns([1, 2])

with col_input:
    # Casilla para registrar el ahorro actual (Empieza en 0)
    ahorro_actual = st.number_input("💰 ¿Cuánto tenemos ahorrado hoy? (USD)", min_value=0.0, max_value=float(META_USD), step=10.0)

with col_bar:
    # Cálculo del porcentaje
    porcentaje = ahorro_actual / META_USD
    
    # Barra de progreso
    st.progress(porcentaje)
    
    # Mensajes motivacionales según el avance
    if porcentaje == 0:
        st.caption("¡Todo gran viaje comienza con un primer paso! 🚶‍♂️")
    elif porcentaje < 0.5:
        st.caption(f"¡Vamos bien! Llevamos el {porcentaje*100:.1f}% de la meta.")
    elif porcentaje < 1.0:
        st.caption(f"¡Ya falta poco! Estamos al {porcentaje*100:.1f}%. 🔥")
    else:
        st.balloons()
        st.success(f"¡LO LOGRAMOS! Juntamos los ${META_USD} USD 🎉")

st.divider()

# 3. CALCULADORA CONVERSORA
st.subheader("🧮 Calculadora de Cambios")
pestana_felix, pestana_ara = st.tabs(["👨 Soy Félix (Soles)", "👩 Soy Ara (Pesos)"])

# Pestaña Félix
with pestana_felix:
    c1, c2 = st.columns(2)
    with c1:
        monto_soles = st.number_input("Tengo Soles (S/)", value=100, step=10, key="s_input")
    with c2:
        if monto_soles > 0:
            final_pesos = (monto_soles / pen_venta) * blue_compra
            st.markdown(f"""
            <div class="result-card">
                <span>Allá reciben:</span>
                <div class="big-font">$ {final_pesos:,.0f} ARS</div>
            </div>
            """, unsafe_allow_html=True)

# Pestaña Ara
with pestana_ara:
    c1, c2 = st.columns(2)
    with c1:
        monto_pesos = st.number_input("Veo Pesos ($)", value=5000, step=500, key="p_input")
    with c2:
        if monto_pesos > 0:
            final_soles = (monto_pesos / blue_compra) * pen_venta
            st.markdown(f"""
            <div class="result-card" style="border-color: #fff;">
                <span>En Perú son:</span>
                <div class="big-font">S/ {final_soles:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

st.write("---")
st.caption("Aplicación creada por Félix para organizar nuestros sueños.")
