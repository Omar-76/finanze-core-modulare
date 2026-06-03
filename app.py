import streamlit as st
from supabase import create_client, Client

# Configurazione Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# CSS personalizzato per stile e rimozione spazio bianco superiore
st.markdown("""
<style>
    .css-18e3th9 {
        padding-top: 0rem;
        margin-top: 0rem;
    }
    header {
        display: none;
    }
    .container {
        max-width: 400px;
        margin: 40px auto 0 auto;
        padding: 20px 30px 30px 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-radius: 12px;
        background-color: #ffffff;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ccc;
        padding: 10px;
        font-size: 16px;
        transition: border-color 0.3s ease;
    }
    .stTextInput>div>div>input:focus {
        border-color: #4CAF50;
        outline: none;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .message {
        border-radius: 8px;
        padding: 12px;
        margin-top: 15px;
        font-weight: 600;
    }
    .success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .warning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeeba;
    }
    h1 {
        text-align: center;
        color: #4CAF50;
        margin-bottom: 10px;
    }
    h3 {
        text-align: center;
        color: #333;
        margin-top: 30px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

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

    st.title("Gestione Spese e Budget Personale e Condiviso")

    if st.session_state.page == "login":
        if "user" not in st.session_state:
            st.markdown("<div class='container'>", unsafe_allow_html=True)

            email = st.text_input("Email", placeholder="Inserisci la tua email")
            password = st.text_input("Password", type="password", placeholder="Inserisci la tua password")
            if st.button("Login"):
                if not email or not password:
                    st.warning("Inserisci email e password")
                else:
                    try:
                        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        if user.user is not None:
                            st.session_state["user"] = user.user
                            st.success("Login effettuato con successo!")
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
                # Non chiamiamo st.experimental_rerun() qui, Streamlit aggiornerà la pagina automaticamente

            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown(f"<h2 style='text-align:center; color:#4CAF50;'>Benvenuto {st.session_state['user'].email}!</h2>", unsafe_allow_html=True)
            if st.button("Logout"):
                st.session_state.pop("user")
                # Non chiamiamo st.experimental_rerun() qui, Streamlit aggiornerà la pagina automaticamente

    elif st.session_state.page == "register":
        import register
        register.show_register_page()

if __name__ == "__main__":
    main()
