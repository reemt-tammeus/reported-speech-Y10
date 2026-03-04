import streamlit as st
import random
import re

# --- KONFIGURATION ---
st.set_page_config(
    page_title="Reported Speech Pro Trainer", 
    page_icon="schullogo.png", 
    layout="centered"
)

# 1. OPTIMIERUNG: Caching & Vollständigkeit
@st.cache_data
def get_data():
    """Vollständiger Datensatz: 150 Statements, 50 Questions, 50 Orders."""
    return {
        "Statements": [
            {"direct": "I am hungry.", "prefix": "He said that", "answer": "he was hungry", "explanation": "Pronomen: I ➔ he | Zeit: am ➔ was"},
            {"direct": "We are watching a movie.", "prefix": "They said that", "answer": "they were watching a movie", "explanation": "Pronomen: We ➔ they | Zeit: are watching ➔ were watching"},
            {"direct": "I have finished my project.", "prefix": "She said that", "answer": "she had finished her project", "explanation": "my ➔ her | have finished ➔ had finished"},
            {"direct": "I will call you tomorrow.", "prefix": "He said that", "answer": ["he would call me the next day", "he would call me the following day"], "explanation": "will ➔ would | tomorrow ➔ the next day"},
            {"direct": "The sun rises in the east.", "prefix": "The teacher said that", "answer": "the sun rose in the east", "explanation": "rises ➔ rose (Backshift)"},
            {"direct": "I don't like coffee.", "prefix": "She said that", "answer": "she didn't like coffee", "explanation": "don't ➔ didn't"},
            {"direct": "We went to Paris last year.", "prefix": "They said that", "answer": ["they had gone to Paris the year before", "they had gone to Paris the previous year"], "explanation": "went ➔ had gone | last year ➔ the year before"},
            {"direct": "I can speak three languages.", "prefix": "He said that", "answer": "he could speak three languages", "explanation": "can ➔ could"},
            {"direct": "I am playing the guitar.", "prefix": "She said that", "answer": "she was playing the guitar", "explanation": "am playing ➔ was playing"},
            {"direct": "I have never been to London.", "prefix": "He said that", "answer": "he had never been to London", "explanation": "have been ➔ had been"},
            {"direct": "My brother is ill.", "prefix": "She said that", "answer": "her brother was ill", "explanation": "My ➔ her | is ➔ was"},
            {"direct": "We will help you with the bags.", "prefix": "They said that", "answer": "they would help me with the bags", "explanation": "We ➔ they | will ➔ would"},
            {"direct": "I saw a ghost.", "prefix": "The boy said that", "answer": "he had seen a ghost", "explanation": "saw ➔ had seen"},
            {"direct": "I am not coming to the party.", "prefix": "He said that", "answer": "he was not coming to the party", "explanation": "am not ➔ was not"},
            {"direct": "The train leaves at five.", "prefix": "She said that", "answer": "the train left at five", "explanation": "leaves ➔ left"},
            {"direct": "I have lost my phone.", "prefix": "He said that", "answer": "he had lost his phone", "explanation": "my ➔ his | have lost ➔ had lost"},
            {"direct": "We are very happy here.", "prefix": "They said that", "answer": "they were very happy there", "explanation": "here ➔ there | are ➔ were"},
            {"direct": "I didn't do it.", "prefix": "She said that", "answer": "she hadn't done it", "explanation": "didn't do ➔ hadn't done"},
            {"direct": "It is raining outside.", "prefix": "He said that", "answer": "it was raining outside", "explanation": "is ➔ was"},
            {"direct": "I will be there on time.", "prefix": "She said that", "answer": "she would be there on time", "explanation": "will ➔ would"},
            {"direct": "I have a new car.", "prefix": "He said that", "answer": "he had a new car", "explanation": "have ➔ had"},
            {"direct": "The children are sleeping.", "prefix": "She said that", "answer": "the children were sleeping", "explanation": "are ➔ were"},
            {"direct": "I went shopping yesterday.", "prefix": "He said that", "answer": ["he had gone shopping the day before", "he had gone shopping the previous day"], "explanation": "went ➔ had gone | yesterday ➔ the day before"},
            {"direct": "I can't find my keys.", "prefix": "She said that", "answer": "she couldn't find her keys", "explanation": "can't ➔ couldn't"},
            {"direct": "We are going on holiday.", "prefix": "They said that", "answer": "they were going on holiday", "explanation": "are ➔ were"},
            {"direct": "I have already eaten.", "prefix": "He said that", "answer": "he had already eaten", "explanation": "have ➔ had"},
            {"direct": "I don't know the answer.", "prefix": "She said that", "answer": "she didn't know the answer", "explanation": "don't ➔ didn't"},
            {"direct": "I will buy a new house.", "prefix": "He said that", "answer": "he would buy a new house", "explanation": "will ➔ would"},
            {"direct": "The pizza is delicious.", "prefix": "They said that", "answer": "the pizza was delicious", "explanation": "is ➔ was"},
            {"direct": "I was at home all night.", "prefix": "She said that", "answer": "she had been at home all night", "explanation": "was ➔ had been"},
            {"direct": "I am learning Spanish.", "prefix": "He said that", "answer": "he was learning Spanish", "explanation": "am learning ➔ was learning"},
            {"direct": "My father works in a bank.", "prefix": "She said that", "answer": "her father worked in a bank", "explanation": "works ➔ worked"},
            {"direct": "We have seen this film before.", "prefix": "They said that", "answer": "they had seen that film before", "explanation": "have seen ➔ had seen | this ➔ that"},
            {"direct": "I don't have enough money.", "prefix": "He said that", "answer": "he didn't have enough money", "explanation": "don't ➔ didn't"},
            {"direct": "I will send the email now.", "prefix": "She said that", "answer": ["she would send the email then", "she would send the email at that time"], "explanation": "will ➔ would | now ➔ then"},
            {"direct": "The museum is closed.", "prefix": "He said that", "answer": "the museum was closed", "explanation": "is ➔ was"},
            {"direct": "I am meeting a friend.", "prefix": "She said that", "answer": "she was meeting a friend", "explanation": "am meeting ➔ was meeting"},
            {"direct": "We lived in Berlin for five years.", "prefix": "They said that", "answer": "they had lived in Berlin for five years", "explanation": "lived ➔ had lived"},
            {"direct": "I haven't seen her for ages.", "prefix": "He said that", "answer": "he hadn't seen her for ages", "explanation": "haven't ➔ hadn't"},
            {"direct": "I forgot my umbrella.", "prefix": "She said that", "answer": "she had forgotten her umbrella", "explanation": "forgot ➔ had forgotten"},
            {"direct": "The cake tastes great.", "prefix": "He said that", "answer": "the cake tasted great", "explanation": "tastes ➔ tasted"},
            {"direct": "I am not afraid of spiders.", "prefix": "She said that", "answer": "she was not afraid of spiders", "explanation": "am ➔ was"},
            {"direct": "We will win the match.", "prefix": "They said that", "answer": "they would win the match", "explanation": "will ➔ would"},
            {"direct": "I broke the vase.", "prefix": "The girl said that", "answer": "she had broken the vase", "explanation": "broke ➔ had broken"},
            {"direct": "I am feeling better today.", "prefix": "He said that", "answer": ["he was feeling better that day", "he was feeling better today"], "explanation": "am feeling ➔ was feeling | today ➔ that day"},
            {"direct": "My parents are coming over.", "prefix": "She said that", "answer": "her parents were coming over", "explanation": "My ➔ her"},
            {"direct": "I have to go now.", "prefix": "He said that", "answer": "he had to go then", "explanation": "have to ➔ had to | now ➔ then"},
            {"direct": "I won't tell anyone.", "prefix": "She said that", "answer": "she wouldn't tell anyone", "explanation": "won't ➔ wouldn't"},
            {"direct": "The weather is beautiful.", "prefix": "They said that", "answer": "the weather was beautiful", "explanation": "is ➔ was"},
            {"direct": "I didn't see the accident.", "prefix": "He said that", "answer": "he hadn't seen the accident", "explanation": "didn't see ➔ hadn't seen"},
            {"direct": "I am waiting for the bus.", "prefix": "He said that", "answer": "he was waiting for the bus", "explanation": "am ➔ was"},
            {"direct": "We have lived here for ten years.", "prefix": "They said that", "answer": "they had lived there for ten years", "explanation": "here ➔ there | have lived ➔ had lived"},
            {"direct": "I will do my best.", "prefix": "She said that", "answer": "she would do her best", "explanation": "will ➔ would | my ➔ her"},
            {"direct": "I didn't see you at the party.", "prefix": "He told me that", "answer": "he hadn't seen me at the party", "explanation": "didn't ➔ hadn't seen | you ➔ me"},
            {"direct": "The water is boiling.", "prefix": "She said that", "answer": "the water was boiling", "explanation": "is ➔ was"},
            {"direct": "I have already finished my breakfast.", "prefix": "He said that", "answer": "he had already finished his breakfast", "explanation": "my ➔ his"},
            {"direct": "We are going to the cinema tonight.", "prefix": "They said that", "answer": "they were going to the cinema that night", "explanation": "tonight ➔ that night"},
            {"direct": "I can't swim very well.", "prefix": "She said that", "answer": "she couldn't swim very well", "explanation": "can't ➔ couldn't"},
            {"direct": "I found a wallet on the street.", "prefix": "He said that", "answer": "he had found a wallet on the street", "explanation": "found ➔ had found"},
            {"direct": "My sister is a doctor.", "prefix": "She said that", "answer": "her sister was a doctor", "explanation": "is ➔ was"},
            {"direct": "I will bring the book back tomorrow.", "prefix": "He said that", "answer": ["he would bring the book back the next day", "he would bring the book back the following day"], "explanation": "tomorrow ➔ the next day"},
            {"direct": "The shops are closed on Sundays.", "prefix": "She said that", "answer": "the shops were closed on Sundays", "explanation": "are ➔ were"},
            {"direct": "I am reading a very good book.", "prefix": "He said that", "answer": "he was reading a very good book", "explanation": "am reading ➔ was reading"},
            {"direct": "We haven't been to the zoo yet.", "prefix": "They said that", "answer": "they hadn't been to the zoo yet", "explanation": "haven't ➔ hadn't"},
            {"direct": "I don't like spicy food.", "prefix": "She said that", "answer": "she didn't like spicy food", "explanation": "don't ➔ didn't"},
            {"direct": "I will call you as soon as I arrive.", "prefix": "He said that", "answer": "he would call me as soon as he arrived", "explanation": "will ➔ would | arrive ➔ arrived"},
            {"direct": "The dog is barking at the cat.", "prefix": "She said that", "answer": "the dog was barking at the cat", "explanation": "is ➔ was"},
            {"direct": "I have lost my passport.", "prefix": "He said that", "answer": "he had lost his passport", "explanation": "my ➔ his"},
            {"direct": "We saw a great play last night.", "prefix": "They said that", "answer": ["they had seen a great play the night before", "they had seen a great play the previous night"], "explanation": "last night ➔ the night before"},
            {"direct": "I am not feeling very well.", "prefix": "She said that", "answer": "she was not feeling very well", "explanation": "am ➔ was"},
            {"direct": "I will make a cake for your birthday.", "prefix": "He said that", "answer": "he would make a cake for my birthday", "explanation": "your ➔ my"},
            {"direct": "My parents are on holiday.", "prefix": "She said that", "answer": "her parents were on holiday", "explanation": "My ➔ her"},
            {"direct": "I have been working hard all day.", "prefix": "He said that", "answer": "he had been working hard all day", "explanation": "have been working ➔ had been working"},
            {"direct": "We are moving to a new house.", "prefix": "They said that", "answer": "they were moving to a new house", "explanation": "are ➔ were"},
            {"direct": "I didn't have time to do my hair.", "prefix": "She said that", "answer": "she hadn't had time to do her hair", "explanation": "didn't ➔ hadn't had"},
            {"direct": "I can help you with your homework.", "prefix": "He said that", "answer": "he could help me with my homework", "explanation": "you ➔ me | your ➔ my"},
            {"direct": "The meeting starts at nine o'clock.", "prefix": "She said that", "answer": "the meeting started at nine o'clock", "explanation": "starts ➔ started"},
            {"direct": "I have never seen such a beautiful sunset.", "prefix": "He said that", "answer": "he had never seen such a beautiful sunset", "explanation": "have seen ➔ had seen"},
            {"direct": "We don't have any milk left.", "prefix": "They said that", "answer": "they didn't have any milk left", "explanation": "don't ➔ didn't"},
            {"direct": "I am going to buy some new shoes.", "prefix": "She said that", "answer": "she was going to buy some new shoes", "explanation": "am going ➔ was going"},
            {"direct": "I will send you a postcard from Rome.", "prefix": "He said that", "answer": "he would send me a postcard from Rome", "explanation": "you ➔ me"},
            {"direct": "The car is being repaired.", "prefix": "She said that", "answer": "the car was being repaired", "explanation": "is being ➔ was being"},
            {"direct": "I have already seen this movie twice.", "prefix": "He said that", "answer": "he had already seen that movie twice", "explanation": "this ➔ that"},
            {"direct": "We played tennis for two hours.", "prefix": "They said that", "answer": "they had played tennis for two hours", "explanation": "played ➔ had played"},
            {"direct": "I am not happy with my new job.", "prefix": "She said that", "answer": "she was not happy with her new job", "explanation": "my ➔ her"},
            {"direct": "I will be home by seven.", "prefix": "He said that", "answer": "he would be home by seven", "explanation": "will ➔ would"},
            {"direct": "My computer is broken.", "prefix": "She said that", "answer": "her computer was broken", "explanation": "My ➔ her"},
            {"direct": "I have forgotten my password again.", "prefix": "He said that", "answer": "he had forgotten his password again", "explanation": "my ➔ his"},
            {"direct": "We are having a party next Saturday.", "prefix": "They said that", "answer": ["they were having a party the following Saturday", "they were having a party the next Saturday"], "explanation": "next Saturday ➔ following Saturday"},
            {"direct": "I don't understand the question.", "prefix": "She said that", "answer": "she didn't understand the question", "explanation": "don't ➔ didn't"},
            {"direct": "I will pay for the drinks.", "prefix": "He said that", "answer": "he would pay for the drinks", "explanation": "will ➔ would"},
            {"direct": "The flight was delayed by two hours.", "prefix": "She said that", "answer": "the flight had been delayed by two hours", "explanation": "was ➔ had been"},
            {"direct": "I am learning how to drive.", "prefix": "He said that", "answer": "he was learning how to drive", "explanation": "am ➔ was"},
            {"direct": "We haven't seen our neighbours for weeks.", "prefix": "They said that", "answer": "they hadn't seen their neighbours for weeks", "explanation": "haven't ➔ hadn't"},
            {"direct": "I can't go out because I have a cold.", "prefix": "She said that", "answer": "she couldn't go out because she had a cold", "explanation": "can't ➔ couldn't"},
            {"direct": "I will meet you at the station.", "prefix": "He said that", "answer": "he would meet me at the station", "explanation": "you ➔ me"},
            {"direct": "The music is too loud.", "prefix": "She said that", "answer": "the music was too loud", "explanation": "is ➔ was"},
            {"direct": "I have just received a letter from my penfriend.", "prefix": "He said that", "answer": "he had just received a letter from his penfriend", "explanation": "my ➔ his"},
            {"direct": "We are going to visit our grandparents.", "prefix": "They said that", "answer": "they were going to visit their grandparents", "explanation": "our ➔ their"},
            {"direct": "I didn't like the ending of the book.", "prefix": "She said that", "answer": "she hadn't liked the ending of the book", "explanation": "didn't ➔ hadn't liked"},
            {"direct": "I must go to the dentist.", "prefix": "He said that", "answer": "he had to go to the dentist", "explanation": "must ➔ had to"},
            {"direct": "We are playing hide and seek.", "prefix": "They said that", "answer": "they were playing hide and seek", "explanation": "are ➔ were"},
            {"direct": "I have been to Japan twice.", "prefix": "She said that", "answer": "she had been to Japan twice", "explanation": "have been ➔ had been"},
            {"direct": "I will do the washing up later.", "prefix": "He said that", "answer": "he would do the washing up later", "explanation": "will ➔ would"},
            {"direct": "The car belongs to my uncle.", "prefix": "She said that", "answer": "the car belonged to her uncle", "explanation": "my ➔ her"},
            {"direct": "I don't have any brothers or sisters.", "prefix": "He said that", "answer": "he didn't have any brothers or sisters", "explanation": "don't ➔ didn't"},
            {"direct": "We visited the museum two days ago.", "prefix": "They said that", "answer": ["they had visited the museum two days before", "they had visited the museum two days earlier"], "explanation": "ago ➔ before"},
            {"direct": "I can play the flute.", "prefix": "She said that", "answer": "she could play the flute", "explanation": "can ➔ could"},
            {"direct": "I am looking for my glasses.", "prefix": "He said that", "answer": "he was looking for his glasses", "explanation": "my ➔ his"},
            {"direct": "I have just finished a marathon.", "prefix": "She said that", "answer": "she had just finished a marathon", "explanation": "have ➔ had"},
            {"direct": "My friend is moving to New York.", "prefix": "He said that", "answer": "his friend was moving to New York", "explanation": "My ➔ his"},
            {"direct": "We will be late for the concert.", "prefix": "They said that", "answer": "they would be late for the concert", "explanation": "will ➔ would"},
            {"direct": "I saw a famous actor in the park.", "prefix": "She said that", "answer": "she had seen a famous actor in the park", "explanation": "saw ➔ had seen"},
            {"direct": "I am not interested in politics.", "prefix": "He said that", "answer": "he was not interested in politics", "explanation": "am ➔ was"},
            {"direct": "The flowers smell wonderful.", "prefix": "She said that", "answer": "the flowers smelled wonderful", "explanation": "smell ➔ smelled"},
            {"direct": "I have lost my appetite.", "prefix": "He said that", "answer": "he had lost his appetite", "explanation": "my ➔ his"},
            {"direct": "We are waiting for the results.", "prefix": "They said that", "answer": "they were waiting for the results", "explanation": "are ➔ were"},
            {"direct": "I didn't mean to hurt your feelings.", "prefix": "She told me that", "answer": "she hadn't meant to hurt my feelings", "explanation": "your ➔ my"},
            {"direct": "It is getting dark.", "prefix": "He said that", "answer": "it was getting dark", "explanation": "is ➔ was"},
            {"direct": "I will buy you a present.", "prefix": "She said that", "answer": "she would buy me a present", "explanation": "you ➔ me"},
            {"direct": "I have a terrible headache.", "prefix": "He said that", "answer": "he had a terrible headache", "explanation": "have ➔ had"},
            {"direct": "The birds are singing.", "prefix": "She said that", "answer": "the birds were singing", "explanation": "are ➔ were"},
            {"direct": "I bought this dress in London.", "prefix": "She said that", "answer": ["she had bought that dress in London", "she had bought this dress in London"], "explanation": "this ➔ that"},
            {"direct": "I can't remember his name.", "prefix": "He said that", "answer": "he couldn't remember his name", "explanation": "can't ➔ couldn't"},
            {"direct": "We are going to the beach tomorrow.", "prefix": "They said that", "answer": ["they were going to the beach the next day", "they were going to the beach the following day"], "explanation": "tomorrow ➔ the next day"},
            {"direct": "I have already cleaned the kitchen.", "prefix": "He said that", "answer": "he had already cleaned the kitchen", "explanation": "have ➔ had"},
            {"direct": "I don't think it's a good idea.", "prefix": "She said that", "answer": "she didn't think it was a good idea", "explanation": "don't ➔ didn't"},
            {"direct": "I will lend you my umbrella.", "prefix": "He said that", "answer": "he would lend me his umbrella", "explanation": "you ➔ me | my ➔ his"},
            {"direct": "The soup is too salty.", "prefix": "They said that", "answer": "the soup was too salty", "explanation": "is ➔ was"},
            {"direct": "I was sleeping when the phone rang.", "prefix": "She said that", "answer": "she had been sleeping when the phone rang", "explanation": "was sleeping ➔ had been sleeping"},
            {"direct": "I am writing a letter to my grandmother.", "prefix": "He said that", "answer": "he was writing a letter to his grandmother", "explanation": "my ➔ his"},
            {"direct": "My cousin lives in Australia.", "prefix": "She said that", "answer": "her cousin lived in Australia", "explanation": "My ➔ her"},
            {"direct": "We have spent all our money.", "prefix": "They said that", "answer": "they had spent all their money", "explanation": "our ➔ their"},
            {"direct": "I don't feel like going out.", "prefix": "He said that", "answer": "he didn't feel like going out", "explanation": "don't ➔ didn't"},
            {"direct": "I will fix the car next week.", "prefix": "She said that", "answer": ["she would fix the car the following week", "she would fix the car the next week"], "explanation": "next week ➔ following week"},
            {"direct": "The water is too cold for swimming.", "prefix": "He said that", "answer": "the water was too cold for swimming", "explanation": "is ➔ was"},
            {"direct": "I am having a great time.", "prefix": "She said that", "answer": "she was having a great time", "explanation": "am ➔ was"},
            {"direct": "We traveled around Europe last summer.", "prefix": "They said that", "answer": ["they had traveled around Europe the summer before", "they had traveled around Europe the previous summer"], "explanation": "last summer ➔ the summer before"},
            {"direct": "I haven't heard from him lately.", "prefix": "He said that", "answer": "he hadn't heard from him lately", "explanation": "haven't ➔ hadn't"},
            {"direct": "I forgot to lock the door.", "prefix": "She said that", "answer": "she had forgotten to lock the door", "explanation": "forgot ➔ had forgotten"},
            {"direct": "The performance starts at 8 PM.", "prefix": "He said that", "answer": "the performance started at 8 PM", "explanation": "starts ➔ started"},
            {"direct": "I am not ready yet.", "prefix": "She said that", "answer": "she was not ready yet", "explanation": "am ➔ was"},
            {"direct": "We will enjoy the show.", "prefix": "They said that", "answer": "they would enjoy the show", "explanation": "will ➔ would"},
            {"direct": "I made a mistake.", "prefix": "The student said that", "answer": "he had made a mistake", "explanation": "made ➔ had made"},
            {"direct": "I am working on a new project.", "prefix": "He said that", "answer": "he was working on a new project", "explanation": "am ➔ was"},
            {"direct": "My parents are proud of me.", "prefix": "She said that", "answer": "her parents were proud of her", "explanation": "me ➔ her"},
            {"direct": "I have to finish this by noon.", "prefix": "He said that", "answer": ["he had to finish that by noon", "he had to finish this by noon"], "explanation": "this ➔ that"},
            {"direct": "I won't forget your birthday.", "prefix": "She said that", "answer": "she wouldn't forget my birthday", "explanation": "your ➔ my"},
            {"direct": "The movie was very boring.", "prefix": "They said that", "answer": "the movie had been very boring", "explanation": "was ➔ had been"},
            {"direct": "I didn't understand the instructions.", "prefix": "He said that", "answer": "he hadn't understood the instructions", "explanation": "didn't ➔ hadn't"}
        ],
        "Questions": [
            {"direct": "Where is the station?", "prefix": "He asked me", "answer": "where the station was", "explanation": "Wortstellung: Subjekt vor Verb."},
            {"direct": "Do you like tea?", "prefix": "She asked him if", "answer": "he liked tea", "explanation": "Einleitung mit if/whether."},
            {"direct": "What are you doing?", "prefix": "They asked us", "answer": "what we were doing", "explanation": "Zeit: are ➔ were."},
            {"direct": "Have you seen my keys?", "prefix": "He asked her if", "answer": "she had seen his keys", "explanation": "Zeit: have ➔ had."},
            {"direct": "Can you swim?", "prefix": "She asked me if", "answer": "I could swim", "explanation": "can ➔ could."},
            {"direct": "Why did you call?", "prefix": "He asked me", "answer": "why I had called", "explanation": "Zeit: did call ➔ had called."},
            {"direct": "Will it rain tomorrow?", "prefix": "She asked if", "answer": ["it would rain the next day", "it would rain the following day"], "explanation": "tomorrow ➔ the next day."},
            {"direct": "Where have you been?", "prefix": "My mom asked me", "answer": "where I had been", "explanation": "have ➔ had."},
            {"direct": "Is he coming to the party?", "prefix": "She asked if", "answer": "he was coming to the party", "explanation": "is ➔ was."},
            {"direct": "How much does this cost?", "prefix": "He asked", "answer": "how much that cost", "explanation": "this ➔ that."},
            {"direct": "Do you live here?", "prefix": "She asked me if", "answer": "I lived there", "explanation": "here ➔ there."},
            {"direct": "When will the movie start?", "prefix": "He asked", "answer": "when the movie would start", "explanation": "will ➔ would."},
            {"direct": "What time is it?", "prefix": "She asked me", "answer": "what time it was", "explanation": "Subjekt am Ende."},
            {"direct": "Are you busy?", "prefix": "He asked if", "answer": "I was busy", "explanation": "are ➔ was."},
            {"direct": "Where did you buy that car?", "prefix": "She asked him", "answer": "where he had bought that car", "explanation": "did ➔ had."},
            {"direct": "Can I help you?", "prefix": "The waiter asked if", "answer": "he could help me", "explanation": "you ➔ me."},
            {"direct": "Why are you crying?", "prefix": "He asked her", "answer": "why she was crying", "explanation": "are ➔ were."},
            {"direct": "Have you finished your homework?", "prefix": "The teacher asked if", "answer": "I had finished my homework", "explanation": "have ➔ had."},
            {"direct": "What do you want?", "prefix": "He asked me", "answer": "what I wanted", "explanation": "want ➔ wanted."},
            {"direct": "Did you see the news?", "prefix": "She asked if", "answer": "I had seen the news", "explanation": "did ➔ had seen."},
            {"direct": "How often do you exercise?", "prefix": "He asked me", "answer": "how often I exercised", "explanation": "exercise ➔ exercised."},
            {"direct": "Is there a bank nearby?", "prefix": "She asked", "answer": "if there was a bank nearby", "explanation": "is ➔ was."},
            {"direct": "What will happen next?", "prefix": "He asked", "answer": "what would happen next", "explanation": "will ➔ would."},
            {"direct": "Are they playing well?", "prefix": "She asked if", "answer": "they were playing well", "explanation": "are ➔ were."},
            {"direct": "Where can I park?", "prefix": "He asked", "answer": "where he could park", "explanation": "can ➔ could."},
            {"direct": "Do you have a pen?", "prefix": "She asked if", "answer": "I had a pen", "explanation": "have ➔ had."},
            {"direct": "Why is the shop closed?", "prefix": "He asked", "answer": "why the shop was closed", "explanation": "is ➔ was."},
            {"direct": "How did you find me?", "prefix": "She asked him", "answer": "how he had found her", "explanation": "me ➔ her."},
            {"direct": "Will you be home late?", "prefix": "He asked if", "answer": "I would be home late", "explanation": "will ➔ would."},
            {"direct": "Are we lost?", "prefix": "She asked if", "answer": "they were lost", "explanation": "we ➔ they."},
            {"direct": "What is your name?", "prefix": "He asked me", "answer": "what my name was", "explanation": "is ➔ was."},
            {"direct": "Do you speak English?", "prefix": "She asked him if", "answer": "he spoke English", "explanation": "speak ➔ spoke."},
            {"direct": "How long have you lived here?", "prefix": "He asked", "answer": "how long I had lived there", "explanation": "here ➔ there."},
            {"direct": "Where are you going for vacation?", "prefix": "She asked me", "answer": "where I was going for vacation", "explanation": "are ➔ was."},
            {"direct": "Can we go now?", "prefix": "They asked if", "answer": ["they could go then", "they could go at that time"], "explanation": "now ➔ then."},
            {"direct": "What were you thinking?", "prefix": "He asked me", "answer": "what I had been thinking", "explanation": "were ➔ had been."},
            {"direct": "Is it cold outside?", "prefix": "She asked if", "answer": "it was cold outside", "explanation": "is ➔ was."},
            {"direct": "Did you enjoy the meal?", "prefix": "The host asked if", "answer": "we had enjoyed the meal", "explanation": "did ➔ had enjoyed."},
            {"direct": "Why can't you come?", "prefix": "He asked me", "answer": "why I couldn't come", "explanation": "can't ➔ couldn't."},
            {"direct": "Who told you that?", "prefix": "She asked", "answer": "who had told him that", "explanation": "told ➔ had told."},
            {"direct": "Are you coming with us?", "prefix": "He asked if", "answer": "I was coming with them", "explanation": "us ➔ them."},
            {"direct": "Where does she work?", "prefix": "He asked", "answer": "where she worked", "explanation": "work ➔ worked."},
            {"direct": "Have you ever been to Paris?", "prefix": "She asked if", "answer": "I had ever been to Paris", "explanation": "have ➔ had."},
            {"direct": "What did you say?", "prefix": "He asked me", "answer": "what I had said", "explanation": "did ➔ had said."},
            {"direct": "Is your father at home?", "prefix": "She asked if", "answer": "my father was at home", "explanation": "your ➔ my."},
            {"direct": "How many books did you buy?", "prefix": "He asked", "answer": "how many books I had bought", "explanation": "did ➔ had bought."},
            {"direct": "Do you like chocolate?", "prefix": "She asked if", "answer": "I liked chocolate", "explanation": "like ➔ liked."},
            {"direct": "Will you marry me?", "prefix": "He asked her if", "answer": "she would marry him", "explanation": "me ➔ him."},
            {"direct": "What's wrong?", "prefix": "She asked", "answer": "what was wrong", "explanation": "is ➔ was."},
            {"direct": "Where did I leave my phone?", "prefix": "He asked himself", "answer": "where he had left his phone", "explanation": "my ➔ his."}
        ],
        "Orders and Requests": [
            {"direct": "Open the window!", "prefix": "He told me", "answer": "to open the window", "explanation": "to-Infinitive."},
            {"direct": "Don't touch that!", "prefix": "She warned me", "answer": "not to touch that", "explanation": "not to-Infinitive."},
            {"direct": "Please sit down.", "prefix": "He asked us", "answer": "to sit down", "explanation": "Bitte wird to-Inf."},
            {"direct": "Stop talking!", "prefix": "The teacher told them", "answer": "to stop talking", "explanation": "to-Infinitive."},
            {"direct": "Clean your room!", "prefix": "His mother told him", "answer": "to clean his room", "explanation": "your ➔ his."},
            {"direct": "Don't be late!", "prefix": "She told me", "answer": "not to be late", "explanation": "not to-Infinitive."},
            {"direct": "Give me the book.", "prefix": "He asked me", "answer": "to give him the book", "explanation": "me ➔ him."},
            {"direct": "Hurry up!", "prefix": "She told us", "answer": "to hurry up", "explanation": "to-Infinitive."},
            {"direct": "Please help me.", "prefix": "He asked her", "answer": "to help him", "explanation": "me ➔ him."},
            {"direct": "Don't smoke here.", "prefix": "The man told us", "answer": "not to smoke there", "explanation": "here ➔ there."},
            {"direct": "Wait for me!", "prefix": "She told him", "answer": "to wait for her", "explanation": "me ➔ her."},
            {"direct": "Listen carefully.", "prefix": "The speaker told the audience", "answer": "to listen carefully", "explanation": "to-Infinitive."},
            {"direct": "Don't forget the milk.", "prefix": "She reminded me", "answer": "not to forget the milk", "explanation": "not to-Infinitive."},
            {"direct": "Eat your vegetables!", "prefix": "The father told the child", "answer": "to eat his vegetables", "explanation": "your ➔ his."},
            {"direct": "Please call me later.", "prefix": "She asked me", "answer": "to call her later", "explanation": "me ➔ her."},
            {"direct": "Don't park here.", "prefix": "The officer told him", "answer": "not to park there", "explanation": "here ➔ there."},
            {"direct": "Show me your passport.", "prefix": "The official told her", "answer": "to show him her passport", "explanation": "me ➔ him."},
            {"direct": "Be quiet!", "prefix": "He told them", "answer": "to be quiet", "explanation": "to-Infinitive."},
            {"direct": "Don't tell anyone.", "prefix": "She told me", "answer": "not to tell anyone", "explanation": "not to-Infinitive."},
            {"direct": "Turn off the lights.", "prefix": "He told us", "answer": "to turn off the lights", "explanation": "to-Infinitive."},
            {"direct": "Please lend me some money.", "prefix": "He asked his friend", "answer": "to lend him some money", "explanation": "me ➔ him."},
            {"direct": "Don't drink the water.", "prefix": "They warned us", "answer": "not to drink the water", "explanation": "not to-Infinitive."},
            {"direct": "Fasten your seatbelts.", "prefix": "The pilot told the passengers", "answer": "to fasten their seatbelts", "explanation": "your ➔ their."},
            {"direct": "Come here!", "prefix": "The boss told me", "answer": "to come there", "explanation": "here ➔ there."},
            {"direct": "Don't make a mess.", "prefix": "She told the kids", "answer": "not to make a mess", "explanation": "not to-Infinitive."},
            {"direct": "Take a deep breath.", "prefix": "The doctor told him", "answer": "to take a deep breath", "explanation": "to-Infinitive."},
            {"direct": "Please send me the file.", "prefix": "She asked him", "answer": "to send her the file", "explanation": "me ➔ her."},
            {"direct": "Don't look back.", "prefix": "He told her", "answer": "not to look back", "explanation": "not to-Infinitive."},
            {"direct": "Put the gun down!", "prefix": "The police told him", "answer": "to put the gun down", "explanation": "to-Infinitive."},
            {"direct": "Read the instructions.", "prefix": "She told me", "answer": "to read the instructions", "explanation": "to-Infinitive."},
            {"direct": "Don't feed the animals.", "prefix": "The sign told us", "answer": "not to feed the animals", "explanation": "not to-Infinitive."},
            {"direct": "Follow me.", "prefix": "The guide told them", "answer": "to follow him", "explanation": "me ➔ him."},
            {"direct": "Please be patient.", "prefix": "She asked us", "answer": "to be patient", "explanation": "to-Infinitive."},
            {"direct": "Don't worry so much.", "prefix": "He told me", "answer": "not to worry so much", "explanation": "not to-Infinitive."},
            {"direct": "Sign the document.", "prefix": "The lawyer told her", "answer": "to sign the document", "explanation": "to-Infinitive."},
            {"direct": "Don't scream.", "prefix": "He told her", "answer": "not to scream", "explanation": "not to-Infinitive."},
            {"direct": "Buckle up!", "prefix": "The driver told the passengers", "answer": "to buckle up", "explanation": "to-Infinitive."},
            {"direct": "Don't open the door.", "prefix": "She told him", "answer": "not to open the door", "explanation": "not to-Infinitive."},
            {"direct": "Try again.", "prefix": "The coach told me", "answer": "to try again", "explanation": "to-Infinitive."},
            {"direct": "Please hold the line.", "prefix": "The secretary asked him", "answer": "to hold the line", "explanation": "to-Infinitive."},
            {"direct": "Don't use your phone.", "prefix": "The teacher told the students", "answer": "not to use their phones", "explanation": "your ➔ their."},
            {"direct": "Go to bed!", "prefix": "The mother told the boy", "answer": "to go to bed", "explanation": "to-Infinitive."},
            {"direct": "Don't jump!", "prefix": "They told him", "answer": "not to jump", "explanation": "not to-Infinitive."},
            {"direct": "Pass the salt, please.", "prefix": "He asked her", "answer": "to pass the salt", "explanation": "to-Infinitive."},
            {"direct": "Don't cry over spilled milk.", "prefix": "She told me", "answer": "not to cry over spilled milk", "explanation": "not to-Infinitive."},
            {"direct": "Watch your step.", "prefix": "He told us", "answer": "to watch our step", "explanation": "to-Infinitive."},
            {"direct": "Don't run across the street.", "prefix": "The father told his son", "answer": "not to run across the street", "explanation": "not to-Infinitive."},
            {"direct": "Tell me the truth.", "prefix": "She told him", "answer": "to tell her the truth", "explanation": "me ➔ her."},
            {"direct": "Don't drive so fast.", "prefix": "She told him", "answer": "not to drive so fast", "explanation": "not to-Infinitive."},
            {"direct": "Please bring some wine.", "prefix": "He asked them", "answer": "to bring some wine", "explanation": "to-Infinitive."}
        ]
    }

# --- LOGIK-FUNKTIONEN ---
def normalize(text):
    """3. KORREKTUR: If/Whether Äquivalenz & Robustheit."""
    if not text: return ""
    text = text.lower().strip()
    # Behandle if und whether gleich
    text = text.replace("whether", "if")
    # Entferne Satzzeichen am Ende
    text = re.sub(r'[.!?;]$', '', text) 
    return re.sub(r'\s+', ' ', text)

def submit_answer():
    """2. KORREKTUR: Robuster Smart-Strip (Leerzeichen-unabhängig)."""
    user_val = st.session_state.get(f"temp_input", "").strip()
    if not user_val and st.session_state.feedback:
        next_question()
        return

    current_q = st.session_state.current_pool[st.session_state.index]
    prefix = current_q['prefix']
    
    norm_user = normalize(user_val)
    norm_prefix = normalize(prefix)
    
    # Schneide Präfix ab, falls vorhanden
    if norm_user.startswith(norm_prefix):
        processed_user_input = norm_user[len(norm_prefix):].strip()
    else:
        processed_user_input = norm_user

    correct_answers = current_q['answer']
    if isinstance(correct_answers, str):
        correct_answers = [correct_answers]
        
    normalized_corrects = [normalize(ans) for ans in correct_answers]
    
    if normalize(processed_user_input) in normalized_corrects:
        st.session_state.score += 1
        st.session_state.feedback = ("success", "✨ Richtig!")
    else:
        main_solution = correct_answers[0]
        st.session_state.feedback = ("error", f"Falsch. Korrekt: **{prefix} {main_solution}**")

def start_exercise(category):
    data = get_data()
    if category == "Mix":
        full_pool = data["Statements"] + data["Questions"] + data["Orders and Requests"]
    else:
        full_pool = data[category]
    st.session_state.current_pool = random.sample(full_pool, min(15, len(full_pool)))
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.step = "quiz"
    st.session_state.feedback = None

def next_question():
    st.session_state.index += 1
    st.session_state.feedback = None
    st.session_state.temp_input = "" # Input leeren für nächsten Satz
    if st.session_state.index >= len(st.session_state.current_pool):
        st.session_state.step = "result"

# --- INITIALISIERUNG ---
if 'step' not in st.session_state:
    st.session_state.update({'step': "menu", 'score': 0, 'index': 0, 'feedback': None, 'temp_input': ""})

# --- UI HEADER ---
header_col1, header_col2 = st.columns([5, 1])
with header_col1:
    st.title("🇬🇧 Reported Speech Pro")
with header_col2:
    try:
        st.image("schullogo.png", width=100)
    except:
        st.caption("Logo fehlt")
st.markdown("---")

# --- HAUPTTEIL ---
if st.session_state.step == "menu":
    st.subheader("Wähle deine Kategorie:")
    cols = st.columns(2)
    with cols[0]:
        if st.button("Statements", use_container_width=True): start_exercise("Statements")
        if st.button("Questions", use_container_width=True): start_exercise("Questions")
    with cols[1]:
        if st.button("Orders", use_container_width=True): start_exercise("Orders and Requests")
        if st.button("Mix Mode", use_container_width=True): start_exercise("Mix")

elif st.session_state.step == "quiz":
    q = st.session_state.current_pool[st.session_state.index]
    st.progress(st.session_state.index / len(st.session_state.current_pool))
    st.write(f"Satz {st.session_state.index + 1} / {len(st.session_state.current_pool)}")
    st.info(f"Direkte Rede: **\"{q['direct']}\"**")
    
    # 1. KORREKTUR: Workflow-Optimierung für Enter-Taste
    st.text_input(
        f"{q['prefix']} ...", 
        key="temp_input", 
        on_change=submit_answer,
        placeholder="Lösung tippen & Enter drücken..."
    )
    
    if st.session_state.feedback:
        f_type, f_msg = st.session_state.feedback
        if f_type == "success": st.success(f_msg)
        else:
            st.error(f_msg)
            st.warning(f"💡 **Regel:** {q['explanation']}")
        
        st.button("Weiter (Enter)", on_click=next_question, type="primary")
        st.caption("Tipp: Drücke einfach nochmal Enter im Textfeld oben, um fortzufahren.")
    else:
        st.button("Prüfen", on_click=submit_answer)

elif st.session_state.step == "result":
    st.balloons()
    st.header("Training beendet!")
    st.metric("Dein Score", f"{st.session_state.score} / {len(st.session_state.current_pool)}")
    if st.button("Zurück zum Hauptmenü"):
        st.session_state.step = "menu"
        st.rerun()import streamlit as st
import random
import re

# --- KONFIGURATION ---
st.set_page_config(
    page_title="Reported Speech Pro", 
    page_icon="schullogo.png", # Nutzt das Logo auch als Tab-Icon
    layout="centered"
)

def get_data():
    """Vollständiger Datensatz mit Alternativantworten und Erklärungen."""
    return {
        "Statements": [
            {"direct": "I am hungry.", "prefix": "He said that", "answer": "he was hungry", "explanation": "am ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "We are watching a movie.", "prefix": "They said that", "answer": "they were watching a movie", "explanation": "are watching ➔ were watching (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I have finished my project.", "prefix": "She said that", "answer": "she had finished her project", "explanation": "have finished ➔ had finished (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "I will call you tomorrow.", "prefix": "He said that", "answer": ["he would call me the next day", "he would call me the following day"], "explanation": "will ➔ would | tomorrow ➔ the next day / the following day"},
            {"direct": "The sun rises in the east.", "prefix": "The teacher said that", "answer": "the sun rose in the east", "explanation": "rises ➔ rose (Fakt im Backshift)"},
            {"direct": "I don't like coffee.", "prefix": "She said that", "answer": "she didn't like coffee", "explanation": "don't ➔ didn't (Present Simple ➔ Past Simple)"},
            {"direct": "We went to Paris last year.", "prefix": "They said that", "answer": ["they had gone to Paris the year before", "they had gone to Paris the previous year"], "explanation": "went ➔ had gone (Past Simple ➔ Past Perfect) | last year ➔ year before"},
            {"direct": "I can speak three languages.", "prefix": "He said that", "answer": "he could speak three languages", "explanation": "can ➔ could (Modalverb Backshift)"},
            {"direct": "I am playing the guitar.", "prefix": "She said that", "answer": "she was playing the guitar", "explanation": "am playing ➔ was playing (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I have never been to London.", "prefix": "He said that", "answer": "he had never been to London", "explanation": "have been ➔ had been (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "My brother is ill.", "prefix": "She said that", "answer": "her brother was ill", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "We will help you with the bags.", "prefix": "They said that", "answer": "they would help me with the bags", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "I saw a ghost.", "prefix": "The boy said that", "answer": "he had seen a ghost", "explanation": "saw ➔ had seen (Past Simple ➔ Past Perfect)"},
            {"direct": "I am not coming to the party.", "prefix": "He said that", "answer": "he was not coming to the party", "explanation": "am not ➔ was not (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "The train leaves at five.", "prefix": "She said that", "answer": "the train left at five", "explanation": "leaves ➔ left (Present Simple ➔ Past Simple)"},
            {"direct": "I have lost my phone.", "prefix": "He said that", "answer": "he had lost his phone", "explanation": "have lost ➔ had lost (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "We are very happy here.", "prefix": "They said that", "answer": "they were very happy there", "explanation": "are ➔ were | here ➔ there"},
            {"direct": "I didn't do it.", "prefix": "She said that", "answer": "she hadn't done it", "explanation": "didn't do ➔ hadn't done (Past Simple ➔ Past Perfect)"},
            {"direct": "It is raining outside.", "prefix": "He said that", "answer": "it was raining outside", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "I will be there on time.", "prefix": "She said that", "answer": "she would be there on time", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "I have a new car.", "prefix": "He said that", "answer": "he had a new car", "explanation": "have ➔ had (Present Simple ➔ Past Simple)"},
            {"direct": "The children are sleeping.", "prefix": "She said that", "answer": "the children were sleeping", "explanation": "are ➔ were (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I went shopping yesterday.", "prefix": "He said that", "answer": ["he had gone shopping the day before", "he had gone shopping the previous day"], "explanation": "went ➔ had gone | yesterday ➔ the day before"},
            {"direct": "I can't find my keys.", "prefix": "She said that", "answer": "she couldn't find her keys", "explanation": "can't ➔ couldn't (Modalverb Backshift)"},
            {"direct": "We are going on holiday.", "prefix": "They said that", "answer": "they were going on holiday", "explanation": "are ➔ were (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I have already eaten.", "prefix": "He said that", "answer": "he had already eaten", "explanation": "have eaten ➔ had eaten (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "I don't know the answer.", "prefix": "She said that", "answer": "she didn't know the answer", "explanation": "don't ➔ didn't (Present Simple ➔ Past Simple)"},
            {"direct": "I will buy a new house.", "prefix": "He said that", "answer": "he would buy a new house", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "The pizza is delicious.", "prefix": "They said that", "answer": "the pizza was delicious", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "I was at home all night.", "prefix": "She said that", "answer": "she had been at home all night", "explanation": "was ➔ had been (Past Simple ➔ Past Perfect)"},
            {"direct": "I am learning Spanish.", "prefix": "He said that", "answer": "he was learning Spanish", "explanation": "am learning ➔ was learning (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "My father works in a bank.", "prefix": "She said that", "answer": "her father worked in a bank", "explanation": "works ➔ worked (Present Simple ➔ Past Simple)"},
            {"direct": "We have seen this film before.", "prefix": "They said that", "answer": ["they had seen that film before", "they had seen this film before"], "explanation": "have seen ➔ had seen (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "I don't have enough money.", "prefix": "He said that", "answer": "he didn't have enough money", "explanation": "don't have ➔ didn't have (Present Simple ➔ Past Simple)"},
            {"direct": "I will send the email now.", "prefix": "She said that", "answer": ["she would send the email then", "she would send the email at that time"], "explanation": "will ➔ would | now ➔ then"},
            {"direct": "The museum is closed.", "prefix": "He said that", "answer": "the museum was closed", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "I am meeting a friend.", "prefix": "She said that", "answer": "she was meeting a friend", "explanation": "am meeting ➔ was meeting (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "We lived in Berlin for five years.", "prefix": "They said that", "answer": "they had lived in Berlin for five years", "explanation": "lived ➔ had lived (Past Simple ➔ Past Perfect)"},
            {"direct": "I haven't seen her for ages.", "prefix": "He said that", "answer": "he hadn't seen her for ages", "explanation": "haven't seen ➔ hadn't seen (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "I forgot my umbrella.", "prefix": "She said that", "answer": "she had forgotten her umbrella", "explanation": "forgot ➔ had forgotten (Past Simple ➔ Past Perfect)"},
            {"direct": "The cake tastes great.", "prefix": "He said that", "answer": "the cake tasted great", "explanation": "tastes ➔ tasted (Present Simple ➔ Past Simple)"},
            {"direct": "I am not afraid of spiders.", "prefix": "She said that", "answer": "she was not afraid of spiders", "explanation": "am ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "We will win the match.", "prefix": "They said that", "answer": "they would win the match", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "I broke the vase.", "prefix": "The girl said that", "answer": "she had broken the vase", "explanation": "broke ➔ had broken (Past Simple ➔ Past Perfect)"},
            {"direct": "I am feeling better today.", "prefix": "He said that", "answer": ["he was feeling better that day", "he was feeling better today"], "explanation": "am feeling ➔ was feeling | today ➔ that day"},
            {"direct": "My parents are coming over.", "prefix": "She said that", "answer": "her parents were coming over", "explanation": "are coming ➔ were coming (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I have to go now.", "prefix": "He said that", "answer": ["he had to go then", "he had to go at that time"], "explanation": "have to ➔ had to | now ➔ then"},
            {"direct": "I won't tell anyone.", "prefix": "She said that", "answer": "she wouldn't tell anyone", "explanation": "won't ➔ wouldn't (Future ➔ Conditional)"},
            {"direct": "The weather is beautiful.", "prefix": "They said that", "answer": "the weather was beautiful", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "I didn't see the accident.", "prefix": "He said that", "answer": "he hadn't seen the accident", "explanation": "didn't see ➔ hadn't seen (Past Simple ➔ Past Perfect)"},
            {"direct": "I am waiting for the bus.", "prefix": "He said that", "answer": "he was waiting for the bus", "explanation": "am waiting ➔ was waiting (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "We have lived here for ten years.", "prefix": "They said that", "answer": "they had lived there for ten years", "explanation": "have lived ➔ had lived | here ➔ there"},
            {"direct": "I will do my best.", "prefix": "She said that", "answer": "she would do her best", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "I didn't see you at the party.", "prefix": "He told me that", "answer": "he hadn't seen me at the party", "explanation": "didn't see ➔ hadn't seen (Past Simple ➔ Past Perfect)"},
            {"direct": "The water is boiling.", "prefix": "She said that", "answer": "the water was boiling", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "I have already finished my breakfast.", "prefix": "He said that", "answer": "he had already finished his breakfast", "explanation": "have finished ➔ had finished (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "We are going to the cinema tonight.", "prefix": "They said that", "answer": ["they were going to the cinema that night", "they were going to the cinema tonight"], "explanation": "are going ➔ were going | tonight ➔ that night"},
            {"direct": "I can't swim very well.", "prefix": "She said that", "answer": "she couldn't swim very well", "explanation": "can't ➔ couldn't (Modalverb Backshift)"},
            {"direct": "I found a wallet on the street.", "prefix": "He said that", "answer": "he had found a wallet on the street", "explanation": "found ➔ had found (Past Simple ➔ Past Perfect)"},
            {"direct": "My sister is a doctor.", "prefix": "She said that", "answer": "her sister was a doctor", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "I will bring the book back tomorrow.", "prefix": "He said that", "answer": ["he would bring the book back the next day", "he would bring the book back the following day"], "explanation": "will ➔ would | tomorrow ➔ next day"},
            {"direct": "The shops are closed on Sundays.", "prefix": "She said that", "answer": "the shops were closed on Sundays", "explanation": "are ➔ were (Present Simple ➔ Past Simple)"},
            {"direct": "I am reading a very good book.", "prefix": "He said that", "answer": "he was reading a very good book", "explanation": "am reading ➔ was reading (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "We haven't been to the zoo yet.", "prefix": "They said that", "answer": "they hadn't been to the zoo yet", "explanation": "haven't been ➔ hadn't been (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "I don't like spicy food.", "prefix": "She said that", "answer": "she didn't like spicy food", "explanation": "don't ➔ didn't (Present Simple ➔ Past Simple)"},
            {"direct": "I will call you as soon as I arrive.", "prefix": "He said that", "answer": "he would call me as soon as he arrived", "explanation": "will ➔ would | arrive ➔ arrived"},
            {"direct": "The dog is barking at the cat.", "prefix": "She said that", "answer": "the dog was barking at the cat", "explanation": "is barking ➔ was barking (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I have lost my passport.", "prefix": "He said that", "answer": "he had lost his passport", "explanation": "have lost ➔ had lost (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "We saw a great play last night.", "prefix": "They said that", "answer": ["they had seen a great play the night before", "they had seen a great play the previous night"], "explanation": "saw ➔ had seen | last night ➔ night before"},
            {"direct": "I am not feeling very well.", "prefix": "She said that", "answer": "she was not feeling very well", "explanation": "am not ➔ was not (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I will make a cake for your birthday.", "prefix": "He said that", "answer": "he would make a cake for my birthday", "explanation": "will ➔ would | your ➔ my"},
            {"direct": "My parents are on holiday.", "prefix": "She said that", "answer": "her parents were on holiday", "explanation": "are ➔ were (Present Simple ➔ Past Simple)"},
            {"direct": "I have been working hard all day.", "prefix": "He said that", "answer": "he had been working hard all day", "explanation": "have been working ➔ had been working (Pres. Perf. Cont. ➔ Past Perf. Cont.)"},
            {"direct": "We are moving to a new house.", "prefix": "They said that", "answer": "they were moving to a new house", "explanation": "are ➔ were (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I didn't have time to do my hair.", "prefix": "She said that", "answer": "she hadn't had time to do her hair", "explanation": "didn't have ➔ hadn't had (Past Simple ➔ Past Perfect)"},
            {"direct": "I can help you with your homework.", "prefix": "He said that", "answer": "he could help me with my homework", "explanation": "can ➔ could (Modalverb Backshift)"},
            {"direct": "The meeting starts at nine o'clock.", "prefix": "She said that", "answer": "the meeting started at nine o'clock", "explanation": "starts ➔ started (Present Simple ➔ Past Simple)"},
            {"direct": "I have never seen such a beautiful sunset.", "prefix": "He said that", "answer": "he had never seen such a beautiful sunset", "explanation": "have seen ➔ had seen (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "We don't have any milk left.", "prefix": "They said that", "answer": "they didn't have any milk left", "explanation": "don't ➔ didn't (Present Simple ➔ Past Simple)"},
            {"direct": "I am going to buy some new shoes.", "prefix": "She said that", "answer": "she was going to buy some new shoes", "explanation": "am going ➔ was going (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I will send you a postcard from Rome.", "prefix": "He said that", "answer": "he would send me a postcard from Rome", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "The car is being repaired.", "prefix": "She said that", "answer": "the car was being repaired", "explanation": "is being ➔ was being (Pres. Cont. Passive ➔ Past Cont. Passive)"},
            {"direct": "I have already seen this movie twice.", "prefix": "He said that", "answer": ["he had already seen that movie twice", "he had already seen this movie twice"], "explanation": "have seen ➔ had seen (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "We played tennis for two hours.", "prefix": "They said that", "answer": "they had played tennis for two hours", "explanation": "played ➔ had played (Past Simple ➔ Past Perfect)"},
            {"direct": "I am not happy with my new job.", "prefix": "She said that", "answer": "she was not happy with her new job", "explanation": "am ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "I will be home by seven.", "prefix": "He said that", "answer": "he would be home by seven", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "My computer is broken.", "prefix": "She said that", "answer": "her computer was broken", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "I have forgotten my password again.", "prefix": "He said that", "answer": "he had forgotten his password again", "explanation": "have forgotten ➔ had forgotten (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "We are having a party next Saturday.", "prefix": "They said that", "answer": ["they were having a party the following Saturday", "they were having a party the next Saturday"], "explanation": "are having ➔ were having | next Saturday ➔ following Saturday"},
            {"direct": "I don't understand the question.", "prefix": "She said that", "answer": "she didn't understand the question", "explanation": "don't ➔ didn't (Present Simple ➔ Past Simple)"},
            {"direct": "I will pay for the drinks.", "prefix": "He said that", "answer": "he would pay for the drinks", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "The flight was delayed by two hours.", "prefix": "She said that", "answer": "the flight had been delayed by two hours", "explanation": "was ➔ had been (Past Simple ➔ Past Perfect)"},
            {"direct": "I am learning how to drive.", "prefix": "He said that", "answer": "he was learning how to drive", "explanation": "am learning ➔ was learning (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "We haven't seen our neighbours for weeks.", "prefix": "They said that", "answer": "they hadn't seen their neighbours for weeks", "explanation": "haven't seen ➔ hadn't seen (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "I can't go out because I have a cold.", "prefix": "She said that", "answer": "she couldn't go out because she had a cold", "explanation": "can't ➔ couldn't | have ➔ had"},
            {"direct": "I will meet you at the station.", "prefix": "He said that", "answer": "he would meet me at the station", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "The music is too loud.", "prefix": "She said that", "answer": "the music was too loud", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "I have just received a letter from my penfriend.", "prefix": "He said that", "answer": "he had just received a letter from his penfriend", "explanation": "have received ➔ had received (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "We are going to visit our grandparents.", "prefix": "They said that", "answer": "they were going to visit their grandparents", "explanation": "are going ➔ were going (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I didn't like the ending of the book.", "prefix": "She said that", "answer": "she hadn't liked the ending of the book", "explanation": "didn't like ➔ hadn't liked (Past Simple ➔ Past Perfect)"},
            {"direct": "I must go to the dentist.", "prefix": "He said that", "answer": "he had to go to the dentist", "explanation": "must ➔ had to (Modalverb Backshift)"},
            {"direct": "We are playing hide and seek.", "prefix": "They said that", "answer": "they were playing hide and seek", "explanation": "are playing ➔ were playing (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I have been to Japan twice.", "prefix": "She said that", "answer": "she had been to Japan twice", "explanation": "have been ➔ had been (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "I will do the washing up later.", "prefix": "He said that", "answer": "he would do the washing up later", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "The car belongs to my uncle.", "prefix": "She said that", "answer": "the car belonged to her uncle", "explanation": "belongs ➔ belonged (Present Simple ➔ Past Simple)"},
            {"direct": "I don't have any brothers or sisters.", "prefix": "He said that", "answer": "he didn't have any brothers or sisters", "explanation": "don't have ➔ didn't have (Present Simple ➔ Past Simple)"},
            {"direct": "We visited the museum two days ago.", "prefix": "They said that", "answer": ["they had visited the museum two days before", "they had visited the museum two days earlier"], "explanation": "visited ➔ had visited | ago ➔ before"},
            {"direct": "I can play the flute.", "prefix": "She said that", "answer": "she could play the flute", "explanation": "can ➔ could (Modalverb Backshift)"},
            {"direct": "I am looking for my glasses.", "prefix": "He said that", "answer": "he was looking for his glasses", "explanation": "am looking ➔ was looking (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I have just finished a marathon.", "prefix": "She said that", "answer": "she had just finished a marathon", "explanation": "have finished ➔ had finished (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "My friend is moving to New York.", "prefix": "He said that", "answer": "his friend was moving to New York", "explanation": "is moving ➔ was moving (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "We will be late for the concert.", "prefix": "They said that", "answer": "they would be late for the concert", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "I saw a famous actor in the park.", "prefix": "She said that", "answer": "she had seen a famous actor in the park", "explanation": "saw ➔ had seen (Past Simple ➔ Past Perfect)"},
            {"direct": "I am not interested in politics.", "prefix": "He said that", "answer": "he was not interested in politics", "explanation": "am ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "The flowers smell wonderful.", "prefix": "She said that", "answer": "the flowers smelled wonderful", "explanation": "smell ➔ smelled (Present Simple ➔ Past Simple)"},
            {"direct": "I have lost my appetite.", "prefix": "He said that", "answer": "he had lost his appetite", "explanation": "have lost ➔ had lost (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "We are waiting for the results.", "prefix": "They said that", "answer": "they were waiting for the results", "explanation": "are waiting ➔ were waiting (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I didn't mean to hurt your feelings.", "prefix": "She told me that", "answer": "she hadn't meant to hurt my feelings", "explanation": "didn't mean ➔ hadn't meant (Past Simple ➔ Past Perfect)"},
            {"direct": "It is getting dark.", "prefix": "He said that", "answer": "it was getting dark", "explanation": "is getting ➔ was getting (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I will buy you a present.", "prefix": "She said that", "answer": "she would buy me a present", "explanation": "will ➔ would | you ➔ me"},
            {"direct": "I have a terrible headache.", "prefix": "He said that", "answer": "he had a terrible headache", "explanation": "have ➔ had (Present Simple ➔ Past Simple)"},
            {"direct": "The birds are singing.", "prefix": "She said that", "answer": "the birds were singing", "explanation": "are singing ➔ were singing (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "I bought this dress in London.", "prefix": "She said that", "answer": ["she had bought that dress in London", "she had bought this dress in London"], "explanation": "bought ➔ had bought | this ➔ that"},
            {"direct": "I can't remember his name.", "prefix": "He said that", "answer": "he couldn't remember his name", "explanation": "can't ➔ couldn't (Modalverb Backshift)"},
            {"direct": "We are going to the beach tomorrow.", "prefix": "They said that", "answer": ["they were going to the beach the next day", "they were going to the beach the following day"], "explanation": "are going ➔ were going | tomorrow ➔ next day"},
            {"direct": "I have already cleaned the kitchen.", "prefix": "He said that", "answer": "he had already cleaned the kitchen", "explanation": "have cleaned ➔ had cleaned (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "I don't think it's a good idea.", "prefix": "She said that", "answer": "she didn't think it was a good idea", "explanation": "don't ➔ didn't | is ➔ was"},
            {"direct": "I will lend you my umbrella.", "prefix": "He said that", "answer": "he would lend me his umbrella", "explanation": "will ➔ would | you ➔ me"},
            {"direct": "The soup is too salty.", "prefix": "They said that", "answer": "the soup was too salty", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "I was sleeping when the phone rang.", "prefix": "She said that", "answer": "she had been sleeping when the phone rang", "explanation": "was sleeping ➔ had been sleeping (Past Cont. ➔ Past Perf. Cont.)"},
            {"direct": "I am writing a letter to my grandmother.", "prefix": "He said that", "answer": "he was writing a letter to his grandmother", "explanation": "am writing ➔ was writing (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "My cousin lives in Australia.", "prefix": "She said that", "answer": "her cousin lived in Australia", "explanation": "lives ➔ lived (Present Simple ➔ Past Simple)"},
            {"direct": "We have spent all our money.", "prefix": "They said that", "answer": "they had spent all their money", "explanation": "have spent ➔ had spent (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "I don't feel like going out.", "prefix": "He said that", "answer": "he didn't feel like going out", "explanation": "don't ➔ didn't (Present Simple ➔ Past Simple)"},
            {"direct": "I will fix the car next week.", "prefix": "She said that", "answer": ["she would fix the car the following week", "she would fix the car the next week"], "explanation": "will ➔ would | next week ➔ following week"},
            {"direct": "The water is too cold for swimming.", "prefix": "He said that", "answer": "the water was too cold for swimming", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "I am having a great time.", "prefix": "She said that", "answer": "she was having a great time", "explanation": "am having ➔ was having (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "We traveled around Europe last summer.", "prefix": "They said that", "answer": ["they had traveled around Europe the summer before", "they had traveled around Europe the previous summer"], "explanation": "traveled ➔ had traveled | last summer ➔ summer before"},
            {"direct": "I haven't heard from him lately.", "prefix": "He said that", "answer": "he hadn't heard from him lately", "explanation": "haven't heard ➔ hadn't heard (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "I forgot to lock the door.", "prefix": "She said that", "answer": "she had forgotten to lock the door", "explanation": "forgot ➔ had forgotten (Past Simple ➔ Past Perfect)"},
            {"direct": "The performance starts at 8 PM.", "prefix": "He said that", "answer": "the performance started at 8 PM", "explanation": "starts ➔ started (Present Simple ➔ Past Simple)"},
            {"direct": "I am not ready yet.", "prefix": "She said that", "answer": "she was not ready yet", "explanation": "am ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "We will enjoy the show.", "prefix": "They said that", "answer": "they would enjoy the show", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "I made a mistake.", "prefix": "The student said that", "answer": "he had made a mistake", "explanation": "made ➔ had made (Past Simple ➔ Past Perfect)"},
            {"direct": "I am working on a new project.", "prefix": "He said that", "answer": "he was working on a new project", "explanation": "am working ➔ was working (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "My parents are proud of me.", "prefix": "She said that", "answer": "her parents were proud of her", "explanation": "are ➔ were | me ➔ her"},
            {"direct": "I have to finish this by noon.", "prefix": "He said that", "answer": ["he had to finish that by noon", "he had to finish this by noon"], "explanation": "have to ➔ had to | this ➔ that"},
            {"direct": "I won't forget your birthday.", "prefix": "She said that", "answer": "she wouldn't forget my birthday", "explanation": "won't ➔ wouldn't | your ➔ my"},
            {"direct": "The movie was very boring.", "prefix": "They said that", "answer": "the movie had been very boring", "explanation": "was ➔ had been (Past Simple ➔ Past Perfect)"},
            {"direct": "I didn't understand the instructions.", "prefix": "He said that", "answer": "he hadn't understood the instructions", "explanation": "didn't understand ➔ hadn't understood (Past Simple ➔ Past Perfect)"}
        ],
        "Questions": [
            {"direct": "Where is the station?", "prefix": "He asked me", "answer": "where the station was", "explanation": "Wortstellung: Verb 'was' ans Ende wie im Aussagesatz."},
            {"direct": "Do you like tea?", "prefix": "She asked him if", "answer": "he liked tea", "explanation": "if-Satz | like ➔ liked (Present Simple ➔ Past Simple)"},
            {"direct": "What are you doing?", "prefix": "They asked us", "answer": "what we were doing", "explanation": "are doing ➔ were doing (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "Have you seen my keys?", "prefix": "He asked her if", "answer": "she had seen his keys", "explanation": "have seen ➔ had seen (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "Can you swim?", "prefix": "She asked me if", "answer": "I could swim", "explanation": "can ➔ could (Modalverb Backshift)"},
            {"direct": "Why did you call?", "prefix": "He asked me", "answer": "why I had called", "explanation": "did call ➔ had called (Past Simple ➔ Past Perfect)"},
            {"direct": "Will it rain tomorrow?", "prefix": "She asked if", "answer": ["it would rain the next day", "it would rain the following day"], "explanation": "will ➔ would | tomorrow ➔ next day"},
            {"direct": "Where have you been?", "prefix": "My mom asked me", "answer": "where I had been", "explanation": "have been ➔ had been (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "Is he coming to the party?", "prefix": "She asked if", "answer": "he was coming to the party", "explanation": "is coming ➔ was coming (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "How much does this cost?", "prefix": "He asked", "answer": "how much that cost", "explanation": "cost ➔ cost (Past Simple) | this ➔ that"},
            {"direct": "Do you live here?", "prefix": "She asked me if", "answer": "I lived there", "explanation": "live ➔ lived | here ➔ there"},
            {"direct": "When will the movie start?", "prefix": "He asked", "answer": "when the movie would start", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "What time is it?", "prefix": "She asked me", "answer": "what time it was", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "Are you busy?", "prefix": "He asked if", "answer": "I was busy", "explanation": "are ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "Where did you buy that car?", "prefix": "She asked him", "answer": "where he had bought that car", "explanation": "did buy ➔ had bought (Past Simple ➔ Past Perfect)"},
            {"direct": "Can I help you?", "prefix": "The waiter asked if", "answer": ["he could help me", "he could help us"], "explanation": "can ➔ could (Modalverb Backshift)"},
            {"direct": "Why are you crying?", "prefix": "He asked her", "answer": "why she was crying", "explanation": "are crying ➔ were crying (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "Have you finished your homework?", "prefix": "The teacher asked if", "answer": "I had finished my homework", "explanation": "have finished ➔ had finished (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "What do you want?", "prefix": "He asked me", "answer": "what I wanted", "explanation": "want ➔ wanted (Present Simple ➔ Past Simple)"},
            {"direct": "Did you see the news?", "prefix": "She asked if", "answer": "I had seen the news", "explanation": "did see ➔ had seen (Past Simple ➔ Past Perfect)"},
            {"direct": "How often do you exercise?", "prefix": "He asked me", "answer": "how often I exercised", "explanation": "exercise ➔ exercised (Present Simple ➔ Past Simple)"},
            {"direct": "Is there a bank nearby?", "prefix": "She asked", "answer": "if there was a bank nearby", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "What will happen next?", "prefix": "He asked", "answer": "what would happen next", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "Are they playing well?", "prefix": "She asked if", "answer": "they were playing well", "explanation": "are playing ➔ were playing (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "Where can I park?", "prefix": "He asked", "answer": "where he could park", "explanation": "can ➔ could (Modalverb Backshift)"},
            {"direct": "Do you have a pen?", "prefix": "She asked if", "answer": "I had a pen", "explanation": "have ➔ had (Present Simple ➔ Past Simple)"},
            {"direct": "Why is the shop closed?", "prefix": "He asked", "answer": "why the shop was closed", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "How did you find me?", "prefix": "She asked him", "answer": "how he had found her", "explanation": "did find ➔ had found (Past Simple ➔ Past Perfect)"},
            {"direct": "Will you be home late?", "prefix": "He asked if", "answer": "I would be home late", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "Are we lost?", "prefix": "She asked if", "answer": "they were lost", "explanation": "are ➔ were (Present Simple ➔ Past Simple)"},
            {"direct": "What is your name?", "prefix": "He asked me", "answer": "what my name was", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "Do you speak English?", "prefix": "She asked him if", "answer": "he spoke English", "explanation": "speak ➔ spoke (Present Simple ➔ Past Simple)"},
            {"direct": "How long have you lived here?", "prefix": "He asked", "answer": "how long I had lived there", "explanation": "have lived ➔ had lived | here ➔ there"},
            {"direct": "Where are you going for vacation?", "prefix": "She asked me", "answer": "where I was going for vacation", "explanation": "are going ➔ was going (Pres. Cont. ➔ Past Cont.)"},
            {"direct": "Can we go now?", "prefix": "They asked if", "answer": ["they could go then", "they could go at that time"], "explanation": "can ➔ could | now ➔ then"},
            {"direct": "What were you thinking?", "prefix": "He asked me", "answer": "what I had been thinking", "explanation": "were thinking ➔ had been thinking (Past Cont. ➔ Past Perf. Cont.)"},
            {"direct": "Is it cold outside?", "prefix": "She asked if", "answer": "it was cold outside", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "Did you enjoy the meal?", "prefix": "The host asked if", "answer": "we had enjoyed the meal", "explanation": "did enjoy ➔ had enjoyed (Past Simple ➔ Past Perfect)"},
            {"direct": "Why can't you come?", "prefix": "He asked me", "answer": "why I couldn't come", "explanation": "can't ➔ couldn't (Modalverb Backshift)"},
            {"direct": "Who told you that?", "prefix": "She asked", "answer": "who had told him that", "explanation": "told ➔ had told (Past Simple ➔ Past Perfect)"},
            {"direct": "Are you coming with us?", "prefix": "He asked if", "answer": "I was coming with them", "explanation": "are coming ➔ was coming | us ➔ them"},
            {"direct": "Where does she work?", "prefix": "He asked", "answer": "where she worked", "explanation": "works ➔ worked (Present Simple ➔ Past Simple)"},
            {"direct": "Have you ever been to Paris?", "prefix": "She asked if", "answer": "I had ever been to Paris", "explanation": "have been ➔ had been (Pres. Perf. ➔ Past Perf.)"},
            {"direct": "What did you say?", "prefix": "He asked me", "answer": "what I had said", "explanation": "did say ➔ had said (Past Simple ➔ Past Perfect)"},
            {"direct": "Is your father at home?", "prefix": "She asked if", "answer": "my father was at home", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "How many books did you buy?", "prefix": "He asked", "answer": "how many books I had bought", "explanation": "did buy ➔ had bought (Past Simple ➔ Past Perfect)"},
            {"direct": "Do you like chocolate?", "prefix": "She asked if", "answer": "I liked chocolate", "explanation": "like ➔ liked (Present Simple ➔ Past Simple)"},
            {"direct": "Will you marry me?", "prefix": "He asked her if", "answer": "she would marry him", "explanation": "will ➔ would (Future ➔ Conditional)"},
            {"direct": "What's wrong?", "prefix": "She asked", "answer": "what was wrong", "explanation": "is ➔ was (Present Simple ➔ Past Simple)"},
            {"direct": "Where did I leave my phone?", "prefix": "He asked himself", "answer": "where he had left his phone", "explanation": "did leave ➔ had left (Past Simple ➔ Past Perfect)"}
        ],
        "Orders and Requests": [
            {"direct": "Open the window!", "prefix": "He told me", "answer": "to open the window", "explanation": "Befehl: to + Infinitive"},
            {"direct": "Don't touch that!", "prefix": "She warned me", "answer": "not to touch that", "explanation": "Verneinter Befehl: not + to + Infinitive"},
            {"direct": "Please sit down.", "prefix": "He asked us", "answer": "to sit down", "explanation": "Bitte: to + Infinitive"},
            {"direct": "Stop talking!", "prefix": "The teacher told them", "answer": "to stop talking", "explanation": "Befehl: to + Infinitive"},
            {"direct": "Clean your room!", "prefix": "His mother told him", "answer": "to clean his room", "explanation": "Befehl: to + Infinitive"},
            {"direct": "Don't be late!", "prefix": "She told me", "answer": "not to be late", "explanation": "Verneinter Befehl: not + to + Infinitive"},
            {"direct": "Give me the book.", "prefix": "He asked me", "answer": "to give him the book", "explanation": "Bitte: to + Infinitive | me ➔ him"},
            {"direct": "Hurry up!", "prefix": "She told us", "answer": "to hurry up", "explanation": "Befehl: to + Infinitive"},
            {"direct": "Please help me.", "prefix": "He asked her", "answer": "to help him", "explanation": "Bitte: to + Infinitive | me ➔ him"},
            {"direct": "Don't smoke here.", "prefix": "The man told us", "answer": "not to smoke there", "explanation": "not to + Infinitive | here ➔ there"},
            {"direct": "Wait for me!", "prefix": "She told him", "answer": "to wait for her", "explanation": "me ➔ her"},
            {"direct": "Listen carefully.", "prefix": "The speaker told the audience", "answer": "to listen carefully", "explanation": "to + Infinitive"},
            {"direct": "Don't forget the milk.", "prefix": "She reminded me", "answer": "not to forget the milk", "explanation": "not to + Infinitive"},
            {"direct": "Eat your vegetables!", "prefix": "The father told the child", "answer": "to eat his vegetables", "explanation": "your ➔ his"},
            {"direct": "Please call me later.", "prefix": "She asked me", "answer": "to call her later", "explanation": "me ➔ her"},
            {"direct": "Don't park here.", "prefix": "The officer told him", "answer": "not to park there", "explanation": "here ➔ there"},
            {"direct": "Show me your passport.", "prefix": "The official told her", "answer": "to show him her passport", "explanation": "me ➔ him | your ➔ her"},
            {"direct": "Be quiet!", "prefix": "He told them", "answer": "to be quiet", "explanation": "to + Infinitive"},
            {"direct": "Don't tell anyone.", "prefix": "She told me", "answer": "not to tell anyone", "explanation": "not to + Infinitive"},
            {"direct": "Turn off the lights.", "prefix": "He told us", "answer": "to turn off the lights", "explanation": "to + Infinitive"},
            {"direct": "Please lend me some money.", "prefix": "He asked his friend", "answer": "to lend him some money", "explanation": "me ➔ him"},
            {"direct": "Don't drink the water.", "prefix": "They warned us", "answer": "not to drink the water", "explanation": "not to + Infinitive"},
            {"direct": "Fasten your seatbelts.", "prefix": "The pilot told the passengers", "answer": "to fasten their seatbelts", "explanation": "your ➔ their"},
            {"direct": "Come here!", "prefix": "The boss told me", "answer": "to come there", "explanation": "here ➔ there"},
            {"direct": "Don't make a mess.", "prefix": "She told the kids", "answer": "not to make a mess", "explanation": "not to + Infinitive"},
            {"direct": "Take a deep breath.", "prefix": "The doctor told him", "answer": "to take a deep breath", "explanation": "to + Infinitive"},
            {"direct": "Please send me the file.", "prefix": "She asked him", "answer": "to send her the file", "explanation": "me ➔ her"},
            {"direct": "Don't look back.", "prefix": "He told her", "answer": "not to look back", "explanation": "not to + Infinitive"},
            {"direct": "Put the gun down!", "prefix": "The police told him", "answer": "to put the gun down", "explanation": "to + Infinitive"},
            {"direct": "Read the instructions.", "prefix": "She told me", "answer": "to read the instructions", "explanation": "to + Infinitive"},
            {"direct": "Don't feed the animals.", "prefix": "The sign told us", "answer": "not to feed the animals", "explanation": "not to + Infinitive"},
            {"direct": "Follow me.", "prefix": "The guide told them", "answer": "to follow him", "explanation": "me ➔ him"},
            {"direct": "Please be patient.", "prefix": "She asked us", "answer": "to be patient", "explanation": "to + Infinitive"},
            {"direct": "Don't worry so much.", "prefix": "He told me", "answer": "not to worry so much", "explanation": "not to + Infinitive"},
            {"direct": "Sign the document.", "prefix": "The lawyer told her", "answer": "to sign the document", "explanation": "to + Infinitive"},
            {"direct": "Don't scream.", "prefix": "He told her", "answer": "not to scream", "explanation": "not to + Infinitive"},
            {"direct": "Buckle up!", "prefix": "The driver told the passengers", "answer": "to buckle up", "explanation": "to + Infinitive"},
            {"direct": "Don't open the door.", "prefix": "She told him", "answer": "not to open the door", "explanation": "not to + Infinitive"},
            {"direct": "Try again.", "prefix": "The coach told me", "answer": "to try again", "explanation": "to + Infinitive"},
            {"direct": "Please hold the line.", "prefix": "The secretary asked him", "answer": "to hold the line", "explanation": "to + Infinitive"},
            {"direct": "Don't use your phone.", "prefix": "The teacher told the students", "answer": "not to use their phones", "explanation": "your ➔ their"},
            {"direct": "Go to bed!", "prefix": "The mother told the boy", "answer": "to go to bed", "explanation": "to + Infinitive"},
            {"direct": "Don't jump!", "prefix": "They told him", "answer": "not to jump", "explanation": "not to + Infinitive"},
            {"direct": "Pass the salt, please.", "prefix": "He asked her", "answer": "to pass the salt", "explanation": "to + Infinitive"},
            {"direct": "Don't cry over spilled milk.", "prefix": "She told me", "answer": "not to cry over spilled milk", "explanation": "not to + Infinitive"},
            {"direct": "Watch your step.", "prefix": "He told us", "answer": "to watch our step", "explanation": "to + Infinitive"},
            {"direct": "Don't run across the street.", "prefix": "The father told his son", "answer": "not to run across the street", "explanation": "not to + Infinitive"},
            {"direct": "Tell me the truth.", "prefix": "She told him", "answer": "to tell her the truth", "explanation": "me ➔ her"},
            {"direct": "Don't drive so fast.", "prefix": "She told him", "answer": "not to drive so fast", "explanation": "not to + Infinitive"},
            {"direct": "Please bring some wine.", "prefix": "He asked them", "answer": "to bring some wine", "explanation": "to + Infinitive"}
        ]
    }

# --- LOGIK-FUNKTIONEN ---
def normalize(text):
    text = text.lower().strip()
    text = re.sub(r'[.!?;]$', '', text) 
    return re.sub(r'\s+', ' ', text)

def start_exercise(category):
    data = get_data()
    if category == "Mix":
        full_pool = data["Statements"] + data["Questions"] + data["Orders and Requests"]
    else:
        full_pool = data[category]
    st.session_state.current_pool = random.sample(full_pool, min(15, len(full_pool)))
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.step = "quiz"
    st.session_state.feedback = None
    st.session_state.last_category = category

def submit_answer():
    user_val = st.session_state.get(f"input_{st.session_state.index}", "")
    current_q = st.session_state.current_pool[st.session_state.index]
    correct_answers = current_q['answer']
    if isinstance(correct_answers, str):
        correct_answers = [correct_answers]
    normalized_user = normalize(user_val)
    normalized_corrects = [normalize(ans) for ans in correct_answers]
    if normalized_user in normalized_corrects:
        st.session_state.score += 1
        st.session_state.feedback = ("success", "✨ Richtig!")
    else:
        main_solution = correct_answers[0]
        st.session_state.feedback = ("error", f"Falsch. Korrekt: **{current_q['prefix']} {main_solution}**")

def next_question():
    st.session_state.index += 1
    st.session_state.feedback = None
    if st.session_state.index >= len(st.session_state.current_pool):
        st.session_state.step = "result"

# --- INITIALISIERUNG ---
for key, val in {'step': "menu", 'score': 0, 'index': 0, 'feedback': None, 'current_pool': []}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- UI HEADER (MIT LOGO OBEN RECHTS) ---
header_col1, header_col2 = st.columns([5, 1])

with header_col1:
    st.title("🇬🇧 Reported Speech Pro")

with header_col2:
    try:
        st.image("schullogo.png", width=100)
    except:
        # Falls das Logo fehlt, zeige eine dezente Info oder lass es leer
        st.caption("Logo-Platzhalter")

st.markdown("---")

# --- HAUPTTEIL ---
if st.session_state.step == "menu":
    st.subheader("Wähle deine Kategorie:")
    cols = st.columns(2)
    with cols[0]:
        if st.button("Statements (Aussagen)", use_container_width=True): start_exercise("Statements")
        if st.button("Questions (Fragen)", use_container_width=True): start_exercise("Questions")
    with cols[1]:
        if st.button("Orders (Befehle)", use_container_width=True): start_exercise("Orders and Requests")
        if st.button("Mix Mode (Alles)", use_container_width=True): start_exercise("Mix")

elif st.session_state.step == "quiz":
    q = st.session_state.current_pool[st.session_state.index]
    st.progress(st.session_state.index / len(st.session_state.current_pool))
    st.write(f"Frage {st.session_state.index + 1} / {len(st.session_state.current_pool)} | Score: {st.session_state.score}")
    st.info(f"Direkte Rede: **\"{q['direct']}\"**")
    st.text_input(f"{q['prefix']} ...", key=f"input_{st.session_state.index}", on_change=submit_answer if st.session_state.feedback is None else None)
    if st.session_state.feedback:
        f_type, f_msg = st.session_state.feedback
        if f_type == "success": st.success(f_msg)
        else: st.error(f_msg)
        if "explanation" in q: st.warning(f"💡 **Regel:** {q['explanation']}")
        st.button("Weiter", on_click=next_question, type="primary")
    else:
        st.button("Prüfen", on_click=submit_answer)

elif st.session_state.step == "result":
    st.balloons()
    st.header("Ergebnis!")
    st.metric("Erreichte Punkte", f"{st.session_state.score} / {len(st.session_state.current_pool)}")
    if st.button("Nochmal zum Menü"):
        st.session_state.step = "menu"
        st.rerun()

