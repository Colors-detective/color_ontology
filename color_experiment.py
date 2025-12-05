
import streamlit as st
import sqlite3
import random
import time
import pandas as pd
import os


st.markdown(
    """
    <style>
        .stApp {
            background-color: #C6C6C6;
        }

        [data-testid="stSidebar"] {
            background-color: #f5f5f5;
        }
    </style>
    """,
    unsafe_allow_html=True
)

import random
# Folder with stimuli
stimuli_folder = os.path.join(os.path.dirname(__file__), "stimuli")

if "stimuli" not in st.session_state:
    st.session_state.stimuli = sorted(os.listdir(stimuli_folder))

if "trial_idx" not in st.session_state:
    st.session_state.trial_idx = 0

if "participant_info_done" not in st.session_state:
    st.session_state.participant_info_done = False

if "paused" not in st.session_state:
    st.session_state.paused = False

if "results" not in st.session_state:
    st.session_state.results = []

if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "participant_id" not in st.session_state:
    st.session_state.participant_id = random.randint(2000, 6000)

if "gender" not in st.session_state:
    st.session_state.gender = None  # will be set by user

if "age" not in st.session_state:
    st.session_state.age = None  # will be set by user

if "country" not in st.session_state:
    st.session_state.country = None  # will be set by user

# Participant info page
if not st.session_state.participant_info_done:

    left, center, right = st.columns([1, 40, 1])
    with center:
        st.title("Welcome to the Color Naming Experiment!")
        st.subheader("Please read the purpose of this experiment.")
        st.markdown(
            "We are a Color Diversity Lab team based in Japan, interested in studying various phenomena "
            "related to the perception of colors. Our experiment aims to build an ethnosemantic analysis of cultures and their color categorization. "
            "Labels and names attributed to colors will precious data get a glimpse of how in a language, cultures defined concepts, beliefs and hierarchisation of color categories."
            "In agreeing to take the study, you will be asked to provided some information related to your gender, place of residence, first language of proficiency, second language and third language of proficiency ."
        )

        agree = st.checkbox("I agree to the terms and conditions")
        Disagree= st.checkbox ("I disagree to take to the terms and conditions and want to leave.")

        if agree:
            st.write("Great! Before proceeding please provide the following information. "
                     "They will not be disclosed to the public.")

            st.markdown("---")
            st.subheader("Participant Information")

            st.write(f"Your Participant ID: **{st.session_state.participant_id}**")

            st.session_state.gender = st.radio("Gender", ["Male", "Female", "Other"])

            age_list = [str(i) for i in range(0, 81)]
            st.session_state.age = st.selectbox("Age", age_list)

            countries = ["Russia", "Japan", "France", "United States", "Senegal", "Other"]

            st.session_state.lang1 = st.selectbox("Language of Proficiency 1", Language1)
            st.session_state.lang2 = st.selectbox("Language of Proficiency 2", Language2)
            st.session_state.lang3 = st.selectbox("Language of Proficiency 3", Language3)
            st.session_state.lang4 = st.selectbox("Language of Proficiency 4", other)

            if st.button("Submit Info"):
                st.session_state.participant_info_done = True
                st.rerun()
    if Disagree:
     st.title("Thank you for participating!")
     st.write("You may now exit the browser.")

    st.stop()



# Participant info page
if not st.session_state.participant_info_done:

    left, center, right = st.columns([1, 40, 1])
    with center:
        st.title("Welcome to the Color Naming experiment!")
        st.subheader("Please insert your information before starting.")
        st.subheader("Thank you!")

        st.markdown("### Participant Info")
        st.write(f"Your Participant ID: **{st.session_state.participant_id}**")

        st.session_state.gender = st.radio("Gender", ["Male", "Female", "Other"])

        age_list = [str(i) for i in range(0, 81)]
        st.session_state.age = st.selectbox("Age", age_list)

        countries = ["Russia", "Japan", "France","United States", "Senegal", "Other"]

        st.session_state.country = st.selectbox("Country", countries)
        if st.button("Submit Info"):
            st.session_state.participant_info_done = True
            st.session_state.trigger_rerun = not st.session_state.get("trigger_rerun", False)

    st.stop()  



# trial workflow for the end and layout of the stimuli and time


trial = st.session_state.trial_idx
if st.session_state.participant_info_done:
 if trial >= len(st.session_state.stimuli):
    st.success("Experiment finished! Congratulations! Thank you for your precious participations. You can have a preview of your inputs responses.")
    st.write(st.session_state.results)
    df = pd.DataFrame(st.session_state.results)
       # Add participant info columns at the end
    df["participant_id"] = st.session_state.participant_id
    df["gender"] = st.session_state.gender
    df["age"] = st.session_state.age
    df["country"] = st.session_state.country
    st.dataframe(df)
    df.to_csv("final_results.csv", index=True) 
    st.balloons()
    st.stop()
    
    

    
trial = st.session_state.trial_idx
if st.session_state.participant_info_done:
 st.markdown("""
### Instructions  
Please look at each color stimulus and type the color name that best describes it.  
Click **Next** to move to the following stimulus.  
There is no wrong answer — enjoy the experiment!
""")

# Show the current image
filename = st.session_state.stimuli[trial]
img_path = os.path.join(stimuli_folder, filename)
st.image(img_path, caption=f"Trial {trial+1}", use_container_width=True)



# to save the results
def save_trial_result(trial_idx, img_path, typed_color, rt, audio_input):
    st.session_state.results.append({
        "trial": trial_idx,
        "image": img_path,
        "typed_color": typed_color,
        "rt": rt,
        "audio_input": audio_input,
    })


 # to pause the experiment
if st.session_state.paused:
    st.subheader("Experiment paused")
    if st.button("Resume"):
        st.session_state.paused = False
    st.stop()   

    # to make buttons

col1, col2, col3, col4 = st.columns(4)


if col1.button("Pause ⏸️"):
    st.session_state.paused = True
#answer inputs style either writing or audio
typed_color = st.text_input("Your answer", key=f"resp_{trial}", value="") 
audio_value = st.audio_input("Record your voice", key=f"audio_{trial}")


if st.session_state.start_time is None:
    st.session_state.start_time = time.time()
rt = time.time() - st.session_state.start_time    


if col2.button("Next⏭️"):
    typed_color = st.session_state[f"resp_{trial}"]  # get current input

    if typed_color.strip() == "" and not audio_value:
        st.error("Please enter a color name or record a voice input before continuing.")
    else:
        
        save_trial_result(
            trial_idx=trial,
            img_path=img_path,
            typed_color=typed_color.lower() if typed_color else None,
            rt=rt,
            audio_input=audio_value,
        )
        st.session_state.trial_idx += 1
        st.session_state.trigger_rerun = not st.session_state.get("trigger_rerun", False)
if col4.button ("voiced instructions 🗣️"):
  st.audio("cat-purr.mp3", format="audio/mpeg", loop=True)
         
# Submit final results early
with col3:
    if st.button("✅ End"):
              st.success("Are you sure to submit now?")
              df = pd.DataFrame(st.session_state.results)
              st.dataframe(df)
              df.to_csv("final_results.csv", index=True) 
              st.ballon()
