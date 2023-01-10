import streamlit as st
import whisper
from pytube import YouTube
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

import os
import re

model = whisper.load_model("base")
summarizer = pipeline("summarization")

@st.cache(allow_output_mutation=True) #loads the pipeline model but I have no idea why is this as a function
def load_summarizer():
    model = pipeline("summarization")
    return model

def get_video_metadata(url): #gets the video metadata from url
    yt = YouTube(url)
    st.image(yt.thumbnail_url)
    st.header(yt.title)
    return url.split("=")[1] #video id after =

def get_audio(url: object) -> object: #function that converts video to audio file
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=".")
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file) #renames the file as .mp3 file extension
    a = new_file
    return a #function returns the new audio file


def get_text(url): #function that converts audio to text
    if url != '': output_text_transcribe = ''
    result = model.transcribe(get_audio(url))
    return result['text'].strip()


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
        video_id = get_video_metadata(url)
        video_transcript = get_text(video_id)
        text_chunks = generate_text_chunks(video_transcript)
        res = summarizer(text_chunks)
        video_summary = ' '.join([summ['summary_text'] for summ in res])
        st.write(video_summary)
