import streamlit as st
from dotenv import load_dotenv
import os
from supabase import create_client

# Carica variabili d'ambiente dal file .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Crea client Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def check_user_approved(email: str) -> bool:
    """Controlla se l'utente è presente e approvato nella tabella allowed_users."""
    response = supabase.table("allowed_users").select("license_status").eq("email", email).single().execute()
    if response.error or response.data is None:
        return False
    return response.data.get("license_status") == "active"


def login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Accedi"):
        auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if auth_response.user is not None:
            if check_user_approved(email):
                st.success(f"Benvenuto {email}!")
                st.session_state["logged_in"] = True
                st.session_state["user_email"] = email
            else:
                st.error("Utente non approvato. Contatta l'amministratore.")
        else:
            st.error("Email o password errati")



def logout():
    supabase.auth.sign_out()
    st.session_state["logged_in"] = False
    st.session_state["user_email"] = None
    st.experimental_rerun()


def main():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        login()
    else:
        st.write(f"Sei loggato come {st.session_state['user_email']}")
        if st.button("Logout"):
            logout()


if __name__ == "__main__":
    main()
