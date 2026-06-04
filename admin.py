import streamlit as st
import layout


def show_admin_page(supabase):
    layout.page_title("Pannello Amministratore")
    layout.page_container_start()

    st.subheader("Utenti Registrati")
    try:
        users_resp = supabase.table('allowed_users').select('*').execute()
        users = users_resp.data if users_resp.data else []
    except Exception as e:
        st.error(f"Errore nel recupero utenti: {e}")
        users = []

    if users:
        for user in users:
            st.markdown(f"- {user.get('email')} - {user.get('first_name', '')} {user.get('last_name', '')} - Piano: {user.get('plan_id', 'Nessuno')} - Accesso: {'Attivo' if user.get('license_status', '') == 'active' else 'Bloccato'}")
            col1, col2, col3 = st.columns([1,1,2])
            with col1:
                if st.button(f"Blocca accesso {user.get('email')}", key=f"block_{user.get('id')}"):
                    supabase.table('allowed_users').update({'license_status': 'blocked'}).eq('id', user.get('id')).execute()
                    st.experimental_rerun()
            with col2:
                if st.button(f"Sblocca accesso {user.get('email')}", key=f"unblock_{user.get('id')}"):
                    supabase.table('allowed_users').update({'license_status': 'active'}).eq('id', user.get('id')).execute()
                    st.experimental_rerun()
            with col3:
                if st.button(f"Assegna piano gratuito {user.get('email')}", key=f"freeplan_{user.get('id')}"):
                    # Supponiamo id=1 sia il piano gratuito
                    supabase.table('allowed_users').update({'plan_id': 1}).eq('id', user.get('id')).execute()
                    st.experimental_rerun()
    else:
        st.info("Nessun utente registrato.")

    st.markdown("---")
    st.subheader("Gestione Piani di Abbonamento")
    try:
        plans_resp = supabase.table('subscription_plans').select('*').execute()
        plans = plans_resp.data if plans_resp.data else []
    except Exception as e:
        st.error(f"Errore nel recupero piani: {e}")
        plans = []

    if plans:
        for plan in plans:
            st.markdown(f"- ID: {plan.get('id')} - {plan.get('plan_type')} - Prezzo: €{plan.get('price_euro')} - Durata: {plan.get('duration_days')} giorni - {plan.get('description')}")
    else:
        st.info("Nessun piano di abbonamento disponibile.")

    st.markdown("---")
    st.subheader("Aggiungi Nuovo Piano di Abbonamento")

    with st.form("add_plan_form"):
        plan_type = st.text_input("Tipo di Piano", max_chars=50)
        price_euro = st.number_input("Prezzo (€)", min_value=0.0, format="%.2f")
        duration_days = st.number_input("Durata (giorni)", min_value=1, step=1)
        description = st.text_area("Descrizione", max_chars=300)
        submitted = st.form_submit_button("Aggiungi Piano")

        if submitted:
            if not plan_type:
                st.error("Il tipo di piano è obbligatorio.")
            else:
                try:
                    insert_resp = supabase.table('subscription_plans').insert({
                        'plan_type': plan_type,
                        'price_euro': price_euro,
                        'duration_days': duration_days,
                        'description': description
                    }).execute()
                    if insert_resp.get("error") is not None:
                        st.error(f"Errore nell'inserimento: {insert_resp['error']['message']}")
                    elif insert_resp.status_code >= 400:
                        st.error(f"Errore nell'inserimento: status code {insert_resp.status_code}")
                    else:
                        st.success("Piano aggiunto con successo!")
                        st.experimental_rerun()
                except Exception as e:
                    st.error(f"Errore durante l'inserimento: {e}")

    st.markdown("---")
    st.subheader("Statistiche e Monitoraggio")
    try:
        active_users_resp = supabase.table('allowed_users').select('*').eq('license_status', 'active').execute()
        active_users = active_users_resp.data if active_users_resp.data else []
        total_revenue_resp = supabase.table('allowed_users').select('total_revenue').execute()
        total_revenue = sum([u.get('total_revenue', 0) for u in total_revenue_resp.data]) if total_revenue_resp.data else 0
    except Exception as e:
        st.error(f"Errore nel recupero statistiche: {e}")
        active_users = []
        total_revenue = 0

    st.markdown(f"- Utenti attivi: {len(active_users)}")
    st.markdown(f"- Ricavi totali: €{total_revenue}")

    layout.page_container_end()
