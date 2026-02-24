import streamlit as st

def visualizza_intestino(sintomi_selezionati):
    st.write(f"### Analisi Gastrointestinale: {', '.join(sintomi_selezionati)}")
    
    # Definizione comune per intensità e note
    intensita = st.slider("Intensità del disturbo (1-10)", 1, 10, 5)
    frequenza = st.number_input("Episodi/Scariche nelle ultime 24h", min_value=1, max_value=20, value=1)
    note = st.text_area("Note (es. consistenza, legame con cibi particolari)")
    
    st.write("---")
    st.write("**Anamnesi Roma IV (Sospetta IBS)**")
    
    # Domande con punteggio
    q1 = st.radio("1) Dolore addominale ricorrente (almeno 1gg/sett negli ultimi 3 mesi)?", ["No", "Sì"]) == "Sì"
    q2 = st.radio("2) Il dolore cambia dopo l'evacuazione?", ["No", "Sì"]) == "Sì"
    q3 = st.radio("3) Cambiamento frequenza scariche rispetto al solito?", ["No", "Sì"]) == "Sì"
    q4 = st.radio("4) Cambiamento aspetto/forma feci?", ["No", "Sì"]) == "Sì"
    
    # Punto 5: Sottotipo
    consistenza = st.selectbox("5) Consistenza abituale feci:", 
                                ["Diarrea (IBS-D)", "Stipsi (IBS-C)", "Alternata (IBS-M)"])
    
    q6 = st.radio("6) Senso di gonfiore, muco o svuotamento incompleto?", ["No", "Sì"]) == "Sì"
    
    st.write("---")
    st.write("⚠️ **Segnali di Allerta (Red Flags)**")
    # Red Flags (Se uno è Sì, lo score cade)
    rf1 = st.checkbox("Presenza di sangue nelle feci")
    rf2 = st.checkbox("Calo di peso involontario negli ultimi mesi")
    rf3 = st.checkbox("I sintomi ti svegliano durante la notte")
    rf4 = st.checkbox("Anemia accertata o febbre persistente")
    rf5 = st.checkbox("Età > 50 anni e sintomi di prima comparsa")

    # Calcolo Score
    punteggio = 0
    if q1: punteggio += 3
    if q2: punteggio += 1
    if q3: punteggio += 1
    if q4: punteggio += 1
    if q6: punteggio += 1
    
    red_flag_presente = any([rf1, rf2, rf3, rf4, rf5])
    
    return {
        "punteggio": punteggio,
        "red_flags": red_flag_presente,
        "dati": {
            "Sintomi": ", ".join(sintomi_selezionati),
            "Sottotipo": consistenza,
            "Punteggio_IBS": punteggio,
            "Intensita": intensita,
            "Frequenza": frequenza,
            "Note": note,
            "Red_Flags": "Sì" if red_flag_presente else "No"
        }
    }

def calcola_responso_intestino(punti, red_flags):
    if red_flags:
        return "🔴 Necessari esami organici (Red Flags presenti). L'IBS non è la diagnosi primaria.", "Critico"
    
    if punti >= 6:
        return "🟠 Alta probabilità (>85%). Fortemente indicativo di IBS. Procedere con test non invasivi.", "Alto"
    elif punti >= 4:
        return "🟡 Moderata probabilità (50-60%). Compatibile con IBS. Monitoraggio 4 settimane.", "Medio"
    else:
        return "🟢 Bassa probabilità (<5%). Indagare altre cause (dieta, intolleranze).", "Basso"