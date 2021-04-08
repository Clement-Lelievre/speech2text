# import streamlit as st
# import speech_recognition as sr
# import time
# from threading import Thread
# from streamlit.report_thread import add_report_ctx
# from streamlit.report_thread import get_report_ctx

# st.set_page_config(
#     page_title="Speech to text", 
#     page_icon="🗣️",
#     layout="centered", # wide
#     initial_sidebar_state="auto") # collapsed


# st.title('Speech to text app')

# language = st.selectbox('Choose language', help='Choose the language you want to speak to the mic', options = ('French','English'))
# if language == 'French':
#     language = "fr-FR"
# else:
#     language = 'en-US'

# duration = st.slider('Choose speaking duration (seconds)', min_value= 10, max_value=60, value = 10, step=10, help = 'Choose how long to record your voice')


# def progress_bar(duration):
#     ctx = get_report_ctx()
#     add_report_ctx(None, ctx)
#     latest_iteration = st.empty()
#     bar = st.progress(0)
#     for i in range(duration+1):
#         latest_iteration.text(f'{duration - i} seconds left')
#         bar.progress((100//duration)*i)
#         time.sleep(1)
#     st.text('Analyzing your speech...')

# r = sr.Recognizer()
# if st.button('Speak', help='Once you click, speak and wait for the transcription'):
#     t = Thread(target=progress_bar, args=(duration,)) # I need a thread in order to show progress bar and record simultanesouly
#     add_report_ctx(t)
#     t.start()
#     try:
#         with sr.Microphone() as source:
#             # read the audio data from the microphone
#             audio_data = r.record(source, duration=duration)
#             # convert speech to text
#             text = r.recognize_google(audio_data, language= language)
#             st.info(text)
#     except Exception as e:
#         st.error('Could not process audio')
    

    
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

stt_button = Button(label="Speak", width=100)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))