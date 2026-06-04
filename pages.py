import streamlit as st
import admin  # importa il modulo admin

def show_main_app(supabase):
    st.sidebar.title("Menu")

    # Definisci le pagine disponibili nella sidebar, inclusa la pagina admin
    pages = {
        "Dashboard": show_dashboard,
        "Profilo": show_profile,
        "Impostazioni": show_settings,
        "Admin": lambda supabase=supabase: admin.show_admin_page(supabase)
    }

    choice = st.sidebar.radio("Seleziona una pagina", list(pages.keys()))
    pages[choice](supabase)

def show_dashboard(supabase):
    st.title("Dashboard")
    st.write("Benvenuto nella dashboard principale.")
    # Logica dashboard...

def show_profile(supabase):
    st.title("Profilo Utente")
    st.write("Gestisci il tuo profilo qui.")
    # Logica profilo...

def show_settings(supabase):
    st.title("Impostazioni")
    st.write("Configura le impostazioni dell'app.")
    # Logica impostazioni...
