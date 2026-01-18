import streamlit as st
import toml
import random
import time
import pandas as pd
import os
from datetime import datetime 
import psycopg2
from supabase import create_client
from io import BytesIO
import tempfile
import uuid


secrets = toml.load(".streamlit/secrets_bi.toml")

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
POSTGRES = st.secrets["postgres"]



def get_db_connection():
    return psycopg2.connect(
        host=POSTGRES["host"],
        dbname=POSTGRES["dbname"],
        user=POSTGRES["user"],
        password=POSTGRES["password"],
        port=POSTGRES["port"]
    )

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


if "phase" not in st.session_state:
    st.session_state.phase = 1

if "language_order" not in st.session_state:
    if random.random() < 0.5:
        st.session_state.language_order = ["EN", "FR"]
    else:
        st.session_state.language_order = ["FR", "EN"]   

if "trial_idx" not in st.session_state:
    st.session_state.trial_idx = 0

if "rt" not in st.session_state:
    st.session_state.rt = None 

if "participant_info_done" not in st.session_state:
    st.session_state.participant_info_done = False

if "trial_submitted" not in st.session_state:
    st.session_state.trial_submitted = False
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

if "end" not in st.session_state:
    st.session_state.end = False  # will be set by user

if "age" not in st.session_state:
    st.session_state.age = None  # will be set by user

if "country" not in st.session_state:
    st.session_state.country = None  # will be set by user
    # --- Initialize participant info state ---
if "lang1" not in st.session_state:
    st.session_state.lang1 = ""
if "lang2" not in st.session_state:
    st.session_state.lang2 = ""
if "lang3" not in st.session_state:
    st.session_state.lang3 = ""

if "input_method" not in st.session_state:
    st.session_state.input_method = None 

if "contexts1" not in st.session_state:
    st.session_state.contexts1 = ""
if "contexts2" not in st.session_state:
    st.session_state.contexts2 = ""
if "contexts3" not in st.session_state:
    st.session_state.contexts3 = ""

if "contexts11" not in st.session_state:
    st.session_state.contexts11 = ""
if "contexts22" not in st.session_state:
    st.session_state.contexts22 = ""
if "contexts33" not in st.session_state:
    st.session_state.contexts33 = ""
if "culture1" not in st.session_state:
    st.session_state.culture1 = ""
if "culture2" not in st.session_state:
    st.session_state.culture2 = ""
if "culture3" not in st.session_state:
    st.session_state.culture3 = ""
defaults = {
    # ratings (numbers)
    "r1": None, "r2": None, "r3": None,
    "culture_rate1": None, "culture_rate2": None, "culture_rate3": None,

    # languages
    "lang1": "", "lang2": "", "lang3": "",

    # fluency ages
    "fluency1": "", "fluency2": "", "fluency3": "",

    # contexts
    "contexts1": "", "contexts11": "", "contexts111": "",
    "contexts_rating1": "", "contexts_rating11": "", "contexts_rating111": "",

    # communication methods (multiselect)
    "method_of_interpersonal_communication": [],

    # cultures
    "culture1": "", "culture2": "", "culture3": "",

    # experiment control
    "trial_idx": 0,
    "start_time": None,
    "trigger_rerun": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value



# Participant info page
if not st.session_state.participant_info_done:
   
    left, center, right = st.columns([1, 40, 1])
    with center:
        st.title("Welcome to our color naming Experiment!")
        st.subheader("Please read thouroughlly the purpose, terms and condition of the experiment.")
        st.markdown(
            "We are the Color Diversity Lab team based in Japan, interested in studying various phenomena "
            "related to the perception of colors. Our current experiment aims to build an ethnosemantic analysis of colors and compare their conceptual shape between languages. The study addresses the fundamental question: whethercolor categories are inherently inferred from the most saturated colors. " \
            "Labels and names attributed to colors will be precious data to get a glimpse of how a language and culture define concepts, beliefs andd cognitive hierarchisation of color categories. " 
            "In the experiment, you will be encouraged to give a name to a color that will be presented to you at each trial. You will be shown one colored square to name. Two addition options, on the left and right, will be given if you cannot find a name to categorize the color that appears."
            "Therefore you will have three color options per trial, summed to 60 colors to names. " \
            "The format of response submission is **free**, **not time constrained**, and you can be as much **descriptive or specific** as possible. "
            "You can either type your response or record it for each of the given colors. "
            "We encourage every participant to finish all the trials and provide names most of the colors appearing during the trials. " \
            "You are free to **pause** and **resume** later the experiment when feeling exhausted. None of your data will be lost if you remain the page open." \
            "After reading the purpose of the experiment and the following terms, and if agree, you will be ask to provide: your, gender, your age, your current location of residency for the last year, your current residency for the last month, your first language of acquisition, and if applicable, your second and third language of acquisition." \
            " You will be also ask to rate your fluency for each of the given languages you speak, your culture of identification and your different at which you make full use of those languages. "
            
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
            "The collected data will be used for the purpose of **scientific research exclusively**. They may be reused and shared with other collaborators of the scientific community of the research project. " \
                 " interested in the study data for the purpose of ulterior scientific research, under the condition that they remain fully anonymized."
            
        )

        st.subheader("Contact ")
        st.markdown(
            "You can reach out anytime if you have any complaints, suggestions or curiosity driven questions related to our study.                               " \
            ""
            "**Experimenter: Meissa Sow** (Graduate School of Design, Kyushu University, Japan) email address: sow.ndeye.meissa.042@s.kyushu-u.ac.jp     " \
            "**Principal Investigator: Prof.Chihiro Hiramatsu** (Graduate School of Design, Kyushu University, Japan)  " \
            
            )
        
        agree = ["**I confirm that I have read and understood the information above and agree to participate voluntarily in this study**","**I do not agree to the terms and conditions and wish to leave.**"]
        st.session_state.consent=st.radio(f"if you have read the terms and conditions above:", agree)


        if st.session_state.consent==agree[0]:
            st.write("Great! Before proceeding please provide the following information. "
                     "They will not be disclosed to the public.")

            st.markdown("---")
            st.subheader("Participant Information")

            st.write(f"Your Participant ID: **{st.session_state.participant_id}**")

            st.session_state.gender = st.radio("Gender", ["Male", "Female", "Other"])

            age_list = [str(i) for i in range(5, 150)]
            st.session_state.age = st.selectbox("Age", age_list)
            education=["None","less than primary school","up to primary school","up high school","with some college years", "finished college or currently enrolled","with some graduate school", "finished my masters or currently enrolled in a Master course", "holding a PhD/M.D/J.D degree or currently enrolled"]
            st.session_state.education = st.selectbox("Please provide your highest level of education if you have been to school. If you do not have any schooling experience, please select'None'", education)
            country_birth = ["Russia", "Japan", "France", "United States", "Senegal", "Other"]
            st.session_state.country_birth = st.selectbox("Country of birth)", country_birth)
            countries = ["Russia", "Japan", "France", "United States", "Senegal", "Other"]
            st.session_state.countries = st.selectbox("Country of Residence (for the last year)", countries)
            countries2 = ["Russia", "Japan", "France", "United States", "Senegal", "Other"]
            st.session_state.countries2 = st.selectbox("Country of Residence (for the last six months)", countries2)

            years=[str(i) for i in range(1940, 2026)]
            st.session_state.last_education = st.selectbox("When was the last time you went to school?", years)
            yes_and_no=["Maybe","Yes","No I do not have any vision problem"]
            st.session_state.vision = st.selectbox("Do you have any vision problems?", yes_and_no)
            
            langs = ["None", "Russian", "Japanese", "French", "English", "Chinese", "Wolof", "Spanish", ]
            scores = [str(i) for i in range(1, 11)]
            contexts= ["interacting with friends","interacting with family","reading","Watching TV","Listening to the radio/music","internet and social media","through social gatherings: parties, religious festivals, religious ceremonies, city events, national events"]
            method_of_interpersonal_communication=["writting: through emails, with text chats, SMS, postal letters","orally: audio messages through voice notes, talking and oral speech"]
            daily_use_frequency= ["daily","often in week","often in a month","not that often(less times within a year)","rarely","not anymore"]
            

        

            st.title("Linguistic Proficiency Assessment")

            #Language of proficiency 1 and rating
            with st.container(border=True):
                st.selectbox("**Choose the dominant language you speak**", langs, index=0, key="lang1") 
                st.radio(
                f"**How confident are you in speaking the {st.session_state.lang1} language?**",
                options=scores,
                horizontal=True,
                key="r1"
                )
                st.caption("1 = None · 2 = Very low · 3 = low · 4 = Fair · 5 = slightly less than adequate · 6 = adequate  · 7 = slightly more than adequate · 8 = good· 9 = Very good · 10 = Excellen or Perfect")
                age_fluency = ["Birth"] + [str(i) for i in range(1, 150)] #became fluent, reading experience,began to be fluent, began acquiring
                st.selectbox("**At which age did you start speaking that language? Please try to give an approximate age**", age_fluency,key="fluency1")

         #contexts of use and rating for language 1
                st.session_state.contexts1= st.selectbox("**Do you still speak the language? if yes, when do you mostly make use of that language?**", contexts, index=0,key="context_use_1")
                st.session_state.contexts_rating1 = st.radio(f"**How often do you speak that language in that context of {st.session_state.contexts1}**", daily_use_frequency, horizontal=True, index=0,key="contexts_1")
                

                st.session_state.contexts2= st.selectbox("**When else do you mostly make use of that language?**", contexts, index=0,key="context_use_2")
                st.session_state.contexts_rating2 = st.radio(f"**How often do you speak that language in that context of {st.session_state.contexts2}**", daily_use_frequency, horizontal=True, index=0, key="contexts_2")

                st.session_state.contexts3= st.selectbox("**When else do you mostly make use of that language? Please give an estimation of often**", contexts, index=0,key="context_use_3")
                st.session_state.contexts_rating3 = st.radio(f"**How often do you speak that language in that context of {st.session_state.contexts3}**", daily_use_frequency, horizontal=True, index=0,key="contexts_3")

                st.session_state.method_of_interpersonal_communication = st.multiselect("**How do you usually communicate in that language?**",method_of_interpersonal_communication, key="com1")



         #Language of proficiency 2 and rating
            with st.container(border=True):
                st.selectbox("**Do you speak any other language? Please specify by selecting one of them from the list.**", langs, index=0, key="lang2") 
                st.radio(
                f"**How confident are you in speaking the {st.session_state.lang2} language?**",
                options=scores,
                horizontal=True,
                key="r2"
                )
                st.caption("1 = None · 2 = Very low · 3 = low · 4 = Fair · 5 = slightly less than adequate · 6 = adequate  · 7 = slightly more than adequate · 8 = good· 9 = Very good · 10 = Excellen or Perfect")
                age_fluency = ["Birth"] + [str(i) for i in range(1, 150)] #became fluent, reading experience,began to be fluent, began acquiring
                st.selectbox("**At which age did you start speaking that language? Please try to give an approximate age**", age_fluency,key="fluency2")
         #contexts of use and rating for language 2
                st.session_state.contexts11= st.selectbox("**Do you still speak the language? if yes, when do you mostly make use of that language?**", contexts, index=0,key="context_use_11")
                st.radio(f"How often do you speak that language in that context of {st.session_state.contexts11}", daily_use_frequency, horizontal=True, index=0,key="contexts_11")

                st.session_state.contexts22= st.selectbox("**When else do you mostly make use of that language?**", contexts, index=0,key="context_use_22")
                st.radio(f"**How often do you speak that language in that context of {st.session_state.contexts22}**", daily_use_frequency, horizontal=True, index=0, key="contexts_22")

                st.session_state.contexts33= st.selectbox("**When else do you mostly make use of that language? Please give an estimation of often**", contexts, index=0,key="context_use_33")
                st.session_state.contexts_rating33 = st.radio(f"**How often do you speak that language in that context of {st.session_state.contexts33}**", daily_use_frequency, horizontal=True, index=0,key="contexts_33")

                st.session_state.method_of_interpersonal_communication = st.multiselect("**How do you usually communicate in that language?**",method_of_interpersonal_communication,key="com2")
                


                #Language of proficiency 3 and rating
            with st.container(border=True):
                st.selectbox("**Do you speak any other language? Please specify by selecting one of them from the list.**", langs, index=0, key="lang3") 
                st.radio(
                f"**How confident are you in speaking the {st.session_state.lang3} language?**",
                options=scores,
                horizontal=True,
                key="r3"
                )
                st.caption("1 = None · 2 = Very low · 3 = low · 4 = Fair · 5 = slightly less than adequate · 6 = adequate  · 7 = slightly more than adequate · 8 = good· 9 = Very good · 10 = Excellen or Perfect")
                age_fluency = ["Birth"] + [str(i) for i in range(1, 150)] #became fluent, reading experience,began to be fluent, began acquiring
                st.selectbox("**At which age did you start speaking that language? Please try to give an approximate age**", age_fluency,key="fluency3")
         #contexts of use and rating for language 3
                st.session_state.contexts111 = st.selectbox("**Do you still speak the language? if yes, when do you mostly make use of that language?**", contexts, index=0,key="context_use_111")
                st.session_state.contexts_rating111 = st.radio(f"**How often do you speak that language in that context of {st.session_state.contexts111}**", daily_use_frequency, horizontal=True, index=0,key="contexts_111")

                st.session_state.contexts222 = st.selectbox("**When else do you mostly make use of that language?**", contexts, index=0)
                st.session_state.contexts_rating222 = st.radio(f"**How often do you speak that language in that context of {st.session_state.contexts222}**", daily_use_frequency, horizontal=True, index=0, key="contexts_222")

                st.session_state.contexts333 = st.selectbox("**When else do you mostly make use of that language? Please give an estimation of often**", contexts, index=0)
                st.session_state.contexts_rating333 = st.radio(f"**How often do you speak that language in that context of {st.session_state.contexts333}**", daily_use_frequency, horizontal=True, index=0,key="contexts_333")

                st.session_state.method_of_interpersonal_communication = st.multiselect("**How do you usually communicate in that language?**",method_of_interpersonal_communication,key="com3")

               ###CULTURES
            with st.container(border=True):
                cultures=["None","wolof","japanese","french","american","european","vietnamese","serere","Pular","Russian","lebou","canadian","I prefer to not tell"]
                st.selectbox("**In which culture do you identify yourselft the most?**", cultures, index=0 ,key="culture1")
                st.radio(f"**Please estimate how much you self-identify in {st.session_state.culture1} culture**", scores, horizontal=True, index=0,key="culture_rate1")

                st.selectbox("**Any other culture?**", cultures, index=0 ,key="culture2")
                st.radio(f"**Please estimate how much you self identify in {st.session_state.culture2} culture?**", scores, horizontal=True, index=0,key="culture_rate2")

                st.selectbox("**Any other culture you have identified?**", cultures, index=0,key="culture3")
                st.radio(f"**Please give an estimation here as well for {st.session_state.culture3} culture**", scores, horizontal=True, index=0,key="culture_rate3")
            

    if st.session_state.consent == agree[1]:
           st.title("Thank you for your attention! You may now close the browser.")  
           st.stop()
        




    if st.button("Submit Info"):
            st.session_state.participant_info_done = True
            st.session_state.trigger_rerun = not st.session_state.get("trigger_rerun", True)
    st.stop()     


# 
#phase 1 phase 2 trial emphasis and logic trial workflow for the end and layout of the stimuli and time
    
trial = st.session_state.trial_idx
total_trials = len(st.session_state.stimuli)

if st.session_state.participant_info_done and trial >= total_trials:

    if st.session_state.phase == 1:
        # Move to phase 2
        st.session_state.phase = 2
        st.session_state.trial_idx = 0
        st.session_state.start_time = None

        st.success("Phase 1 completed. The experiment will now continue in French 🇫🇷")
        st.info("Veuillez continuer en français.")
        st.rerun()

    else:
        # End experiment after phase 2
        st.session_state.experiment_finished = True
if st.session_state.get("experiment_finished"):
    st.success("Experiment finished! Congratulations! Thank you for your precious participation.")
    st.balloons()
    st.stop()



if st.session_state.participant_info_done:
 if st.session_state.phase == 1:
        st.markdown("""
### Instructions (English)
Please look at the colored square appearing on your screen and provide a description or a name to it.
...
Thank you for cooperation and enjoy the experiment!
""")
 else:
        st.markdown("Veuillez observer le carré coloré affiché à l'écran et fournir une description ou un nom de cette couleur."
"Vous pouvez utiliser un mot, plusieurs mots ou un paragraphe.")
#There are other options on the  on ⬅️**LEFT** or ➡️**RIGHT** that will unravel each, a color picker for you to choose a color that you can name"
with st.expander("🔊 **Voiced Instructions**", expanded=True):
    st.write("Click on the button 'Play' to release the voiced instructions.")
   
    st.audio("Voiced_instructions.mp3", format="audio/mpeg")

# with st.expander("**Ranking guide**🏆",expanded= True):
#     st.write("""Rank according to what you feel is the most typical color.**Please, remember that there is no bad answer**"
#     "- **1=Best**: The most typical and representative of the category."
#     "- **2=Good**: Quite close to typical, but not totally."
#     "- **3=Alternative**: Could be typical or not."
#     "- **0=Indifferent**: No ranking or preference."
#     """)
if st.session_state.phase == 1:
    st.info("Phase 1 / 2 – English 🇬🇧")
else:
    st.info("Phase 2 / 2 – Français 🇫🇷")
st.progress(trial / total_trials)
st.subheader(f"Trial {trial + 1} of {total_trials}")

# Show the current image
filename = st.session_state.stimuli[trial]
img_path = os.path.join(stimuli_folder, filename)
image = filename
participant_id = st.session_state.participant_id
if "start_time" not in st.session_state:
    st.session_state.start_time = None

if st.session_state.start_time is None:
    st.session_state.start_time = time.time()


    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def save_trial_to_supabase(
    participant_id, trial, image, typed_color, rt, 
    left_hex_code=None, left_color_name=None, 
    right_hex_code=None, right_color_name=None,
    left_rank=None, center_rank=None, right_rank=None,phase=None,
    gender=None, age=None, education=None, country_birth=None,
    countries=None, countries2=None, last_education=None, vision=None,
    lang1="", r1=None, fluency1="", contexts1="", contexts_rating1="",
    lang2="", r2=None, fluency2="", contexts11="", contexts_rating11="",
    lang3="", r3=None, fluency3="", contexts111="", contexts_rating111="",
    method_of_interpersonal_communication=None, 
    culture1="", culture_rate1=None,
    culture2="", culture_rate2=None,
    culture3="", culture_rate3=None
          ):
    if method_of_interpersonal_communication is None:
        method_of_interpersonal_communication = []

    conn = get_db_connection()
    cur = conn.cursor()

#   4 new columns here 
    
    cur.execute("""
        INSERT INTO response_bilinguals (
            participant_id, trial, image, typed_color, rt, phase,
            gender, age, education, country_birth, 
            residence_last_year, residence_six_months, last_year_school, vision_issues,
            lang1, r1, fluency1, contexts1, contexts_rating1,
            lang2, r2, fluency2, contexts11, contexts_rating11,
            lang3, r3, fluency3, contexts111, contexts_rating111,
            method_of_interpersonal_communication,
            culture1, culture_rate1, culture2, culture_rate2, culture3, culture_rate3
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
    """, (
        participant_id, trial, image, typed_color, rt,
        left_hex_code, left_color_name, right_hex_code, right_color_name,
        left_rank, center_rank, right_rank, phase,
        gender, age, education, country_birth, 
        countries, countries2, last_education, vision,
        lang1, r1, fluency1, contexts1, contexts_rating1,
        lang2, r2, fluency2, contexts11, contexts_rating11,
        lang3, r3, fluency3, contexts111, contexts_rating111,
        method_of_interpersonal_communication,
        culture1, culture_rate1, culture2, culture_rate2, culture3, culture_rate3
    ))

    conn.commit()
    cur.close()
    conn.close()
   
 # to pause the experiment
if st.session_state.paused:
    st.subheader("Experiment paused")
    if st.button("Resume ▶️"):
        st.session_state.paused = False
        st.session_state.start_time = time.time()
        st.rerun()
    st.stop()

with st.expander(" Click here to Pause ⏸️"):
    st.write("⚠️**CAUTION** You can press 'Pause ⏸️' to stop and resume later. However, you need to remain your window open, otherwise your progress will be lost.")
    
    # Toggle button: If paused, show 'Resume'; if not, show 'Pause'
    if not st.session_state.paused:
        if st.button("Pause ⏸️"):
            st.session_state.paused = True
            st.rerun()
    else:
        if st.button("Resume ▶️"):
            st.session_state.paused = False
            # Reset start_time so the pause duration isn't counted in RT
            st.session_state.start_time = time.time() 
            st.rerun()


# Layou screen
# st.markdown("""
#     <style>
#         .color-preview {
#             width: 100%;
#             height: 200px;
#             border-radius: 10px;
#             border: none;
#             margin-bottom: 10px;
#             display: flex;
#             align-items: center;
#             justify-content: center;
#             color: white;
#             font-weight: bold;
#             text-shadow: 1px 1px 2px black;
#         }
#     </style>
# """, unsafe_allow_html=True)

_, col_center, _ = st.columns([1, 4, 1]) #col_left, col_center, col_right = st.columns([2, 2, 2])

# rank_options = ["0", "1", "2", "3"]
# with col_left:
#     with st.expander("⬅️**LEFT**", expanded=False):
#         l_hex = st.color_picker("", "#808080", key=f"foc_h_{trial}", label_visibility="collapsed")
#         # 2. The Large Preview Square
#         st.markdown(f'<div class="color-preview" style="background-color: {l_hex};"></div>', unsafe_allow_html=True)
#         left_text = st.text_input("Type your response here ⌨️📝", key=f"foc_n_{trial}", placeholder="Ex: Saturated Red")
#         left_audio = st.audio_input("Record your answer here🎤", key=f"left_a_{trial}")
#         # NEW: Ranking for Left
        
#         left_rank = st.selectbox("Rank", rank_options, key=f"rank_l_{trial}")
        

with col_center:
    with st.container(border=True):
      
      filename = st.session_state.stimuli[trial]
      img_path = os.path.join(stimuli_folder, filename)
      st.image(img_path, use_container_width=True)
      

      
    
    # # css to change dimension without children
    #   st.markdown(
    #     """
    #     <style>
    #         /* image from the center */
    #         [data-testid="stImage"] img {
    #             height: 200px !important;
    #             width: auto !important;
    #             object-fit: none;
    #             border-radius: 10px;
    #         }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )
      typed_color = st.text_input("Type your response here ⌨️📝", key=f"resp_{trial}")
      audio_value = st.audio_input("Record your answer here🎤", key=f"center_a_{trial}")
    #   center_rank = st.selectbox("Rank", rank_options, key=f"rank_c_{trial}")

# with col_right:
#      with st.expander("➡️ **RIGHT**", expanded=False):
#         r_hex = st.color_picker("", "#808080", key=f"var_h_{trial}", label_visibility="collapsed")
#         # 2. The Large Preview Square
#         st.markdown(f'<div class="color-preview" style="background-color: {r_hex};"></div>', unsafe_allow_html=True)
#         right_text = st.text_input("Type your response here ⌨️📝", key=f"var_n_{trial}", placeholder="Ex: Light Red")
#         right_audio = st.audio_input("Record your answer here🎤", key=f"right_a_{trial}")
#         right_rank = st.selectbox("Rank", rank_options, key=f"rank_r_{trial}")
        
# --- BUTTONS ---
st.markdown("---")
sub_col, next_col = st.columns(2)


if sub_col.button("Submit Response ✅", use_container_width=True):
    # # --- DYNAMIC VALIDATION ---
    # # This checks if ANY of the 6 inputs are filled
    # has_text = any([
    #     typed_color and typed_color.strip(), 
    #     left_text and left_text.strip(), 
    #     right_text and right_text.strip()
    # ])
    # has_audio = any([audio_value, left_audio, right_audio])

    # if not (has_text or has_audio):
    #     st.error("Please provide at least one response (typed or recorded) in any section.")
    # else:
    typed = bool(typed_color and typed_color.strip())
    audio = bool(audio_value)
    rt = time.time() - st.session_state.start_time
    if not typed and not audio:
        st.error("Please provide a response (text or audio).")
        st.stop()

    chosen_method = "audio" if audio else "text"

    if st.session_state.input_method is None:
        st.session_state.input_method = chosen_method
    elif st.session_state.input_method != chosen_method:
        st.error(f"You must continue using {st.session_state.input_method} for all trials.")
        st.stop()

    rt = time.time() - st.session_state.start_time

        # 1. UPLOAD CENTER STIMULUS AUDIO (Includes filename)
    if audio_value is not None:
            audio_bytes = audio_value.read()
            if isinstance(audio_bytes, memoryview): audio_bytes = audio_bytes.tobytes()
            if len(audio_bytes) > 0:
                # Includes the stimulus image name
                center_filename = f"center_{image}_part_{st.session_state.participant_id}_trial_{st.session_state.trial_idx}_{uuid.uuid4().hex}.wav"
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                    tmp_file.write(audio_bytes)
                    tmp_path = tmp_file.name
                supabase.storage.from_("center_color_audio").upload(center_filename, tmp_path, {"content-type": "audio/wav"})
                os.remove(tmp_path)

        # 2. UPLOAD LEFT FOCAL AUDIO (Includes Hex Code)
    # if left_audio is not None:
    #         left_bytes = left_audio.read()
    #         if isinstance(left_bytes, memoryview): left_bytes = left_bytes.tobytes()
    #         if len(left_bytes) > 0:
    #             # Removes '#' from hex for a safe filename
    #             clean_l_hex = l_hex.lstrip('#')
    #             left_audio_filename = f"left_{clean_l_hex}_part_{st.session_state.participant_id}_trial_{st.session_state.trial_idx}_{uuid.uuid4().hex}.wav"
    #             with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_left:
    #                 tmp_left.write(left_bytes)
    #                 l_tmp_path = tmp_left.name
    #             supabase.storage.from_("left_color_audio").upload(left_audio_filename, l_tmp_path, {"content-type": "audio/wav"})
    #             os.remove(l_tmp_path)

    #     # 3. UPLOAD RIGHT VARIANT AUDIO (Includes Hex Code)
    # if right_audio is not None:
    #         right_bytes = right_audio.read()
    #         if isinstance(right_bytes, memoryview): right_bytes = right_bytes.tobytes()
    #         if len(right_bytes) > 0:
    #             clean_r_hex = r_hex.lstrip('#')
    #             right_audio_filename = f"right_{clean_r_hex}_part_{st.session_state.participant_id}_trial_{st.session_state.trial_idx}_{uuid.uuid4().hex}.wav"
    #             with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_right:
    #                 tmp_right.write(right_bytes)
    #                 r_tmp_path = tmp_right.name
    #             # Note: Fixed bucket name and variable path from your snippet
    #             supabase.storage.from_("right_color_audio").upload(right_audio_filename, r_tmp_path, {"content-type": "audio/wav"})
    #             os.remove(r_tmp_path)
                    

            # ---- save to database (Including new picker fields) ----
            save_trial_to_supabase(
                participant_id=st.session_state.participant_id,
                trial=st.session_state.trial_idx,
                image=filename, # Ensure 'filename' is defined in your trial loop----
                typed_color=typed_color,
                rt=rt,
                # left_hex_code=l_hex,       # The hex from left picker
                # left_color_name=left_text,  # The text from left input
                # right_hex_code=r_hex,      # The hex from right picker
                # right_color_name=right_text,
                # left_rank=left_rank,
                # center_rank=center_rank,
                # right_rank=right_rank, # The text from right input
                phase= st.session_state.age,
                gender=st.session_state.gender,
                age=st.session_state.age,
                education=st.session_state.education,
                country_birth=st.session_state.country_birth,
                countries=st.session_state.countries,
                countries2=st.session_state.countries2,
                last_education=st.session_state.last_education,
                vision=st.session_state.vision, 
                lang1=st.session_state.lang1,
                r1=st.session_state.r1,
                fluency1=st.session_state.fluency1,
                contexts1=st.session_state.contexts1,
                contexts_rating1=st.session_state.contexts_rating1,
                lang2=st.session_state.lang2,
                r2=st.session_state.r2,
                fluency2=st.session_state.fluency2,
                contexts11=st.session_state.contexts11,
                contexts_rating11=st.session_state.contexts_rating11,
                lang3=st.session_state.lang3,
                r3=st.session_state.r3,
                fluency3=st.session_state.fluency3,
                contexts111=st.session_state.contexts111,
                contexts_rating111=st.session_state.contexts_rating111,
                method_of_interpersonal_communication=st.session_state.method_of_interpersonal_communication,
                culture1=st.session_state.culture1,
                culture_rate1=st.session_state.culture_rate1,
                culture2=st.session_state.culture2,
                culture_rate2=st.session_state.culture_rate2,
                culture3=st.session_state.culture3,
                culture_rate3=st.session_state.culture_rate3,
            )
        
    st.session_state.trial_submitted = True
         
    st.rerun()

#SUCCESS FEEDBACK
if st.session_state.get("trial_submitted"):
    st.success("✅ Your response has been submitted!")
    st.info("Please click 'Next Trial ⏭️' to proceed.")

# NEXT TRIAL BUTTON 
if next_col.button("Next Trial ⏭️", use_container_width=True):

    if not st.session_state.trial_submitted:
        st.warning("Please Submit first.")
        st.stop()

    st.session_state.trial_idx += 1
    st.session_state.trial_submitted = False
    st.session_state.start_time = None

    # Phase finished?
    if st.session_state.trial_idx >= total_trials:

        if st.session_state.phase == 1:
            # Move to phase 2
            st.session_state.phase = 2
            st.session_state.trial_idx = 0
            st.success("Phase 1 completed. Starting French phase 🇫🇷")

        else:
            # Experiment finished
            st.session_state.experiment_finished = True

st.rerun() 
