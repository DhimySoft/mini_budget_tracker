import streamlit as st

def set_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #e0eafc, #cfdef3);
        }

        .main {
            background: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 15px;
            animation: fadeIn 1s ease-in-out;
        }

        @keyframes fadeIn {
            0%   {opacity: 0; transform: translateY(20px);}
            100% {opacity: 1; transform: translateY(0);}
        }

        h1, h2, h3 {
            font-weight: 600;
            color: #333;
        }

        .stButton>button {
            border-radius: 10px;
            background: linear-gradient(45deg, #6a11cb, #2575fc);
            color: white;
            font-weight: 600;
            transition: 0.3s;
        }

        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
