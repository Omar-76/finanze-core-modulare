import streamlit as st
import admin  # importa il modulo admin
from datetime import datetime, timedelta

def show_main_app(supabase):
    st.sidebar.title("Menu")

    user = st.session_state.user
    if user:
        try:
            user_db_resp = supabase.table('allowed_users').select('*').eq('email', user.email).single().execute()
            user_db = user_db_resp.data if user_db_resp.data else {}
        except Exception:
            user_db = {}

        first_name = user_db.get('first_name', '')
        last_name = user_db.get('last_name', '')
        created_at_str = user_db.get('created_at')
        plan_start_date_str = user_db.get('plan_start_date')
        plan_id = user_db.get('plan_id')

        duration_days = get_plan_duration(supabase, plan_id)
        days_left = calculate_days_left(plan_start_date_str, duration_days)

        st.sidebar.markdown(f"### {first_name} {last_name}")
        st.sidebar.markdown(f"**Data registrazione:** {format_date(created_at_str)}")
        st.sidebar.markdown(f"**Giorni mancanti piano:** {days_left if days_left >= 0 else 'Scaduto'}")
    else:
        st.sidebar.info("Nessun utente loggato")

    user_email = user.email if user else ""
    is_admin = (user_email == "tuo_admin@email.it")  # Sostituisci con la tua email admin

    pages = {
        "Dashboard": show_dashboard,
        "Profilo": show_profile,
        "Impostazioni": show_settings,
    }
    if is_admin:
        pages["Admin"] = lambda supabase=supabase: admin.show_admin_page(supabase)

    choice = st.sidebar.radio("Seleziona una pagina", list(pages.keys()))
    pages[choice](supabase)


def show_dashboard(supabase):
    st.title("Dashboard")
    st.write("Benvenuto nella dashboard principale.")


def show_profile(supabase):
    st.title("Profilo Utente")
    st.write("Gestisci il tuo profilo qui.")


def show_settings(supabase):
    st.title("Impostazioni")
    st.write("Configura le impostazioni dell'app.")


def get_plan_duration(supabase, plan_id):
    if not plan_id:
        return 0
    try:
        plan_resp = supabase.table('subscription_plans').select('duration_days').eq('id', plan_id).single().execute()
        if plan_resp.data:
            return plan_resp.data.get('duration_days', 0)
    except:
        pass
    return 0


def calculate_days_left(plan_start_date_str, duration_days):
    if not plan_start_date_str or duration_days is None:
        return -1
    try:
        plan_start_date = datetime.fromisoformat(plan_start_date_str)
        end_date = plan_start_date + timedelta(days=duration_days + 1)
        today = datetime.now()
        delta = (end_date - today).days
        return delta
    except:
        return -1


def format_date(date_str):
    if not date_str:
        return "N/D"
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d/%m/%Y")
    except:
        return date_str
