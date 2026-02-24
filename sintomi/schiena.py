import streamlit as st

def visualizza_schiena():
    st.write("### Mal di Schiena")
    intensita = st.slider("Intensità (1-10)", 1, 10, 5)
    frequenza = st.number_input("Ripetizioni al giorno", min_value=1, max_value=24, value=1)
    note = st.text_area("Note aggiuntive")
    
    st.write("---")
    st.write("**Anamnesi Rapida**")
    p1 = st.radio("Il dolore cambia con il movimento?", ["No", "Sì"]) == "Sì"
    p2 = st.radio("Peggiora in certi momenti?", ["No", "Sì"]) == "Sì"
    p3 = st.radio("Dove rimane?", ["Gamba", "Schiena"]) == "Schiena"
    p4 = st.radio("Formicolii?", ["Sì", "No"]) == "No"
    p5 = st.radio("Zona toraco-lombare?", ["No", "Sì"]) == "Sì"
    p6 = st.radio("Dopo sforzo?", ["No", "Sì"]) == "Sì"
    p7 = st.radio("Dolore acuto?", ["No", "Sì"]) == "Sì"
    p8 = st.radio("Episodi passati?", ["No", "Sì"]) == "Sì"
    p9 = st.radio("Perdita peso?", ["Sì", "No"]) == "No"
    p10 = st.radio("Dolore a riposo?", ["Sì", "No"]) == "No"
    p11 = st.radio("Febbre?", ["Sì", "No"]) == "No"
    p12 = st.radio("Problemi vescica?", ["Sì", "No"]) == "No"
    
    punteggio = sum([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12])
    
    return {
        "punteggio": punteggio,
        "dati": {
            "Sintomo": "Mal di Schiena",
            "Punteggio": punteggio,
            "Intensita": intensita,
            "Frequenza_Giorno": frequenza,
            "Note": note
        }
    }

def calcola_responso_schiena(punti):
    if punti >= 12: return "🟢 100% Meccanico", "Basso"
    elif punti >= 10: return "🟡 95% Meccanico", "Medio"
    elif punti >= 8: return "🟠 73% Meccanico (Possibile Ernia)", "Alto"
    else: return "🔴 0-35% Meccanico (Necessari esami)", "Critico"