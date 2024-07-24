import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from fpdf import FPDF
from groq import Groq
from prompts import conceptual_prompt_template, factual_prompt_template, mathematical_prompt_template
import re

# Ensure the API keys are loaded correctly
if 'GOOGLE_API_KEY' not in os.environ:
    st.error("Google API key not found. Make sure it is set in the .env file.")
    st.stop()

if 'GROQ_API_KEY' not in os.environ:
    st.error("Groq API key not found. Make sure it is set in the .env file.")
    st.stop()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Function to extract video ID from different YouTube URL formats
def extract_video_id(youtube_video_url):
    # Regular expressions for different YouTube URL formats
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?.*?v=([^&]+)',
        r'(?:https?:\/\/)?youtu\.be\/([^?&]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, youtube_video_url)
        if match:
            return match.group(1)
    return None

# Getting transcript data from YouTube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = extract_video_id(youtube_video_url)
        if not video_id:
            st.error("Invalid YouTube URL format. Please enter a valid link.")
            return None
        
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        st.error(f"Error extracting transcript: {e}")
        return None

# Getting the summary based on prompt from Google Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None

# Getting the summary based on prompt from Groq API
def generate_groq_content(transcript_text, prompt, model):
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt + transcript_text}],
            model=model,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None

# Function to save text as PDF
def save_text_as_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)

# Layout of the Streamlit app
st.sidebar.title("Settings")
llm_choice = st.sidebar.selectbox("Select LLM", ["gemini-pro", "llama3-8b-8192"])  # Add other Groq models if available
course_type = st.sidebar.selectbox("Select the course type", ["Conceptual", "Factual", "Mathematical / Calculative"])
word_limit = st.sidebar.selectbox("Select Word Limit", ["Short (100 words)", "Medium (250 words)", "Detailed (500 words)"])
thumbnail_size = st.sidebar.slider("Thumbnail Size", min_value=100, max_value=400, value=200)

word_limit_value = {"Short (100 words)": "100", "Medium (250 words)": "250", "Detailed (500 words)": "500"}[word_limit]

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter your YouTube video link here:")

if youtube_link:
    try:
        video_id = youtube_link.split("v=")[1].split("&")[0]
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", width=thumbnail_size)
    except IndexError:
        st.error("Invalid YouTube URL format. Please enter a valid link.")

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    
    if transcript_text:
        if course_type == "Conceptual":
            prompt_template = conceptual_prompt_template
        elif course_type == "Factual":
            prompt_template = factual_prompt_template
        elif course_type == "Mathematical / Calculative":
            prompt_template = mathematical_prompt_template
        
        prompt = prompt_template.format(word_limit=word_limit_value)
        
        if llm_choice == "gemini-pro":
            summary = generate_gemini_content(transcript_text, prompt)
        else:
            summary = generate_groq_content(transcript_text, prompt, llm_choice)
    

        if summary:
            st.markdown("## Detailed Notes:")

            # Split the summary into lines and process them
            lines = summary.split("\n")
            formatted_lines = []
            for line in lines:
                if line.startswith("Topic"):
                    formatted_lines.append(f"## {line}")  # Make the topic name larger
                else:
                    formatted_lines.append(line.replace("Q", "\n\nQ").replace("A", "\nA"))

            formatted_summary = "\n".join(formatted_lines)
            st.write(formatted_summary)
            
            # Add a button to download the summary as PDF
            pdf_filename = st.text_input("Enter PDF Filename (without extension):", "detailed_notes")
            if st.button("Download as PDF"):
                if summary:
                    pdf_filename = pdf_filename if pdf_filename else "detailed_notes"
                    save_text_as_pdf(summary, f"{pdf_filename}.pdf")
                    with open(f"{pdf_filename}.pdf", "rb") as pdf_file:
                        st.download_button(
                            label="Download PDF",
                            data=pdf_file,
                            file_name=f"{pdf_filename}.pdf",
                            mime="application/pdf"
                        )
