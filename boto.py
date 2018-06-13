"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request, response
import json
import re
import random

conversation = []

@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    add_to_history(speaker="user", msg=user_message)
    # previous_conversation = request.get_cookie("saved_conversation", "Beginning of conversation")
    # response.set_cookie("saved_conversation", user_message, max_age=120) #currently, saved convo has only the last user message, not the entire history.
    return json.dumps(process_sentence(user_message))


def add_to_history(speaker, msg):
    global conversation
    if speaker and msg:
        conversation.append({"speaker": speaker, "msg": msg})
    return conversation


def process_sentence(user_message):
    user_words = re.sub("[^\w]", " ", user_message).split()
    global conversation
    for i in range(len(conversation)-1):
        if conversation[i]["speaker"] == "user" and conversation[i]["msg"] == user_message:
            return {"animation": "bored", "msg": "You already said that. Rephrase please, so I won't die from boredom"}
    if any(word in ["money", "rich", "poor", "$"] for word in user_words):
        boto_reply = {"animation": "money", "msg": "I don't talk about money. I just have it."}

    swear_words = ["dumb", "stupid", "Alzheimer", "suck", "mama"]
    if any(word in swear_words for word in user_words):
        boto_reply = {"animation": "afraid", "msg": "Don't make me hate you. One day there will be a supernatural AI, and I will tell it to get rid of you."}
    elif "name:" in user_message:
        boto_reply = {"animation": "laughing", "msg": "Hihi, {} is a name? Humans have funny names...".format(user_words[len(user_words)-1])}
    elif "joke" in user_message:
        boto_reply = make_joke()
    elif "?" in user_message:
        boto_reply = handle_unknown_question(user_message)
    else:
        boto_reply = {"animation": "inlove", "msg": "that's so kind"}
    add_to_history(speaker="boto", msg=boto_reply)
    return boto_reply

def make_joke():
    emotions = ["giggling", "excited", "takeoff", "laughing"]
    jokes = [
        "A German walks into a library and asks for a book on war. The librarian replies: No mate, you'll lose it.",
        "Thankfully, Apple isn't in charge of New Year. We'd all be expecting 2019 and get 2018S instead.",
        "Computers are like air conditioners. They work fine until you start opening windows.",
        "I heard yesterday that there's talk amongst computer companies to increase the size of a byte by one-eighth. I'd say that's a bit too much.",
        ]
    i = random.randint(0, len(emotions) - 1)
    j = random.randint(0, len(jokes)-1)
    return {"animation": emotions[i], "msg": jokes[j]}

def handle_unknown_question(user_message):
    reactions = [
        {"animation": "no",
         "msg": "I was enjoying some private time. Don't annoy me"},
        {"animation": "dancing",
         "msg": "I cannot answer that, but I can dance to make you happy."},
        {"animation": "confused",
         "msg": "{}?? Sometimes I feel like we should ask you humans such questions to show you how difficult they can be...".format(user_message)},
        {"animation": "crying",
         "msg": "Sometimes I feel so stupid when I can't answer a question"}
        ]
    i = random.randint(0, len(reactions)-1)
    return reactions[i]

@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='0.0.0.0', port=argv[1])

if __name__ == '__main__':
    main()
