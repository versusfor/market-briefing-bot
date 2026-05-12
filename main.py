import requests
import matplotlib.pyplot as plt

from datetime import datetime
from zoneinfo import ZoneInfo

# ================================
# TELEGRAM
# ================================

TELEGRAM_TOKEN = "8774099880:AAFyVd-Id8eC4sGVztg9W0Z-1kPstLu6Hb0"
CHAT_ID = "1373100163"

# ================================
# NEWS API
# ================================

NEWS_API_KEY = "34551ef6b32345ceaa49cb5709f61296"

# ================================
# TELEGRAM MENSAJES
# ================================

def send(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

def send_photo(path):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"

    with open(path, "rb") as photo:

        requests.post(
            url,
            files={"photo": photo},
            data={"chat_id": CHAT_ID}
        )

# ================================
# PRECIOS
# ================================

def price(symbol):

    try:

        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"

        data = requests.get(url).json()

        return data["quoteResponse"]["result"][0]["regularMarketPrice"]

    except:

        return None

# ================================
# SESIONES
# ================================

def get_session():

    now = datetime.now(ZoneInfo("America/Santiago"))
    hour = now.hour

    # TOKYO
    if 19 <= hour or hour < 2:
        return "🌏 TOKYO SESSION"

    # NEW YORK
    elif 8 <= hour < 12:
        return "🇺🇸 NEW YORK SESSION"

    else:
        return "⏳ PRE-MARKET / TRANSICIÓN"

# ================================
# CONTEXTO MERCADO
# ================================

def sentiment(vix, dxy, btc):

    if None in (vix, dxy, btc):

        return "🟡 Mercado sin claridad. Esperar confirmación antes de operar."

    # RISK OFF
    if vix > 20 and dxy > 104:

        return (
            "🔴 Mercado defensivo.\n"
            "Hay miedo y fortaleza del dólar.\n"
            "Mayor probabilidad de volatilidad o caídas."
        )

    # RISK ON
    if vix < 15 and btc > 65000:

        return (
            "🟢 Mercado con apetito por riesgo.\n"
            "Condiciones más limpias para buscar compras."
        )

    return (
        "🟡 Mercado mixto.\n"
        "No hay dirección clara todavía."
    )

# ================================
# SETUPS
# ================================

def setup(price_now, resistance, support, sentiment_text):

    if price_now is None:
        return "N/A"

    # LONG
    if price_now > resistance and "🟢" in sentiment_text:

        return "🟢 LONG SETUP"

    # SHORT
    if price_now < support and "🔴" in sentiment_text:

        return "🔴 SHORT SETUP"

    return "🟡 NO TRADE"

# ================================
# NEWS REALES
# ================================

def get_news():

    try:

        url = (
            "https://newsapi.org/v2/everything?"
            "q=inflation OR Federal Reserve OR interest rates OR Nasdaq OR Bitcoin"
            "&language=es"
            "&sortBy=publishedAt"
            "&pageSize=3"
            f"&apiKey={NEWS_API_KEY}"
        )

        data = requests.get(url).json()

        articles = data.get("articles", [])

        news = []

        for article in articles[:3]:

            title = article.get("title", "Sin título")

            news.append(f"• {title[:90]}")

        while len(news) < 3:

            news.append("• Sin noticia relevante")

        return news

    except:

        return [
            "• Error cargando noticias",
            "• Error cargando noticias",
            "• Error cargando noticias"
        ]

# ================================
# MINI GRÁFICO
# ================================

def create_chart(price_now, resistance, support, name):

    try:

        fig, ax = plt.subplots()

        simulated_data = [
            price_now * 0.98,
            price_now * 0.99,
            price_now,
            price_now * 1.01,
            price_now
        ]

        ax.plot(simulated_data)

        ax.axhline(
            resistance,
            linestyle="--"
        )

        ax.axhline(
            support,
            linestyle="--"
        )

        ax.set_title(name)

        file_name = f"{name}.png"

        plt.savefig(file_name)

        plt.close()

        return file_name

    except:

        return None

# ================================
# BUILD MENSAJE
# ================================

def build():

    now = datetime.now(
        ZoneInfo("America/Santiago")
    ).strftime("%H:%M")

    session = get_session()

    # DATOS
    vix = price("%5EVIX")
    dxy = price("DX-Y.NYB")
    btc = price("BTC-USD")
    nasdaq = price("^NDX")
    gold = price("GC=F")

    # CONTEXTO
    market_context = sentiment(
        vix,
        dxy,
        btc
    )

    # NIVELES
    nsq_r, nsq_s = 18000, 17500
    btc_r, btc_s = 70000, 65000
    gold_r, gold_s = 2400, 2300

    # SETUPS
    nsq_setup = setup(
        nasdaq,
        nsq_r,
        nsq_s,
        market_context
    )

    btc_setup = setup(
        btc,
        btc_r,
        btc_s,
        market_context
    )

    gold_setup = setup(
        gold,
        gold_r,
        gold_s,
        market_context
    )

    # DECISIÓN
    if "LONG" in (nsq_setup + btc_setup):

        decision = "🟢 MERCADO OPERABLE LONG"

    elif "SHORT" in (nsq_setup + btc_setup):

        decision = "🔴 MERCADO OPERABLE SHORT"

    else:

        decision = "🟡 ESPERAR CONFIRMACIÓN"

    # NOTICIAS
    news = get_news()

    # MENSAJE
    msg = f"""
📊 MARKET BRIEFING PRO
{session} | {now}

━━━━━━━━━━━━━━━
🧠 CONTEXTO

{market_context}

VIX: {vix}
DXY: {dxy}

━━━━━━━━━━━━━━━
🚨 SETUPS

NSQ100 → {nsq_setup}
BTC → {btc_setup}
ORO → {gold_setup}

━━━━━━━━━━━━━━━
📉 NIVELES CLAVE

NSQ100 → {nsq_r} / {nsq_s}
BTC → {btc_r} / {btc_s}
ORO → {gold_r} / {gold_s}

━━━━━━━━━━━━━━━
📰 MACRO HOY

{news[0]}
{news[1]}
{news[2]}

━━━━━━━━━━━━━━━
⚠️ DECISIÓN FINAL

{decision}

• Solo entrar con confirmación
• Evitar operar noticias fuertes
• Reducir riesgo si VIX alto

━━━━━━━━━━━━━━━
"""

    return msg

# ================================
# RUN
# ================================

def run():

    # MENSAJE
    send(build())

    # GRÁFICO NSQ100
    nasdaq = price("^NDX")

    chart = create_chart(
        nasdaq,
        18000,
        17500,
        "NSQ100"
    )

    if chart:

        send_photo(chart)

# ================================
# START
# ================================

if __name__ == "__main__":

    run()
