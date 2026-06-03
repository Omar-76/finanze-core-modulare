import streamlit as st
from supabase import create_client, Client

# Configurazione Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Stesso CSS per coerenza grafica
st.markdown("""
<style>
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
    h1 {
        text-align: center;
        color: #4CAF50;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

def show_register_page():
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.markdown("<h1>Registrazione Nuovo Utente</h1>", unsafe_allow_html=True)

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
            # Controllo duplicati email e telefono
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
        st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    show_register_page()
