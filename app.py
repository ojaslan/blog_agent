from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Response Function
def get_gemini_response(prompt, image=None):
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    try:
        if prompt and image:
            response = model.generate_content([prompt, image])
        elif image:
            response = model.generate_content([image])
        elif prompt:
            response = model.generate_content([prompt])
        else:
            return "Please provide input text or upload an image."
        return response.text
    except Exception as e:
        return f"Error: {e}"

# ---------- Streamlit UI Setup ----------
st.set_page_config(page_title="GenAI Blog Generator", page_icon="🧠", layout="centered")

# -------- Custom CSS Styling --------
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.5rem 1rem;
        }
        .stDownloadButton>button {
            background-color: #007ACC;
            color: white;
            border-radius: 8px;
            padding: 0.4rem 1rem;
        }
        .css-1aumxhk {
            padding: 2rem 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Header Section ----------
st.image("https://cdn-icons-png.flaticon.com/512/857/857681.png", width=80)
st.title("🧠 GenAI Blog & Topic Generator")
st.markdown("Unlock your creativity using **Google Gemini 2.5 Flash** with just a prompt or image!")

st.divider()

# ---------- Input Section ----------
with st.container():
    task = st.selectbox("📌 Choose a task", ["Generate Blog Titles", "Generate Full Blog", "Get Blog Topics"])
    input_text = st.text_area("📝 Enter a topic or idea:", placeholder="E.g. AI in education, travel in Europe, etc.", height=120)

    uploaded_file = st.file_uploader("📷 Upload an image (optional)", type=["jpg", "jpeg", "png"])
    image = None
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="✅ Image Preview", use_column_width=True)

# ---------- Generate Button ----------
if st.button("🚀 Generate"):
    with st.spinner("Thinking with Gemini..."):
        # Build the dynamic prompt
        if task == "Generate Blog Titles":
            prompt = f"Suggest 5 creative and engaging blog titles about: {input_text}"
        elif task == "Generate Full Blog":
            prompt = f"Write a 300-word blog article on: {input_text}"
        else:
            prompt = f"Give 5 blog topic ideas related to: {input_text}"

        # Get Gemini response
        response = get_gemini_response(prompt, image)

        # ---------- Output Section ----------
        st.markdown("### 📄 Generated Output")
        st.success(response)

        # ---------- Download Option ----------
        st.download_button("📥 Download Result", response, file_name="genai_blog.txt", mime="text/plain")


