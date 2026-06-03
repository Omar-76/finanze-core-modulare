import streamlit as st

def apply_global_style():
    st.markdown("""
    <style>
        .css-18e3th9 {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        header {
            display: none !important;
        }
        main > div:first-child {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        .container {
            max-width: 400px;
            margin: 40px auto 0 auto;
            padding: 20px 30px 30px 30px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-radius: 12px;
            background-color: #ffffff;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 10px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        .stTextInput>div>div>input:focus {
            border-color: #4CAF50;
            outline: none;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .message {
            border-radius: 8px;
            padding: 12px;
            margin-top: 15px;
            font-weight: 600;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .warning {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeeba;
        }
        h1 {
            text-align: center;
            color: #4CAF50;
            margin-bottom: 10px;
        }
        h3 {
            text-align: center;
            color: #333;
            margin-top: 30px;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

def page_title(text):
    st.markdown(f"<h1>{text}</h1>", unsafe_allow_html=True)

def page_container_start():
    st.markdown("<div class='container'>", unsafe_allow_html=True)

def page_container_end():
    st.markdown("</div>", unsafe_allow_html=True)
