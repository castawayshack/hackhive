import pandas as pd
import nltk
import numpy as np
import string
import warnings
import requests
import pickle
import random
import json
import os
import telebot

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = [["What is the theme of the hackathon?.",0],["What are the themes of the hackathon?",0],
        ["When does the hackathon take place?",1],
        ["What is the prize for the winning team?",2],["what do the winners get?",2],["Are there any prizes for the hackathon?",2],
        ["When does the registration for the hackathon close?",3],["When is the registration deadline for the hackathon?",3],["Is there a registration deadline?",3],["Hackathon registration deadline?",3],
        ["Who are the sponsors of the hackathon?",4],["Who is sponsoring the Hackathon?",4],["Do we have big prizes for the hackathon?",4],[" Is there any prize for the winning team of the hackathon?",4],
        ["When is the hackathon taking place?",5],["What is the schedule for the hackathon?",5],["Could you give me a detail schedule for the hackathon?",5],["Hackathon schedule?",5], ["What is the format of the hackathon event?",5],
        ["I have a general question about the hackathon, who can I contact for more information?",6],["Who do I contact for general enquiries?",6],["Could I have the organizing comittee's email for further contact?",6],
        ["What is the eligibility criteria?",7],["Does the hackathon have any eligibility criteria?",7],["Are their any age limits?",7],["Can anyone take part in the hackathon?",7],
        ["What is hackathons code of conduct and rules ?",8],["Cocs",8],["cocs?",8],["Code of Conduct?",8],
        ["Can I use pre-existing code in my hackathon project?",9],["Can i used pre-existing modules?",9], ["Can I use existing APIs?",9],
        ["What is the judging criteria?",10],["Can you tell us about the judging criteria?",10],["Is there any judging criteria you could inform us about?",10],["What are the rules of the hackathon?",11],["Could I know the rules of the hackathon?",11],["I would like to know about the rules please",11],["Could we get tips for the hackathons?",12],["Any tips?",12],["Do you have any advice for newbies?",12]]

df = pd.DataFrame(data, columns = ["Text","Intent"])
df

# Lemmitization

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def Normalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

x = df['Text']
y = df['Intent']

vectorizer = TfidfVectorizer(tokenizer=Normalize,stop_words = 'english')

X = vectorizer.fit_transform(x)

# training a Naive Bayes classifier 
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(X, y) 

X_test = ["hackathon"]
prediction = lr.predict(vectorizer.transform(X_test))

prediction

# To get the probability of test data to be present in each Intent

a = lr.predict_proba(vectorizer.transform(X_test))
a

responses = {0 : {"intent":"theme","response":['The theme of the hackathon is Sustainability in AI','The different themes of the hackathon are open innovation and NLP, computer vision, robotics and automation, ML in healthcare, AI powered Smart Cities,AI in Finance and Trading, AI-powered Autonomous Vehicles, AI in Agriculture and Environment, AI in Gaming and Entertainment, AI in Supply Chain and Logistics.',]}, 
      1 : {"intent":"date","response":['The hackathon takes place on the weekend of April 10th-11th',]},
      2 : {"intent":"prize","response":['The prizes for the hackathon include $5000 for the winning team, $2500 for 1st runner up, $1000 for 2nd runner up, and also prizes for sponsor tracks.',]},
      3 : {"intent":"deadline","response":['The registration for the hackathon ends on January 1st']},
      4 : {"intent":"sponsors","response":['The sponsors of the hackathon are ABC, XYZ, IJK, KLP, RYT, HGD, WIJ, SOF']},
      5 : {"intent":"schedule","response":['The hackathon is taking place from January 5th to January 9th.','The Hackathon Schedule is as follows-\n3rd Jan - Shortlisted Ideas Declaration\n4th Jan - Online Idea Pitching: This is the first round of the hackathon, where participants present their ideas to a panel of judges. The judges will then select the top ideas to move on to the next round.\n5th Jan to 6th Jan - Hack Period: This is the main round of the hackathon, where participants work on their selected ideas to develop a working prototype or solution. This round typically lasts for several hours or even a few days, depending on the length of the hackathon.\n7th Jan - Demos: The final round of the hackathon, where participants present their finished solutions to a panel of judges. The judges will then select the winning teams based on the criteria such as originality, feasibility, and impact.\nEach round is eliminative, meaning that not all teams will advance to the next round. Only the top teams from each round will move on to the next round until a winner is chosen.']},
      6 : {"intent":"contact","response":['You can contact the hackathon organizers for more information at generalinfo@gmail.com',]},
      7 : {"intent":"eligibility","response":["The Eligibility criteria are: \n\t1. Participants must be currently enrolled as full-time students in an accredited college or university.\n\t2. Participants must have a valid ID or passport to verify their identity and age.\n\t3. Participants must be able to provide proof of enrollment in a college or university.\n\t4. Participants must be able to attend the entire duration of the hackathon.\n\t5. Participants must agree to abide by the hackathon's code of conduct and rules.\n\t6. Participants must have necessary permissions from their respective college/university to participate in the event.",]},
      8 : {"intent":"coc","response":['Code of Conduct: 1. All participants must abide by the rules and regulations of the hackathon. 2. All participants must respect the rights and dignity of others, including but not limited to, participants, staff, and judges. 3. Discrimination, harassment, or any form of misconduct will not be tolerated. This includes but is not limited to, discrimination based on race, gender, sexual orientation, religion, national origin, age, or disability. 4. All participants must refrain from cheating or any form of dishonesty. 5. The use of drugs or alcohol during the hackathon is strictly prohibited. 6. Participating in the hackathon grants the organizers the right to use their names and images for promotional purposes.']},
      9 : {"intent":"pre-existing code","response":['You are allowed to use pre-existing code in your hackathon project as long as it is properly cited.','You are permitted to use pre-existing libraries for your submissions, however no plagiarism would be tolerated.']},
      10 : {"intent":"judging","response":["The judging criteria includes factors such as the innovation and originality of the idea, the potential impact and feasibility of the solution, the technical execution and execution of the idea, the overall design and user experience, and the team's ability to present and communicate their idea effectively",]},
      11 : {"intent":"rules","response": ["Rules: \n\t1. The hackathon is open to all college students. \n\t2. Each team can have a maximum of 4 members.\n\t3. The hackathon will be held on a designated date and time, and all participants must be present for the duration of the event.\n\t4. Each team must submit a working prototype or proof of concept of their hack by the end of the hackathon.\n\t5. The judges' decision is final and binding.\n\t6. Prizes will be awarded to the top teams as determined by the judges.\n\t7. The organizers reserve the right to modify the rules or code of conduct at any time without notice.\n\t8. All participants must respect the intellectual property rights of others. \n\t9. Each team has to submit their final code on Git or any other platform before the end of the hackathon.\n\t10. Plagiarism is not allowed and any team found guilty of plagiarism will be disqualified."]},
      12 : {"intent":"tips","response": ["Here are some tips for hackathon participants:\n\tStart early: Plan and start working on your idea as soon as possible to make the most of the time available.\n\tNetwork: Meet other participants, form teams, and build relationships with mentors and industry experts.\n\tFocus on the problem: Make sure you understand the problem you're trying to solve and keep that in mind throughout the hackathon.\n\tStay organized: Keep track of your progress and make sure your team is on the same page.\n\tKeep it simple: Avoid overcomplicating your solution and focus on creating a minimum viable product (MVP).\n\tGet enough rest: Make sure to take breaks and get enough sleep to stay fresh and focused.\n\tPractice presentation skills: Be prepared to present your solution to a panel of judges, so practice your pitch and presentation skills.\n\tHave fun: Remember to have fun and enjoy the experience. You'll learn a lot and make great memories."]},   
      13 : {"intent": "confusion", "response":["Ummm! Please rephrase your sentence. I am not that smart."] }}


#class telegram_bot():
#    def __init__(self):
#      API_KEY = os.environ['API_KEY']
#      token = API_KEY
#      self.token= token 
#      self.url = f"https://api.telegram.org/bot{self.token}"

#    def get_updates(self,offset=None):
#        url = self.url+"/getUpdates?timeout=100"
#        if offset:
#            url = url+f"&offset={offset+1}"
#        url_info = requests.get(url)
#        return json.loads(url_info.content)
#    def send_message(self,msg,chat_id):
#        url = self.url + f"/sendMessage?chat_id={chat_id}&text={msg}"
#        if msg is not None:
#            requests.get(url)

#    def grab_token(self):
#      return tokens


# To get responnse

bot = telebot.TeleBot(API_KEY)

def response(user_response):
    text_test = [user_response]
    X_test = vectorizer.transform(text_test)
    prediction = lr.predict(X_test)
    reply = random.choice(responses[prediction[0]]['response'])
    return reply

# To get indent
def intent(user_response):
    text_intent = [user_response]
    X_test_intent = vectorizer.transform(text_intent)
    predicted_intent = lr.predict(X_test_intent)
    intent_predicted = responses[predicted_intent[0]]['intent']
    return intent_predicted

def bot_initialize(user_msg):
    flag=True
    while(flag==True):
        user_response = user_msg
        
        user_intent = intent(user_response)
        
        if(user_intent != 'goodbye'):
            if(user_response == '/start'):
                resp = """Hi! There. I am Habot-your guide for solving all of your hackathon queries. I can accept your registration, answer your questions, and show you tutorials as well as resources to help you on your hackathon journey.\nType Bye to Exit."""
                return resp
            
            elif (user_intent == 'theme'):
                resp = str(random.choice(responses[0]['response'])) + ", Awaiting the great ideas you would be bringing to the table."
                return resp
              
            elif(user_intent == 'date'):
                resp = random.choice(responses[1]['response'])
                return resp
            
            elif(user_intent == 'prize'):
                resp = random.choice(responses[2]['response'])
                return resp

            elif(user_intent == 'deadline'):
                resp = random.choice(responses[3]['response'])
                return resp
              
            elif(user_intent == 'sponsors'):
                resp = random.choice(responses[4]['response'])
                return resp
        
            elif(user_intent == 'schedule'):
                resp = random.choice(responses[5]['response'])
                return resp

            elif(user_intent == 'contact'):
                resp = random.choice(responses[6]['response'])
                return resp
            
            elif(user_intent == 'eligibility'):
                resp = random.choice(responses[7]['response'])
                return resp
              
            elif(user_intent == 'coc'):
                resp = random.choice(responses[8]['response'])
                return resp
            
            elif(user_intent == 'pre-existing code'):
                resp = random.choice(responses[9]['response'])
                return resp
              
            elif(user_intent == 'judging'):
                resp = random.choice(responses[10]['response'])
                return resp

            elif(user_intent == 'rules'):
                resp = random.choice(responses[11]['response'])
                return resp

            elif(user_intent == 'tips'):
                resp = random.choice(responses[12]['response'])
                return resp

          #elif(user_intent == "flowers"):
           #     user_response=user_response.lower()
            #    resp = "I will suggest you to give :-\n " + response(user_response)
             #   return resp
            
            else:
                resp = "Ummm! Please rephrase your sentence. I am not that smart."
                return resp
            
        else:
            flag = False
            resp = random.choice(responses[13]['response'])
            return resp



