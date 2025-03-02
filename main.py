import streamlit as st
import pandas as pd
import numpy as np
import math

from utils import calc_elos

# Postavljanje konfiguracije stranice
st.set_page_config(
    page_title="ELO Kalkulator",
    layout="wide"
)

# Dodavanje naslova i opisa
st.title("GDSI ELO Kalkulator")
st.write("Unesite ELO prije meča, broj mečeva svakog igrača i rezultat prva dva seta te dobijte novi ELO za oba igrača. Unos rezultata trećeg seta je onemogućen jer 3. set nije bitan za izračun ELO-a.")

# Stvaranje kontejnera za glavni sadržaj aplikacije
main_container = st.container()

# Stvaranje dva stupca za igrače
with main_container:
    # Red zaglavlja
    header_cols = st.columns([1, 2, 1, 1, 1, 0.2, 1, 1])
    header_cols[0].write("**Igrač**")
    header_cols[1].write("**ELO**")
    header_cols[2].write("**Broj mečeva**")
    header_cols[3].write("**Set 1**")
    header_cols[4].write("**Set 2**")
    header_cols[5].write("")
    header_cols[6].write("**Novi ELO**")
    header_cols[7].write("**Razlika**")
    
    # Red za Igrača 1
    p1_cols = st.columns([1, 2, 1, 1, 1, 0.2, 1, 1])
    p1_cols[5].write("")
    p1_cols[0].write("**Igrač 1**")
    elo1 = p1_cols[1].number_input("ELO 1", min_value=0.0, value=1432.33, step=0.01, key="elo1", label_visibility="collapsed")
    matches1 = p1_cols[2].number_input("Mečevi 1", min_value=0, value=66, step=1, key="matches1", label_visibility="collapsed")
    set11 = p1_cols[3].number_input("Set 1-1", min_value=0, max_value=7, value=6, step=1, key="set11", label_visibility="collapsed")
    set12 = p1_cols[4].number_input("Set 1-2", min_value=0, max_value=7, value=7, step=1, key="set12", label_visibility="collapsed")
    
    # Red za Igrača 2
    p2_cols = st.columns([1, 2, 1, 1, 1, 0.2, 1, 1])
    p2_cols[5].write("")
    p2_cols[0].write("**Igrač 2**")
    elo2 = p2_cols[1].number_input("ELO 2", min_value=0.0, value=1329.68, step=0.01, key="elo2", label_visibility="collapsed")
    matches2 = p2_cols[2].number_input("Mečevi 2", min_value=0, value=18, step=1, key="matches2", label_visibility="collapsed")
    set21 = p2_cols[3].number_input("Set 2-1", min_value=0, max_value=7, value=4, step=1, key="set21", label_visibility="collapsed")
    set22 = p2_cols[4].number_input("Set 2-2", min_value=0, max_value=7, value=6, step=1, key="set22", label_visibility="collapsed")

# Izračunaj nove ELO bodove ako su sva potrebna polja popunjena
if all([elo1, elo2, matches1, matches2, set11 is not None, set12 is not None, set21 is not None, set22 is not None]):
    # Stvaranje strukture rezultata meča
    match_result = [(set11, set21), (set12, set22)]
    
    # Dodaj treći set ako oba igrača imaju rezultat za njega
    if (set11 > set21 and set12 < set22) or (set11 < set21 and set12 > set22):
        match_result.append((10, 8)) # rezultat 3. seta je nebitan pa su 10 i 8 samo fiktivno dodani
    
    # Izračunaj nove ELO bodove
    new_elo1, new_elo2 = calc_elos(elo1, matches1, elo2, matches2, match_result)
    
    # Prikaži rezultate
    p1_cols[6].markdown(f"<h4 style='color:blue'>{round(new_elo1, 0)}</h4>", unsafe_allow_html=True)
    p2_cols[6].markdown(f"<h4 style='color:blue'>{round(new_elo2, 0)}</h4>", unsafe_allow_html=True)
    
    # Izračunaj i prikaži razlike
    diff1 = new_elo1 - elo1
    diff2 = new_elo2 - elo2
    
    if diff1 > 0:
        p1_cols[7].markdown(f"<h4 style='color:green'>+{round(diff1, 2)}</h4>", unsafe_allow_html=True)
    else:
        p1_cols[7].markdown(f"<h4 style='color:red'>{round(diff1, 2)}</h4>", unsafe_allow_html=True)
        
    if diff2 > 0:
        p2_cols[7].markdown(f"<h4 style='color:green'>+{round(diff2, 2)}</h4>", unsafe_allow_html=True)
    else:
        p2_cols[7].markdown(f"<h4 style='color:red'>{round(diff2, 2)}</h4>", unsafe_allow_html=True)