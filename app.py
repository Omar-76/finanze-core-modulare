import streamlit as st
from supabase import create_client
import layout
import admin  # modulo admin separato

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ADMIN_EMAIL = "omarcorio@libero.it"  # Sostituisci con la tua email reale

def send_password_reset(email: str):
    try:
        response = supabase.auth.reset_password_for_email(email)
        if hasattr(response, "error") and response.error:
            st.error(f"Errore: {response.error.message}")
        else:
            st.success("Link per il reset della password inviato via email.")
    except Exception as e:
        st.error(f"Errore durante l'invio del link: {e}")

def main():
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "user" not in st.session_state:
        st.session_state.user = None

    layout.apply_global_style()

    # Se utente è loggato, aggiorna pagina in base al ruolo
    if st.session_state.user is not None:
        if st.session_state.user.email == ADMIN_EMAIL:
            st.session_state.page = "admin"
        else:
            st.session_state.page = "login"

    if st.session_state.page == "login":
        layout.page_title("Gestione Spese e Budget Personale e Condiviso")
        layout.page_container_start()

        # Sincronizza input con session_state per autofill
        if "email_input" not in st.session_state:
            st.session_state.email_input = ""
        if "password_input" not in st.session_state:
            st.session_state.password_input = ""

        email = st.text_input("Email", value=st.session_state.email_input, placeholder="Inserisci la tua email", key="email_input")
        password = st.text_input("Password", type="password", placeholder="Inserisci la tua password", key="password_input")

        
        if st.button("Login"):
            if not email or not password:
                st.warning("Inserisci email e password")
            else:
                try:
                    user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    if user.user is not None:
                        st.session_state.user = user.user
                        st.success("Login effettuato con successo!")
                        # Aggiorna pagina in base al ruolo senza reload
                        if user.user.email == ADMIN_EMAIL:
                            st.session_state.page = "admin"
                        else:
                            st.session_state.page = "login"
                    else:
                        st.error("Email o password errati")
                except Exception as e:
                    st.error(f"Errore durante il login: {e}")

        st.markdown("---")
        st.subheader("Hai dimenticato la password?")
        reset_email = st.text_input("Inserisci la tua email per ricevere il link di reset", key="reset_email")
        if st.button("Invia link di reset"):
            if reset_email:
                send_password_reset(reset_email)
            else:
                st.warning("Inserisci un'email valida")

        st.markdown("---")
        if st.button("Registrati"):
            st.session_state.page = "register"

        layout.page_container_end()

    elif st.session_state.page == "register":
        import register
        register.show_register_page()

    elif st.session_state.page == "admin":
        admin.show_admin_page(supabase)

    # Pulsante logout visibile solo se utente loggato
    if st.session_state.user is not None:
        st.markdown(f"<h4 style='text-align:center; color:#4CAF50;'>Benvenuto {st.session_state.user.email}!</h4>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.page = "login"
            # Pulisce input per sicurezza
            st.session_state.email_input = ""
            st.session_state.password_input = ""

if __name__ == "__main__":
    main()
