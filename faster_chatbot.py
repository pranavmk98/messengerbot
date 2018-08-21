from Crypto.Cipher import AES
from fbchat import log, Client
from fbchat.models import *
from queue import Queue

import chat
import threading

running = True
q = Queue()

class MessageThread(Thread):        

    def __init__(self, chatbot, message, thread_id, thread_type):
        self.message = message
        self.chatbot = chatbot
        self.thread_id = thread_id
        self.thread_type = thread_type
        super(MessageThread, self).__init__()

    def run(self):
        response = self.chatbot.get_response(self.message)
        q.put((response, self.thread_id, self.thread_type))
        return

# Subclass fbchat.Client and override required methods
class EchoBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        global running
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        # log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
        print(message_object.text)
        print(thread_id)

        # If you're not the author, echo
        if int(thread_id) == 100018707857490:
            if message_object.text == 'start':
                running = True
            elif message_object.text == 'stop':
                print('Stopping')
                running = False
        elif author_id != self.uid and thread_type == ThreadType.USER and running:
            thr = MessageThread(chatbot, message_object.text[2:-1], thread_id, thread_type)
            print("Thinking of response")
            thr.start()
            # response = chatbot.get_response(message_object.text).text[2:-1]
            self.send(m, thread_id=thread_id, thread_type=thread_type)

def send_message(object):
    while True:
        response, thread_id, thread_type = q.get()
        m = Message(text=str(response))
        print("Sending response: " + srt(response))
        object.send(m, thread_id=thread_id, thread_type=thread_type)
        q.task_done()

pwd = input() # Input password
client = EchoBot("pranavmk98@gmail.com", pwd)

sender = threading.Thread(target=send_message, args=client)
sneder.start()
chatbot = chat.create()
# chat.train(chatbot)
client.listen()