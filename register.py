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

    # Recupera i piani ordinati per prezzo crescente (correzione: desc=False)
    try:
        response = supabase.table('subscription_plans').select('*').order('price_euro', desc=False).execute()
        plans = response.data if response.data else []
    except Exception as e:
        st.error(f"Errore nel recupero dei piani di abbonamento: {e}")
        plans = []

    st.markdown("---")
    st.subheader("Scegli un piano di abbonamento")

    selected_plan_id = None

    # Visualizza i piani come quadri cliccabili con stile personalizzato
    cols = st.columns(len(plans)) if plans else []
    for i, plan in enumerate(plans):
        with cols[i]:
            price = plan.get('price_euro', 0)
            duration = plan.get('duration_days', 'N/A')
            description = plan.get('description', '')
            plan_id = plan.get('id')

            style = """
                border: 2px solid #4CAF50;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                text-align: center;
                cursor: pointer;
                user-select: none;
            """
            price_style = "font-size: 28px; font-weight: bold; color: #4CAF50; margin-bottom: 10px;"
            duration_style = "font-size: 16px; margin-bottom: 10px;"
            description_style = "font-size: 14px; color: #555;"

            if st.button(f"", key=f"plan_{plan_id}"):
                selected_plan_id = plan_id
                st.session_state['selected_plan'] = plan

            st.markdown(f"""
                <div style="{style}">
                    <div style="{price_style}">€{price}</div>
                    <div style="{duration_style}">{duration} giorni</div>
                    <div style="{description_style}">{description}</div>
                </div>
            """, unsafe_allow_html=True)

    if 'selected_plan' in st.session_state:
        selected_plan = st.session_state['selected_plan']
        price = selected_plan.get('price_euro', 0)

        if price == 0:
            if st.button("Conferma registrazione con piano gratuito"):
                if not (first_name and last_name and email and phone and password and confirm_password):
                    st.warning("Compila tutti i campi.")
                elif password != confirm_password:
                    st.error("Le password non corrispondono.")
                else:
                    try:
                        user = supabase.auth.sign_up({"email": email, "password": password})
                        if user.user is not None:
                            supabase.table('allowed_users').insert({
                                'email': email,
                                'first_name': first_name,
                                'last_name': last_name,
                                'phone_encrypted': phone,
                                'plan_id': selected_plan.get('id')
                            }).execute()
                            st.success("Registrazione avvenuta con successo! Puoi ora effettuare il login.")
                            del st.session_state['selected_plan']
                        else:
                            st.error("Errore durante la registrazione.")
                    except Exception as e:
                        st.error(f"Errore durante la registrazione: {e}")
        else:
            st.info("Per i piani a pagamento, la procedura di acquisto sarà implementata a breve.")

    if st.button("Torna al login"):
        st.session_state.page = "login"
        if 'selected_plan' in st.session_state:
            del st.session_state['selected_plan']

    layout.page_container_end()
