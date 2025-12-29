import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import base64

# 1. Configuration
genai.configure(api_key="AIzaSyAMLLIfa2oZcRUrmooaXaQy8HCgWo0mzQk")
model = genai.GenerativeModel('gemini-2.5-flash')

def speak_text(text):
    """Function to convert text to speech and play it automatically"""
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")
    with open("temp.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        # This hidden HTML snippet forces the browser to play the audio
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

# 2. UI Layout
st.title("👁️ Voice Vision")
st.write("Take a photo to hear what is in front of you.")

img = st.camera_input("Scan environment")

if img:
    img = Image.open(img)
    # 3. AI Processing
    with st.spinner("Analyzing..."):
        # We tell the AI to keep it short for audio
        prompt = "You are an assistant for the blind. Describe this scene in 1-2 short sentences. Be direct."
        response = model.generate_content([prompt, img])
        
        description = response.text
        st.success(description)
        
        # 4. Speak the result
        speak_text(description)