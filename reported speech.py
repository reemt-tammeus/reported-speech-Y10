import streamlit as st
import random
import re

# --- KONFIGURATION ---
st.set_page_config(
    page_title="Reported Speech Pro Trainer", 
    page_icon="📝", 
    layout="centered"
)

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
            {"direct": "My parents are proud of me.", "prefix": "She said that", "answer": "her parents were proud of her", "explanation": "are ➔ were"},
            {"direct": "I have to finish this.", "prefix": "He said that", "answer": "he had to finish that", "explanation": "have to ➔ had to"},
            {"direct": "I won't forget your birthday.", "prefix": "She said that", "answer": ["she wouldn't forget my birthday", "she would not forget my birthday"], "explanation": "won't ➔ wouldn't"},
            {"direct": "The movie was very boring.", "prefix": "They said that", "answer": "the movie had been very boring", "explanation": "was ➔ had been"},
            {"direct": "I didn't understand the instructions.", "prefix": "He said that", "answer": ["he hadn't understood the instructions", "he had not understood the instructions"], "explanation": "didn't ➔ hadn't"}
        ],
        "Questions": [
            {"direct": "Where is the station?", "prefix": "He asked me", "answer": "where the station was", "explanation": "is ➔ was"},
            {"direct": "Do you like tea?", "prefix": "She asked him if", "answer": "he liked tea", "explanation": "do ➔ entfällt | like ➔ liked"},
            {"direct": "What are you doing?", "prefix": "They asked us", "answer": "what we were doing", "explanation": "are ➔ were"},
            {"direct": "Have you seen my keys?", "prefix": "He asked her if", "answer": "she had seen his keys", "explanation": "have ➔ had"},
            {"direct": "Can you swim?", "prefix": "She asked me if", "answer": "I could swim", "explanation": "can ➔ could"},
            {"direct": "Why did you call?", "prefix": "He asked me", "answer": "why I had called", "explanation": "did call ➔ had called"},
            {"direct": "Will it rain tomorrow?", "prefix": "She asked if", "answer": "it would rain the next day", "explanation": "will ➔ would"},
            {"direct": "Where have you been?", "prefix": "My mom asked me", "answer": "where I had been", "explanation": "have ➔ had"},
            {"direct": "Is he coming to the party?", "prefix": "She asked if", "answer": "he was coming to the party", "explanation": "is ➔ was"},
            {"direct": "How much does this cost?", "prefix": "He asked", "answer": "how much that cost", "explanation": "this ➔ that"},
            {"direct": "Do you live here?", "prefix": "She asked me if", "answer": "I lived there", "explanation": "here ➔ there"},
            {"direct": "When will the movie start?", "prefix": "He asked", "answer": "when the movie would start", "explanation": "will ➔ would"},
            {"direct": "What time is it?", "prefix": "She asked me", "answer": "what time it was", "explanation": "is ➔ was"},
            {"direct": "Are you busy?", "prefix": "He asked if", "answer": "I was busy", "explanation": "are ➔ was"},
            {"direct": "Where did you buy that car?", "prefix": "She asked him", "answer": "where he had bought that car", "explanation": "did ➔ had"},
            {"direct": "Can I help you?", "prefix": "The waiter asked if", "answer": "he could help me", "explanation": "can ➔ could"},
            {"direct": "Why are you crying?", "prefix": "He asked her", "answer": "why she was crying", "explanation": "are ➔ was"},
            {"direct": "Have you finished your homework?", "prefix": "The teacher asked if", "answer": "I had finished my homework", "explanation": "have ➔ had"},
            {"direct": "What do you want?", "prefix": "He asked me", "answer": "what I wanted", "explanation": "do ➔ entfällt"},
            {"direct": "Did you see the news?", "prefix": "She asked if", "answer": "I had seen the news", "explanation": "did ➔ had"},
            {"direct": "How often do you exercise?", "prefix": "He asked me", "answer": "how often I exercised", "explanation": "do ➔ entfällt"},
            {"direct": "Is there a bank nearby?", "prefix": "She asked", "answer": "if there was a bank nearby", "explanation": "is ➔ was"},
            {"direct": "What will happen next?", "prefix": "He asked", "answer": "what would happen next", "explanation": "will ➔ would"},
            {"direct": "Are they playing well?", "prefix": "She asked if", "answer": "they were playing well", "explanation": "are ➔ were"},
            {"direct": "Where can I park?", "prefix": "He asked", "answer": "where he could park", "explanation": "can ➔ could"},
            {"direct": "Do you have a pen?", "prefix": "She asked if", "answer": "I had a pen", "explanation": "do ➔ entfällt"},
            {"direct": "Why is the shop closed?", "prefix": "He asked", "answer": "why the shop was closed", "explanation": "is ➔ was"},
            {"direct": "How did you find me?", "prefix": "She asked him", "answer": "how he had found her", "explanation": "did ➔ had"},
            {"direct": "Will you be home late?", "prefix": "He asked if", "answer": "I would be home late", "explanation": "will ➔ would"},
            {"direct": "Are we lost?", "prefix": "She asked if", "answer": "they were lost", "explanation": "are ➔ were"},
            {"direct": "What is your name?", "prefix": "He asked me", "answer": "what my name was", "explanation": "is ➔ was"},
            {"direct": "Do you speak English?", "prefix": "She asked him if", "answer": "he spoke English", "explanation": "do ➔ entfällt"},
            {"direct": "How long have you lived here?", "prefix": "He asked", "answer": "how long I had lived there", "explanation": "here ➔ there"},
            {"direct": "Where are you going?", "prefix": "She asked me", "answer": "where I was going", "explanation": "are ➔ was"},
            {"direct": "Can we go now?", "prefix": "They asked if", "answer": "they could go then", "explanation": "now ➔ then"},
            {"direct": "What were you thinking?", "prefix": "He asked me", "answer": "what I had been thinking", "explanation": "were ➔ had been"},
            {"direct": "Is it cold outside?", "prefix": "She asked if", "answer": "it was cold outside", "explanation": "is ➔ was"},
            {"direct": "Did you enjoy the meal?", "prefix": "The host asked if", "answer": "we had enjoyed the meal", "explanation": "did ➔ had"},
            {"direct": "Why can't you come?", "prefix": "He asked me", "answer": ["why I couldn't come", "why I could not come"], "explanation": "can't ➔ couldn't"},
            {"direct": "Who told you that?", "prefix": "She asked", "answer": "who had told him that", "explanation": "told ➔ had told"},
            {"direct": "Are you coming with us?", "prefix": "He asked if", "answer": "I was coming with them", "explanation": "us ➔ them"},
            {"direct": "Where does she work?", "prefix": "He asked", "answer": "where she worked", "explanation": "does ➔ entfällt"},
            {"direct": "Have you ever been to Paris?", "prefix": "She asked if", "answer": "I had ever been to Paris", "explanation": "have ➔ had"},
            {"direct": "What did you say?", "prefix": "He asked me", "answer": "what I had said", "explanation": "did ➔ had"},
            {"direct": "Is your father at home?", "prefix": "She asked if", "answer": "my father was at home", "explanation": "is ➔ was"},
            {"direct": "How many books did you buy?", "prefix": "He asked", "answer": "how many books I had bought", "explanation": "did ➔ had"},
            {"direct": "Do you like chocolate?", "prefix": "She asked if", "answer": "I liked chocolate", "explanation": "do ➔ entfällt"},
            {"direct": "Will you marry me?", "prefix": "He asked her if", "answer": "she would marry him", "explanation": "will ➔ would"},
            {"direct": "What's wrong?", "prefix": "She asked", "answer": "what was wrong", "explanation": "is ➔ was"},
            {"direct": "Where did I leave my phone?", "prefix": "He asked himself", "answer": "where he had left his phone", "explanation": "did ➔ had"}
        ],
        "Orders and Requests": [
            {"direct": "Open the window!", "prefix": "He told me", "answer": "to open the window", "explanation": "Infinitiv mit 'to'"},
            {"direct": "Don't touch that!", "prefix": "She warned me", "answer": "not to touch that", "explanation": "Verneint: 'not to'"},
            {"direct": "Please sit down.", "prefix": "He asked us", "answer": "to sit down", "explanation": "to-Infinitiv"},
            {"direct": "Stop talking!", "prefix": "The teacher told them", "answer": "to stop talking", "explanation": "to-Infinitiv"},
            {"direct": "Clean your room!", "prefix": "His mother told him", "answer": "to clean his room", "explanation": "to-Infinitiv"},
            {"direct": "Don't be late!", "prefix": "She told me", "answer": "not to be late", "explanation": "not to"},
            {"direct": "Give me the book.", "prefix": "He asked me", "answer": "to give him the book", "explanation": "me ➔ him"},
            {"direct": "Hurry up!", "prefix": "She told us", "answer": "to hurry up", "explanation": "to-Infinitiv"},
            {"direct": "Please help me.", "prefix": "He asked her", "answer": "to help him", "explanation": "me ➔ him"},
            {"direct": "Don't smoke here.", "prefix": "The man told us", "answer": "not to smoke there", "explanation": "here ➔ there"},
            {"direct": "Wait for me!", "prefix": "She told him", "answer": "to wait for her", "explanation": "me ➔ her"},
            {"direct": "Listen carefully.", "prefix": "The speaker told them", "answer": "to listen carefully", "explanation": "to-Infinitiv"},
            {"direct": "Don't forget the milk.", "prefix": "She reminded me", "answer": "not to forget the milk", "explanation": "not to"},
            {"direct": "Eat your vegetables!", "prefix": "The father told him", "answer": "to eat his vegetables", "explanation": "to-Infinitiv"},
            {"direct": "Please call me later.", "prefix": "She asked me", "answer": "to call her later", "explanation": "me ➔ her"},
            {"direct": "Don't park here.", "prefix": "The officer told him", "answer": "not to park there", "explanation": "here ➔ there"},
            {"direct": "Show me your passport.", "prefix": "The official told her", "answer": "to show him her passport", "explanation": "me ➔ him"},
            {"direct": "Be quiet!", "prefix": "He told them", "answer": "to be quiet", "explanation": "to-Infinitiv"},
            {"direct": "Don't tell anyone.", "prefix": "She told me", "answer": "not to tell anyone", "explanation": "not to"},
            {"direct": "Turn off the lights.", "prefix": "He told us", "answer": "to turn off the lights", "explanation": "to-Infinitiv"},
            {"direct": "Please lend me money.", "prefix": "He asked his friend", "answer": "to lend him money", "explanation": "me ➔ him"},
            {"direct": "Don't drink the water.", "prefix": "They warned us", "answer": "not to drink the water", "explanation": "not to"},
            {"direct": "Fasten your seatbelts.", "prefix": "The pilot told them", "answer": "to fasten their seatbelts", "explanation": "your ➔ their"},
            {"direct": "Come here!", "prefix": "The boss told me", "answer": "to come there", "explanation": "here ➔ there"},
            {"direct": "Don't make a mess.", "prefix": "She told the kids", "answer": "not to make a mess", "explanation": "not to"},
            {"direct": "Take a deep breath.", "prefix": "The doctor told him", "answer": "to take a deep breath", "explanation": "to-Infinitiv"},
            {"direct": "Please send me the file.", "prefix": "She asked him", "answer": "to send her the file", "explanation": "me ➔ her"},
            {"direct": "Don't look back.", "prefix": "He told her", "answer": "not to look back", "explanation": "not to"},
            {"direct": "Put the gun down!", "prefix": "The police told him", "answer": "to put the gun down", "explanation": "to-Infinitiv"},
            {"direct": "Read the instructions.", "prefix": "She told me", "answer": "to read the instructions", "explanation": "to-Infinitiv"},
            {"direct": "Don't feed the animals.", "prefix": "The sign told us", "answer": "not to feed the animals", "explanation": "not to"},
            {"direct": "Follow me.", "prefix": "The guide told them", "answer": "to follow him", "explanation": "me ➔ him"},
            {"direct": "Please be patient.", "prefix": "She asked us", "answer": "to be patient", "explanation": "to-Infinitiv"},
            {"direct": "Don't worry so much.", "prefix": "He told me", "answer": "not to worry so much", "explanation": "not to"},
            {"direct": "Sign the document.", "prefix": "The lawyer told her", "answer": "to sign the document", "explanation": "to-Infinitiv"},
            {"direct": "Don't scream.", "prefix": "He told her", "answer": "not to scream", "explanation": "not to"},
            {"direct": "Buckle up!", "prefix": "The driver told them", "answer": "to buckle up", "explanation": "to-Infinitiv"},
            {"direct": "Don't open the door.", "prefix": "She told him", "answer": "not to open the door", "explanation": "not to"},
            {"direct": "Try again.", "prefix": "The coach told me", "answer": "to try again", "explanation": "to-Infinitiv"},
            {"direct": "Please hold the line.", "prefix": "The secretary asked him", "answer": "to hold the line", "explanation": "to-Infinitiv"},
            {"direct": "Don't use your phone.", "prefix": "The teacher told them", "answer": "not to use their phones", "explanation": "your ➔ their"},
            {"direct": "Go to bed!", "prefix": "The mother told him", "answer": "to go to bed", "explanation": "to-Infinitiv"},
            {"direct": "Don't jump!", "prefix": "They told him", "answer": "not to jump", "explanation": "not to"},
            {"direct": "Pass the salt, please.", "prefix": "He asked her", "answer": "to pass the salt", "explanation": "to-Infinitiv"},
            {"direct": "Don't cry.", "prefix": "She told me", "answer": "not to cry", "explanation": "not to"},
            {"direct": "Watch your step.", "prefix": "He told us", "answer": "to watch our step", "explanation": "to-Infinitiv"},
            {"direct": "Don't run.", "prefix": "The father told him", "answer": "not to run", "explanation": "not to"},
            {"direct": "Tell me the truth.", "prefix": "She told him", "answer": "to tell her the truth", "explanation": "me ➔ her"},
            {"direct": "Don't drive so fast.", "prefix": "She told him", "answer": "not to drive so fast", "explanation": "not to"},
            {"direct": "Please bring wine.", "prefix": "He asked them", "answer": "to bring wine", "explanation": "to-Infinitiv"}
        ],
        "Backshift": [
            {"direct": "I work in a bank.", "prefix": "Paul said that he", "suffix": "in a bank.", "answer": "worked", "explanation": "Backshift: Present Simple ➔ Past Simple"},
            {"direct": "We are watching a movie.", "prefix": "They said that they", "suffix": "a movie.", "answer": "were watching", "explanation": "Backshift: Pres. Progressive ➔ Past Progressive"},
            {"direct": "She lost her keys yesterday.", "prefix": "I said that she", "suffix": "her keys the day before.", "answer": ["had lost", "'d lost"], "explanation": "Backshift: Past Simple ➔ Past Perfect"},
            {"direct": "I have finished my homework.", "prefix": "Sarah told me that she", "suffix": "her homework.", "answer": ["had finished", "'d finished"], "explanation": "Backshift: Present Perfect ➔ Past Perfect"},
            {"direct": "I will help you with the bags.", "prefix": "He said that he", "suffix": "me with the bags.", "answer": ["would help", "'d help"], "explanation": "Backshift: Will-Future ➔ Would-Conditional"},
            {"direct": "I can swim very well.", "prefix": "Leo said that he", "suffix": "swim very well.", "answer": "could", "explanation": "Backshift: can ➔ could"},
            {"direct": "We must go home now.", "prefix": "They explained that they", "suffix": "go home then.", "answer": "had to", "explanation": "Backshift: must ➔ had to | now ➔ then"},
            {"direct": "I am writing an email.", "prefix": "Tim said that he", "suffix": "an email.", "answer": "was writing", "explanation": "Backshift: Pres. Progressive ➔ Past Progressive"},
            {"direct": "They live in Berlin.", "prefix": "She said that they", "suffix": "in Berlin.", "answer": "lived", "explanation": "Backshift: Present Simple ➔ Past Simple"},
            {"direct": "I bought a new car last week.", "prefix": "Marc said that he", "suffix": "a new car the week before.", "answer": ["had bought", "'d bought"], "explanation": "Backshift: Past Simple ➔ Past Perfect"},
            {"direct": "We have visited Italy twice.", "prefix": "They explained that they", "suffix": "Italy twice.", "answer": ["had visited", "'d visited"], "explanation": "Backshift: Present Perfect ➔ Past Perfect"},
            {"direct": "It will rain later.", "prefix": "The report said that it", "suffix": "rain later.", "answer": ["would rain", "'d rain"], "explanation": "Backshift: Will-Future ➔ Would-Conditional"},
            {"direct": "You may leave early.", "prefix": "The teacher said that I", "suffix": "leave early.", "answer": "might", "explanation": "Backshift: may ➔ might"},
            {"direct": "I don't like coffee.", "prefix": "Elena said that she", "suffix": "coffee.", "answer": ["did not like", "didn't like"], "explanation": "Backshift: Present Simple (neg) ➔ Past Simple"},
            {"direct": "We are listening to music.", "prefix": "The girls said that they", "suffix": "to music.", "answer": "were listening", "explanation": "Backshift: Pres. Progressive ➔ Past Progressive"},
            {"direct": "He didn't see the sign.", "prefix": "I said that he", "suffix": "the sign.", "answer": ["had not seen", "hadn't seen"], "explanation": "Backshift: Past Simple (neg) ➔ Past Perfect"},
            {"direct": "I have lost my passport.", "prefix": "The tourist told me that he", "suffix": "his passport.", "answer": ["had lost", "'d lost"], "explanation": "Backshift: Present Perfect ➔ Past Perfect"},
            {"direct": "I won't be late.", "prefix": "Julia promised that she", "suffix": "late.", "answer": ["would not be", "wouldn't be"], "explanation": "Backshift: Will-Future (neg) ➔ Would-Conditional"},
            {"direct": "I must study for the test.", "prefix": "Ben said that he", "suffix": "study for the test.", "answer": "had to", "explanation": "Backshift: must ➔ had to"},
            {"direct": "The train arrives at 8.", "prefix": "The clerk said that the train", "suffix": "at 8.", "answer": "arrived", "explanation": "Backshift: Present Simple ➔ Past Simple"},
            {"direct": "We are eating lunch.", "prefix": "They told us that they", "suffix": "lunch.", "answer": "were eating", "explanation": "Backshift: Pres. Progressive ➔ Past Progressive"},
            {"direct": "I went to the doctor yesterday.", "prefix": "Sam said that he", "suffix": "to the doctor the day before.", "answer": ["had gone", "'d gone"], "explanation": "Backshift: Past Simple ➔ Past Perfect"},
            {"direct": "I haven't seen that film yet.", "prefix": "Lisa said that she", "suffix": "that film yet.", "answer": ["had not seen", "hadn't seen"], "explanation": "Backshift: Present Perfect (neg) ➔ Past Perfect"},
            {"direct": "I will send you a postcard.", "prefix": "Clara promised that she", "suffix": "me a postcard.", "answer": ["would send", "'d send"], "explanation": "Backshift: Will-Future ➔ Would-Conditional"},
            {"direct": "I can't come to the party.", "prefix": "Tom said that he", "suffix": "come to the party.", "answer": ["could not", "couldn't"], "explanation": "Backshift: can't ➔ couldn't"},
            {"direct": "I play the guitar every day.", "prefix": "Anna said that she", "suffix": "the guitar every day.", "answer": "played", "explanation": "Backshift: Present Simple ➔ Past Simple"},
            {"direct": "We are making pizza.", "prefix": "The boys told us that they", "suffix": "pizza.", "answer": "were making", "explanation": "Backshift: Pres. Progressive ➔ Past Progressive"},
            {"direct": "They missed the bus.", "prefix": "I explained that they", "suffix": "the bus.", "answer": ["had missed", "'d missed"], "explanation": "Backshift: Past Simple ➔ Past Perfect"},
            {"direct": "I have never been to London.", "prefix": "Mike said that he", "suffix": "to London.", "answer": ["had never been", "'d never been"], "explanation": "Backshift: Present Perfect ➔ Past Perfect"},
            {"direct": "I will call you later.", "prefix": "My mom promised that she", "suffix": "me later.", "answer": ["would call", "'d call"], "explanation": "Backshift: Will-Future ➔ Would-Conditional"},
            {"direct": "I can speak three languages.", "prefix": "The student said that she", "suffix": "speak three languages.", "answer": "could", "explanation": "Backshift: can ➔ could"},
            {"direct": "You must wear a helmet.", "prefix": "The officer told him that he", "suffix": "wear a helmet.", "answer": "had to", "explanation": "Backshift: must ➔ had to"},
            {"direct": "The water is very cold.", "prefix": "The swimmer said that the water", "suffix": "very cold.", "answer": "was", "explanation": "Backshift: am/is/are ➔ was/were"},
            {"direct": "We are waiting for the taxi.", "prefix": "They said that they", "suffix": "for the taxi.", "answer": "were waiting", "explanation": "Backshift: Pres. Progressive ➔ Past Progressive"},
            {"direct": "I saw a famous actor yesterday.", "prefix": "Sophie told me that she", "suffix": "a famous actor the day before.", "answer": ["had seen", "'d seen"], "explanation": "Backshift: Past Simple ➔ Past Perfect"},
            {"direct": "He has already left the office.", "prefix": "The secretary said that he", "suffix": "the office.", "answer": ["had already left", "'d already left"], "explanation": "Backshift: Present Perfect ➔ Past Perfect"},
            {"direct": "We will win the match.", "prefix": "The coach was sure that they", "suffix": "the match.", "answer": ["would win", "'d win"], "explanation": "Backshift: Will-Future ➔ Would-Conditional"},
            {"direct": "You may use my laptop.", "prefix": "Dad said that I", "suffix": "use his laptop.", "answer": "might", "explanation": "Backshift: may ➔ might"},
            {"direct": "I don't know the answer.", "prefix": "The boy admitted that he", "suffix": "the answer.", "answer": ["did not know", "didn't know"], "explanation": "Backshift: Present Simple (neg) ➔ Past Simple"},
            {"direct": "They are playing football in the park.", "prefix": "Lucy said that they", "suffix": "football in the park.", "answer": "were playing", "explanation": "Backshift: Pres. Progressive ➔ Past Progressive"},
            {"direct": "I didn't go to the party.", "prefix": "Kevin said that he", "suffix": "to the party.", "answer": ["had not gone", "hadn't gone"], "explanation": "Backshift: Past Simple (neg) ➔ Past Perfect"},
            {"direct": "I have forgotten my umbrella.", "prefix": "The woman said that she", "suffix": "her umbrella.", "answer": ["had forgotten", "'d forgotten"], "explanation": "Backshift: Present Perfect ➔ Past Perfect"},
            {"direct": "I won't tell anyone your secret.", "prefix": "Emily promised that she", "suffix": "anyone my secret.", "answer": ["would not tell", "wouldn't tell"], "explanation": "Backshift: Will-Future (neg) ➔ Would-Conditional"},
            {"direct": "I must finish this report.", "prefix": "The manager explained that he", "suffix": "that report.", "answer": "had to finish", "explanation": "Backshift: must ➔ had to | this ➔ that"},
            {"direct": "We like our new house.", "prefix": "They said that they", "suffix": "their new house.", "answer": "liked", "explanation": "Backshift: Present Simple ➔ Past Simple"},
            {"direct": "It is snowing outside.", "prefix": "Grandpa said that it", "suffix": "outside.", "answer": "was snowing", "explanation": "Backshift: is snowing ➔ was snowing"},
            {"direct": "The plane landed an hour ago.", "prefix": "The pilot said that the plane", "suffix": "an hour before.", "answer": ["had landed", "'d landed"], "explanation": "Backshift: Past Simple ➔ Past Perfect | ago ➔ before"},
            {"direct": "I have cleaned the kitchen.", "prefix": "David told us that he", "suffix": "the kitchen.", "answer": ["had cleaned", "'d cleaned"], "explanation": "Backshift: Present Perfect ➔ Past Perfect"},
            {"direct": "I will bring some cake.", "prefix": "Maria said that she", "suffix": "some cake.", "answer": ["would bring", "'d bring"], "explanation": "Backshift: Will-Future ➔ Would-Conditional"},
            {"direct": "I can't find my glasses.", "prefix": "The old man complained that he", "suffix": "find his glasses.", "answer": ["could not", "couldn't"], "explanation": "Backshift: can't ➔ couldn't"}
        ]
    }

# --- LOGIK ---
def normalize(text):
    if not text: return ""
    text = text.lower().strip()
    # Typografische Apostrophe (iOS/Mac) korrigieren
    text = text.replace("’", "'").replace("´", "'").replace("`", "'")
    text = text.replace("whether", "if")
    text = re.sub(r'[.!?;]+$', '', text)
    return re.sub(r'\s+', ' ', text)

def evaluate_answer(user_val):
    q = st.session_state.current_pool[st.session_state.index]
    norm_user = normalize(user_val)
    norm_prefix = normalize(q['prefix'])
    
    # Prefix-Stripping (Falls der Nutzer den Satzanfang mit abtippt)
    if norm_user.startswith(norm_prefix):
        processed = norm_user[len(norm_prefix):].strip()
    else:
        processed = norm_user

    # Suffix-Stripping (Speziell für Backshift: Falls der Nutzer das Satzende mit abtippt)
    if 'suffix' in q and q['suffix']:
        norm_suffix = normalize(q['suffix'])
        if processed.endswith(norm_suffix):
            processed = processed[:-len(norm_suffix)].strip()

    # Double-That/If Correction
    prefix_words = norm_prefix.split()
    if prefix_words:
        last_word = prefix_words[-1]
        if processed.startswith(last_word + " "):
            processed = processed[len(last_word):].strip()

    answers = q['answer']
    if isinstance(answers, str): answers = [answers]
    
    if any(normalize(processed) == normalize(ans) for ans in answers):
        st.session_state.score += 1
        st.session_state.feedback = ("success", "✨ Richtig!")
    else:
        display_ans = answers[0]
        # Für Lückentexte geben wir den kompletten Lösungssatz als Extra-Hilfe aus
        if 'suffix' in q and q['suffix']:
            st.session_state.feedback = ("error", f"Falsch. Korrekt: **{display_ans}**\n\n*(Ganzer Satz: {q['prefix']} {display_ans} {q['suffix']})*")
        else:
            st.session_state.feedback = ("error", f"Falsch. Korrekt: **{q['prefix']} {display_ans}**")

def submit_answer():
    user_val = st.session_state.get("temp_input", "").strip()
    # Leere Eingaben mit Enter ignorieren wir hier (verhindert feststecken)
    if not user_val: return
    evaluate_answer(user_val)

def skip_question():
    # Wird vom Button aufgerufen, wenn man nicht weiterweiß
    evaluate_answer("[LEER]")

def next_question():
    st.session_state.index += 1
    st.session_state.feedback = None
    st.session_state.temp_input = ""
    if st.session_state.index >= len(st.session_state.current_pool):
        st.session_state.step = "result"

def start_exercise(category):
    data = get_data()
    st.session_state.last_category = category
    
    # Fairer Mix-Mode aus allen Pools gleichmäßig
    if category == "Mix":
        pool = []
        for cat in ["Statements", "Questions", "Orders and Requests", "Backshift"]:
            cat_pool = data[cat]
            pool.extend(random.sample(cat_pool, min(4, len(cat_pool))))
        random.shuffle(pool)
        st.session_state.current_pool = pool[:15]
    else:
        pool = data[category]
        st.session_state.current_pool = random.sample(pool, min(15, len(pool)))
        
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.step = "quiz"
    st.session_state.feedback = None

# --- APP START ---
if 'step' not in st.session_state: st.session_state.step = "menu"

st.title("🇬🇧 Reported Speech Trainer")

if st.session_state.step == "menu":
    st.subheader("Kategorie wählen:")
    
    # Backshift Button ganz oben und hervorgehoben
    if st.button("Backshift of Tenses", use_container_width=True, type="primary"): 
        start_exercise("Backshift")
        
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Statements", use_container_width=True): start_exercise("Statements")
        if st.button("Questions", use_container_width=True): start_exercise("Questions")
    with col2:
        if st.button("Orders / Requests", use_container_width=True): start_exercise("Orders and Requests")
        if st.button("Mix Mode", use_container_width=True): start_exercise("Mix")

elif st.session_state.step == "quiz":
    q = st.session_state.current_pool[st.session_state.index]
    total_q = len(st.session_state.current_pool)
    
    st.progress(st.session_state.index / total_q)
    st.write(f"**Satz {st.session_state.index + 1} / {total_q}**")
    
    # Visuelles Bereinigen von abschließenden Kommas
    clean_direct = q['direct'].rstrip(', ')
    st.info(f"Direkt: **\"{clean_direct}\"**")
    
    # Eingabefeld deaktivieren, wenn Feedback da ist, um Double-Callbacks zu verhindern
    input_disabled = st.session_state.feedback is not None
    
    # UX Check für Lückentext (Backshift) vs Normal
    if 'suffix' in q:
        # Lückentext Darstellung
        st.markdown(f"📝 *{q['prefix']}* `______` *{q['suffix']}*")
        input_label = "Trage die fehlende Verbform ein:"
        placeholder = "z.B. had gone"
    else:
        # Normale Darstellung
        input_label = f"{q['prefix']} ..."
        placeholder = "Antwort eingeben & Enter..."
    
    st.text_input(
        input_label, 
        key="temp_input", 
        on_change=submit_answer,
        placeholder=placeholder,
        disabled=input_disabled
    )
    
    # Der verlässliche Überspringen-Button
    if not st.session_state.feedback:
        st.button("Ich weiß es nicht / Lösung zeigen", on_click=skip_question)
    
    # Feedback & Weiter-Button
    if st.session_state.feedback:
        t, m = st.session_state.feedback
        if t == "success": st.success(m)
        else:
            st.error(m)
            st.warning(f"💡 Tipp: {q['explanation']}")
        st.button("Weiter", on_click=next_question, type="primary")

elif st.session_state.step == "result":
    total_q = len(st.session_state.current_pool)
    st.balloons()
    st.header("Ergebnis")
    st.metric("Punkte", f"{st.session_state.score} / {total_q}")
    if st.button("Nochmal", use_container_width=True): start_exercise(st.session_state.last_category)
    if st.button("Menü", use_container_width=True): st.session_state.step = "menu"
