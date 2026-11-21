import streamlit as st
import os
import time
import json

from core.extractors import extract_text
from core.merger import scan_document
from core.redactor import redact_text
from core.report import generate_report
from gateway_ui import render_gateway_ui
from scanner_ui import render_scanner_ui
from utils.theme import apply_custom_theme
from utils.locales import t

st.set_page_config(page_title="RedactFlow | Nima Sharifi Niko",
                   page_icon="🔒", layout="wide")

if "lang" not in st.session_state:
    st.session_state["lang"] = "en"
if "theme_mode" not in st.session_state:
    st.session_state["theme_mode"] = "light"

apply_custom_theme()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&display=swap');
    .classic-title {
        font-family: 'Cinzel', serif;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .profile-link {
        color: #FF4500 !important;
        text-decoration: none;
        font-weight: bold;
        margin: 0 10px;
    }
    .profile-link:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

TYPE_COLORS = {
    "PERSON": "#FFB3B3", "EMAIL": "#A7F3D0", "PHONE": "#BAE6FD",
    "IBAN": "#D9F99D", "CREDIT_CARD": "#FEF08A", "IP_ADDRESS": "#E9D5FF",
    "ADDRESS": "#FED7AA",
}


def highlight_text(text, findings):
    if not findings:
        return text
    sorted_f = sorted(findings, key=lambda x: x["start"], reverse=True)
    result = text
    for item in sorted_f:
        color = TYPE_COLORS.get(item["type"], "#E2E8F0")
        original = result[item["start"]:item["end"]]
        tag = f'<span style="background-color:{color}; color:#0F172A; padding:2px 4px; border-radius:4px; font-weight:600; border-bottom: 2px solid #FF4500;" title="{item["type"]}">{original}</span>'
        result = result[:item["start"]] + tag + result[item["end"]:]
    return result


def main():
    with st.sidebar:
        st.markdown(
            f'<h2 class="classic-title" style="text-align: center; font-size: 22px;">{t("app_title")}</h2>', unsafe_allow_html=True)
        st.markdown(
            '<p style="text-align: center; font-size: 13px; color: #64748B;">Developed by Nima Sharifi Niko</p>', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center;"><a href="https://github.com/nimasharifiniko" target="_blank" class="profile-link">GitHub</a> | <a href="https://www.linkedin.com/in/nima-sharifiniko/" target="_blank" class="profile-link">LinkedIn</a></div>', unsafe_allow_html=True)
        st.divider()

        # Language and Theme Toggle Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🇬🇧 EN" if st.session_state["lang"] == "fa" else "🇮🇷 FA", use_container_width=True):
                st.session_state["lang"] = "en" if st.session_state["lang"] == "fa" else "fa"
                st.rerun()
        with col2:
            if st.button("🌙" if st.session_state["theme_mode"] == "light" else "☀️", use_container_width=True):
                st.session_state["theme_mode"] = "dark" if st.session_state["theme_mode"] == "light" else "light"
                st.rerun()

        st.divider()

        pages = {
            "doc": t("nav_doc"),
            "gateway": t("nav_gateway"),
            "scanner": t("nav_scanner")
        }
        choice = st.radio(t("menu"), options=list(
            pages.keys()), format_func=lambda x: pages[x])

        st.divider()

        st.subheader(t("settings"))
        use_llm = st.toggle(t("enable_llm"), value=True)
        generate_map = st.toggle(t("generate_map"), value=False)
        st.divider()

        st.subheader(t("pii_to_detect"))
        active_types = set()

        st.write(f"**{t('high_priority')}**")
        if st.checkbox(t("emails"), value=True):
            active_types.add("EMAIL")
        if st.checkbox(t("phones"), value=True):
            active_types.add("PHONE")
        if st.checkbox(t("ibans"), value=True):
            active_types.add("IBAN")
        if st.checkbox(t("cards"), value=True):
            active_types.add("CREDIT_CARD")
        if st.checkbox(t("ips"), value=True):
            active_types.add("IP_ADDRESS")

        st.write("")
        st.write(f"**{t('contextual')}**")
        if st.checkbox(t("names"), value=True):
            active_types.add("PERSON")
        if st.checkbox(t("addresses"), value=True):
            active_types.add("ADDRESS")

    st.markdown(
        f'<h1 class="classic-title">{t("app_title")}</h1>', unsafe_allow_html=True)
    st.caption(t("app_caption"))

    if choice == "doc":
        uploaded_file = st.file_uploader(
            t("upload_doc"), type=["txt", "pdf", "docx"])

        if uploaded_file is not None:
            temp_dir = "temp_uploads"
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            if st.button(t("analyze_btn"), type="primary"):
                with st.spinner(t("analyzing")):
                    start_time = time.time()
                    text = extract_text(temp_path)
                    raw_findings = scan_document(text, use_llm=use_llm)
                    raw_findings = [
                        f for f in raw_findings if f["type"] in active_types]
                    processing_time = time.time() - start_time

                    st.session_state["original_text"] = text
                    st.session_state["raw_findings"] = raw_findings
                    st.session_state["processing_time"] = processing_time
                    st.session_state["filename"] = uploaded_file.name

            if "raw_findings" in st.session_state:
                raw_findings = st.session_state["raw_findings"]
                original_text = st.session_state["original_text"]
                processing_time = st.session_state["processing_time"]

                st.divider()

                st.markdown(
                    f'<h3 class="classic-title" style="font-size:18px;">{t("review_findings")}</h3>', unsafe_allow_html=True)
                st.markdown('<div class="glass-panel">',
                            unsafe_allow_html=True)

                confirmed_findings = []
                if not raw_findings:
                    st.info(t("no_pii"))
                else:
                    for i, item in enumerate(raw_findings):
                        is_low = item.get("confidence") == "low"
                        badge = f'<span style="color:#FF4500; font-size:12px; font-weight:bold;">{t("needs_review")}</span>' if is_low else ''

                        col1, col2 = st.columns([5, 1])
                        with col1:
                            st.markdown(
                                f"**{item['type']}** : `{item['text']}` {badge}", unsafe_allow_html=True)
                        with col2:
                            if st.checkbox(t("confirm"), value=not is_low, key=f"chk_{i}"):
                                confirmed_findings.append(item)
                st.markdown('</div>', unsafe_allow_html=True)

                redacted_text, mapping = redact_text(
                    original_text, confirmed_findings, generate_mapping=generate_map)
                report = generate_report(
                    confirmed_findings, processing_time, st.session_state["filename"])

                c1, c2, c3, c4 = st.columns(4)
                c1.metric(t("confirmed_entities"),
                          report["total_entities_found"])
                c2.metric(t("flagged_review"), len(
                    [f for f in raw_findings if f.get("confidence") == "low"]))
                c3.metric(t("proc_time"), f"{round(processing_time, 2)}s")
                c4.metric(t("pii_types"), len(report["breakdown_by_type"]))

                st.divider()

                left_col, right_col = st.columns(2)

                with left_col:
                    st.subheader(t("original_hl"))
                    html = highlight_text(original_text, confirmed_findings)
                    st.markdown(
                        f'<div style="background-color: {"#1E232E" if st.session_state["theme_mode"] == "dark" else "#FFFFFF"}; border: 1px solid #D1D5DB; border-radius: 8px; padding: 15px; font-family: monospace; white-space: pre-wrap; line-height: 1.8; color: {"#E2E8F0" if st.session_state["theme_mode"] == "dark" else "#0F172A"};">{html}</div>',
                        unsafe_allow_html=True
                    )

                with right_col:
                    st.subheader(t("redacted_doc"))
                    st.markdown(
                        f'<div style="background-color: {"#1E232E" if st.session_state["theme_mode"] == "dark" else "#FFFFFF"}; border: 1px solid #D1D5DB; border-radius: 8px; padding: 15px; font-family: monospace; white-space: pre-wrap; line-height: 1.8; color: {"#E2E8F0" if st.session_state["theme_mode"] == "dark" else "#0F172A"};">{redacted_text}</div>',
                        unsafe_allow_html=True
                    )

                st.divider()
                dl1, dl2 = st.columns(2)
                fname = st.session_state.get("filename", "document.txt")
                with dl1:
                    st.download_button(t("dl_redacted"), data=redacted_text,
                                       file_name=f"redacted_{fname}", mime="text/plain")
                with dl2:
                    report_json = json.dumps(
                        report, indent=2, ensure_ascii=False)
                    st.download_button(t("dl_report"), data=report_json,
                                       file_name=f"report_{fname}.json", mime="application/json")

    elif choice == "gateway":
        render_gateway_ui()

    elif choice == "scanner":
        render_scanner_ui()


if __name__ == "__main__":
    main()
