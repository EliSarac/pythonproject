import streamlit as st
from pytube import YouTube
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
#import whisper
#import os
#import re

@st.cache(allow_output_mutation=True)
def load_summarizer():
    model = pipeline("summarization")
    return model


def get_video_metadata(url):
    yt = YouTube(url)
    st.image(yt.thumbnail_url)
    st.header(yt.title)
    return url.split("=")[1]


def get_video_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    result = ""
    for i in transcript:
        result += ' ' + i['text']
    return result


def generate_text_chunks(text):
    res = []
    num_iters = int(len(text) / 1000)
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        res.append(text[start:end])
    return res


st.markdown("<h1 style='text-align: center; color: white;'>Youtube Video Summarizer</h1><br>", unsafe_allow_html=True)
st.markdown("View a summary of any Youtube video using its url.")

video_url = st.text_input("Enter YouTube video URL")

button = st.button("Summarize")

summarizer = load_summarizer()
with st.spinner("Generating Summary.."):
    if button and video_url:
        video_id = get_video_metadata(video_url)
        video_transcript = get_video_transcript(video_id)  # replace with get audio
        text_chunks = generate_text_chunks(video_transcript)
        res = summarizer(text_chunks)
        video_summary = ' '.join([summ['summary_text'] for summ in res])
        st.write(video_summary)
