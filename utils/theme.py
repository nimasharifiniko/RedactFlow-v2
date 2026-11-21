import streamlit as st


def apply_custom_theme():
    theme_mode = st.session_state.get("theme_mode", "light")

    if theme_mode == "dark":
        bg_color = "#0E1117"
        text_color = "#E2E8F0"

        sidebar_bg = "rgba(22, 26, 35, 0.65)"
        panel_bg = "rgba(30, 35, 46, 0.5)"
        input_bg = "rgba(30, 35, 46, 0.8)"
        border_color = "rgba(255, 69, 0, 0.4)"
        shadow_color = "rgba(255, 69, 0, 0.15)"
        btn_bg = "rgba(255, 69, 0, 0.85)"
        btn_hover = "rgba(255, 69, 0, 1)"

    else:
        bg_color = "#F1F5F9"
        text_color = "#1A1D20"

        sidebar_bg = "rgba(255, 255, 255, 0.7)"
        panel_bg = "rgba(255, 255, 255, 0.6)"
        input_bg = "rgba(255, 255, 255, 0.85)"
        border_color = "rgba(226, 232, 240, 0.8)"
        shadow_color = "rgba(0, 0, 0, 0.05)"
        btn_bg = "#FF4500"
        btn_hover = "#E63E00"

    css = f"""
    <style>
        /* main app background */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background-color: {bg_color} !important;
        }}
        
        /* global text color */
        h1, h2, h3, h4, h5, h6, p, span, label, li, div[data-testid="stMarkdownContainer"] {{
            color: {text_color} !important;
        }}
        
        /* glassmorphism sidebar */
        [data-testid="stSidebar"] {{
            background: {sidebar_bg} !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            border-right: 1px solid {border_color} !important;
        }}
        
        /* glassmorphism panels */
        .glass-panel {{
            background: {panel_bg} !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border: 1px solid {border_color} !important;
            border-radius: 15px !important;
            box-shadow: 0 4px 15px {shadow_color} !important;
            color: {text_color} !important;
            transition: all 0.3s ease !important;
        }}
        
        .glass-panel:hover {{
            border-color: rgba(255, 69, 0, 0.6) !important;
            box-shadow: 0 6px 20px rgba(255, 69, 0, 0.2) !important;
        }}
        
        /* --- FILE UPLOADER ULTIMATE FIX --- */
        /* Target the main uploader container */
        [data-testid="stFileUploader"] {{
            background-color: transparent !important;
        }}

        /* Target the dropzone area (outer section) */
        [data-testid="stFileUploadDropzone"], [data-testid="stFileUploaderDropzone"] {{
            background-color: {input_bg} !important;
            border: 1px dashed {border_color} !important;
            border-radius: 15px !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            padding: 20px !important;
            transition: all 0.3s ease !important;
        }}
        
        /* Target the inner section/divs that might have a hardcoded white background */
        [data-testid="stFileUploadDropzone"] section,
        [data-testid="stFileUploadDropzone"] > div {{
            background-color: transparent !important;
            color: {text_color} !important;
        }}

        [data-testid="stFileUploadDropzone"]:hover {{
            border-color: #FF4500 !important;
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.2) !important;
        }}
        
        /* Text inside dropzone */
        [data-testid="stFileUploadDropzone"] span,
        [data-testid="stFileUploadDropzone"] small,
        [data-testid="stFileUploadDropzone"] p {{
            color: {text_color} !important;
        }}
        
        /* The internal "Browse files" button */
        [data-testid="stFileUploadDropzone"] button {{
            background-color: {btn_bg} !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            border: 1px solid {border_color} !important;
        }}
        
        /* The SVG icon inside the browse button */
        [data-testid="stFileUploadDropzone"] button svg {{
            fill: #FFFFFF !important;
            color: #FFFFFF !important;
        }}
        /* ---------------------------------- */
        
        /* general buttons */
        .stButton>button {{
            background-color: {btn_bg} !important;
            color: #FFFFFF !important;
            border: 1px solid transparent !important;
            border-radius: 10px !important;
            box-shadow: 0 0 10px {shadow_color} !important;
            transition: all 0.3s ease-in-out !important;
        }}
        
        .stButton>button:hover {{
            background-color: {btn_hover} !important;
            box-shadow: 0 0 20px rgba(255, 69, 0, 0.5) !important;
            transform: translateY(-2px);
            border-color: #FF4500 !important;
        }}
        
        /* text inputs and text areas */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
            background-color: {input_bg} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
        }}
        
        .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {{
            border-color: #FF4500 !important;
            box-shadow: 0 0 10px rgba(255, 69, 0, 0.2) !important;
        }}
        
        /* toggle and checkbox text */
        .stCheckbox, .stToggle {{
            color: {text_color} !important;
        }}
        
        /* metrics */
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
            color: {text_color} !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
