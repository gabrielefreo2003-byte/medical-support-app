import streamlit as st

def visualizza_orticaria():
    st.write("### Analisi Orticaria Acuta")
    
    # --- AREA DEFINIZIONE (UAS - Urticaria Activity Score) ---
    st.write("**Valutazione Gravità (UAS)**")
    punteggio_pomfi = st.select_slider(
        "Presenza di pomfi (24h):",
        options=[0, 1, 2, 3],
        help="0: Nessuno, 1: <20 pomfi, 2: 20-50 pomfi, 3: >50 pomfi"
    )
    punteggio_prurito = st.select_slider(
        "Intensità prurito:",
        options=[0, 1, 2, 3],
        help="0: Assente, 1: Lieve, 2: Moderato, 3: Intenso (invalidante)"
    )
    
    uas_giornaliero = punteggio_pomfi + punteggio_prurito
    note = st.text_area("Note aggiuntive (es. zone colpite, alimenti sospetti)")

    st.write("---")
    st.write("**Domande Anamnestiche**")
    
    # Domande con punteggio
    q1 = st.checkbox("Compaiono pomfi che migrano o scompaiono entro 24h?") # +4
    q2 = st.checkbox("Il fastidio principale è il prurito intenso?") # +3
    q3 = st.checkbox("Compaiono senza motivo apparente (non legati a freddo/pressione)?") # +3
    q4 = st.checkbox("Hai gonfiori su labbra, palpebre o mani (angioedema)?") # +2
    q5 = st.checkbox("Febbre, mal di gola o uso di FANS (es. aspirina) negli ultimi 7-10gg?") # +2

    st.write("---")
    st.error("**Segnali di Allarme (Pericolo Anafilassi)**")
    # Red Flags
    rf1 = st.checkbox("Costrizione alla gola o difficoltà a deglutire")
    rf2 = st.checkbox("Voce rauca improvvisa")
    rf3 = st.checkbox("Respiro sibilante o 'fame d'aria'")
    rf4 = st.checkbox("Forte dolore addominale o vomito improvviso")

    # Calcolo Score Diagnostico
    punteggio_diag = 0
    if q1: punteggio_diag += 4
    if q2: punteggio_diag += 3
    if q3: punteggio_diag += 3
    if q4: punteggio_diag += 2
    if q5: punteggio_diag += 2

    has_anafilassi = any([rf1, rf2, rf3, rf4])

    return {
        "punteggio_diag": punteggio_diag,
        "uas_score": uas_giornaliero,
        "anafilassi": has_anafilassi,
        "dati": {
            "Sintomo": "Orticaria",
            "Punteggio_Diag": punteggio_diag,
            "UAS_Daily": uas_giornaliero,
            "Note": note,
            "Urgenza_Anafilassi": "SI" if has_anafilassi else "NO"
        }
    }

def calcola_responso_orticaria(punti_diag, uas, anafilassi):
    if anafilassi:
        return "🚨 **PERICOLO ANAFILASSI**: Contatta immediatamente il pronto soccorso o il 118!", "CRITICO"
    
    testo = ""
    # Logica probabilità
    if punti_diag >= 10: testo = "Probabilità ALTA di Orticaria Acuta Spontanea."
    elif punti_diag >= 6: testo = "Probabilità MEDIA (valutare orticaria inducibile)."
    else: testo = "Probabilità BASSA (es. dermatite, punture o vasculite)."

    # Logica Gravità UAS
    if uas > 4:
        testo += " | **Gravità elevata**: valutare inizio/aumento terapia con il medico."
    
    return testo, "Alto" if uas > 4 else "Basso"