import streamlit as st
from supabase import create_client, Client

# Recupera i segreti da Streamlit Cloud
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Inizializza il client Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Funzione per il login
def login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if not email or not password:
            st.warning("Inserisci email e password")
            return
        try:
            # Effettua il login con Supabase Auth
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if user.user is not None:
                st.session_state["user"] = user.user
                st.success("Login effettuato con successo!")
            else:
                st.error("Email o password errati")
        except Exception as e:
            st.error(f"Errore durante il login: {e}")

# Funzione per il logout
def logout():
    if "user" in st.session_state:
        st.session_state.pop("user")
        st.success("Logout effettuato")

# Funzione principale
def main():
    if "user" not in st.session_state:
        login()
    else:
        st.write(f"Benvenuto {st.session_state['user'].email}!")
        if st.button("Logout"):
            logout()

if __name__ == "__main__":
    main()
