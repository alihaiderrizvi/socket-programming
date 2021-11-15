from flask import Flask
from flask_sock import Sock
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

app = Flask(__name__)
sock = Sock(app)

@sock.route('/')
def bot_chat(ws):
    print('making model . . .')
    tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
    model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")
    print('ready to chat!')
    
    flag = True
    while flag:
        message = ws.receive()
        print('user:', message)
        if message == 'disconnect':
            flag = False
            break
        inputs = tokenizer(message, return_tensors="pt")
        res = model.generate(**inputs)
        reply = tokenizer.decode(res[0])
        reply = reply.replace('<s>', '')
        reply = reply.replace('</s>', '')
        print('bot:', reply)
        ws.send(reply)