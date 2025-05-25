import requests
from datetime import datetime

# === CONFIGURACIÓN INICIAL ===
ciudad_actual = "Cartagena"
lat = 10.4006
lon = -75.5144
openweather_api = "1fd4e1f2a68bcdf3b85d37cf59e07338"
telegram_bot_token = "7137024853:AAFBgsW0ZF9tYA3uBTD3q5j9Th1Hfhw7tyA"
chat_id = "729628766"

def obtener_datos_clima():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=es&appid={openweather_api}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

def generar_mensaje(datos):
    if not datos:
        return "❌ No se pudo obtener el clima."

    temp = datos['main']['temp']
    sensacion = datos['main']['feels_like']
    humedad = datos['main']['humidity']
    viento = datos['wind']['speed']
    descripcion = datos['weather'][0]['description'].capitalize()
    visibilidad = datos.get('visibility', 0) / 1000

    mensaje = f"📍 Ciudad: {ciudad_actual}\n"
    mensaje += f"🕒 Última lectura: {datetime.now().strftime('%H:%M:%S')}\n\n"
    mensaje += f"🌡️ Temp: {temp}°C | Sensación: {sensacion}°C\n"
    mensaje += f"💧 Humedad: {humedad}%\n"
    mensaje += f"🌬️ Viento: {viento} m/s\n"
    mensaje += f"🌫️ Visibilidad: {visibilidad:.1f} km\n"
    mensaje += f"📄 Estado: {descripcion}\n"
    return mensaje

def enviar_mensaje_telegram(texto):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": texto, "parse_mode": "Markdown"}
    requests.post(url, json=data)

datos = obtener_datos_clima()
mensaje = generar_mensaje(datos)
enviar_mensaje_telegram(mensaje)
