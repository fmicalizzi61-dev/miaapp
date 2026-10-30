import math
import pandas as pd
import streamlit as st

# Configurazione della pagina dell'app
st.set_page_config(
    page_title="Calcolo Muro in C.A.", page_icon="🏗️", layout="centered"
)

st.title("🏗️ Pre-dimensionamento Muro di Sostegno")
st.write(
    "Inserisci i parametri geometrici e geotecnici per il calcolo delle spinte"
    " e delle armature."
)

# --- SEZIONE INPUT UTENTE ( Sidebar pulita ) ---
st.sidebar.header("📐 Dati Geometrici & Terreno")

h_stelo = st.sidebar.number_input(
    "Altezza dello stelo H (m)", min_value=1.0, max_value=10.0, value=4.0, step=0.1
)
gamma = st.sidebar.number_input(
    "Peso specifico terreno γ (kN/m³)",
    min_value=14.0,
    max_value=24.0,
    value=18.0,
    step=0.5,
)
phi_terreno = st.sidebar.number_input(
    "Angolo d'attrito φ (°)", min_value=15, max_value=45, value=30, step=1
)
q_sovraccarico = st.sidebar.number_input(
    "Sovraccarico q (kN/m²)", min_value=0.0, max_value=50.0, value=10.0, step=1.0
)

st.sidebar.header("🛠️ Armatura")
phi_barre = st.sidebar.selectbox(
    "Diametro barre Φ (mm)", [10, 12, 14, 16, 18, 20], index=3
)
passo_barre = st.sidebar.slider(
    "Interasse barre (cm)", min_value=10, max_value=30, value=15, step=1
)

# --- CALCOLI GEOTECNICI (Rankine) ---
phi_rad = math.radians(phi_terreno)
ka = math.tan(math.radians(45) - (phi_rad / 2)) ** 2
spinta_terreno = 0.5 * gamma * (h_stelo**2) * ka
spinta_q = q_sovraccarico * h_stelo * ka
spinta_totale = spinta_terreno + spinta_q

m_terreno = spinta_terreno * (h_stelo / 3)
m_q = spinta_q * (h_stelo / 2)
m_tot = m_terreno + m_q

# Area armatura effettiva (cm²/m)
area_singola = (math.pi * (phi_barre**2)) / 4
as_presente = (area_singola * (100 / passo_barre)) / 100

# --- VISUALIZZAZIONE RISULTATI A SCHERMO ---
st.subheader("📊 Risultati della Verifica")

col1, col2 = st.columns(2)
with col1:
  st.metric(label="Coefficiente Spinta (Ka)", value=f"{ka:.3f}")
  st.metric(label="Spinta Totale (S)", value=f"{spinta_totale:.2f} kN/m")
with col2:
  st.metric(label="Momento Sollecitante (Med)", value=f"{m_tot:.2f} kNm/m")
  st.metric(
      label="Armatura Disposta (As)",
      value=f"{as_presente:.2f} cm²/m",
      delta=f"Φ{phi_barre}/{passo_barre}cm",
  )

st.markdown("---")

# Tabella di confronto rapido per vari passi
st.subheader("📋 Tabella di raffronto interassi")
tabella_dati = []
for p in [10, 12, 15, 20, 25]:
  as_calc = ((math.pi * (phi_barre**2)) / 4 * (100 / p)) / 100
  tabella_dati.append({
      "Diametro": f"Φ{phi_barre}",
      "Passo": f"{p} cm",
      "As (cm²/m)": f"{as_calc:.2f}",
  })

st.table(pd.DataFrame(tabella_dati))