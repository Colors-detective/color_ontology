<<<<<<< HEAD
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
stimuli_folder = r"C:\Users\davor\Documents\research_articles\color_naming_experiment_webdev\stimuli"
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
        st.title("Welcome to the Color Naming experiment!")
        st.subheader("Please insert your information before starting.")
        st.subheader("Thank you!")

        st.markdown("### Participant Info")
        st.write(f"Your Participant ID: **{st.session_state.participant_id}**")

        st.session_state.gender = st.radio("Gender", ["Male", "Female", "Other"])

        age_list = [str(i) for i in range(0, 81)]
        st.session_state.age = st.selectbox("Age", age_list)

        countries = ["United States", "Japan", "France", "Senegal", "Other"]
        st.session_state.country = st.selectbox("Country", countries)

        if st.button("Submit Info"):
            st.session_state.participant_info_done = True
            st.session_state.trigger_rerun = not st.session_state.get("trigger_rerun", False)

    st.stop()  



# trial workflow for the end and layout of the stimuli and time


trial = st.session_state.trial_idx
if st.session_state.participant_info_done:
 st.markdown("""
### Instructions  
Please look at each color stimulus and type the color name that best describes it.  
Click **Next** to move to the following stimulus.  
There is no wrong answer — enjoy the experiment!
""")

if trial >= len(st.session_state.stimuli):
    st.success("Experiment finished! Congratulations!")
    st.write(st.session_state.results)
    df = pd.DataFrame(st.session_state.results)
        # Add participant info columns at the end
    df["participant_id"] = st.session_state.participant_id
    df["gender"] = st.session_state.gender
    df["age"] = st.session_state.age
    df["country"] = st.session_state.country
    st.dataframe(df)
    df.to_csv("final_results.csv", index=True) 
    st.ballon()
    st.stop()


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

    if typed_color.strip() == "":
        st.error("Please enter a color name before continuing.")
    else:
        save_trial_result(
            trial_idx=trial,
            img_path=img_path,
            typed_color=typed_color.lower().strip(),
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
=======
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
stimuli_folder = r"C:\Users\davor\Documents\research_articles\color_naming_experiment_webdev\stimuli"
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
        st.title("Welcome to the Color Naming experiment!")
        st.subheader("Please insert your information before starting.")
        st.subheader("Thank you!")

        st.markdown("### Participant Info")
        st.write(f"Your Participant ID: **{st.session_state.participant_id}**")

        st.session_state.gender = st.radio("Gender", ["Male", "Female", "Other"])

        age_list = [str(i) for i in range(0, 81)]
        st.session_state.age = st.selectbox("Age", age_list)

        countries = ["United States", "Japan", "France", "Senegal", "Other"]
        st.session_state.country = st.selectbox("Country", countries)

        if st.button("Submit Info"):
            st.session_state.participant_info_done = True
            st.session_state.trigger_rerun = not st.session_state.get("trigger_rerun", False)

    st.stop()  



# trial workflow for the end and layout of the stimuli and time


trial = st.session_state.trial_idx
if st.session_state.participant_info_done:
 st.markdown("""
### Instructions  
Please look at each color stimulus and type the color name that best describes it.  
Click **Next** to move to the following stimulus.  
There is no wrong answer — enjoy the experiment!
""")

if trial >= len(st.session_state.stimuli):
    st.success("Experiment finished! Congratulations!")
    st.write(st.session_state.results)
    df = pd.DataFrame(st.session_state.results)
        # Add participant info columns at the end
    df["participant_id"] = st.session_state.participant_id
    df["gender"] = st.session_state.gender
    df["age"] = st.session_state.age
    df["country"] = st.session_state.country
    st.dataframe(df)
    df.to_csv("final_results.csv", index=True) 
    st.ballon()
    st.stop()


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

    if typed_color.strip() == "":
        st.error("Please enter a color name before continuing.")
    else:
        save_trial_result(
            trial_idx=trial,
            img_path=img_path,
            typed_color=typed_color.lower().strip(),
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
>>>>>>> 48b1a23 (Add stimuli folder and experiment files)
              st.ballon()             