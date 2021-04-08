import streamlit as st
import speech_recognition as sr
import time
#from threading import Thread
from streamlit.report_thread import add_report_ctx
from streamlit.report_thread import get_report_ctx

st.set_page_config(
    page_title="Speech to text", 
    page_icon="🗣️",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed


st.title('Speech to text app')

language = st.selectbox('Choose language', help='Choose the language you want to speak to the mic', options = ('French','English'))
if language == 'French':
    language = "fr-FR"
else:
    language = 'en-US'

duration = st.slider('Choose speaking duration (seconds)', min_value= 10, max_value=60, value = 10, step=10, help = 'Choose how long to record your voice')


def progress_bar(duration):
    #ctx = get_report_ctx()

    #add_report_ctx(None, ctx)
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(duration+1):
        latest_iteration.text(f'{duration - i} seconds left')
        bar.progress((100//duration)*i)
        time.sleep(1)
    st.text('Analyzing your speech...')

if st.button('Speak', help='Once you click, speak and wait for the transcription'):
    # t = Thread(target=progress_bar, args=(duration,))
    # add_report_ctx(t)
    # t.start()
    #progress_bar(duration)
    with sr.Microphone() as source:
        # read the audio data from the microphone
        audio_data = r.record(source, duration=duration)
        # convert speech to text
        text = r.recognize_google(audio_data, language= language)
        st.info(text)
    

    
    