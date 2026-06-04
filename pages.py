import streamlit as st

def show_main_app(supabase):
    st.sidebar.title("Menu")

    # Definisci le pagine disponibili nella sidebar
    pages = {
        "Dashboard": show_dashboard,
        "Profilo": show_profile,
        "Impostazioni": show_settings
    }

    # Seleziona pagina dalla sidebar
    choice = st.sidebar.radio("Seleziona una pagina", list(pages.keys()))

    # Mostra la pagina selezionata
    pages[choice](supabase)


def show_dashboard(supabase):
    st.title("Dashboard")
    st.write("Benvenuto nella dashboard principale.")
    # Qui puoi aggiungere la logica per mostrare conti, transazioni, ecc.


def show_profile(supabase):
    st.title("Profilo Utente")
    st.write("Gestisci il tuo profilo qui.")
    # Qui puoi aggiungere la logica per modificare dati utente


def show_settings(supabase):
    st.title("Impostazioni")
    st.write("Configura le impostazioni dell'app.")
    # Qui puoi aggiungere la logica per le impostazioni
