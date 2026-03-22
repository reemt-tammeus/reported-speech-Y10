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
            {"direct": "I am waiting for the bus.", "prefix": "He said that", "answer": "he was waiting for the bus", "explanation": "am ➔ was"},
            {"direct": "We have lived here for ten years.", "prefix": "They said that", "answer": "they had lived there for ten years", "explanation": "here ➔ there"},
            {"direct": "I will do my best.", "prefix": "She said that", "answer": "she would do her best", "explanation": "my ➔ her"},
            {"direct": "I didn't see you at the party.", "prefix": "He told me that", "answer": ["he hadn't seen me at the party", "he had not seen me at the party"], "explanation": "didn't see ➔ hadn't seen"},
            {"direct": "The water is boiling.", "prefix": "She said that", "answer": "the water was boiling", "explanation": "is ➔ was"},
            {"direct": "I have already finished my breakfast.", "prefix": "He said that", "answer": "he had already finished his breakfast", "explanation": "my ➔ his"},
            {"direct": "We are going to the cinema tonight.", "prefix": "They said that", "answer": "they were going to the cinema that night", "explanation": "tonight ➔ that night"},
            {"direct": "I can't swim very well.", "prefix": "She said that", "answer": ["she couldn't swim very well", "she could not swim very well"], "explanation": "can't ➔ couldn't"},
            {"direct": "I found a wallet.", "prefix": "He said that", "answer": "he had found a wallet", "explanation": "found ➔ had found"},
            {"direct": "My sister is a doctor.", "prefix": "She said that", "answer": "her sister was a doctor", "explanation": "is ➔ was"},
            {"direct": "I will bring the book back.", "prefix": "He said that", "answer": "he would bring the book back", "explanation": "will ➔ would"},
            {"direct": "The shops are closed.", "prefix": "She said that", "answer": "the shops were closed", "explanation": "are ➔ were"},
            {"direct": "I am reading a book.", "prefix": "He said that", "answer": "he was reading a book", "explanation": "am ➔ was"},
            {"direct": "We haven't been to the zoo yet.", "prefix": "They said that", "answer": ["they hadn't been to the zoo yet", "they had not been to the zoo yet"], "explanation": "haven't ➔ hadn't"},
            {"direct": "I don't like spicy food.", "prefix": "She said that", "answer": ["she didn't like spicy food", "she did not like spicy food"], "explanation": "don't ➔ didn't"},
            {"direct": "I will call you.", "prefix": "He said that", "answer": "he would call me", "explanation": "will ➔ would"},
            {"direct": "The dog is barking.", "prefix": "She said that", "answer": "the dog was barking", "explanation": "is ➔ was"},
            {"direct": "I have lost my passport.", "prefix": "He said that", "answer": "he had lost his passport", "explanation": "my ➔ his"},
            {"direct": "We saw a great play.", "prefix": "They said that", "answer": "they had seen a great play", "explanation": "saw ➔ had seen"},
            {"direct": "I am not feeling well.", "prefix": "She said that", "answer": ["she was not feeling well", "she wasn't feeling well"], "explanation": "am ➔ was"},
            {"direct": "I will make a cake.", "prefix": "He said that", "answer": "he would make a cake", "explanation": "will ➔ would"},
            {"direct": "My parents are on holiday.", "prefix": "She said that", "answer": "her parents were on holiday", "explanation": "are ➔ were"},
            {"direct": "I have been working hard.", "prefix": "He said that", "answer": "he had been working hard", "explanation": "have been ➔ had been"},
            {"direct": "We are moving.", "prefix": "They said that", "answer": "they were moving", "explanation": "are ➔ were"},
            {"direct": "I didn't have time.", "prefix": "She said that", "answer": ["she hadn't had time", "she had not had time"], "explanation": "didn't have ➔ hadn't had"},
            {"direct": "I can help you.", "prefix": "He said that", "answer": "he could help me", "explanation": "can ➔ could"},
            {"direct": "The meeting starts at nine.", "prefix": "She said that", "answer": "the meeting started at nine", "explanation": "starts ➔ started"},
            {"direct": "I have never seen this sunset.", "prefix": "He said that", "answer": "he had never seen that sunset", "explanation": "this ➔ that"},
            {"direct": "We don't have any milk.", "prefix": "They said that", "answer": ["they didn't have any milk", "they did not have any milk"], "explanation": "don't ➔ didn't"},
            {"direct": "I am going to buy shoes.", "prefix": "She said that", "answer": "she was going to buy shoes", "explanation": "am ➔ was"},
            {"direct": "I will send a postcard.", "prefix": "He said that", "answer": "he would send me a postcard", "explanation": "will ➔ would"},
            {"direct": "The car is being repaired.", "prefix": "She said that", "answer": "the car was being repaired", "explanation": "is ➔ was"},
            {"direct": "I have already seen this movie.", "prefix": "He said that", "answer": "he had already seen that movie", "explanation": "this ➔ that"},
            {"direct": "We played tennis.", "prefix": "They said that", "answer": "they had played tennis", "explanation": "played ➔ had played"},
            {"direct": "I am not happy with my job.", "prefix": "She said that", "answer": ["she was not happy with her job", "she wasn't happy with her job"], "explanation": "my ➔ her"},
            {"direct": "I will be home by seven.", "prefix": "He said that", "answer": "he would be home by seven", "explanation": "will ➔ would"},
            {"direct": "My computer is broken.", "prefix": "She said that", "answer": "her computer was broken", "explanation": "is ➔ was"},
            {"direct": "I have forgotten my password.", "prefix": "He said that", "answer": "he had forgotten his password", "explanation": "have forgotten ➔ had forgotten"},
            {"direct": "We are having a party.", "prefix": "They said that", "answer": "they were having a party", "explanation": "are having ➔ were having"},
            {"direct": "I don't understand.", "prefix": "She said that", "answer": ["she didn't understand", "she did not understand"], "explanation": "don't ➔ didn't"},
            {"direct": "I will pay.", "prefix": "He said that", "answer": "he would pay", "explanation": "will ➔ would"},
            {"direct": "The flight was delayed.", "prefix": "She said that", "answer": "the flight had been delayed", "explanation": "was ➔ had been"},
            {"direct": "I am learning to drive.", "prefix": "He said that", "answer": "he was learning to drive", "explanation": "am ➔ was"},
            {"direct": "We haven't seen our neighbours.", "prefix": "They said that", "answer": ["they hadn't seen their neighbours", "they had not seen their neighbours"], "explanation": "haven't ➔ hadn't"},
            {"direct": "I can't go out.", "prefix": "She said that", "answer": ["she couldn't go out", "she could not go out"], "explanation": "can't ➔ couldn't"},
            {"direct": "I will meet you.", "prefix": "He said that", "answer": "he would meet me", "explanation": "will ➔ would"},
            {"direct": "The music is too loud.", "prefix": "She said that", "answer": "the music was too loud", "explanation": "is ➔ was"},
            {"direct": "I have just received a letter.", "prefix": "He said that", "answer": "he had just received a letter", "explanation": "have received ➔ had received"},
            {"direct": "We are visiting grandparents.", "prefix": "They said that", "answer": "they were visiting their grandparents", "explanation": "are ➔ were"},
            {"direct": "I didn't like the ending.", "prefix": "She said that", "answer": ["she hadn't liked the ending", "she had not liked the ending"], "explanation": "didn't like ➔ hadn't liked"},
            {"direct": "I must go to the dentist.", "prefix": "He said that", "answer": "he had to go to the dentist", "explanation": "must ➔ had to"},
            {"direct": "We are playing hide and seek.", "prefix": "They said that", "answer": "they were playing hide and seek", "explanation": "are ➔ were"},
            {"direct": "I have been to Japan twice.", "prefix": "She said that", "answer": "she had been to Japan twice", "explanation": "have been ➔ had been"},
            {"direct": "I will do the washing up.", "prefix": "He said that", "answer": "he would do the washing up", "explanation": "will ➔ would"},
            {"direct": "The car belongs to my uncle.", "prefix": "She said that", "answer": "the car belonged to her uncle", "explanation": "belongs ➔ belonged"},
            {"direct": "I don't have any siblings.", "prefix": "He said that", "answer": ["he didn't have any siblings", "he did not have any siblings"], "explanation": "don't ➔ didn't"},
            {"direct": "We visited the museum.", "prefix": "They said that", "answer": "they had visited the museum", "explanation": "visited ➔ had visited"},
            {"direct": "I can play the flute.", "prefix": "She said that", "answer": "she could play the flute", "explanation": "can ➔ could"},
            {"direct": "I am looking for my glasses.", "prefix": "He said that", "answer": "he was looking for his glasses", "explanation": "am ➔ was"},
            {"direct": "I have just finished a marathon.", "prefix": "She said that", "answer": "she had just finished a marathon", "explanation": "have finished ➔ had finished"},
            {"direct": "My friend is moving.", "prefix": "He said that", "answer": "his friend was moving", "explanation": "my ➔ his"},
            {"direct": "We will be late.", "prefix": "They said that", "answer": "they would be late", "explanation": "will ➔ would"},
            {"direct": "I saw a famous actor.", "prefix": "She said that", "answer": "she had seen a famous actor", "explanation": "saw ➔ had seen"},
            {"direct": "I am not interested.", "prefix": "He said that", "answer": ["he was not interested", "he wasn't interested"], "explanation": "am ➔ was"},
            {"direct": "The flowers smell wonderful.", "prefix": "She said that", "answer": "the flowers smelled wonderful", "explanation": "smell ➔ smelled"},
            {"direct": "I have lost my appetite.", "prefix": "He said that", "answer": "he had lost his appetite", "explanation": "have lost ➔ had lost"},
            {"direct": "We are waiting for results.", "prefix": "They said that", "answer": "they were waiting for results", "explanation": "are ➔ were"},
            {"direct": "I didn't mean to hurt you.", "prefix": "She told me that", "answer": ["she hadn't meant to hurt me", "she had not meant to hurt me"], "explanation": "didn't mean ➔ hadn't meant"},
            {"direct": "It is getting dark.", "prefix": "He said that", "answer": "it was getting dark", "explanation": "is ➔ was"},
            {"direct": "I will buy you a present.", "prefix": "She said that", "answer": "she would buy me a present", "explanation": "will ➔ would"},
            {"direct": "I have a terrible headache.", "prefix": "He said that", "answer": "he had a terrible headache", "explanation": "have ➔ had"},
            {"direct": "The birds are singing.", "prefix": "She said that", "answer": "the birds were singing", "explanation": "are ➔ were"},
            {"direct": "I bought this dress.", "prefix": "She said that", "answer": "she had bought that dress", "explanation": "this ➔ that"},
            {"direct": "I can't remember his name.", "prefix": "He said that", "answer": ["he couldn't remember his name", "he could not remember his name"], "explanation": "can't ➔ couldn't"},
            {"direct": "We are going to the beach.", "prefix": "They said that", "answer": "they were going to the beach", "explanation": "are ➔ were"},
            {"direct": "I have already cleaned it.", "prefix": "He said that", "answer": "he had already cleaned it", "explanation": "have ➔ had"},
            {"direct": "I don't think it's a good idea.", "prefix": "She said that", "answer": ["she didn't think it was a good idea", "she did not think it was a good idea"], "explanation": "don't ➔ didn't"},
            {"direct": "I will lend you my umbrella.", "prefix": "He said that", "answer": "he would lend me his umbrella", "explanation": "will ➔ would"},
            {"direct": "The soup is too salty.", "prefix": "They said that", "answer": "the soup was too salty", "explanation": "is ➔ was"},
            {"direct": "I was sleeping when it rang.", "prefix": "She said that", "answer": "she had been sleeping when it rang", "explanation": "was sleeping ➔ had been sleeping"},
            {"direct": "I am writing a letter.", "prefix": "He said that", "answer": "he was writing a letter", "explanation": "am ➔ was"},
            {"direct": "My cousin lives in Australia.", "prefix": "She said that", "answer": "her cousin lived in Australia", "explanation": "lives ➔ lived"},
            {"direct": "We have spent all our money.", "prefix": "They said that", "answer": "they had spent all their money", "explanation": "have spent ➔ had spent"},
            {"direct": "I don't feel like going out.", "prefix": "He said that", "answer": ["he didn't feel like going out", "he did not feel like going out"], "explanation": "don't ➔ didn't"},
            {"direct": "I will fix the car.", "prefix": "She said that", "answer": "she would fix the car", "explanation": "will ➔ would"},
            {"direct": "The water is too cold.", "prefix": "He said that", "answer": "the water was too cold", "explanation": "is ➔ was"},
            {"direct": "I am having a great time.", "prefix": "She said that", "answer": "she was having a great time", "explanation": "am ➔ was"},
            {"direct": "We traveled last summer.", "prefix": "They said that", "answer": "they had traveled the summer before", "explanation": "traveled ➔ had traveled"},
            {"direct": "I haven't heard from him.", "prefix": "He said that", "answer": ["he hadn't heard from him", "he had not heard from him"], "explanation": "haven't ➔ hadn't"},
            {"direct": "I forgot to lock the door.", "prefix": "She said that", "answer": "she had forgotten to lock the door", "explanation": "forgot ➔ had forgotten"},
            {"direct": "The performance starts at 8.", "prefix": "He said that", "answer": "the performance started at 8", "explanation": "starts ➔ started"},
            {"direct": "I am not ready yet.", "prefix": "She said that", "answer": ["she was not ready yet", "she wasn't ready yet"], "explanation": "am ➔ was"},
            {"direct": "We will enjoy the show.", "prefix": "They said that", "answer": "they would enjoy the show", "explanation": "will ➔ would"},
            {"direct": "I made a mistake.", "prefix": "The student said that", "answer": "he had made a mistake", "explanation": "made ➔ had made"},
            {"direct": "I am working on a project.", "prefix": "He said that", "answer": "he was working on a project", "explanation": "am ➔ was"},
