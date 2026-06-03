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

    if st.button("Registrati"):
        if not (first_name and last_name and email and phone and password and confirm_password):
            st.warning("Compila tutti i campi.")
        elif password != confirm_password:
            st.error("Le password non corrispondono.")
        else:
            existing_email = supabase.table('allowed_users').select('email').eq('email', email).execute()
            existing_phone = supabase.table('allowed_users').select('phone_encrypted').eq('phone_encrypted', phone).execute()
            if existing_email.data and len(existing_email.data) > 0:
                st.error("Email già registrata.")
            elif existing_phone.data and len(existing_phone.data) > 0:
                st.error("Numero di telefono già registrato.")
            else:
                try:
                    user = supabase.auth.sign_up({"email": email, "password": password})
                    if user.user is not None:
                        supabase.table('allowed_users').insert({
                            'email': email,
                            'first_name': first_name,
                            'last_name': last_name,
                            'phone_encrypted': phone
                        }).execute()
                        st.success("Registrazione avvenuta con successo! Controlla la tua email per la verifica.")
                    else:
                        st.error("Errore durante la registrazione.")
                except Exception as e:
                    st.error(f"Errore durante la registrazione: {e}")

    if st.button("Torna al login"):
        st.session_state.page = "login"

    layout.page_container_end()

if __name__ == "__main__":
    show_register_page()
