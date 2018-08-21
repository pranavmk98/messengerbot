# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.comparisons import *

import conversation_pal
import queue
import threading
q = queue.Queue()

class MessageThread(threading.Thread):        

    def __init__(self, chatbot, message):
        self.message = message
        self.chatbot = chatbot
        super(MessageThread, self).__init__()

    def run(self):
        print("Thinking")
        response = self.chatbot.get_response(self.message)
        # print("Inserting response in queue")
        q.put(response)
        return

# Create a new chat bot named Bob
def create():
    chatbot = ChatBot(
        'Bob',
        trainer = 'chatterbot.trainers.ListTrainer',
        storage_adapter = "chatterbot.storage.MongoDatabaseAdapter",
        logic_adapters= [
            {
                "import_path": "chatterbot.logic.BestMatch",
                # "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
                "response_selection_method": "chatterbot.response_selection.get_first_response"
            }
        ],
        preprocessors = [
            'chatterbot.preprocessors.convert_to_ascii'
        ],
        # database = 'blank_slate1'
        # statement_comparison_function = jaccard_similarity,
    )
    return chatbot

def train(chatbot):
    c = []
    for i in conversation_pal.convo:
        c.append(i.encode("utf-8", "ignore"))
    chatbot.train(c)

def output_message(chatbot):
    while True:
        print("Response: " + str(q.get().text[2:-1]))
        q.task_done()

# chatbot = create()
# sender = threading.Thread(target=output_message, args=(chatbot,))
# sender.start()

# while True:
#     x = input()
#     thr = MessageThread(chatbot, x)
#     thr.start()
#     response = chatbot.get_response(x)