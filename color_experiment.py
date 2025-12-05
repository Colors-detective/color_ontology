
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
        st.title("Welcome to our color naming Experiment!")
        st.subheader("Please read read thouroughlly the purpose, terms and condition of the experiment.")
        st.markdown(
            "We are a Color Diversity Lab team based in Japan, interested in studying various phenomena "
            "related to the perception of colors. Our current experiment aims to build an ethnosemantic analysis of cultures and their **color categorization**. "
            "In the experiment, you will be encouraged to give a name to a color that will be presented to you at each trial. You will be shown in total **300 trials** successively.Therefore in principle, **300 names** " \
            "are expected to be collected per participant." \
            "The format of providing names is **free**, **not time constrained**, and you can be as much **descriptive or specific** as possible. "
            "You can either type your response or record it. "
            "We encourage every participant to provide their effort into finishing the color naming task through **at least 80% of the trials.** " \
            "You are free to **pause** and **resume** later the experiment when feeling exhausted. None of your data will be lost if you remain the page open. "
            "Labels and names attributed to colors will precious data to get a glimpse of how a language and culture define concepts, beliefs and hierarchisation of color categories. "
        )
        st.subheader("Participation in the Project")
        st.markdown(
            "Your participation in this project is **voluntary**. You understand that you will **not be paid** for your participation. You may withdraw and discontinue participation at any time without penalty." \
            " If you feel uncomfortable in any way during the experiment, you have the right to leave by clicking on the button `**End**´ to force the experiment to stop, then simply close the browser."
            " With your permission, your response time, responses in either format (text and audio) will be saved. "
            "In agreeing to participate to the experiment, you will be asked to provided additionnally, some information related to your gender, your place of residence, your country of birth, your" \
            " first language of proficiency, and if applicable, your second language, third and fourth of proficiency. "
        )
        st.subheader("Confidentiality ")
        st.markdown(
            "To ensure anonymosity, you will be assigned a random ID of participation after agreeing to the terms and conditions of the experiment. "
            "Your **anonymousity** as a participant in this study will **remain the same** through the carried study. No information allowing your identification will be stored. The experiment results will be stored in a secure and encrypted database " \
            "located in the server of our laboratory under the supervision of our team and University authority. " \
            
        )
        st.subheader("Data Usage")
        st.markdown(
            "The collected data will be used for the purpose of **scientific research exclusively**. They may be communicated to the scientific partners of the research project and to the authorities upon their explicit request in case of a criminal investigation. " \
            "They may also be reused by the research team of Color Diversity Lab or any other lab interested in the study data for the purpose of ulterior scientific research, under the condition that they remain fully pseudonymized.  "
            
        )

        st.subheader("Contact ")
        st.markdown(
            "You can reach out anytime if you have any complaints, suggestions or curiosity driven questions related to our study.                               " \
            ""
            "**Experimenter: Meissa Sow** (Graduate School of Design, Kyushu University, Japan) email address: sow.ndeye.meissa.042@s.kyushu-u.ac.jp     " \
            "**Principal Investigator: Prof.Chihiro Hiramatsu** (Graduate School of Design, Kyushu University, Japan)  " \
            
            )
        agree = st.checkbox("**I agree to the terms and conditions, and wave my rights to take participation to the study**")
        Disagree= st.checkbox ("**I disagree to the terms and conditions and therefore want to leave.**")

        if agree:
            st.write("Great! Before proceeding please provide the following information. "
                     "They will not be disclosed to the public.")

            st.markdown("---")
            st.subheader("Participant Information")

            st.write(f"Your Participant ID: **{st.session_state.participant_id}**")

            st.session_state.gender = st.radio("Gender", ["Male", "Female", "Other"])

            age_list = [str(i) for i in range(0, 81)]
            st.session_state.age = st.selectbox("Age", age_list)

            country_birth = ["Russia", "Japan", "France", "United States", "Senegal", "Other"]
            st.session_state.country_birth = st.selectbox("Country of birth)", country_birth)
            countries = ["Russia", "Japan", "France", "United States", "Senegal", "Other"]
            st.session_state.countries = st.selectbox("Country of Residence (for at least a year)", countries)
            countries2 = ["Russia", "Japan", "France", "United States", "Senegal", "Other"]
            st.session_state.countries2 = st.selectbox("Country of Residence (for at least six months)", countries2)

            # Defining the variables
            Language1 = ["Russian", "Japanese", "French", "English", "Chinese", "Wolof", "Spanish"]
            Language2 = ["None", "Japanese", "French", "English", "Chinese", "Wolof", "Spanish"]
            Language3 = ["None", "Russian", "Japanese", "French", "English", "Chinese", "Wolof", "Spanish"]
            other = ["None", "Japanese", "French", "English", "Chinese", "Wolof", "Spanish"]

            st.session_state.lang1 = st.selectbox("Language of Proficiency 1", Language1)
            st.session_state.lang2 = st.selectbox("Language of Proficiency 2", Language2)
            st.session_state.lang3 = st.selectbox("Language of Proficiency 3", Language3)
            st.session_state.lang4 = st.selectbox("Language of Proficiency 4", other)

            if st.button("Submit Info"):
                st.session_state.participant_info_done = True
                st.rerun()
    if Disagree:
     st.title("Thank you for your attention!")
     st.write("You may now close the browser.")

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
    df["Country of birth"] = st.session_state.country_birth
    df["Country of Residence (for at least a year)"]= st.session_state.countries
    df["Country of Residence (for at least six months)"]= st.session_state.countries2
    df["Language of Proficiency 1 or birth language"]= st.session_state.lang1
    df["Language of Proficiency 2"]= st.session_state.lang2
    df["Language of Proficiency 3"]= st.session_state.lang3
    df["Other"]= st.session_state.lang4


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
