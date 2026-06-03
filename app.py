import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_password_reset(email: str):
    try:
        response = supabase.auth.reset_password_for_email(email)
        if hasattr(response, "error") and response.error:
            st.error(f"Errore: {response.error.message}")
        else:
            st.success("Link per il reset della password inviato via email.")
    except Exception as e:
        st.error(f"Errore durante l'invio del link: {e}")

def login():
    st.markdown("<h1 style='text-align:center; color:#4CAF50;'>Login</h1>", unsafe_allow_html=True)
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
    st.markdown("""
    <style>
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
    .container {
        max-width: 400px;
        margin: auto;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-radius: 12px;
        background-color: #ffffff;
    }
    .forgot-password {
        margin-top: 20px;
        text-align: center;
        font-size: 14px;
        color: #555;
    }
    .forgot-password input {
        width: 100%;
        margin-top: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    if "user" not in st.session_state:
        with st.container():
            st.markdown("<div class='container'>", unsafe_allow_html=True)
            login()
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align:center; color:#333;'>Hai dimenticato la password?</h3>", unsafe_allow_html=True)
            reset_email = st.text_input("Inserisci la tua email per ricevere il link di reset", key="reset_email")
            if st.button("Invia link di reset"):
                if reset_email:
                    send_password_reset(reset_email)
                else:
                    st.warning("Inserisci un'email valida")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2 style='text-align:center; color:#4CAF50;'>Benvenuto {st.session_state['user'].email}!</h2>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.pop("user")
            st.success("Logout effettuato")

if __name__ == "__main__":
    main()
