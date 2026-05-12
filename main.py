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
# PRECIO
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
# DATOS 15M
# =========================================

def get_15m_data(symbol):

    try:

        url = (
            f"https://api.twelvedata.com/time_series?"
            f"symbol={symbol}"
            f"&interval=15min"
            f"&outputsize=200"
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

        return closes

    except:

        return None

# =========================================
# EMA
# =========================================

def ema(data, period):

    ema_values = []

    multiplier = 2 / (period + 1)

    sma = sum(data[:period]) / period

    ema_values.append(sma)

    for price_now in data[period:]:

        new_ema = (
            (price_now - ema_values[-1])
            * multiplier
        ) + ema_values[-1]

        ema_values.append(new_ema)

    return ema_values

# =========================================
# ESTRATEGIA EMA 55 / 144
# =========================================

def ema_strategy(symbol):

    data = get_15m_data(symbol)

    if data is None or len(data) < 150:

        return (
            "🟡 DATOS INSUFICIENTES",
            None,
            None,
            None
        )

    ema55 = ema(data, 55)

    ema144 = ema(data, 144)

    current_price = data[-1]

    current_ema55 = ema55[-1]

    current_ema144 = ema144[-1]

    # =====================================
    # LONG
    # =====================================

    if (
        current_price > current_ema55
        and current_ema55 > current_ema144
    ):

        signal = "🟢 LONG"

    # =====================================
    # SHORT
    # =====================================

    elif (
        current_price < current_ema55
        and current_ema55 < current_ema144
    ):

        signal = "🔴 SHORT"

    else:

        signal = "🟡 NO TRADE"

    return (
        signal,
        data,
        ema55,
        ema144
    )

# =========================================
# SESIÓN
# =========================================

def get_session():

    now = datetime.now(
        ZoneInfo("America/Santiago")
    )

    hour = now.hour

    if 19 <= hour or hour < 2:

        return "🌏 TOKYO SESSION"

    elif 8 <= hour < 12:

        return "🇺🇸 NEW YORK SESSION"

    else:

        return "⏳ PRE-MARKET"

# =========================================
# SENTIMIENTO
# =========================================

def sentiment(vix, dxy, btc):

    if None in (vix, dxy, btc):

        return (
            "🟡 Mercado mixto.\n"
            "Esperar confirmación."
        )

    if vix > 20 and dxy > 104:

        return (
            "🔴 Mercado defensivo.\n"
            "Alta volatilidad."
        )

    if vix < 15 and btc > 65000:

        return (
            "🟢 Mercado con apetito por riesgo."
        )

    return (
        "🟡 Mercado lateral."
    )

# =========================================
# NEWS
# =========================================

def get_news():

    try:

        url = (
            "https://newsapi.org/v2/everything?"
            "q=Federal Reserve OR inflation OR Nasdaq OR Bitcoin"
            "&language=en"
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
            "• Error noticias",
            "• Error noticias",
            "• Error noticias"
        ]

# =========================================
# GRÁFICO EMA
# =========================================

def create_chart(
    name,
    data,
    ema55,
    ema144
):

    try:

        if (
            data is None
            or ema55 is None
            or ema144 is None
        ):

            return None

        plt.style.use(
            "dark_background"
        )

        fig, ax = plt.subplots(
            figsize=(7,4)
        )

        ax.plot(
            data[-100:],
            linewidth=2,
            label="PRECIO"
        )

        ax.plot(
            range(
                55,
                55 + len(ema55[-100:])
            ),
            ema55[-100:],
            linewidth=2,
            label="EMA 55"
        )

        ax.plot(
            range(
                144,
                144 + len(ema144[-100:])
            ),
            ema144[-100:],
            linewidth=2,
            label="EMA 144"
        )

        ax.set_title(
            f"{name} | EMA 55 / 144"
        )

        ax.grid(True)

        ax.legend()

        file_name = f"{name}.png"

        plt.savefig(
            file_name,
            bbox_inches="tight"
        )

        plt.close()

        return file_name

    except:

        return None

# =========================================
# BUILD
# =========================================

def build():

    now = datetime.now(
        ZoneInfo("America/Santiago")
    ).strftime("%H:%M")

    session = get_session()

    # =====================================
    # MERCADO
    # =====================================

    vix = price("VIXY")

    dxy = price("DX")

    btc_price = price("BTC/USD")

    market_context = sentiment(
        vix,
        dxy,
        btc_price
    )

    # =====================================
    # ESTRATEGIAS
    # =====================================

    nsq_signal, _, _, _ = ema_strategy(
        "NASDAQ"
    )

    btc_signal, _, _, _ = ema_strategy(
        "BTC/USD"
    )

    gold_signal, _, _, _ = ema_strategy(
        "XAU/USD"
    )

    # =====================================
    # DECISIÓN
    # =====================================

    if (
        "🟢" in nsq_signal
        or "🟢" in btc_signal
    ):

        decision = (
            "🟢 Sesgo alcista."
        )

    elif (
        "🔴" in nsq_signal
        or "🔴" in btc_signal
    ):

        decision = (
            "🔴 Sesgo bajista."
        )

    else:

        decision = (
            "🟡 Esperar confirmación."
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

VIX → {vix}
DXY → {dxy}

━━━━━━━━━━━━━━━
🚨 EMA 55 / 144

NSQ100 → {nsq_signal}

BTC → {btc_signal}

ORO → {gold_signal}

━━━━━━━━━━━━━━━
📰 MACRO HOY

{news[0]}

{news[1]}

{news[2]}

━━━━━━━━━━━━━━━
⚠️ DECISIÓN

{decision}

• Esperar confirmación
• Evitar sobreoperar
• Riesgo bajo en noticias

━━━━━━━━━━━━━━━
"""

    return msg

# =========================================
# RUN
# =========================================

def run():

    send(build())

    assets = [

        ("NASDAQ", "NSQ100"),

        ("BTC/USD", "BTC"),

        ("XAU/USD", "ORO")

    ]

    for symbol, name in assets:

        signal, data, ema55, ema144 = ema_strategy(
            symbol
        )

        chart = create_chart(
            name,
            data,
            ema55,
            ema144
        )

        if chart:

            send_photo(chart)

# =========================================
# START
# =========================================

if __name__ == "__main__":

    run()
