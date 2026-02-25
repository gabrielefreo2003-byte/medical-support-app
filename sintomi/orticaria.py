import streamlit as st

def visualizza_orticaria():
    st.write("### Analisi Orticaria")
    
    # Area Definizione (UAS)
    st.write("**Valutazione Gravità (UAS)**")
    pomfi = st.select_slider("Punteggio pomfi (24h):", options=[0, 1, 2, 3])
    prurito = st.select_slider("Punteggio prurito:", options=[0, 1, 2, 3])
    uas_score = pomfi + prurito
    
    note = st.text_area("Note aggiuntive")

    st.write("---")
    st.write("**Anamnesi Rapida**")
    p1 = st.checkbox("Pomfi che migrano/scompaiono entro 24h?") # +4
    p2 = st.checkbox("Fastidio principale: prurito intenso?") # +3
    p3 = st.checkbox("Senza motivo apparente?") # +3
    p4 = st.checkbox("Gonfiori localizzati (labbra/occhi)?") # +2
    p5 = st.checkbox("Febbre o uso FANS ultimi 10gg?") # +2

    st.write("---")
    st.error("**Segnali di Allarme (Anafilassi)**")
    a1 = st.checkbox("Costrizione gola / Difficoltà deglutire")
    a2 = st.checkbox("Voce rauca improvvisa")
    a3 = st.checkbox("Respiro sibilante")
    a4 = st.checkbox("Dolore addominale / Vomito improvviso")

    punteggio_diag = (p1*4) + (p2*3) + (p3*3) + (p4*2) + (p5*2)
    alert = any([a1, a2, a3, a4])

    return {
        "punteggio": punteggio_diag,
        "uas": uas_score,
        "alert": alert,
        "dati": {
            "Sintomo": "Orticaria",
            "Punteggio": punteggio_diag,
            "UAS": uas_score,
            "Urgenza": "CRITICO" if alert else "Monitoraggio",
            "Note": note
        }
    }

def calcola_responso_orticaria(punti, uas, alert):
    if alert:
        return "🚨 **PERICOLO ANAFILASSI**: Contatta il 118 immediatamente!", "Critico"
    
    if punti >= 10: res = "Probabilità ALTA di Orticaria Spontanea"
    elif punti >= 6: res = "Probabilità MEDIA"
    else: res = "Probabilità BASSA"
    
    if uas > 4:
        res += " | ⚠️ Gravità elevata (UAS > 4)"
        
    return res, "Alto" if uas > 4 else "Basso"