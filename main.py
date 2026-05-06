import requests
import datetime
import random

TELEGRAM_TOKEN = "TU_TOKEN_AQUI"
CHAT_ID = "TU_CHAT_ID_AQUI"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def get_sentiment():
    vix = random.randint(12, 30)
    if vix < 15:
        return "🟢 RISK ON"
    elif vix < 22:
        return "🟡 NEUTRAL"
    else:
        return "🔴 RISK OFF"

def get_levels(asset):
    price = random.randint(100, 1000)
    return price + 20, price - 20

def build_briefing(session):
    now = datetime.datetime.now().strftime("%H:%M")

    sentiment = get_sentiment()

    message = f"""
==========================
📊 MARKET BRIEFING
Sesión: {session}
Hora: {now}
==========================

🧠 SENTIMIENTO
{sentiment}

📰 NOTICIAS CLAVE
- Mercado atento a inflación
- Movimientos en tecnología
- Volatilidad en cripto

📉 NIVELES CLAVE
"""

    assets = ["NSQ100", "BTC", "ORO", "DXY", "VIX", "BRENT"]

    for a in assets:
        r, s = get_levels(a)
        message += f"\n{a}\nR: {r}\nS: {s}\n"

    message += """

⏰ EVENTOS HOY
- Revisar calendario económico
(ALTO IMPACTO)

⚠️ ACCIÓN
- Esperar confirmación
- Evitar operar en noticias
"""

    return message

def run(session):
    briefing = build_briefing(session)
    send_telegram(briefing)

if __name__ == "__main__":
    run("Manual")
