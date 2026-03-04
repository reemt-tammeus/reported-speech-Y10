import streamlit as st
import random

# --- SEITEN-KONFIGURATION ---
st.set_page_config(page_title="Reported Speech Trainer", page_icon="📝")

# --- INITIALISIERUNG DES DATENSATZES ---
if 'data' not in st.session_state:
    st.session_state.data = {
        "Statements": [
            {"direct": "I am hungry.", "prefix": "He said that", "answer": "he was hungry"},
            {"direct": "We are watching a movie.", "prefix": "They said that", "answer": "they were watching a movie"},
            {"direct": "I have finished my project.", "prefix": "She said that", "answer": "she had finished her project"},
            {"direct": "I will call you tomorrow.", "prefix": "He said that", "answer": "he would call me the next day"},
            {"direct": "The sun rises in the east.", "prefix": "The teacher said that", "answer": "the sun rose in the east"},
            {"direct": "I don't like coffee.", "prefix": "She said that", "answer": "she didn't like coffee"},
            {"direct": "We went to Paris last year.", "prefix": "They said that", "answer": "they had gone to Paris the year before"},
            {"direct": "I can speak three languages.", "prefix": "He said that", "answer": "he could speak three languages"},
            {"direct": "I am playing the guitar.", "prefix": "She said that", "answer": "she was playing the guitar"},
            {"direct": "I have never been to London.", "prefix": "He said that", "answer": "he had never been to London"},
            {"direct": "My brother is ill.", "prefix": "She said that", "answer": "her brother was ill"},
            {"direct": "We will help you with the bags.", "prefix": "They said that", "answer": "they would help me with the bags"},
            {"direct": "I saw a ghost.", "prefix": "The boy said that", "answer": "he had seen a ghost"},
            {"direct": "I am not coming to the party.", "prefix": "He said that", "answer": "he was not coming to the party"},
            {"direct": "The train leaves at five.", "prefix": "She said that", "answer": "the train left at five"},
            {"direct": "I have lost my phone.", "prefix": "He said that", "answer": "he had lost his phone"},
            {"direct": "We are very happy here.", "prefix": "They said that", "answer": "they were very happy there"},
            {"direct": "I didn't do it.", "prefix": "She said that", "answer": "she hadn't done it"},
            {"direct": "It is raining outside.", "prefix": "He said that", "answer": "it was raining outside"},
            {"direct": "I will be there on time.", "prefix": "She said that", "answer": "she would be there on time"},
            {"direct": "I have a new car.", "prefix": "He said that", "answer": "he had a new car"},
            {"direct": "The children are sleeping.", "prefix": "She said that", "answer": "the children were sleeping"},
            {"direct": "I went shopping yesterday.", "prefix": "He said that", "answer": "he had gone shopping the day before"},
            {"direct": "I can't find my keys.", "prefix": "She said that", "answer": "she couldn't find her keys"},
            {"direct": "We are going on holiday.", "prefix": "They said that", "answer": "they were going on holiday"},
            {"direct": "I have already eaten.", "prefix": "He said that", "answer": "he had already eaten"},
            {"direct": "I don't know the answer.", "prefix": "She said that", "answer": "she didn't know the answer"},
            {"direct": "I will buy a new house.", "prefix": "He said that", "answer": "he would buy a new house"},
            {"direct": "The pizza is delicious.", "prefix": "They said that", "answer": "the pizza was delicious"},
            {"direct": "I was at home all night.", "prefix": "She said that", "answer": "she had been at home all night"},
            {"direct": "I am learning Spanish.", "prefix": "He said that", "answer": "he was learning Spanish"},
            {"direct": "My father works in a bank.", "prefix": "She said that", "answer": "her father worked in a bank"},
            {"direct": "We have seen this film before.", "prefix": "They said that", "answer": "they had seen that film before"},
            {"direct": "I don't have enough money.", "prefix": "He said that", "answer": "he didn't have enough money"},
            {"direct": "I will send the email now.", "prefix": "She said that", "answer": "she would send the email then"},
            {"direct": "The museum is closed.", "prefix": "He said that", "answer": "the museum was closed"},
            {"direct": "I am meeting a friend.", "prefix": "She said that", "answer": "she was meeting a friend"},
            {"direct": "We lived in Berlin for five years.", "prefix": "They said that", "answer": "they had lived in Berlin for five years"},
            {"direct": "I haven't seen her for ages.", "prefix": "He said that", "answer": "he hadn't seen her for ages"},
            {"direct": "I forgot my umbrella.", "prefix": "She said that", "answer": "she had forgotten her umbrella"},
            {"direct": "The cake tastes great.", "prefix": "He said that", "answer": "the cake tasted great"},
            {"direct": "I am not afraid of spiders.", "prefix": "She said that", "answer": "she was not afraid of spiders"},
            {"direct": "We will win the match.", "prefix": "They said that", "answer": "they would win the match"},
            {"direct": "I broke the vase.", "prefix": "The girl said that", "answer": "she had broken the vase"},
            {"direct": "I am feeling better today.", "prefix": "He said that", "answer": "he was feeling better that day"},
            {"direct": "My parents are coming over.", "prefix": "She said that", "answer": "her parents were coming over"},
            {"direct": "I have to go now.", "prefix": "He said that", "answer": "he had to go then"},
            {"direct": "I won't tell anyone.", "prefix": "She said that", "answer": "she wouldn't tell anyone"},
            {"direct": "The weather is beautiful.", "prefix": "They said that", "answer": "the weather was beautiful"},
            {"direct": "I didn't see the accident.", "prefix": "He said that", "answer": "he hadn't seen the accident"},
            {"direct": "I am waiting for the bus.", "prefix": "He said that", "answer": "he was waiting for the bus"},
            {"direct": "We have lived here for ten years.", "prefix": "They said that", "answer": "they had lived there for ten years"},
            {"direct": "I will do my best.", "prefix": "She said that", "answer": "she would do her best"},
            {"direct": "I didn't see you at the party.", "prefix": "He told me that", "answer": "he hadn't seen me at the party"},
            {"direct": "The water is boiling.", "prefix": "She said that", "answer": "the water was boiling"},
            {"direct": "I have already finished my breakfast.", "prefix": "He said that", "answer": "he had already finished his breakfast"},
            {"direct": "We are going to the cinema tonight.", "prefix": "They said that", "answer": "they were going to the cinema that night"},
            {"direct": "I can't swim very well.", "prefix": "She said that", "answer": "she couldn't swim very well"},
            {"direct": "I found a wallet on the street.", "prefix": "He said that", "answer": "he had found a wallet on the street"},
            {"direct": "My sister is a doctor.", "prefix": "She said that", "answer": "her sister was a doctor"},
            {"direct": "I will bring the book back tomorrow.", "prefix": "He said that", "answer": "he would bring the book back the next day"},
            {"direct": "The shops are closed on Sundays.", "prefix": "She said that", "answer": "the shops were closed on Sundays"},
            {"direct": "I am reading a very good book.", "prefix": "He said that", "answer": "he was reading a very good book"},
            {"direct": "We haven't been to the zoo yet.", "prefix": "They said that", "answer": "they hadn't been to the zoo yet"},
            {"direct": "I don't like spicy food.", "prefix": "She said that", "answer": "she didn't like spicy food"},
            {"direct": "I will call you as soon as I arrive.", "prefix": "He said that", "answer": "he would call me as soon as he arrived"},
            {"direct": "The dog is barking at the cat.", "prefix": "She said that", "answer": "the dog was barking at the cat"},
            {"direct": "I have lost my passport.", "prefix": "He said that", "answer": "he had lost his passport"},
            {"direct": "We saw a great play last night.", "prefix": "They said that", "answer": "they had seen a great play the night before"},
            {"direct": "I am not feeling very well.", "prefix": "She said that", "answer": "she was not feeling very well"},
            {"direct": "I will make a cake for your birthday.", "prefix": "He said that", "answer": "he would make a cake for my birthday"},
            {"direct": "My parents are on holiday.", "prefix": "She said that", "answer": "her parents were on holiday"},
            {"direct": "I have been working hard all day.", "prefix": "He said that", "answer": "he had been working hard all day"},
            {"direct": "We are moving to a new house.", "prefix": "They said that", "answer": "they were moving to a new house"},
            {"direct": "I didn't have time to do my hair.", "prefix": "She said that", "answer": "she hadn't had time to do her hair"},
            {"direct": "I can help you with your homework.", "prefix": "He said that", "answer": "he could help me with my homework"},
            {"direct": "The meeting starts at nine o'clock.", "prefix": "She said that", "answer": "the meeting started at nine o'clock"},
            {"direct": "I have never seen such a beautiful sunset.", "prefix": "He said that", "answer": "he had never seen such a beautiful sunset"},
            {"direct": "We don't have any milk left.", "prefix": "They said that", "answer": "they didn't have any milk left"},
            {"direct": "I am going to buy some new shoes.", "prefix": "She said that", "answer": "she was going to buy some new shoes"},
            {"direct": "I will send you a postcard from Rome.", "prefix": "He said that", "answer": "he would send me a postcard from Rome"},
            {"direct": "The car is being repaired.", "prefix": "She said that", "answer": "the car was being repaired"},
            {"direct": "I have already seen this movie twice.", "prefix": "He said that", "answer": "he had already seen that movie twice"},
            {"direct": "We played tennis for two hours.", "prefix": "They said that", "answer": "they had played tennis for two hours"},
            {"direct": "I am not happy with my new job.", "prefix": "She said that", "answer": "she was not happy with her new job"},
            {"direct": "I will be home by seven.", "prefix": "He said that", "answer": "he would be home by seven"},
            {"direct": "My computer is broken.", "prefix": "She said that", "answer": "her computer was broken"},
            {"direct": "I have forgotten my password again.", "prefix": "He said that", "answer": "he had forgotten his password again"},
            {"direct": "We are having a party next Saturday.", "prefix": "They said that", "answer": "they were having a party the following Saturday"},
            {"direct": "I don't understand the question.", "prefix": "She said that", "answer": "she didn't understand the question"},
            {"direct": "I will pay for the drinks.", "prefix": "He said that", "answer": "he would pay for the drinks"},
            {"direct": "The flight was delayed by two hours.", "prefix": "She said that", "answer": "the flight had been delayed by two hours"},
            {"direct": "I am learning how to drive.", "prefix": "He said that", "answer": "he was learning how to drive"},
            {"direct": "We haven't seen our neighbours for weeks.", "prefix": "They said that", "answer": "they hadn't seen their neighbours for weeks"},
            {"direct": "I can't go out because I have a cold.", "prefix": "She said that", "answer": "she couldn't go out because she had a cold"},
            {"direct": "I will meet you at the station.", "prefix": "He said that", "answer": "he would meet me at the station"},
            {"direct": "The music is too loud.", "prefix": "She said that", "answer": "the music was too loud"},
            {"direct": "I have just received a letter from my penfriend.", "prefix": "He said that", "answer": "he had just received a letter from his penfriend"},
            {"direct": "We are going to visit our grandparents.", "prefix": "They said that", "answer": "they were going to visit their grandparents"},
            {"direct": "I didn't like the ending of the book.", "prefix": "She said that", "answer": "she hadn't liked the ending of the book"},
            {"direct": "I must go to the dentist.", "prefix": "He said that", "answer": "he had to go to the dentist"},
            {"direct": "We are playing hide and seek.", "prefix": "They said that", "answer": "they were playing hide and seek"},
            {"direct": "I have been to Japan twice.", "prefix": "She said that", "answer": "she had been to Japan twice"},
            {"direct": "I will do the washing up later.", "prefix": "He said that", "answer": "he would do the washing up later"},
            {"direct": "The car belongs to my uncle.", "prefix": "She said that", "answer": "the car belonged to her uncle"},
            {"direct": "I don't have any brothers or sisters.", "prefix": "He said that", "answer": "he didn't have any brothers or sisters"},
            {"direct": "We visited the museum two days ago.", "prefix": "They said that", "answer": "they had visited the museum two days before"},
            {"direct": "I can play the flute.", "prefix": "She said that", "answer": "she could play the flute"},
            {"direct": "I am looking for my glasses.", "prefix": "He said that", "answer": "he was looking for his glasses"},
            {"direct": "I have just finished a marathon.", "prefix": "She said that", "answer": "she had just finished a marathon"},
            {"direct": "My friend is moving to New York.", "prefix": "He said that", "answer": "his friend was moving to New York"},
            {"direct": "We will be late for the concert.", "prefix": "They said that", "answer": "they would be late for the concert"},
            {"direct": "I saw a famous actor in the park.", "prefix": "She said that", "answer": "she had seen a famous actor in the park"},
            {"direct": "I am not interested in politics.", "prefix": "He said that", "answer": "he was not interested in politics"},
            {"direct": "The flowers smell wonderful.", "prefix": "She said that", "answer": "the flowers smelled wonderful"},
            {"direct": "I have lost my appetite.", "prefix": "He said that", "answer": "he had lost his appetite"},
            {"direct": "We are waiting for the results.", "prefix": "They said that", "answer": "they were waiting for the results"},
            {"direct": "I didn't mean to hurt your feelings.", "prefix": "She told me that", "answer": "she hadn't meant to hurt my feelings"},
            {"direct": "It is getting dark.", "prefix": "He said that", "answer": "it was getting dark"},
            {"direct": "I will buy you a present.", "prefix": "She said that", "answer": "she would buy me a present"},
            {"direct": "I have a terrible headache.", "prefix": "He said that", "answer": "he had a terrible headache"},
            {"direct": "The birds are singing.", "prefix": "She said that", "answer": "the birds were singing"},
            {"direct": "I bought this dress in London.", "prefix": "She said that", "answer": "she had bought that dress in London"},
            {"direct": "I can't remember his name.", "prefix": "He said that", "answer": "he couldn't remember his name"},
            {"direct": "We are going to the beach tomorrow.", "prefix": "They said that", "answer": "they were going to the beach the next day"},
            {"direct": "I have already cleaned the kitchen.", "prefix": "He said that", "answer": "he had already cleaned the kitchen"},
            {"direct": "I don't think it's a good idea.", "prefix": "She said that", "answer": "she didn't think it was a good idea"},
            {"direct": "I will lend you my umbrella.", "prefix": "He said that", "answer": "he would lend me his umbrella"},
            {"direct": "The soup is too salty.", "prefix": "They said that", "answer": "the soup was too salty"},
            {"direct": "I was sleeping when the phone rang.", "prefix": "She said that", "answer": "she had been sleeping when the phone rang"},
            {"direct": "I am writing a letter to my grandmother.", "prefix": "He said that", "answer": "he was writing a letter to his grandmother"},
            {"direct": "My cousin lives in Australia.", "prefix": "She said that", "answer": "her cousin lived in Australia"},
            {"direct": "We have spent all our money.", "prefix": "They said that", "answer": "they had spent all their money"},
            {"direct": "I don't feel like going out.", "prefix": "He said that", "answer": "he didn't feel like going out"},
            {"direct": "I will fix the car next week.", "prefix": "She said that", "answer": "she would fix the car the following week"},
            {"direct": "The water is too cold for swimming.", "prefix": "He said that", "answer": "the water was too cold for swimming"},
            {"direct": "I am having a great time.", "prefix": "She said that", "answer": "she was having a great time"},
            {"direct": "We traveled around Europe last summer.", "prefix": "They said that", "answer": "they had traveled around Europe the summer before"},
            {"direct": "I haven't heard from him lately.", "prefix": "He said that", "answer": "he hadn't heard from him lately"},
            {"direct": "I forgot to lock the door.", "prefix": "She said that", "answer": "she had forgotten to lock the door"},
            {"direct": "The performance starts at 8 PM.", "prefix": "He said that", "answer": "the performance started at 8 PM"},
            {"direct": "I am not ready yet.", "prefix": "She said that", "answer": "she was not ready yet"},
            {"direct": "We will enjoy the show.", "prefix": "They said that", "answer": "they would enjoy the show"},
            {"direct": "I made a mistake.", "prefix": "The student said that", "answer": "he had made a mistake"},
            {"direct": "I am working on a new project.", "prefix": "He said that", "answer": "he was working on a new project"},
            {"direct": "My parents are proud of me.", "prefix": "She said that", "answer": "her parents were proud of her"},
            {"direct": "I have to finish this by noon.", "prefix": "He said that", "answer": "he had to finish that by noon"},
            {"direct": "I won't forget your birthday.", "prefix": "She said that", "answer": "she wouldn't forget my birthday"},
            {"direct": "The movie was very boring.", "prefix": "They said that", "answer": "the movie had been very boring"},
            {"direct": "I didn't understand the instructions.", "prefix": "He said that", "answer": "he hadn't understood the instructions"}
        ],
        "Questions": [
            {"direct": "Where is the station?", "prefix": "He asked me", "answer": "where the station was"},
            {"direct": "Do you like tea?", "prefix": "She asked him if", "answer": "he liked tea"},
            {"direct": "What are you doing?", "prefix": "They asked us", "answer": "what we were doing"},
            {"direct": "Have you seen my keys?", "prefix": "He asked her if", "answer": "she had seen his keys"},
            {"direct": "Can you swim?", "prefix": "She asked me if", "answer": "I could swim"},
            {"direct": "Why did you call?", "prefix": "He asked me", "answer": "why I had called"},
            {"direct": "Will it rain tomorrow?", "prefix": "She asked if", "answer": "it would rain the next day"},
            {"direct": "Where have you been?", "prefix": "My mom asked me", "answer": "where I had been"},
            {"direct": "Is he coming to the party?", "prefix": "She asked if", "answer": "he was coming to the party"},
            {"direct": "How much does this cost?", "prefix": "He asked", "answer": "how much that cost"},
            {"direct": "Do you live here?", "prefix": "She asked me if", "answer": "I lived there"},
            {"direct": "When will the movie start?", "prefix": "He asked", "answer": "when the movie would start"},
            {"direct": "What time is it?", "prefix": "She asked me", "answer": "what time it was"},
            {"direct": "Are you busy?", "prefix": "He asked if", "answer": "I was busy"},
            {"direct": "Where did you buy that car?", "prefix": "She asked him", "answer": "where he had bought that car"},
            {"direct": "Can I help you?", "prefix": "The waiter asked if", "answer": "he could help me"},
            {"direct": "Why are you crying?", "prefix": "He asked her", "answer": "why she was crying"},
            {"direct": "Have you finished your homework?", "prefix": "The teacher asked if", "answer": "I had finished my homework"},
            {"direct": "What do you want?", "prefix": "He asked me", "answer": "what I wanted"},
            {"direct": "Did you see the news?", "prefix": "She asked if", "answer": "I had seen the news"},
            {"direct": "How often do you exercise?", "prefix": "He asked me", "answer": "how often I exercised"},
            {"direct": "Is there a bank nearby?", "prefix": "She asked", "answer": "if there was a bank nearby"},
            {"direct": "What will happen next?", "prefix": "He asked", "answer": "what would happen next"},
            {"direct": "Are they playing well?", "prefix": "She asked if", "answer": "they were playing well"},
            {"direct": "Where can I park?", "prefix": "He asked", "answer": "where he could park"},
            {"direct": "Do you have a pen?", "prefix": "She asked if", "answer": "I had a pen"},
            {"direct": "Why is the shop closed?", "prefix": "He asked", "answer": "why the shop was closed"},
            {"direct": "How did you find me?", "prefix": "She asked him", "answer": "how he had found her"},
            {"direct": "Will you be home late?", "prefix": "He asked if", "answer": "I would be home late"},
            {"direct": "Are we lost?", "prefix": "She asked if", "answer": "they were lost"},
            {"direct": "What is your name?", "prefix": "He asked me", "answer": "what my name was"},
            {"direct": "Do you speak English?", "prefix": "She asked him if", "answer": "he spoke English"},
            {"direct": "How long have you lived here?", "prefix": "He asked", "answer": "how long I had lived there"},
            {"direct": "Where are you going for vacation?", "prefix": "She asked me", "answer": "where I was going for vacation"},
            {"direct": "Can we go now?", "prefix": "They asked if", "answer": "they could go then"},
            {"direct": "What were you thinking?", "prefix": "He asked me", "answer": "what I had been thinking"},
            {"direct": "Is it cold outside?", "prefix": "She asked if", "answer": "it was cold outside"},
            {"direct": "Did you enjoy the meal?", "prefix": "The host asked if", "answer": "we had enjoyed the meal"},
            {"direct": "Why can't you come?", "prefix": "He asked me", "answer": "why I couldn't come"},
            {"direct": "Who told you that?", "prefix": "She asked", "answer": "who had told him that"},
            {"direct": "Are you coming with us?", "prefix": "He asked if", "answer": "I was coming with them"},
            {"direct": "Where does she work?", "prefix": "He asked", "answer": "where she worked"},
            {"direct": "Have you ever been to Paris?", "prefix": "She asked if", "answer": "I had ever been to Paris"},
            {"direct": "What did you say?", "prefix": "He asked me", "answer": "what I had said"},
            {"direct": "Is your father at home?", "prefix": "She asked if", "answer": "my father was at home"},
            {"direct": "How many books did you buy?", "prefix": "He asked", "answer": "how many books I had bought"},
            {"direct": "Do you like chocolate?", "prefix": "She asked if", "answer": "I liked chocolate"},
            {"direct": "Will you marry me?", "prefix": "He asked her if", "answer": "she would marry him"},
            {"direct": "What's wrong?", "prefix": "She asked", "answer": "what was wrong"},
            {"direct": "Where did I leave my phone?", "prefix": "He asked himself", "answer": "where he had left his phone"}
        ],
        "Orders and Requests": [
            {"direct": "Open the window!", "prefix": "He told me", "answer": "to open the window"},
            {"direct": "Don't touch that!", "prefix": "She warned me", "answer": "not to touch that"},
            {"direct": "Please sit down.", "prefix": "He asked us", "answer": "to sit down"},
            {"direct": "Stop talking!", "prefix": "The teacher told them", "answer": "to stop talking"},
            {"direct": "Clean your room!", "prefix": "His mother told him", "answer": "to clean his room"},
            {"direct": "Don't be late!", "prefix": "She told me", "answer": "not to be late"},
            {"direct": "Give me the book.", "prefix": "He asked me", "answer": "to give him the book"},
            {"direct": "Hurry up!", "prefix": "She told us", "answer": "to hurry up"},
            {"direct": "Please help me.", "prefix": "He asked her", "answer": "to help him"},
            {"direct": "Don't smoke here.", "prefix": "The man told us", "answer": "not to smoke there"},
            {"direct": "Wait for me!", "prefix": "She told him", "answer": "to wait for her"},
            {"direct": "Listen carefully.", "prefix": "The speaker told the audience", "answer": "to listen carefully"},
            {"direct": "Don't forget the milk.", "prefix": "She reminded me", "answer": "not to forget the milk"},
            {"direct": "Eat your vegetables!", "prefix": "The father told the child", "answer": "to eat his vegetables"},
            {"direct": "Please call me later.", "prefix": "She asked me", "answer": "to call her later"},
            {"direct": "Don't park here.", "prefix": "The officer told him", "answer": "not to park there"},
            {"direct": "Show me your passport.", "prefix": "The official told her", "answer": "to show him her passport"},
            {"direct": "Be quiet!", "prefix": "He told them", "answer": "to be quiet"},
            {"direct": "Don't tell anyone.", "prefix": "She told me", "answer": "not to tell anyone"},
            {"direct": "Turn off the lights.", "prefix": "He told us", "answer": "to turn off the lights"},
            {"direct": "Please lend me some money.", "prefix": "He asked his friend", "answer": "to lend him some money"},
            {"direct": "Don't drink the water.", "prefix": "They warned us", "answer": "not to drink the water"},
            {"direct": "Fasten your seatbelts.", "prefix": "The pilot told the passengers", "answer": "to fasten their seatbelts"},
            {"direct": "Come here!", "prefix": "The boss told me", "answer": "to come there"},
            {"direct": "Don't make a mess.", "prefix": "She told the kids", "answer": "not to make a mess"},
            {"direct": "Take a deep breath.", "prefix": "The doctor told him", "answer": "to take a deep breath"},
            {"direct": "Please send me the file.", "prefix": "She asked him", "answer": "to send her the file"},
            {"direct": "Don't look back.", "prefix": "He told her", "answer": "not to look back"},
            {"direct": "Put the gun down!", "prefix": "The police told him", "answer": "to put the gun down"},
            {"direct": "Read the instructions.", "prefix": "She told me", "answer": "to read the instructions"},
            {"direct": "Don't feed the animals.", "prefix": "The sign told us", "answer": "not to feed the animals"},
            {"direct": "Follow me.", "prefix": "The guide told them", "answer": "to follow him"},
            {"direct": "Please be patient.", "prefix": "She asked us", "answer": "to be patient"},
            {"direct": "Don't worry so much.", "prefix": "He told me", "answer": "not to worry so much"},
            {"direct": "Sign the document.", "prefix": "The lawyer told her", "answer": "to sign the document"},
            {"direct": "Don't scream.", "prefix": "He told her", "answer": "not to scream"},
            {"direct": "Buckle up!", "prefix": "The driver told the passengers", "answer": "to buckle up"},
            {"direct": "Don't open the door.", "prefix": "She told him", "answer": "not to open the door"},
            {"direct": "Try again.", "prefix": "The coach told me", "answer": "to try again"},
            {"direct": "Please hold the line.", "prefix": "The secretary asked him", "answer": "to hold the line"},
            {"direct": "Don't use your phone.", "prefix": "The teacher told the students", "answer": "not to use their phones"},
            {"direct": "Go to bed!", "prefix": "The mother told the boy", "answer": "to go to bed"},
            {"direct": "Don't jump!", "prefix": "They told him", "answer": "not to jump"},
            {"direct": "Pass the salt, please.", "prefix": "He asked her", "answer": "to pass the salt"},
            {"direct": "Don't cry over spilled milk.", "prefix": "She told me", "answer": "not to cry over spilled milk"},
            {"direct": "Watch your step.", "prefix": "He told us", "answer": "to watch our step"},
            {"direct": "Don't run across the street.", "prefix": "The father told his son", "answer": "not to run across the street"},
            {"direct": "Tell me the truth.", "prefix": "She told him", "answer": "to tell her the truth"},
            {"direct": "Don't drive so fast.", "prefix": "She told him", "answer": "not to drive so fast"},
            {"direct": "Please bring some wine.", "prefix": "He asked them", "answer": "to bring some wine"}
        ]
    }

# --- SESSION STATE MANAGEMENT ---
if 'step' not in st.session_state:
    st.session_state.step = "menu"
if 'current_pool' not in st.session_state:
    st.session_state.current_pool = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'last_category' not in st.session_state:
    st.session_state.last_category = "Mix"
if 'feedback' not in st.session_state:
    st.session_state.feedback = None

# --- FUNKTIONEN ---
def start_exercise(category):
    st.session_state.last_category = category
    if category == "Mix":
        full_pool = st.session_state.data["Statements"] + \
                    st.session_state.data["Questions"] + \
                    st.session_state.data["Orders and Requests"]
    else:
        full_pool = st.session_state.data[category]
    
    # Ziehe 15 zufällige Sätze ohne Dubletten
    st.session_state.current_pool = random.sample(full_pool, min(15, len(full_pool)))
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.step = "quiz"
    st.session_state.feedback = None

def check_answer(user_input, correct_answer):
    if user_input.strip().lower() == correct_answer.strip().lower():
        st.session_state.score += 1
        st.session_state.feedback = ("success", "Richtig!")
    else:
        st.session_state.feedback = ("error", f"Leider falsch. Richtig wäre: {st.session_state.current_pool[st.session_state.index]['prefix']} {correct_answer}")

def next_question():
    st.session_state.index += 1
    st.session_state.feedback = None
    if st.session_state.index >= 15:
        st.session_state.step = "result"

# --- UI LAYOUT ---
st.title("🇬🇧 Reported Speech Trainer")
st.markdown("Übe den Backshift (Reporting Verb in the Past)")

if st.session_state.step == "menu":
    st.subheader("Was möchtest du üben?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Statements", use_container_width=True): start_exercise("Statements")
        if st.button("Questions", use_container_width=True): start_exercise("Questions")
    with col2:
        if st.button("Orders and Requests", use_container_width=True): start_exercise("Orders and Requests")
        if st.button("Mix (Alles zusammen)", use_container_width=True): start_exercise("Mix")

elif st.session_state.step == "quiz":
    current_q = st.session_state.current_pool[st.session_state.index]
    
    st.write(f"**Satz {st.session_state.index + 1} von 15** | Punkte: {st.session_state.score}")
    st.info(f"Direkte Rede: **\"{current_q['direct']}\"**")
    
    # Eingabefeld
    user_input = st.text_input(f"{current_q['prefix']} ...", key=f"input_{st.session_state.index}")
    
    if st.session_state.feedback is None:
        if st.button("Prüfen"):
            check_answer(user_input, current_q['answer'])
            st.rerun()
    else:
        # Feedback anzeigen
        type, msg = st.session_state.feedback
        if type == "success": st.success(msg)
        else: st.error(msg)
        
        if st.button("Nächster Satz"):
            next_question()
            st.rerun()

elif st.session_state.step == "result":
    st.balloons()
    st.subheader("Training beendet!")
    st.write(f"Du hast **{st.session_state.score} von 15** Sätzen korrekt umgewandelt.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Noch mal 15 Sätze", use_container_width=True):
            start_exercise(st.session_state.last_category)
            st.rerun()
    with col2:
        if st.button("Zurück zum Hauptmenü", use_container_width=True):
            st.session_state.step = "menu"
            st.rerun()

```

### Wie du die App ausführst:

1. Installiere Python (falls nicht vorhanden).
2. Installiere Streamlit über das Terminal/CMD: `pip install streamlit`.
3. Speichere den Code oben als `app.py`.
4. Starte die App im Terminal mit: `streamlit run app.py`.

Die App öffnet sich dann automatisch in deinem Browser. Viel Erfolg beim Üben mit deinen Schülern!

Soll ich dir noch zeigen, wie du das Design (z.B. Farben oder Schriftarten) anpassen kannst?