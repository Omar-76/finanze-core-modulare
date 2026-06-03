import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_password_reset(email: str):
    try:
        response = supabase.auth.reset_password_for_email(email)
        if response.get("error"):
            st.error(f"Errore: {response['error']['message']}")
        else:
            st.success("Link per il reset della password inviato via email.")
    except Exception as e:
        st.error(f"Errore durante l'invio del link: {e}")

def login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
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
        login()
        st.markdown("---")
        st.subheader("Hai dimenticato la password?")
        reset_email = st.text_input("Inserisci la tua email per ricevere il link di reset")
        if st.button("Invia link di reset"):
            if reset_email:
                send_password_reset(reset_email)
            else:
                st.warning("Inserisci un'email valida")
    else:
        st.write(f"Benvenuto {st.session_state['user'].email}!")
        if st.button("Logout"):
            st.session_state.pop("user")
            st.success("Logout effettuato")

if __name__ == "__main__":
    main()
