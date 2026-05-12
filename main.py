import requests
import matplotlib.pyplot as plt

from datetime import datetime
from zoneinfo import ZoneInfo

# =========================================
# TELEGRAM
# =========================================

TELEGRAM_TOKEN = "8774099880:AAFyVd-Id8eC4sGVztg9W0Z-1kPstLu6Hb0"
CHAT_ID = "1373100163"

# =========================================
# API KEYS
# =========================================

TWELVE_API_KEY = "2dc0921a150b439d8aebda732d168a34"

NEWS_API_KEY = "34551ef6b32345ceaa49cb5709f61296"

# =========================================
# TELEGRAM MENSAJE
# =========================================

def send(msg):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

# =========================================
# TELEGRAM FOTO
# =========================================

def send_photo(path):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"

    with open(path, "rb") as photo:

        requests.post(
            url,
            files={"photo": photo},
            data={"chat_id": CHAT_ID}
        )

# =========================================
# TWELVE DATA PRICE
# =========================================

def price(symbol):

    try:

        url = (
            f"https://api.twelvedata.com/price?"
            f"symbol={symbol}"
            f"&apikey={TWELVE_API_KEY}"
        )

        response = requests.get(url).json()

        value = response.get("price")

        if value is None:
            return None

        return float(value)

    except:

        return None

# =========================================
# NIVELES DINÁMICOS
# =========================================

def levels(price_now):

    if price_now is None:

        return None, None

    resistance = round(price_now * 1.01, 2)

    support = round(price_now * 0.99, 2)

    return resistance, support

# =========================================
# SESIÓN
# =========================================

def get_session():

    now = datetime.now(
        ZoneInfo("America/Santiago")
    )

    hour = now.hour

    # TOKYO
    if 19 <= hour or hour < 2:

        return "🌏 TOKYO SESSION"

    # NEW YORK
    elif 8 <= hour < 12:

        return "🇺🇸 NEW YORK SESSION"

    else:

        return "⏳ PRE-MARKET / TRANSICIÓN"

# =========================================
# CONTEXTO
# =========================================

def sentiment(vix, dxy, btc):

    if None in (vix, dxy, btc):

        return (
            "🟡 Mercado sin claridad.\n"
            "Esperar confirmación."
        )

    # RISK OFF
    if vix > 20 and dxy > 104:

        return (
            "🔴 Mercado defensivo.\n"
            "Hay miedo y fortaleza del dólar.\n"
            "Mayor probabilidad de volatilidad."
        )

    # RISK ON
    if vix < 15 and btc > 65000:

        return (
            "🟢 Mercado con apetito por riesgo.\n"
            "Condiciones favorables para compras."
        )

    return (
        "🟡 Mercado mixto.\n"
        "No hay dirección clara."
    )

# =========================================
# SETUPS
# =========================================

def setup(price_now, resistance, support, sentiment_text):

    if price_now is None:

        return "🟡 DATOS NO DISPONIBLES"

    # LONG
    if (
        price_now > resistance
        and "🟢" in sentiment_text
    ):

        return "🟢 LONG SETUP"

    # SHORT
    if (
        price_now < support
        and "🔴" in sentiment_text
    ):

        return "🔴 SHORT SETUP"

    return "🟡 NO TRADE"

# =========================================
# NEWS
# =========================================

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

            title = article.get(
                "title",
                "Sin título"
            )

            news.append(
                f"• {title[:90]}"
            )

        while len(news) < 3:

            news.append(
                "• Sin noticia relevante"
            )

        return news

    except:

        return [
            "• Error cargando noticias",
            "• Error cargando noticias",
            "• Error cargando noticias"
        ]

# =========================================
# GRÁFICOS REALES 15M
# =========================================

def create_chart(symbol, resistance, support, name):

    try:

        url = (
            f"https://api.twelvedata.com/time_series?"
            f"symbol={symbol}"
            f"&interval=15min"
            f"&outputsize=20"
            f"&apikey={TWELVE_API_KEY}"
        )

        data = requests.get(url).json()

        values = data.get("values")

        if values is None:

            return None

        closes = []

        for candle in reversed(values):

            closes.append(
                float(candle["close"])
            )

        fig, ax = plt.subplots(
            figsize=(6,4)
        )

        ax.plot(closes)

        # RESISTENCIA
        ax.axhline(
            resistance,
            linestyle="--"
        )

        # SOPORTE
        ax.axhline(
            support,
            linestyle="--"
        )

        ax.set_title(f"{name} 15M")

        file_name = f"{name}.png"

        plt.savefig(file_name)

        plt.close()

        return file_name

    except:

        return None

# =========================================
# BUILD BRIEFING
# =========================================

def build():

    now = datetime.now(
        ZoneInfo("America/Santiago")
    ).strftime("%H:%M")

    session = get_session()

    # =====================================
    # ACTIVOS
    # =====================================

    vix = price("VIXY")

    dxy = price("DX")

    btc = price("BTC/USD")

    nasdaq = price("QQQ")

    gold = price("XAU/USD")

    brent = price("BRENT")

    # =====================================
    # CONTEXTO
    # =====================================

    market_context = sentiment(
        vix,
        dxy,
        btc
    )

    # =====================================
    # NIVELES DINÁMICOS
    # =====================================

    nsq_r, nsq_s = levels(nasdaq)

    btc_r, btc_s = levels(btc)

    gold_r, gold_s = levels(gold)

    # =====================================
    # SETUPS
    # =====================================

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

    # =====================================
    # DECISIÓN FINAL
    # =====================================

    if "LONG" in (
        nsq_setup + btc_setup
    ):

        decision = (
            "🟢 Mercado operable LONG"
        )

    elif "SHORT" in (
        nsq_setup + btc_setup
    ):

        decision = (
            "🔴 Mercado operable SHORT"
        )

    else:

        decision = (
            "🟡 Esperar confirmación"
        )

    # =====================================
    # NEWS
    # =====================================

    news = get_news()

    # =====================================
    # MENSAJE
    # =====================================

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

# =========================================
# RUN
# =========================================

def run():

    # MENSAJE
    send(build())

    # =====================================
    # ACTIVOS GRÁFICOS
    # =====================================

    assets = [

        ("QQQ", "NSQ100"),

        ("BTC/USD", "BTC"),

        ("XAU/USD", "ORO")

    ]

    for symbol, name in assets:

        asset_price = price(symbol)

        resistance, support = levels(
            asset_price
        )

        chart = create_chart(
            symbol,
            resistance,
            support,
            name
        )

        if chart:

            send_photo(chart)

# =========================================
# START
# =========================================

if __name__ == "__main__":

    run()
