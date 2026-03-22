import streamlit as st
import random
import re
import streamlit.components.v1 as components

# --- KONFIGURATION ---
st.set_page_config(
    page_title="The Snitch - Reported Speech Trainer", 
    page_icon="📝", 
    layout="centered"
)

# --- DESIGN (CSS) ---
st.markdown("""
<style>
/* Hintergrund schwarz, Standardschrift weiß */
.stApp {
    background-color: #000000;
    color: #ffffff;
}

/* Überschriften, Texte und Labels in Weiß erzwingen */
h1, h2, h3, p, label, .stMarkdown {
    color: #ffffff !important;
}

/* Buttons: Weißer Hintergrund, schwarze Schrift */
div.stButton > button {
    background-color: #ffffff !important;
    border: 2px solid #ffffff !important;
    transition: all 0.3s ease-in-out;
}

/* Die Schrift im Button explizit schwarz machen */
div.stButton > button p {
    color: #000000 !important;
}

/* Hover-Effekt: Invertieren (Schwarz mit weißer Schrift) */
div.stButton > button:hover {
    background-color: #000000 !important;
    border: 2px solid #ffffff !important;
}

/* Hover-Effekt: Schrift im Button weiß machen */
div.stButton > button:hover p {
    color: #ffffff !important;
}

/* Eingabefeld an den Dark Mode anpassen */
.stTextInput input {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
    border: 1px solid #555555 !important;
}
.stTextInput input:focus {
    border: 1px solid #ffffff !important;
}
</style>
""", unsafe_allow_html=True)


# --- VOLLSTÄNDIGER DATENSATZ ---
@st.cache_data
def get_data():
    return {
        "Statements": [
            {"direct": "I am hungry.", "prefix": "He said that", "answer": "he was hungry", "explanation": "am ➔ was"},
            {"direct": "We are watching a movie.", "prefix": "They said that", "answer": "they were watching a movie", "explanation": "are ➔ were"},
            {"direct": "I have finished my project.", "prefix": "She said that", "answer": "she had finished her project", "explanation": "have finished ➔ had finished"},
            {"direct": "I will call you tomorrow.", "prefix": "He said that", "answer": ["he would call me the next day", "he would call me the following day"], "explanation": "will ➔ would | tomorrow ➔ the next day"},
            {"direct": "The sun rises in the east.", "prefix": "The teacher said that", "answer": "the sun rose in the east", "explanation": "rises ➔ rose"},
            {"direct": "I don't like coffee.", "prefix": "She said that", "answer": ["she didn't like coffee", "she did not like coffee"], "explanation": "don't ➔ didn't"},
            {"direct": "We went to Paris last year.", "prefix": "They said that", "answer": "they had gone to Paris the year before", "explanation": "went ➔ had gone"},
            {"direct": "I can speak three languages.", "prefix": "He said that", "answer": "he could speak three languages", "explanation": "can ➔ could"},
            {"direct": "I am playing the guitar.", "prefix": "She said that", "answer": "she was playing the guitar", "explanation": "am playing ➔ was playing"},
            {"direct": "I have never been to London.", "prefix": "He said that", "answer": "he had never been to London", "explanation": "have never been ➔ had never been"},
            {"direct": "My brother is ill.", "prefix": "She said that", "answer": "her brother was ill", "explanation": "my ➔ her | is ➔ was"},
            {"direct": "We will help you.", "prefix": "They said that", "answer": "they would help me", "explanation": "will ➔ would"},
            {"direct": "I saw a ghost.", "prefix": "The boy said that", "answer": "he had seen a ghost", "explanation": "saw ➔ had seen"},
            {"direct": "I am not coming.", "prefix": "He said that", "answer": ["he was not coming", "he wasn't coming"], "explanation": "am not ➔ was not"},
            {"direct": "The train leaves at five.", "prefix": "She said that", "answer": "the train left at five", "explanation": "leaves ➔ left"},
            {"direct": "I have lost my phone.", "prefix": "He said that", "answer": "he had lost his phone", "explanation": "have lost ➔ had lost"},
            {"direct": "We are happy here.", "prefix": "They said that", "answer": "they were happy there", "explanation": "are ➔ were | here ➔ there"},
            {"direct": "I didn't do it.", "prefix": "She said that", "answer": ["she hadn't done it", "she had not done it"], "explanation": "didn't do ➔ hadn't done"},
            {"direct": "It is raining.", "prefix": "He said that", "answer": "it was raining", "explanation": "is ➔ was"},
            {"direct": "I will be there.", "prefix": "She said that", "answer": "she would be there", "explanation": "will ➔ would"},
            {"direct": "I have a new car.", "prefix": "He said that", "answer": "he had a new car", "explanation": "have ➔ had"},
            {"direct": "The children are sleeping.", "prefix": "She said that", "answer": "the children were sleeping", "explanation": "are ➔ were"},
            {"direct": "I went shopping yesterday.", "prefix": "He said that", "answer": "he had gone shopping the day before", "explanation": "yesterday ➔ the day before"},
            {"direct": "I can't find my keys.", "prefix": "She said that", "answer": ["she couldn't find her keys", "she could not find her keys"], "explanation": "can't ➔ couldn't"},
            {"direct": "We are going on holiday.", "prefix": "They said that", "answer": "they were going on holiday", "explanation": "are ➔ were"},
            {"direct": "I have already eaten.", "prefix": "He said that", "answer": "he had already eaten", "explanation": "have ➔ had"},
            {"direct": "I don't know the answer.", "prefix": "She said that", "answer": ["she didn't know the answer", "she did not know the answer"], "explanation": "don't ➔ didn't"},
            {"direct": "I will buy a house.", "prefix": "He said that", "answer": "he would buy a house", "explanation": "will ➔ would"},
            {"direct": "The pizza is delicious.", "prefix": "They said that", "answer": "the pizza was delicious", "explanation": "is ➔ was"},
            {"direct": "I was at home.", "prefix": "She said that", "answer": "she had been at home", "explanation": "was ➔ had been"},
            {"direct": "I am learning Spanish.", "prefix": "He said that", "answer": "he was learning Spanish", "explanation": "am ➔ was"},
            {"direct": "My father works in a bank.", "prefix": "She said that", "answer": "her father worked in a bank", "explanation": "works ➔ worked"},
            {"direct": "We have seen this film before.", "prefix": "They said that", "answer": "they had seen that film before", "explanation": "this ➔ that"},
            {"direct": "I don't have enough money.", "prefix": "He said that", "answer": ["he didn't have enough money", "he did not have enough money"], "explanation": "don't ➔ didn't"},
            {"direct": "I will send the email now.", "prefix": "She said that", "answer": "she would send the email then", "explanation": "now ➔ then"},
            {"direct": "The museum is closed.", "prefix": "He said that", "answer": "the museum was closed", "explanation": "is ➔ was"},
            {"direct": "I am meeting a friend.", "prefix": "She said that", "answer": "she was meeting a friend", "explanation": "am ➔ was"},
            {"direct": "We lived in Berlin.", "prefix": "They said that", "answer": "they had lived in Berlin", "explanation": "lived ➔ had lived"},
            {"direct": "I haven't seen her.", "prefix": "He said that", "answer": ["he hadn't seen her", "he had not seen her"], "explanation": "haven't ➔ hadn't"},
            {"direct": "I forgot my umbrella.", "prefix": "She said that", "answer": "she had forgotten her umbrella", "explanation": "forgot ➔ had forgotten"},
            {"direct": "The cake tastes great.", "prefix": "He said that", "answer": "the cake tasted great", "explanation": "tastes ➔ tasted"},
            {"direct": "I am not afraid.", "prefix": "She said that", "answer": ["she was not afraid", "she wasn't afraid"], "explanation": "am ➔ was"},
            {"direct": "We will win.", "prefix": "They said that", "answer": "they would win", "explanation": "will ➔ would"},
            {"direct": "I broke the vase.", "prefix": "The girl said that", "answer": "she had broken the vase", "explanation": "broke ➔ had broken"},
            {"direct": "I am feeling better today.", "prefix": "He said that", "answer": "he was feeling better that day", "explanation": "today ➔ that day"},
            {"direct": "My parents are coming.", "prefix": "She said that", "answer": "her parents were coming", "explanation": "are ➔ were"},
            {"direct": "I have to go now.", "prefix": "He said that", "answer": "he had to go then", "explanation": "have to ➔ had to"},
            {"direct": "I won't tell anyone.", "prefix": "She said that", "answer": ["she wouldn't tell anyone", "she would not tell anyone"], "explanation": "won't ➔ wouldn't"},
            {"direct": "The weather is beautiful.", "prefix": "They said that", "answer": "the weather was beautiful", "explanation": "is ➔ was"},
            {"direct": "I didn't see the accident.", "prefix": "He said that", "answer": ["he hadn't seen the accident", "he had not seen the accident"], "explanation": "didn't see ➔ hadn't seen"},
            {"direct": "I am waiting for the bus.", "prefix":
