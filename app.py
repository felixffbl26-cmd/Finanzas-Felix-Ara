import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import time
import base64
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
import random
from geopy.distance import geodesic
import pytz

# Cargar variables de entorno
load_dotenv()

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Felix & Ara - Dashboard Completo",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CONFIGURACIÓN DE CLOUDINARY ---
CLOUDINARY_ENABLED = False
try:
    import cloudinary
    import cloudinary.uploader
    CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    API_KEY = os.getenv("CLOUDINARY_API_KEY")
    API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
    
    if CLOUD_NAME and API_KEY and API_SECRET:
        cloudinary.config(cloud_name=CLOUD_NAME, api_key=API_KEY, api_secret=API_SECRET)
        CLOUDINARY_ENABLED = True
except:
    pass

# --- COORDENADAS ---
PUNO_COORDS = (-15.8402, -70.0219)  # Puno, Perú
HUMAHUACA_COORDS = (-23.2050, -65.3511)  # Humahuaca, Argentina

# --- FUNCIONES PARA EL FONDO ---
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
            background-image: linear-gradient(rgba(15, 23, 42, 0.92), rgba(6, 11, 25, 0.96)), url("data:image/jpeg;base64,{img_b64}");
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

set_background("juntos.jpg")

# --- CSS MEJORADO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    .stApp { color: #e2e8f0; }
    
    .glass-card {
        background: rgba(30, 41, 59, 0.5);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px 0 rgba(56, 189, 248, 0.25);
    }
    
    h1, h2, h3 {
        font-weight: 700;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 4s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #3b82f6, #8b5cf6);
        color: white;
        border: none;
        padding: 12px 28px;
        border-radius: 12px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
    }
    
    .love-message {
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.2), rgba(139, 92, 246, 0.2));
        border-left: 4px solid #ec4899;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .postit {
        padding: 15px;
        border-radius: 8px;
        margin: 8px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transform: rotate(-1deg);
        transition: transform 0.2s;
    }
    
    .postit:hover { transform: rotate(0deg) scale(1.02); }
    
    .emoji-float {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .countdown-giant {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        color: #38bdf8;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
    }
    
    .ruleta-container {
        text-align: center;
        padding: 20px;
    }
    
    .ruleta-result {
        font-size: 2rem;
        font-weight: bold;
        color: #fbbf24;
        animation: bounce 0.5s;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }
    </style>
""", unsafe_allow_html=True)

# --- ARCHIVOS DE DATOS ---
ARCHIVO_DB = "ahorros_felix_ara.csv"
ARCHIVO_MENSAJES = "mensajes_amor.csv"
ARCHIVO_GALERIA = "galeria_fotos.csv"
ARCHIVO_FECHAS = "fechas_especiales.csv"
ARCHIVO_VIAJE = "gastos_viaje.csv"
ARCHIVO_MALETA = "checklist_maleta.csv"
ARCHIVO_ITINERARIO = "itinerario.csv"
ARCHIVO_METAS = "metas_hitos.csv"
ARCHIVO_EMERGENCIA = "directorio_emergencia.csv"
ARCHIVO_CAPSULA = "capsula_tiempo.csv"
ARCHIVO_POSTIT = "notas_postit.csv"
ARCHIVO_BESOS = "contador_besos.csv"
ARCHIVO_RETOS = "retos_semanales.csv"
ARCHIVO_DICCIONARIO = "diccionario_cultural.csv"
ARCHIVO_ACTIVIDAD = "ultima_actividad.csv"

# --- NUEVAS FUNCIONALIDADES AVANZADAS ---
try:
    import whisper
    import sounddevice as sd
    from scipy.io.wavfile import write
    import numpy as np
    from sklearn.linear_model import LinearRegression
    WHISPER_ENABLED = True
except:
    WHISPER_ENABLED = False

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- FUNCIONES DE DATOS ---
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
    bob_paralelo = 14.40
    return ars_blue, pen_venta, bob_paralelo

@st.cache_data(ttl=1800)
def obtener_clima(ciudad):
    """Obtener clima de OpenWeatherMap (requiere API key gratuita)"""
    try:
        # Usar API gratuita de wttr.in como alternativa
        if ciudad == "Puno":
            url = "https://wttr.in/Puno,Peru?format=j1"
        else:
            url = "https://wttr.in/Humahuaca,Argentina?format=j1"
        
        r = requests.get(url, timeout=5)
        data = r.json()
        temp = data['current_condition'][0]['temp_C']
        desc = data['current_condition'][0]['weatherDesc'][0]['value']
        return f"{temp}°C", desc
    except:
        return "N/A", "No disponible"

def cargar_db():
    if not os.path.exists(ARCHIVO_DB):
        return pd.DataFrame(columns=["Fecha", "Hora", "Usuario", "Monto", "Moneda", "Total_USD", "Motivo"])
    try:
        df = pd.read_csv(ARCHIVO_DB)
        df['Total_USD'] = pd.to_numeric(df['Total_USD'], errors='coerce')
        return df
    except:
        return pd.DataFrame(columns=["Fecha", "Hora", "Usuario", "Monto", "Moneda", "Total_USD", "Motivo"])

def guardar_registro(usuario, monto, moneda, motivo, tasa_conversion):
    df = cargar_db()
    monto_usd = monto / tasa_conversion[moneda]
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
        df = df[:-1]
        df.to_csv(ARCHIVO_DB, index=False)
        return True
    return False

# --- FUNCIONES PARA MENSAJES ---
def cargar_mensajes():
    if not os.path.exists(ARCHIVO_MENSAJES):
        return pd.DataFrame(columns=["Fecha", "Hora", "De", "Para", "Mensaje"])
    return pd.read_csv(ARCHIVO_MENSAJES)

def guardar_mensaje(de, para, mensaje):
    df = cargar_mensajes()
    nuevo = {
        "Fecha": datetime.now().strftime("%Y-%m-%d"),
        "Hora": datetime.now().strftime("%H:%M:%S"),
        "De": de,
        "Para": para,
        "Mensaje": mensaje
    }
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv(ARCHIVO_MENSAJES, index=False)

# --- FUNCIONES PARA GALERÍA ---
def cargar_galeria():
    if not os.path.exists(ARCHIVO_GALERIA):
        return pd.DataFrame(columns=["Fecha", "Usuario", "Descripcion", "URL", "Archivo_Local"])
    return pd.read_csv(ARCHIVO_GALERIA)

def guardar_foto(usuario, descripcion, uploaded_file):
    df = cargar_galeria()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    local_dir = "galeria_fotos"
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    filename = f"{usuario}_{timestamp}_{uploaded_file.name}"
    local_path = os.path.join(local_dir, filename)
    with open(local_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    cloud_url = ""
    if CLOUDINARY_ENABLED:
        try:
            result = cloudinary.uploader.upload(local_path, folder="felix_ara_memories")
            cloud_url = result['secure_url']
        except:
            pass
    nuevo = {
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Usuario": usuario,
        "Descripcion": descripcion,
        "URL": cloud_url,
        "Archivo_Local": local_path
    }
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv(ARCHIVO_GALERIA, index=False)

# --- FUNCIONES PARA FECHAS ---
def cargar_fechas():
    if not os.path.exists(ARCHIVO_FECHAS):
        df = pd.DataFrame({
            "Evento": ["Aniversario", "Cumpleaños Felix", "Cumpleaños Ara"],
            "Fecha": ["2025-06-15", "2000-10-26", "2003-07-28"],
            "Tipo": ["aniversario", "cumpleaños", "cumpleaños"]
        })
        df.to_csv(ARCHIVO_FECHAS, index=False)
        return df
    return pd.read_csv(ARCHIVO_FECHAS)

def guardar_fecha(evento, fecha, tipo):
    df = cargar_fechas()
    nuevo = {"Evento": evento, "Fecha": fecha.strftime("%Y-%m-%d"), "Tipo": tipo}
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv(ARCHIVO_FECHAS, index=False)

# --- FUNCIONES PARA GASTOS DE VIAJE ---
def cargar_gastos_viaje():
    if not os.path.exists(ARCHIVO_VIAJE):
        return pd.DataFrame(columns=["Categoria", "Descripcion", "Monto", "Moneda", "Monto_USD"])
    return pd.read_csv(ARCHIVO_VIAJE)

def guardar_gasto_viaje(categoria, descripcion, monto, moneda, tasas):
    df = cargar_gastos_viaje()
    monto_usd = monto / tasas[moneda]
    nuevo = {
        "Categoria": categoria,
        "Descripcion": descripcion,
        "Monto": monto,
        "Moneda": moneda,
        "Monto_USD": round(monto_usd, 2)
    }
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv(ARCHIVO_VIAJE, index=False)

# --- FUNCIONES PARA CHECKLIST DE MALETA ---
def cargar_maleta():
    if not os.path.exists(ARCHIVO_MALETA):
        items_default = [
            ("Documentos", "DNI/Pasaporte", False),
            ("Documentos", "Tarjetas de crédito", False),
            ("Documentos", "Seguro de viaje", False),
            ("Ropa", "Abrigo/Chamarra", False),
            ("Ropa", "Ropa interior (7 días)", False),
            ("Ropa", "Zapatos cómodos", False),
            ("Tecnología", "Cargador de celular", False),
            ("Tecnología", "Power bank", False),
            ("Medicinas", "Botiquín básico", False),
            ("Medicinas", "Medicamentos personales", False),
        ]
        df = pd.DataFrame(items_default, columns=["Categoria", "Item", "Completado"])
        df.to_csv(ARCHIVO_MALETA, index=False)
        return df
    return pd.read_csv(ARCHIVO_MALETA)

def actualizar_maleta(df):
    df.to_csv(ARCHIVO_MALETA, index=False)

# --- FUNCIONES PARA ITINERARIO ---
def cargar_itinerario():
    if not os.path.exists(ARCHIVO_ITINERARIO):
        lugares_default = [
            ("Puno", "Islas Flotantes de los Uros", "Lago Titicaca", False),
            ("Puno", "Isla Taquile", "Lago Titicaca", False),
            ("Copacabana", "Basílica de Copacabana", "Bolivia", False),
            ("Copacabana", "Isla del Sol", "Bolivia", False),
            ("Humahuaca", "Quebrada de Humahuaca", "Argentina", False),
            ("Humahuaca", "Cerro de los 14 Colores", "Argentina", False),
        ]
        df = pd.DataFrame(lugares_default, columns=["Ciudad", "Lugar", "Pais", "Visitado"])
        df.to_csv(ARCHIVO_ITINERARIO, index=False)
        return df
    return pd.read_csv(ARCHIVO_ITINERARIO)

def actualizar_itinerario(df):
    df.to_csv(ARCHIVO_ITINERARIO, index=False)

# --- FUNCIONES PARA METAS POR HITOS ---
def cargar_metas():
    if not os.path.exists(ARCHIVO_METAS):
        metas_default = [
            ("Pasajes", 500.0, "USD"),
            ("Hotel (5 noches)", 300.0, "USD"),
            ("Cena de Bienvenida", 100.0, "USD"),
        ]
        df = pd.DataFrame(metas_default, columns=["Concepto", "Monto", "Moneda"])
        df.to_csv(ARCHIVO_METAS, index=False)
        return df
    return pd.read_csv(ARCHIVO_METAS)

# --- FUNCIONES PARA DIRECTORIO DE EMERGENCIA ---
def cargar_emergencia():
    if not os.path.exists(ARCHIVO_EMERGENCIA):
        contactos_default = [
            ("Felix", "Teléfono", "+51 999 999 999"),
            ("Ara", "Teléfono", "+54 999 999 999"),
            ("Hotel Bolivia", "Dirección", "Av. Principal 123, Copacabana"),
            ("Emergencias Perú", "Teléfono", "105"),
            ("Emergencias Argentina", "Teléfono", "911"),
        ]
        df = pd.DataFrame(contactos_default, columns=["Contacto", "Tipo", "Info"])
        df.to_csv(ARCHIVO_EMERGENCIA, index=False)
        return df
    return pd.read_csv(ARCHIVO_EMERGENCIA)

def actualizar_emergencia(df):
    df.to_csv(ARCHIVO_EMERGENCIA, index=False)

# --- FUNCIONES PARA CÁPSULA DEL TIEMPO ---
def cargar_capsula():
    if not os.path.exists(ARCHIVO_CAPSULA):
        return pd.DataFrame(columns=["Fecha_Creacion", "De", "Para", "Mensaje", "Fecha_Apertura"])
    return pd.read_csv(ARCHIVO_CAPSULA)

def guardar_capsula(de, para, mensaje, fecha_apertura):
    df = cargar_capsula()
    nuevo = {
        "Fecha_Creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "De": de,
        "Para": para,
        "Mensaje": mensaje,
        "Fecha_Apertura": fecha_apertura.strftime("%Y-%m-%d")
    }
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv(ARCHIVO_CAPSULA, index=False)

# --- FUNCIONES PARA POST-IT ---
def cargar_postit():
    if not os.path.exists(ARCHIVO_POSTIT):
        return pd.DataFrame(columns=["Fecha", "Hora", "De", "Nota"])
    return pd.read_csv(ARCHIVO_POSTIT)

def guardar_postit(de, nota):
    df = cargar_postit()
    nuevo = {
        "Fecha": datetime.now().strftime("%Y-%m-%d"),
        "Hora": datetime.now().strftime("%H:%M"),
        "De": de,
        "Nota": nota
    }
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv(ARCHIVO_POSTIT, index=False)

# --- FUNCIONES PARA CONTADOR DE BESOS ---
def cargar_besos():
    if not os.path.exists(ARCHIVO_BESOS):
        return pd.DataFrame(columns=["Fecha", "Hora", "De"])
    return pd.read_csv(ARCHIVO_BESOS)

def agregar_beso(de):
    df = cargar_besos()
    nuevo = {
        "Fecha": datetime.now().strftime("%Y-%m-%d"),
        "Hora": datetime.now().strftime("%H:%M:%S"),
        "De": de
    }
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv(ARCHIVO_BESOS, index=False)

# --- FUNCIONES PARA RETOS SEMANALES ---
def cargar_retos():
    if not os.path.exists(ARCHIVO_RETOS):
        df = pd.DataFrame({
            "Semana": [datetime.now().strftime("%Y-W%U")],
            "Videollamadas": [0],
            "Peliculas": [0]
        })
        df.to_csv(ARCHIVO_RETOS, index=False)
        return df
    df = pd.read_csv(ARCHIVO_RETOS)
    semana_actual = datetime.now().strftime("%Y-W%U")
    if df.empty or df.iloc[-1]['Semana'] != semana_actual:
        nuevo = {"Semana": semana_actual, "Videollamadas": 0, "Peliculas": 0}
        df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
        df.to_csv(ARCHIVO_RETOS, index=False)
    return df

def actualizar_retos(df):
    df.to_csv(ARCHIVO_RETOS, index=False)

# --- FUNCIONES PARA DICCIONARIO ---
def cargar_diccionario():
    if not os.path.exists(ARCHIVO_DICCIONARIO):
        palabras = [
            ("Pata", " Perú", "Amigo/a"),
            ("Chamba", " Perú", "Trabajo"),
            ("Jato", " Perú", "Casa"),
            ("Causa", " Perú", "Amigo/Hermano"),
            ("Che", " Argentina", "Oye/Tú"),
            ("Laburo", " Argentina", "Trabajo"),
            ("Bondi", " Argentina", "Autobús"),
            ("Pibe/Piba", " Argentina", "Chico/Chica"),
            ("Boludo/a", " Argentina", "Tonto/a (cariñoso)"),
            ("Quilombo", " Argentina", "Desorden/Lío"),
        ]
        df = pd.DataFrame(palabras, columns=["Palabra", "País", "Significado"])
        df.to_csv(ARCHIVO_DICCIONARIO, index=False)
        return df
    return pd.read_csv(ARCHIVO_DICCIONARIO)

# --- FUNCIONES AVANZADAS: MODO "TE EXTRAÑO" ---
def registrar_actividad():
    """Registra la última vez que se abrió la app"""
    df = pd.DataFrame({
        "Fecha": [datetime.now().strftime("%Y-%m-%d")],
        "Hora": [datetime.now().strftime("%H:%M:%S")]
    })
    df.to_csv(ARCHIVO_ACTIVIDAD, index=False)

def verificar_inactividad():
    """Verifica si han pasado más de 3 días sin abrir la app"""
    if not os.path.exists(ARCHIVO_ACTIVIDAD):
        return 0
    try:
        df = pd.read_csv(ARCHIVO_ACTIVIDAD)
        ultima_fecha = datetime.strptime(df.iloc[-1]['Fecha'], "%Y-%m-%d")
        dias_inactivos = (datetime.now() - ultima_fecha).days
        return dias_inactivos
    except:
        return 0

def enviar_notificacion_email(destinatario, dias):
    """Envía email de notificación (requiere configuración SMTP)"""
    try:
        email_from = os.getenv("EMAIL_FROM")
        email_password = os.getenv("EMAIL_PASSWORD")
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        
        if not email_from or not email_password:
            return False
        
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = destinatario
        msg['Subject'] = "Te extrañamos en Felix & Ara Dashboard"
        
        body = f"""
        Hola,
        
        Han pasado {dias} días desde la última vez que abriste el dashboard de Felix & Ara.
        
        Tu pareja te extraña. Entra para:
        - Ver cuánto han ahorrado juntos
        - Dejar un mensaje de amor
        - Revisar el contador de besos
        - Planificar su próximo encuentro
        
        Con amor,
        Felix & Ara Dashboard
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_from, email_password)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False

# --- FUNCIONES AVANZADAS: CONVERSOR DE VOZ ---
def grabar_audio(duracion=5, sample_rate=16000):
    """Graba audio del micrófono"""
    try:
        st.info(f"Grabando {duracion} segundos... Habla ahora!")
        audio = sd.rec(int(duracion * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        return audio, sample_rate
    except:
        return None, None

def transcribir_audio(audio, sample_rate):
    """Transcribe audio usando Whisper"""
    try:
        # Guardar audio temporal
        temp_file = "temp_audio.wav"
        write(temp_file, sample_rate, audio)
        
        # Cargar modelo Whisper (tiny para rapidez)
        model = whisper.load_model("tiny")
        result = model.transcribe(temp_file, language="es")
        
        # Limpiar archivo temporal
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        return result["text"]
    except:
        return None

def extraer_monto_de_texto(texto):
    """Extrae el monto numérico del texto transcrito"""
    import re
    # Buscar números en el texto
    numeros = re.findall(r'\d+\.?\d*', texto)
    if numeros:
        return float(numeros[0])
    return None

# --- FUNCIONES AVANZADAS: PREDICCIÓN DE META ---
def predecir_fecha_meta(df_ahorros, monto_meta):
    """Predice cuándo se alcanzará la meta usando regresión lineal"""
    if df_ahorros.empty or len(df_ahorros) < 2:
        return None, None
    
    try:
        # Preparar datos
        df_chart = df_ahorros.copy()
        df_chart['Fecha_Obj'] = pd.to_datetime(df_chart['Fecha'])
        df_chart = df_chart.sort_values('Fecha_Obj')
        
        # Calcular días desde el primer ahorro
        primer_dia = df_chart['Fecha_Obj'].min()
        df_chart['Dias'] = (df_chart['Fecha_Obj'] - primer_dia).dt.days
        
        # Calcular acumulado por día
        daily_sum = df_chart.groupby('Dias')['Total_USD'].sum().reset_index()
        daily_sum['Acumulado'] = daily_sum['Total_USD'].cumsum()
        
        if len(daily_sum) < 2:
            return None, None
        
        # Entrenar modelo de regresión lineal
        X = daily_sum[['Dias']].values
        y = daily_sum['Acumulado'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predecir cuántos días faltan para llegar a la meta
        dias_actuales = (datetime.now() - primer_dia).days
        ahorro_actual = df_chart['Total_USD'].sum()
        
        if ahorro_actual >= monto_meta:
            return datetime.now().date(), "Ya alcanzaste la meta!"
        
        # Calcular días necesarios para alcanzar la meta
        dias_necesarios = (monto_meta - model.intercept_) / model.coef_[0]
        fecha_predicha = primer_dia + timedelta(days=int(dias_necesarios))
        
        # Calcular tasa de ahorro diaria
        tasa_diaria = model.coef_[0]
        
        return fecha_predicha.date(), f"Ahorran aproximadamente ${tasa_diaria:.2f} USD por día"
    except:
        return None, None

# --- DATOS GLOBALES ---
ars_val, pen_val, bob_val = obtener_datos_mercado()
TASAS = {"USD": 1.0, "ARS": ars_val, "PEN": pen_val, "BOB": bob_val}

# --- SALUDADOR HORARIO ---
def obtener_saludo():
    hora = datetime.now().hour
    if 5 <= hora < 12:
        return "️ Buenos días, amor", "#fbbf24"
    elif 12 <= hora < 19:
        return "️ Buenas tardes, mi vida", "#f59e0b"
    elif 19 <= hora < 24:
        return " Buenas noches, mi cielo", "#8b5cf6"
    else:
        return " ¿Aún despierto? Te extraño", "#ec4899"

# --- SIDEBAR ---
with st.sidebar:
    st.header("️ Configuración")
    fecha_meta = st.date_input(" Fecha de Encuentro:", datetime(2026, 1, 15))
    
    st.markdown("---")
    saludo, color = obtener_saludo()
    st.markdown(f"<div style='padding:10px; background:{color}22; border-left:4px solid {color}; border-radius:8px;'>{saludo}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button(" Actualizar Datos"):
        st.cache_data.clear()
        st.rerun()
    
    if st.button("️ RESETEAR TODO"):
        for archivo in [ARCHIVO_DB, ARCHIVO_MENSAJES, ARCHIVO_GALERIA, ARCHIVO_VIAJE, ARCHIVO_MALETA, ARCHIVO_ITINERARIO, ARCHIVO_CAPSULA, ARCHIVO_POSTIT, ARCHIVO_BESOS, ARCHIVO_RETOS]:
            if os.path.exists(archivo):
                os.remove(archivo)
        st.rerun()

# --- ENCABEZADO ---
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.markdown("#  Felix & Ara")
    st.caption("Conectando Puno  y Humahuaca ")

with col2:
    # CUENTA REGRESIVA GIGANTE
    ahora = datetime.now()
    delta = datetime.combine(fecha_meta, datetime.min.time()) - ahora
    dias = delta.days
    horas = delta.seconds // 3600
    minutos = (delta.seconds % 3600) // 60
    segundos = delta.seconds % 60
    
    st.markdown(f"""
    <div class="glass-card" style="text-align:center; background: rgba(56, 189, 248, 0.15);">
        <div style="font-size: 0.9rem; color: #ddd; margin-bottom: 5px;">⏰ CUENTA REGRESIVA GIGANTE</div>
        <div class="countdown-giant">{dias}d {horas}h {minutos}m {segundos}s</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # CONTADOR DE DISTANCIA
    distancia_km = round(geodesic(PUNO_COORDS, HUMAHUACA_COORDS).kilometers, 2)
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size: 0.8rem; color: #aaa;"> DISTANCIA</div>
        <div style="font-size: 1.5rem; font-weight: bold; color: #38bdf8;">{distancia_km:,} km</div>
        <div style="font-size: 0.7rem; color: #aaa;">~24h en bus</div>
    </div>
    """, unsafe_allow_html=True)

# --- CLIMA DUAL ---
st.markdown("### ️ Clima Dual en Tiempo Real")
c1, c2 = st.columns(2)
with c1:
    temp_puno, desc_puno = obtener_clima("Puno")
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size: 1rem; color: #aaa;"> PUNO, PERÚ</div>
        <div style="font-size: 2.5rem; font-weight: bold; color: #38bdf8;">{temp_puno}</div>
        <div style="font-size: 0.9rem; color: #ddd;">{desc_puno}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    temp_huma, desc_huma = obtener_clima("Humahuaca")
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-size: 1rem; color: #aaa;"> HUMAHUACA, ARGENTINA</div>
        <div style="font-size: 2.5rem; font-weight: bold; color: #ec4899;">{temp_huma}</div>
        <div style="font-size: 0.9rem; color: #ddd;">{desc_huma}</div>
    </div>
    """, unsafe_allow_html=True)

# --- TABS PRINCIPALES ---
tabs = st.tabs([
    " Finanzas",
    "️ Preparación Viaje", 
    " Amor & Conexión",
    " Entretenimiento",
    " Identidad Cultural",
    " Galería"
])

# ==================== TAB 1: FINANZAS ====================
with tabs[0]:
    st.markdown("###  Conversor Multidivisa")
    k1, k2, k3 = st.columns([1,1,2])
    with k1: amt = st.number_input("Monto", 100.0, key="conv_amt")
    with k2: cur = st.selectbox("Moneda", ["USD", "PEN", "BOB", "ARS"], key="conv_cur")
    base_usd = amt / TASAS[cur]
    with k3:
        st.info(f" **${base_usd:,.2f}** USD |  **S/{base_usd*TASAS['PEN']:,.2f}** |  **Bs{base_usd*TASAS['BOB']:,.2f}** |  **${base_usd*TASAS['ARS']:,.0f}**")
    
    st.markdown("###  Bóveda de Ahorros")
    df = cargar_db()
    total_vault = df["Total_USD"].sum()
    
    col_input, col_viz = st.columns([1, 2])
    with col_input:
        st.metric("Total Acumulado", f"${total_vault:,.2f} USD")
        with st.form("save_form"):
            u = st.radio("Usuario", ["Felix", "Ara"], horizontal=True)
            c = st.selectbox("Moneda", ["USD", "PEN", "ARS", "BOB"])
            m = st.number_input(f"Monto en {c}", min_value=1.0)
            r = st.text_input("Motivo", "Ahorro")
            if st.form_submit_button(" Guardar"):
                guardar_registro(u, m, c, r, TASAS)
                st.success("¡Guardado!")
                time.sleep(0.5)
                st.rerun()
        if st.button("↩️ Deshacer último"):
            if borrar_ultimo():
                st.warning("Borrado")
                time.sleep(0.5)
                st.rerun()
    
    with col_viz:
        if not df.empty:
            df_chart = df.copy()
            df_chart['Fecha_Obj'] = pd.to_datetime(df_chart['Fecha'])
            daily_sum = df_chart.groupby('Fecha_Obj')['Total_USD'].sum().reset_index()
            daily_sum = daily_sum.sort_values('Fecha_Obj')
            daily_sum['Acumulado'] = daily_sum['Total_USD'].cumsum()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_sum['Fecha_Obj'], 
                y=daily_sum['Acumulado'],
                mode='lines+markers',
                line=dict(color='#38bdf8', width=4),
                fill='tozeroy',
                fillcolor='rgba(56, 189, 248, 0.2)'
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'), margin=dict(l=10, r=10, t=10, b=10), height=250
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # --- FUNCIONALIDADES AVANZADAS ---
    st.markdown("---")
    st.markdown("### Funcionalidades Avanzadas con IA")
    
    adv_tabs = st.tabs(["Entrada por Voz", "Modo Te Extraño", "Predicción de Meta"])
    
    # TAB: ENTRADA POR VOZ
    with adv_tabs[0]:
        st.markdown("#### Dictar Ahorro con Voz")
        
        if not WHISPER_ENABLED:
            st.warning("Whisper AI no está instalado. Instala con: pip install openai-whisper sounddevice scipy")
        else:
            st.info("Di algo como: 'Guardé 50 dólares' o 'Ahorré 100 soles'")
            
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                if st.button("Grabar Audio (5 segundos)"):
                    with st.spinner("Grabando..."):
                        audio, sr = grabar_audio(duracion=5)
                        if audio is not None:
                            st.success("Audio grabado!")
                            
                            with st.spinner("Transcribiendo con Whisper AI..."):
                                texto = transcribir_audio(audio, sr)
                                if texto:
                                    st.write(f"**Transcripción:** {texto}")
                                    
                                    monto = extraer_monto_de_texto(texto)
                                    if monto:
                                        st.session_state['monto_voz'] = monto
                                        st.success(f"Monto detectado: {monto}")
                                    else:
                                        st.error("No se detectó un monto numérico")
                                else:
                                    st.error("Error al transcribir")
            
            with col_v2:
                if 'monto_voz' in st.session_state:
                    with st.form("voice_save_form"):
                        st.write(f"**Monto detectado:** {st.session_state['monto_voz']}")
                        u_voz = st.radio("Usuario:", ["Felix", "Ara"], horizontal=True, key="voz_user")
                        c_voz = st.selectbox("Moneda:", ["USD", "PEN", "ARS", "BOB"], key="voz_curr")
                        
                        if st.form_submit_button("Guardar Ahorro"):
                            guardar_registro(u_voz, st.session_state['monto_voz'], c_voz, "Ahorro por voz", TASAS)
                            del st.session_state['monto_voz']
                            st.success("Guardado!")
                            time.sleep(0.5)
                            st.rerun()
    
    # TAB: MODO TE EXTRAÑO
    with adv_tabs[1]:
        st.markdown("#### Sistema de Notificaciones")
        
        # Registrar actividad actual
        registrar_actividad()
        
        dias_inactivos = verificar_inactividad()
        
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            if dias_inactivos >= 3:
                st.error(f"Han pasado {dias_inactivos} días sin actividad!")
            elif dias_inactivos > 0:
                st.warning(f"Última actividad hace {dias_inactivos} día(s)")
            else:
                st.success("Activo hoy")
        
        with col_n2:
            st.info("Configuración de email en .env:\n- EMAIL_FROM\n- EMAIL_PASSWORD\n- SMTP_SERVER\n- SMTP_PORT")
        
        email_felix = st.text_input("Email de Felix:", "felix@example.com")
        email_ara = st.text_input("Email de Ara:", "ara@example.com")
        
        if st.button("Enviar Notificación de Prueba"):
            if enviar_notificacion_email(email_felix, dias_inactivos):
                st.success("Email enviado a Felix!")
            else:
                st.error("Error al enviar. Verifica configuración en .env")
    
    # TAB: PREDICCIÓN DE META
    with adv_tabs[2]:
        st.markdown("#### Predicción con IA")
        
        if not df.empty and len(df) >= 2:
            # Obtener meta del primer hito
            df_metas = cargar_metas()
            if not df_metas.empty:
                meta_principal = df_metas.iloc[0]['Monto']
                
                fecha_pred, info = predecir_fecha_meta(df, meta_principal)
                
                if fecha_pred:
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        st.metric("Meta", f"${meta_principal:.2f} USD")
                        st.metric("Ahorrado", f"${total_vault:.2f} USD")
                    
                    with col_p2:
                        st.metric("Fecha Predicha", fecha_pred.strftime("%d/%m/%Y"))
                        st.caption(info)
                    
                    # Comparar con fecha objetivo
                    fecha_objetivo = datetime(2026, 1, 15).date()
                    if fecha_pred < fecha_objetivo:
                        dias_antes = (fecha_objetivo - fecha_pred).days
                        st.success(f"Van muy bien! Llegarán {dias_antes} días antes de lo planeado")
                    elif fecha_pred > fecha_objetivo:
                        dias_despues = (fecha_pred - fecha_objetivo).days
                        st.warning(f"Necesitan acelerar el ahorro. Llegarán {dias_despues} días después")
                    else:
                        st.success("Perfecto! Llegarán justo a tiempo")
                else:
                    st.info("Necesitas más datos para hacer una predicción precisa")
            else:
                st.info("Configura una meta en 'Metas por Hitos' primero")
        else:
            st.info("Necesitas al menos 2 registros de ahorro para hacer predicciones")

# ==================== TAB 2: PREPARACIÓN VIAJE ====================
with tabs[1]:
    subtabs = st.tabs([" Checklist Maleta", "️ Itinerario", " Metas por Hitos", " Emergencias"])
    
    # CHECKLIST DE MALETA
    with subtabs[0]:
        st.markdown("###  Checklist de Maleta")
        df_maleta = cargar_maleta()
        
        completados = df_maleta['Completado'].sum()
        total_items = len(df_maleta)
        progreso = (completados / total_items) * 100 if total_items > 0 else 0
        
        st.progress(progreso / 100)
        st.caption(f"Progreso: {completados}/{total_items} items ({progreso:.0f}%)")
        
        for categoria in df_maleta['Categoria'].unique():
            st.markdown(f"**{categoria}**")
            items_cat = df_maleta[df_maleta['Categoria'] == categoria]
            
            for idx, row in items_cat.iterrows():
                col1, col2 = st.columns([0.1, 0.9])
                with col1:
                    checked = st.checkbox("", value=row['Completado'], key=f"maleta_{idx}", label_visibility="collapsed")
                    if checked != row['Completado']:
                        df_maleta.at[idx, 'Completado'] = checked
                        actualizar_maleta(df_maleta)
                        st.rerun()
                with col2:
                    st.write(row['Item'])
    
    # ITINERARIO
    with subtabs[1]:
        st.markdown("### ️ Itinerario de Lugares por Visitar")
        df_itinerario = cargar_itinerario()
        
        visitados = df_itinerario['Visitado'].sum()
        total_lugares = len(df_itinerario)
        
        st.metric("Lugares Visitados", f"{visitados}/{total_lugares}")
        
        for ciudad in df_itinerario['Ciudad'].unique():
            st.markdown(f"** {ciudad}**")
            lugares_ciudad = df_itinerario[df_itinerario['Ciudad'] == ciudad]
            
            for idx, row in lugares_ciudad.iterrows():
                col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
                with col1:
                    visitado = st.checkbox("", value=row['Visitado'], key=f"itin_{idx}", label_visibility="collapsed")
                    if visitado != row['Visitado']:
                        df_itinerario.at[idx, 'Visitado'] = visitado
                        actualizar_itinerario(df_itinerario)
                        st.rerun()
                with col2:
                    st.write(f"**{row['Lugar']}**")
                with col3:
                    st.caption(row['Pais'])
    
    # METAS POR HITOS
    with subtabs[2]:
        st.markdown("###  Metas por Hitos")
        df_metas = cargar_metas()
        total_ahorrado = cargar_db()['Total_USD'].sum()
        
        for idx, row in df_metas.iterrows():
            monto_meta = row['Monto']
            progreso_meta = min((total_ahorrado / monto_meta) * 100, 100)
            falta = max(0, monto_meta - total_ahorrado)
            
            st.markdown(f"**{row['Concepto']}**")
            st.progress(progreso_meta / 100)
            col1, col2, col3 = st.columns(3)
            col1.metric("Meta", f"${monto_meta:.2f}")
            col2.metric("Ahorrado", f"${min(total_ahorrado, monto_meta):.2f}")
            col3.metric("Falta", f"${falta:.2f}")
            st.markdown("---")
    
    # DIRECTORIO DE EMERGENCIA
    with subtabs[3]:
        st.markdown("###  Directorio de Emergencia")
        df_emergencia = cargar_emergencia()
        
        st.dataframe(df_emergencia, use_container_width=True, hide_index=True)

# ==================== TAB 3: AMOR & CONEXIÓN ====================
with tabs[2]:
    subtabs_amor = st.tabs([" Mensajes", "⏳ Cápsula del Tiempo", " Post-it", " Contador de Besos"])
    
    # MENSAJES DE AMOR
    with subtabs_amor[0]:
        col1, col2 = st.columns(2)
        with col1:
            with st.form("msg_form"):
                de = st.radio("De:", ["Felix", "Ara"], horizontal=True)
                para = "Ara" if de == "Felix" else "Felix"
                mensaje = st.text_area("Mensaje:", height=100)
                if st.form_submit_button(" Enviar"):
                    if mensaje.strip():
                        guardar_mensaje(de, para, mensaje)
                        st.success("¡Enviado!")
                        time.sleep(0.5)
                        st.rerun()
        
        with col2:
            st.markdown("** Mensajes Recientes**")
            df_msg = cargar_mensajes()
            if not df_msg.empty:
                for idx, row in df_msg.tail(5).iloc[::-1].iterrows():
                    emoji = "" if row['De'] == "Felix" else ""
                    st.markdown(f"""
                    <div class="love-message">
                        <div style="font-size:0.8rem; color:#aaa;">{emoji} {row['De']} → {row['Para']} | {row['Fecha']} {row['Hora']}</div>
                        <div style="margin-top:5px;">{row['Mensaje']}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # CÁPSULA DEL TIEMPO
    with subtabs_amor[1]:
        st.markdown("### ⏳ Cápsula del Tiempo")
        st.info(" Escribe mensajes que solo se desbloquearán el 15 de enero de 2026")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.form("capsula_form"):
                de_cap = st.radio("De:", ["Felix", "Ara"], horizontal=True, key="cap_de")
                para_cap = "Ara" if de_cap == "Felix" else "Felix"
                mensaje_cap = st.text_area("Tu mensaje para el futuro:", height=120)
                if st.form_submit_button(" Guardar en Cápsula"):
                    if mensaje_cap.strip():
                        guardar_capsula(de_cap, para_cap, mensaje_cap, datetime(2026, 1, 15))
                        st.success("¡Mensaje guardado en la cápsula! ")
                        time.sleep(0.5)
                        st.rerun()
        
        with col2:
            df_capsula = cargar_capsula()
            if not df_capsula.empty:
                fecha_apertura = datetime(2026, 1, 15).date()
                hoy = datetime.now().date()
                
                if hoy >= fecha_apertura:
                    st.success(" ¡La cápsula está desbloqueada!")
                    for idx, row in df_capsula.iterrows():
                        st.markdown(f"""
                        <div class="glass-card" style="background: rgba(236, 72, 153, 0.2);">
                            <div style="font-size:0.8rem; color:#aaa;">De: {row['De']} → Para: {row['Para']}</div>
                            <div style="margin-top:10px; font-size:1.1rem;">{row['Mensaje']}</div>
                            <div style="font-size:0.7rem; color:#aaa; margin-top:5px;">Escrito el: {row['Fecha_Creacion']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    dias_falta = (fecha_apertura - hoy).days
                    st.warning(f" Mensajes bloqueados. Faltan {dias_falta} días para abrirlos.")
                    st.metric("Mensajes en la cápsula", len(df_capsula))
    
    # MURO DE POST-IT
    with subtabs_amor[2]:
        st.markdown("###  Muro de Notas Post-it")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            with st.form("postit_form"):
                de_post = st.radio("De:", ["Felix", "Ara"], horizontal=True, key="post_de")
                nota = st.text_input("Nota rápida:", placeholder="Buenos días mi amor ️")
                if st.form_submit_button(" Pegar Post-it"):
                    if nota.strip():
                        guardar_postit(de_post, nota)
                        st.success("¡Nota pegada!")
                        time.sleep(0.3)
                        st.rerun()
        
        with col2:
            df_postit = cargar_postit()
            if not df_postit.empty:
                colores = ["#fef3c7", "#dbeafe", "#fce7f3", "#d1fae5", "#e0e7ff"]
                for idx, row in df_postit.tail(10).iloc[::-1].iterrows():
                    color = random.choice(colores)
                    emoji = "" if row['De'] == "Felix" else ""
                    st.markdown(f"""
                    <div class="postit" style="background:{color}; color:#1f2937;">
                        <div style="font-size:0.75rem; opacity:0.7;">{emoji} {row['De']} - {row['Fecha']} {row['Hora']}</div>
                        <div style="margin-top:5px; font-weight:600;">{row['Nota']}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # CONTADOR DE BESOS
    with subtabs_amor[3]:
        st.markdown("###  Contador de Besos")
        df_besos = cargar_besos()
        total_besos = len(df_besos)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; background: rgba(236, 72, 153, 0.2);">
                <div style="font-size:1rem; color:#ddd;">BESOS ENVIADOS</div>
                <div style="font-size:4rem; font-weight:800; color:#ec4899;">{total_besos}</div>
                <div style="font-size:0.9rem; color:#ddd;"> Te extraño clicks</div>
            </div>
            """, unsafe_allow_html=True)
            
            col_f, col_a = st.columns(2)
            with col_f:
                if st.button(" Felix extraña", use_container_width=True):
                    agregar_beso("Felix")
                    st.balloons()
                    time.sleep(0.5)
                    st.rerun()
            with col_a:
                if st.button(" Ara extraña", use_container_width=True):
                    agregar_beso("Ara")
                    st.balloons()
                    time.sleep(0.5)
                    st.rerun()
        
        with col2:
            if not df_besos.empty:
                st.markdown("**Últimos besos enviados:**")
                for idx, row in df_besos.tail(10).iloc[::-1].iterrows():
                    emoji = "" if row['De'] == "Felix" else ""
                    st.caption(f"{emoji} {row['De']} - {row['Fecha']} {row['Hora']}")

# ==================== TAB 4: ENTRETENIMIENTO ====================
with tabs[3]:
    subtabs_ent = st.tabs([" Ruleta de Comida", " Retos Semanales", " Generador de Citas", " Playlist"])
    
    # RULETA DE COMIDA
    with subtabs_ent[0]:
        st.markdown("###  Ruleta de Comida")
        st.info("️ Gira la ruleta para decidir qué plato típico cenarán en su primer día juntos")
        
        platos = [
            (" Ceviche", "Perú - Pescado fresco marinado en limón"),
            (" Lomo Saltado", "Perú - Carne salteada con papas fritas"),
            (" Ají de Gallina", "Perú - Pollo en crema de ají amarillo"),
            (" Asado", "Argentina - Parrillada de carne"),
            (" Empanadas", "Argentina - Empanadas de carne"),
            (" Milanesa", "Argentina - Carne empanizada"),
            (" Salteñas", "Bolivia - Empanadas jugosas"),
            (" Pique Macho", "Bolivia - Carne con papas fritas"),
            (" Anticuchos", "Bolivia - Brochetas de carne"),
        ]
        
        if 'plato_seleccionado' not in st.session_state:
            st.session_state.plato_seleccionado = None
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button(" GIRAR RULETA", use_container_width=True):
                st.session_state.plato_seleccionado = random.choice(platos)
                st.rerun()
        
        with col2:
            if st.session_state.plato_seleccionado:
                plato, desc = st.session_state.plato_seleccionado
                st.markdown(f"""
                <div class="ruleta-container">
                    <div class="ruleta-result">{plato}</div>
                    <div style="font-size:1.1rem; color:#ddd; margin-top:10px;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # RETOS SEMANALES
    with subtabs_ent[1]:
        st.markdown("###  Retos Semanales")
        df_retos = cargar_retos()
        semana_actual = df_retos.iloc[-1]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(" Videollamadas esta semana", int(semana_actual['Videollamadas']))
            if st.button(" Agregar Videollamada"):
                df_retos.at[df_retos.index[-1], 'Videollamadas'] += 1
                actualizar_retos(df_retos)
                st.rerun()
        
        with col2:
            st.metric(" Películas vistas juntos", int(semana_actual['Peliculas']))
            if st.button(" Agregar Película"):
                df_retos.at[df_retos.index[-1], 'Peliculas'] += 1
                actualizar_retos(df_retos)
                st.rerun()
    
    # GENERADOR DE CITAS VIRTUALES
    with subtabs_ent[2]:
        st.markdown("###  Generador de Citas Virtuales")
        
        ideas_citas = [
            " Ver una película juntos por videollamada",
            " Cocinar el mismo plato al mismo tiempo",
            " Jugar un juego online juntos",
            "️ Tour virtual por un museo",
            " Clase de baile por video",
            " Leer el mismo libro y discutirlo",
            " Dibujar/pintar juntos",
            " Ver el amanecer/atardecer juntos",
            " Compartir y escuchar música nueva",
            "️ Aprender palabras en el idioma del otro",
            " Tomar café/té virtual juntos",
            " Contar historias de su infancia",
        ]
        
        if st.button("Generar Idea de Cita", use_container_width=True):
            idea = random.choice(ideas_citas)
            st.success(f"**Idea:** {idea}")
            st.balloons()
    
    # PLAYLIST DE SPOTIFY
    with subtabs_ent[3]:
        st.markdown("### Playlist Compartida")
        st.info("Configura tu playlist de Spotify compartida aquí")
        
        # Ejemplo de embed de Spotify
        spotify_url = st.text_input("URL de Playlist de Spotify:", "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M")
        
        if spotify_url:
            # Extraer ID de playlist
            if "playlist/" in spotify_url:
                playlist_id = spotify_url.split("playlist/")[1].split("?")[0]
                st.markdown(f"""
                <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/{playlist_id}?utm_source=generator" 
                width="100%" height="380" frameBorder="0" allowfullscreen="" 
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
                """, unsafe_allow_html=True)

# ==================== TAB 5: IDENTIDAD CULTURAL ====================
with tabs[4]:
    subtabs_cult = st.tabs([" Mapa de Ruta", " Diccionario", " Curiosidades"])
    
    # MAPA DE RUTA
    with subtabs_cult[0]:
        st.markdown("### Mapa de la Ruta: Puno → Humahuaca")
        
        st.markdown(f"""
        <div class="glass-card">
            <h4> Ruta Terrestre</h4>
            <p><b>Origen:</b> Puno, Perú  (Lat: {PUNO_COORDS[0]}, Lon: {PUNO_COORDS[1]})</p>
            <p><b>Destino:</b> Humahuaca, Argentina  (Lat: {HUMAHUACA_COORDS[0]}, Lon: {HUMAHUACA_COORDS[1]})</p>
            <p><b>Distancia:</b> {distancia_km:,} km</p>
            <p><b>Tiempo estimado:</b> ~24 horas en bus</p>
            <p><b>Paradas intermedias:</b></p>
            <ul>
                <li> Copacabana, Bolivia</li>
                <li> La Paz, Bolivia</li>
                <li> La Quiaca, Argentina</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Mapa simple con coordenadas
        st.map(pd.DataFrame({
            'lat': [PUNO_COORDS[0], HUMAHUACA_COORDS[0]],
            'lon': [PUNO_COORDS[1], HUMAHUACA_COORDS[1]]
        }))
    
    # DICCIONARIO CULTURAL
    with subtabs_cult[1]:
        st.markdown("### Diccionario Puno-Humahuaca")
        st.caption("Aprende las palabras típicas del otro")
        
        df_dict = cargar_diccionario()
        
        # Buscador
        buscar = st.text_input(" Buscar palabra:", "")
        
        if buscar:
            df_filtrado = df_dict[df_dict['Palabra'].str.contains(buscar, case=False, na=False) | 
                                   df_dict['Significado'].str.contains(buscar, case=False, na=False)]
        else:
            df_filtrado = df_dict
        
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
    
    # CURIOSIDADES DIARIAS
    with subtabs_cult[2]:
        st.markdown("### Curiosidades Diarias")
        
        curiosidades = [
            ("", "El Lago Titicaca es el lago navegable más alto del mundo (3,812 msnm)"),
            ("", "Puno es conocida como la 'Capital Folklórica del Perú'"),
            ("", "Las Islas Flotantes de los Uros están hechas completamente de totora"),
            ("", "La Quebrada de Humahuaca fue declarada Patrimonio de la Humanidad por la UNESCO"),
            ("", "Humahuaca significa 'río sagrado' en lengua omaguaca"),
            ("", "El Cerro de los 14 Colores es una maravilla geológica única"),
            ("", "Bolivia tiene dos capitales: Sucre (constitucional) y La Paz (sede de gobierno)"),
            ("", "El Salar de Uyuni es el desierto de sal más grande del mundo"),
            ("", "La papa es originaria de Perú, con más de 3,000 variedades"),
            ("", "Argentina es el país más visitado de Sudamérica"),
        ]
        
        # Curiosidad del día basada en la fecha
        dia_del_año = datetime.now().timetuple().tm_yday
        curiosidad_hoy = curiosidades[dia_del_año % len(curiosidades)]
        
        st.markdown(f"""
        <div class="glass-card" style="background: rgba(139, 92, 246, 0.2);">
            <h3>{curiosidad_hoy[0]} Curiosidad del Día</h3>
            <p style="font-size:1.2rem; margin-top:15px;">{curiosidad_hoy[1]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(" Ver otra curiosidad"):
            nueva = random.choice(curiosidades)
            st.info(f"{nueva[0]} {nueva[1]}")

# ==================== TAB 6: GALERÍA ====================
with tabs[5]:
    st.markdown("### Galería de Recuerdos")
    
    col_upload, col_gallery = st.columns([1, 2])
    
    with col_upload:
        st.markdown("#### Subir Foto")
        if not CLOUDINARY_ENABLED:
            st.warning(" Cloudinary no configurado. Fotos se guardan localmente.")
        else:
            st.success(" Cloudinary activo")
        
        with st.form("upload_foto"):
            usuario_foto = st.radio("Subido por:", ["Felix", "Ara"], horizontal=True)
            descripcion_foto = st.text_input("Descripción:", placeholder="Nuestro primer viaje")
            uploaded_file = st.file_uploader("Foto", type=['jpg', 'jpeg', 'png', 'gif'])
            
            if st.form_submit_button(" Subir"):
                if uploaded_file:
                    guardar_foto(usuario_foto, descripcion_foto, uploaded_file)
                    st.success("¡Foto subida!")
                    time.sleep(0.5)
                    st.rerun()
    
    with col_gallery:
        st.markdown("#### ️ Recuerdos")
        df_galeria = cargar_galeria()
        
        if not df_galeria.empty:
            for idx, row in df_galeria.iloc[::-1].iterrows():
                emoji = "" if row['Usuario'] == "Felix" else ""
                st.markdown(f"**{emoji} {row['Usuario']}** - {row['Fecha']}")
                st.caption(row['Descripcion'])
                
                try:
                    if row['URL']:
                        st.image(row['URL'], use_container_width=True)
                    else:
                        st.image(row['Archivo_Local'], use_container_width=True)
                except:
                    st.error("Error al cargar imagen")
                
                st.markdown("---")
        else:
            st.info("Aún no hay fotos. ¡Sube la primera!")

# --- FOOTER ---
st.write("---")
st.caption(f" Sistema v10.0 COMPLETO | Sync: {datetime.now().strftime('%H:%M:%S')} | {'️ Cloud' if CLOUDINARY_ENABLED else ' Local'}")