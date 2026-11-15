import streamlit as st
from gateway.privacy_gateway import secure_prompt, restore_response
from gateway.ollama_client import ask_local_llm


def render_gateway_ui():
    st.markdown('<h2 class="classic-title" style="font-size:24px;">🔒 AI Privacy Gateway</h2>', unsafe_allow_html=True)
    st.caption("Send prompts to cloud LLMs without exposing sensitive data. PII is masked locally and restored securely.")
    
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    user_prompt = st.text_area("Enter your prompt:", height=150, placeholder="E.g., Summarize this email from John Doe (john.doe@example.com)...")
    
    if st.button("Secure & Send", type="primary"):
        if not user_prompt.strip():
            st.warning("Please enter a prompt first.")
        else:
            with st.spinner("Masking PII locally..."):
                masked_prompt, mapping = secure_prompt(user_prompt)
                
            with st.spinner("Sending to local LLM..."):
                ai_response = ask_local_llm(masked_prompt)
                
            restored_response = restore_response(ai_response, mapping)
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🛡️ What the LLM Saw (Masked)")
                st.info(masked_prompt)
            with col2:
                st.subheader("🔑 Restored Response")
                st.success(restored_response)
                
            with st.expander("View Token Mapping"):
                st.json(mapping)
                
    st.markdown('</div>', unsafe_allow_html=True)