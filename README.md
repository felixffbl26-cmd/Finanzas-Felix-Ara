# 💕 Dashboard Felix & Ara - VERSIÓN COMPLETA

Dashboard integral para Felix (Perú 🇵🇪) y Ara (Argentina 🇦🇷) con **20+ funcionalidades** que combinan finanzas, planificación de viaje, conexión emocional, entretenimiento y cultura.

---

## ✨ Funcionalidades Completas

### 🎯 Preparación de Viaje
- ✅ **Checklist de Maleta** - Lista interactiva con progreso
- 🗺️ **Itinerario de Citas** - Lugares por visitar con checkboxes
- 🎯 **Metas por Hitos** - Pasajes, hotel, cena con barras de progreso
- 📞 **Directorio de Emergencia** - Contactos y direcciones

### ❤️ Conexión Emocional
- ⏳ **Cápsula del Tiempo** - Mensajes bloqueados hasta 15-ene-2026
- 🌡️ **Clima Dual** - Puno vs Humahuaca en tiempo real
- 📍 **Contador de Distancia** - 843.79 km exactos
- 📝 **Muro de Post-it** - Notas cortas con colores
- ☀️ **Saludador Horario** - Mensaje dinámico según hora
- 💋 **Contador de Besos** - Botón "Te extraño" compartido

### 🎮 Entretenimiento
- 🎲 **Ruleta de Comida** - Platos típicos aleatorios
- 🎵 **Playlist de Spotify** - Widget embebido
- 🎯 **Retos Semanales** - Videollamadas y películas
- 💡 **Generador de Citas** - Ideas para actividades virtuales
- 📸 **Álbum Dinámico** - Galería de fotos mejorada

### 🌍 Identidad Cultural
- 🗺️ **Mapa de Ruta** - Puno → Humahuaca visualizado
- 📖 **Diccionario** - Palabras típicas Puno-Humahuaca
- 🎓 **Curiosidades Diarias** - Datos de Perú y Argentina
- ⏰ **Cuenta Regresiva GIGANTE** - Días/Horas/Min/Seg

### 💰 Finanzas (Mantenidas)
- 🧮 Conversor Multidivisa
- 💰 Bóveda de Ahorros
- 📈 Gráfico de Crecimiento
- 💵 Cotizaciones en Tiempo Real

---

## 🚀 Instalación y Uso

### 1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación:
```bash
python -m streamlit run app.py --server.port 8888
```

### 3. Abrir en navegador:
```
http://localhost:8888
```

---

## 📁 Estructura de Archivos

### Archivos Principales
- `app.py` - Aplicación principal (~1,400 líneas)
- `requirements.txt` - Dependencias
- `.env.example` - Configuración de Cloudinary (opcional)
- `README.md` - Este archivo

### Archivos CSV (creados automáticamente)
- `ahorros_felix_ara.csv` - Ahorros
- `mensajes_amor.csv` - Mensajes
- `galeria_fotos.csv` - Fotos
- `fechas_especiales.csv` - Fechas importantes
- `gastos_viaje.csv` - Gastos de viaje
- `checklist_maleta.csv` - Items de maleta
- `itinerario.csv` - Lugares por visitar
- `metas_hitos.csv` - Metas financieras
- `directorio_emergencia.csv` - Contactos
- `capsula_tiempo.csv` - Mensajes bloqueados
- `notas_postit.csv` - Notas cortas
- `contador_besos.csv` - Historial de extrañar
- `retos_semanales.csv` - Progreso semanal
- `diccionario_cultural.csv` - Palabras típicas

---

## 🎨 Características de Diseño

- **Glassmorphism** con efectos de vidrio
- **Animaciones suaves** en hover y transiciones
- **Gradientes animados** en títulos
- **Cuenta regresiva en tiempo real** con segundos
- **Colores dinámicos** según contexto
- **Fuente Poppins** de Google Fonts
- **6 pestañas principales** organizadas

---

## 🔧 Configuración Opcional

### Cloudinary (Fotos en la Nube)
1. Crear cuenta gratuita en [cloudinary.com](https://cloudinary.com)
2. Copiar `.env.example` a `.env`
3. Completar con tus credenciales:
   ```
   CLOUDINARY_CLOUD_NAME=tu_cloud_name
   CLOUDINARY_API_KEY=tu_api_key
   CLOUDINARY_API_SECRET=tu_api_secret
   ```
4. Reiniciar la app

### Playlist de Spotify
1. Ir a pestaña "🎮 Entretenimiento" → "🎵 Playlist"
2. Pegar URL de tu playlist compartida
3. El reproductor se embebe automáticamente

---

## 💡 Guía de Uso Rápida

### Para Planificar el Viaje:
1. **Checklist de Maleta**: Marca items conforme empaques
2. **Itinerario**: Marca lugares conforme los visiten
3. **Metas por Hitos**: Revisa cuánto falta ahorrar
4. **Directorio**: Ten a mano contactos de emergencia

### Para Conexión Emocional:
1. **Cápsula del Tiempo**: Escribe mensajes para leer juntos en enero 2026
2. **Post-it**: Deja notas de buenos días
3. **Contador de Besos**: Presiona cuando extrañes
4. **Mensajes**: Envíense mensajes de amor

### Para Entretenimiento:
1. **Ruleta de Comida**: Gira para decidir qué cenar
2. **Retos Semanales**: Actualiza cada videollamada/película
3. **Generador de Citas**: Obtén ideas para actividades
4. **Playlist**: Escuchen música juntos

### Para Aprender:
1. **Diccionario**: Busca palabras típicas del otro país
2. **Curiosidades**: Lee el dato del día
3. **Mapa**: Visualiza la ruta del viaje

---

## 📊 APIs Utilizadas

- **wttr.in** - Clima en tiempo real
- **DolarAPI** - Cotización dólar blue Argentina
- **ExchangeRate-API** - Tasas de cambio
- **Cloudinary** (opcional) - Almacenamiento de fotos
- **Spotify** - Reproductor embebido
- **Geopy** - Cálculo de distancias

---

## 🎯 Características Destacadas

### Actualizaciones Automáticas:
- ⏰ Cuenta regresiva se actualiza cada segundo
- 🌡️ Clima se actualiza cada 30 minutos
- ☀️ Saludador cambia según la hora
- 🎓 Curiosidad cambia cada día
- 📅 Retos se resetean cada lunes

### Interactividad:
- ✅ Checkboxes persistentes
- 🎲 Ruleta animada
- 💋 Contador con animación de globos
- 📝 Post-it con colores aleatorios
- 🔒 Cápsula bloqueada hasta fecha específica

---

## 🆘 Solución de Problemas

**No veo los cambios:**
- Presiona `Ctrl + R` en el navegador
- O reinicia el servidor

**Error al instalar dependencias:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Puerto 8888 en uso:**
```bash
python -m streamlit run app.py --server.port 8889
```

**Clima no se actualiza:**
- Verifica conexión a internet
- El API wttr.in es gratuito y puede tener límites

---

## 📈 Estadísticas del Proyecto

- **Líneas de código:** ~1,400
- **Funcionalidades:** 24+
- **Pestañas:** 6 principales, 13 sub-pestañas
- **Archivos CSV:** 14
- **Animaciones CSS:** 5
- **APIs integradas:** 6

---

## 💖 Hecho con Amor

Creado para Felix y Ara - Conectando Puno 🇵🇪 y Humahuaca 🇦🇷

**Versión:** 10.0 COMPLETA  
**Última actualización:** Diciembre 2025  
**Funcionalidades totales:** 20+

---

## 📝 Changelog

### v10.0 (Actual) - VERSIÓN COMPLETA
- ✅ 20+ funcionalidades nuevas implementadas
- ✅ Cuenta regresiva gigante con segundos
- ✅ Clima dual en tiempo real
- ✅ Cápsula del tiempo
- ✅ Ruleta de comida
- ✅ Diccionario cultural
- ✅ Y mucho más...

### v9.0 - Funcionalidades Básicas
- Galería de fotos
- Mensajes de amor
- Calculadora de viaje
- Fechas especiales

### v8.0 - Versión Original
- Conversor de divisas
- Bóveda de ahorros
- Cotizaciones en tiempo real

---

**¡Disfruten su dashboard completo! 🚀💕**
