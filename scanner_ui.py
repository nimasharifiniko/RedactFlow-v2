import streamlit as st
import os
from scanner.discovery import scan_directory


def render_scanner_ui():
    st.markdown('<h2 class="classic-title" style="font-size:24px;">🔍 PII Discovery Scanner</h2>',
                unsafe_allow_html=True)
    st.caption(
        "Bulk-scan local directories to find exposed sensitive data without modifying any files.")

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

    target_dir = st.text_input(
        "Enter directory path to scan:", value="sample_docs")

    if st.button("Scan Directory", type="primary"):
        if not os.path.isdir(target_dir):
            st.error("Directory not found. Please check the path.")
        else:
            with st.spinner("Scanning files in parallel..."):
                results = scan_directory(target_dir)

            if not results:
                st.info("No PII detected in this directory.")
            else:
                total_files = len(results)
                total_pii = sum(r["total"] for r in results)

                
                global_breakdown = {}
                for r in results:
                    for pii_type, count in r["breakdown"].items():
                        global_breakdown[pii_type] = global_breakdown.get(
                            pii_type, 0) + count

                st.success(
                    f"Scan complete! Found {total_pii} PII entities across {total_files} files.")

                st.divider()
                st.subheader("📊 Overview")

                col1, col2, col3 = st.columns(3)
                col1.metric("Files with PII", total_files)
                col2.metric("Total PII Found", total_pii)
                col3.metric("PII Types", len(global_breakdown))

                st.subheader("📈 Breakdown by Type")
                
                st.bar_chart(global_breakdown)

                st.subheader("📂 Detailed Results")
                for r in results:
                    with st.expander(f"📄 {r['filepath']} ({r['total']} PII)"):
                        st.json(r["breakdown"])

    st.markdown('</div>', unsafe_allow_html=True)
