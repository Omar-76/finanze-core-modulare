import streamlit as st
from supabase import create_client, Client

# Configurazione Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# CSS personalizzato per stile e rimozione spazio bianco superiore
st.markdown("""
<style>
    /* Rimuove margine e padding superiori della pagina */
    .css-18e3th9 {
        padding-top: 0rem;
        margin-top: 0rem;
    }
    /* Nasconde eventuali header vuoti */
    header {
        display: none;
    }
    /* Stile container centrale */
    .container {
        max-width: 400px;
        margin: 40px auto 0 auto;
        padding: 20px 30px 30px 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-radius: 12px;
        background-color: #ffffff;
    }
    /* Input con bordi arrotondati e focus verde */
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
    /* Pulsanti verdi con effetto hover */
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
    /* Messaggi con colori distinti */
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
    /* Titolo principale */
    h1 {
        text-align: center;
        color: #4CAF50;
        margin-bottom: 10px;
    }
    /* Sottotitolo */
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

def register_user(first_name, last_name, email, phone, password, confirm_password):
    if password != confirm_password:
        st.error("Le password non corrispondono.")
        return
    # Controllo base email e telefono duplicati
    existing_email = supabase.table('allowed_users').select('email').eq('email', email).execute()
    existing_phone = supabase.table('allowed_users').select('phone_encrypted').eq('phone_encrypted', phone).execute()
    if existing_email.data and len(existing_email.data) > 0:
        st.error("Email già registrata.")
        return
    if existing_phone.data and len(existing_phone.data) > 0:
        st.error("Numero di telefono già registrato.")
        return
    # Creazione utente con Supabase Auth
    try:
        user = supabase.auth.sign_up({"email": email, "password": password})
        if user.user is not None:
            # Inserisci dati aggiuntivi nella tabella allowed_users
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

def login():
    st.markdown("<h1>Gestione Spese e Budget Personale e Condiviso</h1>", unsafe_allow_html=True)
    with st.container():
        email = st.text_input("Email", placeholder="Inserisci la tua email")
        password = st.text_input("Password", type="password", placeholder="Inserisci la tua password")
        if st.button("Login"):
            if not email or not password:
                st.warning("Inserisci email e password")
                return
            try:
                user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                if user.user is not None:
                    st.session_state["user"] = user.user
                    st.success("Login effettuato con successo!")
                else:
                    st.error("Email o password errati")
            except Exception as e:
                st.error(f"Errore durante il login: {e}")

def main():
    if "user" not in st.session_state:
        st.markdown("<div class='container'>", unsafe_allow_html=True)
        mode = st.radio("Seleziona un'opzione", ("Login", "Registrati"))

        if mode == "Login":
            login()
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<h3>Hai dimenticato la password?</h3>", unsafe_allow_html=True)
            reset_email = st.text_input("Inserisci la tua email per ricevere il link di reset", key="reset_email")
            if st.button("Invia link di reset"):
                if reset_email:
                    send_password_reset(reset_email)
                else:
                    st.warning("Inserisci un'email valida")
        else:
            st.markdown("<h3>Registrazione Nuovo Utente</h3>", unsafe_allow_html=True)
            first_name = st.text_input("Nome")
            last_name = st.text_input("Cognome")
            email = st.text_input("Email")
            phone = st.text_input("Numero di telefono")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Conferma Password", type="password")
            if st.button("Registrati"):
                register_user(first_name, last_name, email, phone, password, confirm_password)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2 style='text-align:center; color:#4CAF50;'>Benvenuto {st.session_state['user'].email}!</h2>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.pop("user")
            st.success("Logout effettuato")

if __name__ == "__main__":
    main()
