import streamlit as st
from gateway.privacy_gateway import secure_prompt, restore_response
from gateway.ollama_client import ask_local_llm
from utils.locales import t

def render_gateway_ui():
    st.markdown(f'<h2 class="classic-title" style="font-size:24px;">{t("gw_title")}</h2>', unsafe_allow_html=True)
    st.caption(t("gw_caption"))
    
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    user_prompt = st.text_area(t("gw_input"), height=150, placeholder=t("gw_placeholder"))
    
    if st.button(t("gw_send"), type="primary"):
        if not user_prompt.strip():
            st.warning(t("gw_warn"))
        else:
            with st.spinner(t("gw_mask_spin")):
                masked_prompt, mapping = secure_prompt(user_prompt)
                
            with st.spinner(t("gw_llm_spin")):
                ai_response = ask_local_llm(masked_prompt)
                
            restored_response = restore_response(ai_response, mapping)
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(t("gw_masked_hdr"))
                st.info(masked_prompt)
            with col2:
                st.subheader(t("gw_restored_hdr"))
                st.success(restored_response)
                
            with st.expander(t("gw_mapping_hdr")):
                st.json(mapping)
                
    st.markdown('</div>', unsafe_allow_html=True)