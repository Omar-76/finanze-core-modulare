# Inserimento nuovo piano
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

# Modifica piano
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

# Eliminazione piano
if st.button(f"Elimina", key=f"delete_plan_{plan.get('id')}"):
    if st.confirm(f"Sei sicuro di voler eliminare il piano '{plan.get('plan_type')}'?"):
        delete_resp = supabase.table('subscription_plans').delete().eq('id', plan.get('id')).execute()
        if delete_resp.error:
            st.error(f"Errore durante l'eliminazione: {delete_resp.error.message}")
        else:
            st.success(f"Piano '{plan.get('plan_type')}' eliminato.")
            st.experimental_rerun()
