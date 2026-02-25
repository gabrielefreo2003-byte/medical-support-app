import streamlit as st

def visualizza_allergia():
    st.write("### Analisi Sospetta Allergia")
    
    # Area Definizione
    intensita = st.slider("Intensità dei sintomi (1-10)", 1, 10, 5)
    frequenza = st.number_input("Ripetizioni dell'episodio (es. volte al mese/settimana)", min_value=1, value=1)
    note = st.text_area("Note (es. cosa avevi mangiato o dove ti trovavi)")

    st.write("---")
    st.write("**Anamnesi Allergologica**")
    
    # Domande Anamnestiche (Sì/No)
    q1 = st.checkbox("I sintomi compaiono entro 2 ore dall'esposizione?")
    q2 = st.checkbox("I sintomi durano poco (ore o max 1 giorno)?")
    q3 = st.checkbox("L'episodio si ripete regolarmente?")
    q4 = st.checkbox("Peggiorano con meteo specifico o mesi precisi?")
    q5 = st.checkbox("Hai starnuti, naso chiuso, tosse o sibili?")
    q6 = st.checkbox("Hai pomfi, prurito intenso o gonfiore occhi/labbra?")
    q7 = st.checkbox("Avverti nausea, vomito o diarrea subito dopo i pasti?")
    q9 = st.checkbox("Migliorano se cambi ambiente (es. vacanza)?")
    q10 = st.checkbox("Contatto recente con animali?")
    q11 = st.checkbox("Uso professionale di lattice o chimici?")
    q14 = st.checkbox("Parenti con asma, dermatite o febbre da fieno?")
    q15 = st.checkbox("Antistaminici/Cortisonici hanno funzionato?")

    st.write("---")
    st.error("**⚠️ SEGNALI DI ALLARME (Consulto Medico Necessario)**")
    # Red Flags / Anafilassi
    rf1 = st.checkbox("Senso di gola chiusa o fame d'aria?")
    rf2 = st.checkbox("Gonfiore marcato di lingua o labbra?")
    rf3 = st.checkbox("Svenimento, vertigini o tachicardia?")
    rf4 = st.checkbox("Assunzione di Beta-bloccanti o ACE-inibitori?")

    # Logica Scoring
    punteggio = 0
    if q1: punteggio += 3   # Comparsa entro 30-60 min (approssimato a 2h)
    if q3: punteggio += 3   # Reazione costante al trigger
    if (q6 and q5) or (q6 and q7): punteggio += 4 # Coinvolgimento più apparati
    if q14: punteggio += 1  # Familiarità
    if q15: punteggio += 2  # Risposta a farmaci
    if q4: punteggio += 2   # Calendario/Aperto

    has_alert = any([rf1, rf2, rf3, rf4])

    # Interpretazione Specifica
    suggerimento = ""
    if q5 and not q7: 
        suggerimento = "Probabile Allergia Respiratoria (Pollini se stagionale, Acari/Animali se perenne)."
    if q6 and q7:
        suggerimento = "Sospetta Allergia Alimentare (Orticaria + Dolore addominale)."
    if q6 and not q5 and not q7:
        suggerimento = "Possibile Dermatite da contatto (es. Nichel)."

    return {
        "punteggio": punteggio,
        "alert": has_alert,
        "interpretazione": suggerimento,
        "dati": {
            "Sintomo": "Allergia",
            "Punteggio": punteggio,
            "Intensita": intensita,
            "Urgenza": "CRITICO" if has_alert else "Monitoraggio",
            "Note": note
        }
    }

def calcola_responso_allergia(punti, alert, interpretazione):
    if alert:
        return "🚨 **PERICOLO**: Sintomi compatibili con anafilassi o rischio elevato. Consultare un medico urgentemente.", "Critico"
    
    messaggio = f"Score di probabilità allergica: {punti}. "
    if interpretazione:
        messaggio += f"\n\n**Orientamento:** {interpretazione}"
    
    return messaggio, "Medio" if punti > 5 else "Basso"