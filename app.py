import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
import os

# Importiamo i moduli sintomi
from sintomi.schiena import visualizza_schiena, calcola_responso_schiena
from sintomi.intestino import visualizza_intestino, calcola_responso_intestino # <--- Nuova Importazione

st.set_page_config(page_title="Supporto Medico v1", layout="wide")

DB_FILE = "dati_salute.xlsx"

# Funzione salvataggio (invariata)
def salva_su_excel(nuovi_dati):
    if os.path.exists(DB_FILE):
        df_esistente = pd.read_excel(DB_FILE)
        df_nuovo = pd.concat([df_esistente, pd.DataFrame([nuovi_dati])], ignore_index=True)
    else:
        df_nuovo = pd.DataFrame([nuovi_dati])
    df_nuovo.to_excel(DB_FILE, index=False)

st.markdown("<h2 style='text-align: center;'>Diario Clinico Digitale</h2>", unsafe_allow_html=True)

state = calendar(options={"initialView": "dayGridMonth", "firstDay": 1, "selectable": True}, key="medical_calendar")

if state and "dateClick" in state:
    data_selezionata = (state["dateClick"].get("dateStr") or state["dateClick"].get("date")).split("T")[0]
    st.sidebar.header(f"Data: {data_selezionata}")
    
    # Gestione sintomi multipli con checkbox
    st.sidebar.write("Quali sintomi hai oggi?")
    s_schiena = st.sidebar.checkbox("Mal di Schiena")
    s_diarrea = st.sidebar.checkbox("Diarrea")
    s_stipsi = st.sidebar.checkbox("Stipsi")
    s_nausea = st.sidebar.checkbox("Nausea")

    # LOGICA INTESTINO (Diarrea o Stipsi)
    if s_diarrea or s_stipsi:
        sintomi_attivi = []
        if s_diarrea: sintomi_attivi.append("Diarrea")
        if s_stipsi: sintomi_attivi.append("Stipsi")
        
        with st.sidebar.form("form_intestino"):
            risultato = visualizza_intestino(sintomi_attivi)
            
            if st.form_submit_button("ANALIZZA INTESTINO"):
                consiglio, urgenza = calcola_responso_intestino(risultato["punteggio"], risultato["red_flags"])
                
                dati_finali = risultato["dati"]
                dati_finali["Data"] = data_selezionata
                dati_finali["Urgenza"] = urgenza
                
                salva_su_excel(dati_finali)
                st.session_state.ultimo_risultato = (consiglio, risultato["punteggio"], urgenza)
                st.success("Dati intestinali salvati!")

    # LOGICA SCHIENA (pre-esistente)
    if s_schiena:
        with st.sidebar.form("form_schiena"):
            risultato_s = visualizza_schiena()
            if st.form_submit_button("ANALIZZA SCHIENA"):
                consiglio, urgenza = calcola_responso_schiena(risultato_s["punteggio"])
                dati_finali = risultato_s["dati"]
                dati_finali["Data"] = data_selezionata
                dati_finali["Urgenza"] = urgenza
                salva_su_excel(dati_finali)
                st.session_state.ultimo_risultato = (consiglio, risultato_s["punteggio"], urgenza)
                st.success("Dati schiena salvati!")

    if 'ultimo_risultato' in st.session_state:
        res, pts, urg = st.session_state.ultimo_risultato
        st.info(f"**Esito:** {res} | **Urgenza:** {urg}")

else:
    st.info("Seleziona un giorno sul calendario.")

if st.checkbox("Mostra Database Storico"):
    if os.path.exists(DB_FILE):
        st.dataframe(pd.read_excel(DB_FILE))