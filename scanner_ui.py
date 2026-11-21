import streamlit as st
import os
from scanner.discovery import scan_directory
from utils.locales import t


def render_scanner_ui():
    st.markdown(
        f'<h2 class="classic-title" style="font-size:24px;">{t("sc_title")}</h2>', unsafe_allow_html=True)
    st.caption(t("sc_caption"))

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

    target_dir = st.text_input(t("sc_input"), value="sample_docs")

    if st.button(t("sc_scan_btn"), type="primary"):
        if not os.path.isdir(target_dir):
            st.error(t("sc_err_path"))
        else:
            with st.spinner(t("sc_spin")):
                results = scan_directory(target_dir)

            if not results:
                st.info(t("sc_no_pii"))
            else:
                total_files = len(results)
                total_pii = sum(r["total"] for r in results)

                global_breakdown = {}
                for r in results:
                    for pii_type, count in r["breakdown"].items():
                        global_breakdown[pii_type] = global_breakdown.get(
                            pii_type, 0) + count

                st.success(t("sc_success").format(
                    total_pii=total_pii, total_files=total_files))

                st.divider()
                st.subheader(t("sc_overview"))

                col1, col2, col3 = st.columns(3)
                col1.metric(t("sc_files_pii"), total_files)
                col2.metric(t("sc_total_pii"), total_pii)
                col3.metric(t("sc_pii_types"), len(global_breakdown))

                st.subheader(t("sc_breakdown"))
                st.bar_chart(global_breakdown)

                st.subheader(t("sc_details"))
                for r in results:
                    with st.expander(f"📄 {r['filepath']} ({r['total']} PII)"):
                        st.json(r["breakdown"])

    st.markdown('</div>', unsafe_allow_html=True)
