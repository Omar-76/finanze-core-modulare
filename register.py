import streamlit as st
from supabase import create_client, Client
import layout

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def show_register_page():
    layout.apply_global_style()
    layout.page_title("Registrazione Nuovo Utente")
    layout.page_container_start()

    first_name = st.text_input("Nome")
    last_name = st.text_input("Cognome")
    email = st.text_input("Email")
    phone = st.text_input("Numero di telefono")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Conferma Password", type="password")

    # Pulsante Registrati rimosso o spostato se vuoi

    # Recupera i piani di abbonamento dal DB
    try:
        response = supabase.table('subscription_plans').select('*').execute()
        plans = response.data if response.data else []
    except Exception as e:
        st.error(f"Errore nel recupero dei piani di abbonamento: {e}")
        plans = []

    st.markdown("---")
    st.subheader("Scegli un piano di abbonamento")

    if plans:
        for plan in plans:
            st.markdown(f"**{plan.get('plan_type', 'Piano')}**")
            st.markdown(f"- Prezzo: €{plan.get('price_euro', 'N/A')}")
            st.markdown(f"- Durata: {plan.get('duration_days', 'N/A')} giorni")
            st.markdown(f"- Descrizione: {plan.get('description', '')}")
            st.markdown("---")
    else:
        st.info("Nessun piano di abbonamento disponibile al momento.")

    if st.button("Torna al login"):
        st.session_state.page = "login"

    layout.page_container_end()

if __name__ == "__main__":
    show_register_page()
