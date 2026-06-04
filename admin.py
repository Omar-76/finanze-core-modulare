import streamlit as st
import layout
from datetime import datetime

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
            first_name = user.get('first_name', '')
            last_name = user.get('last_name', '')
            license_status = user.get('license_status', '')
            st.markdown(f"### {first_name} {last_name}")
            st.markdown(f"- **Stato accesso:** {'Attivo' if license_status == 'active' else 'Bloccato'}")
            col1, col2, col3 = st.columns([1,1,2])
            with col1:
                if st.button(f"Blocca accesso", key=f"block_{user.get('id')}"):
                    resp = supabase.table('allowed_users').update({'license_status': 'blocked'}).eq('id', user.get('id')).execute()
                    if resp.error:
                        st.error(f"Errore nel blocco: {resp.error.message}")
                    else:
                        st.experimental_rerun()
            with col2:
                if st.button(f"Sblocca accesso", key=f"unblock_{user.get('id')}"):
                    resp = supabase.table('allowed_users').update({'license_status': 'active'}).eq('id', user.get('id')).execute()
                    if resp.error:
                        st.error(f"Errore nello sblocco: {resp.error.message}")
                    else:
                        st.experimental_rerun()
            with col3:
                if st.button(f"Assegna piano gratuito", key=f"freeplan_{user.get('id')}"):
                    resp = supabase.table('allowed_users').update({'plan_id': 1, 'plan_start_date': datetime.now().isoformat()}).eq('id', user.get('id')).execute()
                    if resp.error:
                        st.error(f"Errore nell'assegnazione piano gratuito: {resp.error.message}")
                    else:
                        st.experimental_rerun()
            st.markdown("---")
    else:
        st.info("Nessun utente registrato.")

    st.subheader("Gestione Piani di Abbonamento")
    try:
        plans_resp = supabase.table('subscription_plans').select('*').execute()
        plans = plans_resp.data if plans_resp.data else []
    except Exception as e:
        st.error(f"Errore nel recupero piani: {e}")
        plans = []

    if plans:
        for plan in plans:
            with st.container():
                st.markdown(f"### {plan.get('plan_type')}")
                st.markdown(f"**Prezzo:** €{plan.get('price_euro')}")
                st.markdown(f"**Durata:** {plan.get('duration_days')} giorni")
                st.markdown(f"**Descrizione:** {plan.get('description')}")
                col1, col2 = st.columns([1,1])
                with col1:
                    if st.button(f"Modifica", key=f"edit_plan_{plan.get('id')}"):
                        edit_plan_form(supabase, plan)
                with col2:
                    if st.button(f"Elimina", key=f"delete_plan_{plan.get('id')}"):
                        if st.confirm(f"Sei sicuro di voler eliminare il piano '{plan.get('plan_type')}'?"):
                            delete_resp = supabase.table('subscription_plans').delete().eq('id', plan.get('id')).execute()
                            if delete_resp.error:
                                st.error(f"Errore durante l'eliminazione: {delete_resp.error.message}")
                            else:
                                st.success(f"Piano '{plan.get('plan_type')}' eliminato.")
                                st.experimental_rerun()
                st.markdown("---")
    else:
        st.info("Nessun piano di abbonamento disponibile.")

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
                    if insert_resp.error:
                        st.error(f"Errore nell'inserimento: {insert_resp.error.message}")
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


def edit_plan_form(supabase, plan):
    st.markdown(f"### Modifica Piano '{plan.get('plan_type')}'")
    with st.form(f"edit_plan_form_{plan.get('id')}"):
        plan_type = st.text_input("Tipo di Piano", value=plan.get('plan_type'), max_chars=50)
        price_euro = st.number_input("Prezzo (€)", value=plan.get('price_euro'), min_value=0.0, format="%.2f")
        duration_days = st.number_input("Durata (giorni)", value=plan.get('duration_days'), min_value=1, step=1)
        description = st.text_area("Descrizione", value=plan.get('description'), max_chars=300)
        submitted = st.form_submit_button("Salva Modifiche")

        if submitted:
            if not plan_type:
                st.error("Il tipo di piano è obbligatorio.")
            else:
                try:
                    update_resp = supabase.table('subscription_plans').update({
                        'plan_type': plan_type,
                        'price_euro': price_euro,
                        'duration_days': duration_days,
                        'description': description
                    }).eq('id', plan.get('id')).execute()
                    if update_resp.error:
                        st.error(f"Errore nell'aggiornamento: {update_resp.error.message}")
                    else:
                        st.success("Piano aggiornato con successo!")
                        st.experimental_rerun()
                except Exception as e:
                    st.error(f"Errore durante l'aggiornamento: {e}")
