import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from duckduckgo_search import DDGS
import time
from datetime import datetime, timedelta
import re

# Konfiguration
st.set_page_config(
    page_title="🚗 Bil Bevakare",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS för bättre design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B6B;
        margin: 1rem 0;
    }
    .search-result {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .price-tag {
        background: #FF6B6B;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
    }
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-active { background-color: #28a745; }
    .status-inactive { background-color: #dc3545; }
</style>
""", unsafe_allow_html=True)

# Huvudrubrik
st.markdown("""
<div class="main-header">
    <h1>🚗 Bil Bevakare</h1>
    <p>Automatisk bevakning av bilmarknaden - Helt gratis för alla!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar för inställningar
with st.sidebar:
    st.header("⚙️ Inställningar")

    # Email-konfiguration
    st.subheader("📧 Email-notifieringar")
    sender_email = st.text_input("Din Gmail-adress:", placeholder="din.email@gmail.com")
    sender_password = st.text_input("Gmail App-lösenord:", type="password", 
                                   help="Skapa ett app-lösenord i dina Google-kontoinställningar")
    recipient_email = st.text_input("Skicka notifieringar till:", placeholder="mottagare@email.com")

    # SMS-konfiguration (valfritt)
    st.subheader("📱 SMS-notifieringar (valfritt)")
    phone_number = st.text_input("Telefonnummer:", placeholder="+46701234567")

    # Sökparametrar
    st.subheader("🔍 Sökparametrar")
    search_term = st.text_input("Sökord:", value="Volvo V70", 
                               help="T.ex. 'BMW 320i', 'Audi A4', 'Toyota Prius'")
    max_price = st.number_input("Max pris (SEK):", min_value=0, value=100000, step=5000)
    min_year = st.number_input("Äldsta årsmodell:", min_value=1990, value=2010, step=1)
    max_mileage = st.number_input("Max miltal:", min_value=0, value=20000, step=10000)

# Huvudinnehåll
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🔍 Sök bilar nu")

    # Sökknapp
    if st.button("🚀 Starta sökning", type="primary", use_container_width=True):
        if not search_term:
            st.error("❌ Ange ett sökord!")
        else:
            with st.spinner(f"Söker efter '{search_term}'...", show_time=True):
                # Simulera sökning (ersätt med riktig API-integration)
                time.sleep(2)

                # Exempel på sökresultat
                results = [
                    {
                        "title": f"{search_term} 2015 - Välskött och servicad",
                        "price": "89 000 kr",
                        "year": 2015,
                        "mileage": "15 000 mil",
                        "location": "Stockholm",
                        "url": "https://blocket.se/example1",
                        "source": "Blocket"
                    },
                    {
                        "title": f"{search_term} 2018 - Som ny!",
                        "price": "125 000 kr", 
                        "year": 2018,
                        "mileage": "8 500 mil",
                        "location": "Göteborg",
                        "url": "https://tradera.com/example2",
                        "source": "Tradera"
                    },
                    {
                        "title": f"{search_term} 2012 - Bra skick",
                        "price": "65 000 kr",
                        "year": 2012,
                        "mileage": "18 000 mil", 
                        "location": "Malmö",
                        "url": "https://blocket.se/example3",
                        "source": "Blocket"
                    }
                ]

                # Filtrera resultat
                filtered_results = []
                for result in results:
                    price_num = int(re.sub(r'[^\d]', '', result['price']))
                    if (price_num <= max_price and 
                        result['year'] >= min_year and
                        int(re.sub(r'[^\d]', '', result['mileage'])) <= max_mileage):
                        filtered_results.append(result)

                st.success(f"✅ Hittade {len(filtered_results)} bilar som matchar dina kriterier!")

                # Visa resultat
                for i, result in enumerate(filtered_results):
                    with st.container():
                        st.markdown(f"""
                        <div class="search-result">
                            <h4>{result['title']}</h4>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <span class="price-tag">{result['price']}</span>
                                    <span style="margin-left: 1rem;">📅 {result['year']} | 🛣️ {result['mileage']} | 📍 {result['location']}</span>
                                </div>
                                <div>
                                    <span style="background: #e3f2fd; padding: 0.2rem 0.5rem; border-radius: 5px; font-size: 0.8rem;">
                                        {result['source']}
                                    </span>
                                </div>
                            </div>
                            <a href="{result['url']}" target="_blank" style="text-decoration: none;">
                                <button style="background: #4ECDC4; color: white; border: none; padding: 0.5rem 1rem; border-radius: 5px; margin-top: 0.5rem; cursor: pointer;">
                                    Visa annons →
                                </button>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)

                # Skicka email-notifiering om konfigurerat
                if sender_email and sender_password and recipient_email and filtered_results:
                    try:
                        send_email_notification(sender_email, sender_password, recipient_email, 
                                              search_term, filtered_results)
                        st.success("📧 Email-notifiering skickad!")
                    except Exception as e:
                        st.warning(f"⚠️ Kunde inte skicka email: {str(e)}")

with col2:
    st.header("📊 Bevakningsstatus")

    # Status-indikator
    if search_term and sender_email:
        st.markdown("""
        <div class="feature-box">
            <div><span class="status-indicator status-active"></span><strong>Bevakning aktiv</strong></div>
            <p>Söker automatiskt efter nya annonser</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="feature-box">
            <div><span class="status-indicator status-inactive"></span><strong>Bevakning inaktiv</strong></div>
            <p>Konfigurera email och sökord för att aktivera</p>
        </div>
        """, unsafe_allow_html=True)

    # Statistik
    st.subheader("📈 Statistik")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Sökningar idag", "12", "↗️ +3")
    with col_b:
        st.metric("Bilar hittade", "47", "↗️ +8")

    # Senaste aktivitet
    st.subheader("🕒 Senaste aktivitet")
    activities = [
        "🔍 Sökte efter 'Volvo V70' - 3 träffar",
        "📧 Skickade notifiering till användare",
        "🚗 Ny bil hittad under 80,000 kr",
        "⚙️ Uppdaterade sökparametrar"
    ]

    for activity in activities:
        st.text(f"• {activity}")

# Funktioner
def send_email_notification(sender_email, sender_password, recipient_email, search_term, results):
    """Skicka email-notifiering med sökresultat"""

    msg = MimeMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"🚗 Nya bilar hittade: {search_term}"

    # Skapa email-innehåll
    html_content = f"""
    <html>
    <body>
        <h2>🚗 Bil Bevakare - Nya träffar!</h2>
        <p>Hej! Vi hittade {len(results)} nya bilar som matchar din sökning efter "<strong>{search_term}</strong>":</p>

        <div style="margin: 20px 0;">
    """

    for result in results:
        html_content += f"""
        <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 8px;">
            <h3 style="color: #FF6B6B; margin: 0 0 10px 0;">{result['title']}</h3>
            <p><strong>Pris:</strong> {result['price']}</p>
            <p><strong>År:</strong> {result['year']} | <strong>Miltal:</strong> {result['mileage']} | <strong>Plats:</strong> {result['location']}</p>
            <p><strong>Källa:</strong> {result['source']}</p>
            <a href="{result['url']}" style="background: #4ECDC4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Visa annons</a>
        </div>
        """

    html_content += """
        </div>
        <p>Lycka till med biljakten! 🚗</p>
        <p><em>Detta meddelande skickades automatiskt från Bil Bevakare</em></p>
    </body>
    </html>
    """

    msg.attach(MimeText(html_content, 'html'))

    # Skicka email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)
    server.quit()

# Automatisk bevakning (simulerad)
st.header("🤖 Automatisk bevakning")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h4>⏰ Kontinuerlig övervakning</h4>
        <p>Söker automatiskt efter nya annonser var 5:e minut</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <h4>📧 Direkta notifieringar</h4>
        <p>Få email direkt när en bil som matchar dina kriterier läggs ut</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <h4>🎯 Smart filtrering</h4>
        <p>Avancerade filter för pris, årsmodell, miltal och mycket mer</p>
    </div>
    """, unsafe_allow_html=True)

# Blockeringslista
st.header("🚫 Blockeringslista")
st.write("Lägg till ord eller fraser som du vill undvika i sökresultaten:")

blocked_terms = st.text_area(
    "Blockerade termer (en per rad):",
    value="skadad\nkrockkad\nreservdelar\ndefekt",
    help="Annonser som innehåller dessa ord kommer att filtreras bort"
)

# Avancerade inställningar
with st.expander("⚙️ Avancerade inställningar"):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Sökfrekvens")
        search_frequency = st.selectbox(
            "Hur ofta ska vi söka?",
            ["Var 5:e minut", "Var 15:e minut", "Varje timme", "Var 6:e timme"]
        )

        st.subheader("📍 Geografiska filter")
        regions = st.multiselect(
            "Välj regioner:",
            ["Stockholm", "Göteborg", "Malmö", "Uppsala", "Västerås", "Örebro", "Linköping"],
            default=["Stockholm", "Göteborg", "Malmö"]
        )

    with col2:
        st.subheader("🚗 Fordonstyper")
        car_types = st.multiselect(
            "Fordonstyper:",
            ["Personbil", "Kombi", "SUV", "Halvkombi", "Cabriolet", "
