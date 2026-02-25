import streamlit as st
from streamlit_calendar import calendar
import pandas as pd
import os

# Importiamo i moduli sintomi
from sintomi.allergia import visualizza_allergia, calcola_responso_allergia
from sintomi.intestino import visualizza_intestino, calcola_responso_intestino
from sintomi.orticaria import visualizza_orticaria, calcola_responso_orticaria
from sintomi.schiena import visualizza_schiena, calcola_responso_schiena

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
    s_allergia = st.sidebar.checkbox("Allergia")
    s_alterazioni_cutanee = st.sidebar.checkbox("Alterazioni cutanee")
    s_angina = st.sidebar.checkbox("Angina")
    s_ansia = st.sidebar.checkbox("Ansia")
    s_astenia = st.sidebar.checkbox("Astenia")
    s_diarrea = st.sidebar.checkbox("Diarrea")
    s_febbre = st.sidebar.checkbox("Febbre")
    s_nausea = st.sidebar.checkbox("Nausea")
    s_orticaria = st.sidebar.checkbox("Orticaria spontanea acuta")
    s_problemi_respiratori = st.sidebar.checkbox("Problemi respiratori")
    s_reflusso = st.sidebar.checkbox("Reflusso")
    s_ripienezza = st.sidebar.checkbox("Sensazione di ripienezza precoce")
    s_schiena = st.sidebar.checkbox("Mal di Schiena")
    s_stipsi = st.sidebar.checkbox("Stipsi")
    s_vertigini = st.sidebar.checkbox("Vertigini")
    s_vomito = st.sidebar.checkbox("Vomito")

    # LOGICA ALLERGIA
    if s_allergia:
        with st.sidebar.form("form_allergia"):
            res_a = visualizza_allergia()
            if st.form_submit_button("ANALIZZA ALLERGIA"):
                consiglio, urgenza = calcola_responso_allergia(res_a["punteggio"], res_a["alert"], res_a["interpretazione"])

                # Salviamo 3 valori
                st.session_state.ultimo_risultato = (consiglio, res_a["punteggio"], urgenza)

                dati_finali = res_a["dati"]
                dati_finali["Data"] = data_selezionata
                salva_su_excel(dati_finali)
                st.success("Dati allergia salvati!")

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

    # LOGICA ORTICARIA
    if s_orticaria:
        with st.sidebar.form("form_orticaria"):
            risultato_s = visualizza_orticaria()
            if st.form_submit_button("ANALIZZA ORTICARIA"):
                consiglio, urgenza = calcola_responso_orticaria(risultato_s["punteggio"], risultato_s["uas"], risultato_s["alert"])
                
                # Salviamo sempre 3 valori per coerenza: (Messaggio, Punteggio, Urgenza)
                st.session_state.ultimo_risultato = (consiglio, risultato_s["punteggio"], urgenza)
                
                dati_finali = risultato_s["dati"]
                dati_finali["Data"] = data_selezionata
                salva_su_excel(dati_finali)
                st.success("Dati orticaria salvati!")

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

    # CORREZIONE ERRORE VISUALIZZAZIONE
if 'ultimo_risultato' in st.session_state:
    res, pts, urg = st.session_state.ultimo_risultato # Ora riceve sempre 3 valori
    st.info(f"**Esito:** {res} | **Score:** {pts} | **Urgenza:** {urg}")

else:
    st.info("Seleziona un giorno sul calendario.")

if st.checkbox("Mostra Database Storico"):
    if os.path.exists(DB_FILE):
        st.dataframe(pd.read_excel(DB_FILE))