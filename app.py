from flask import Flask #, render_template, session, copy_current_request_context
# from flask_socketio import SocketIO, emit, disconnect
# import socket 
# import threading
from flask_sock import Sock
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration


app = Flask(__name__)
sock = Sock(app)
# async_mode = None
# app.config['SECRET_KEY'] = 'secret!'
# socket_ = SocketIO(app, async_mode=async_mode)
# thread = None
# thread_lock = threading.Lock()

# HEADER = 64
# PORT = 5050
# SERVER = '127.0.0.1'
# ADDR = (SERVER, PORT)
# FORMAT = 'utf-8'
# DISCONNECT_MESSAGE = "!DISCONNECT"

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(ADDR)

# def handle_client(conn, addr):
#     print(f"[NEW CONNECTION] {addr} connected.")

#     connected = True
#     while connected:
#         msg_length = conn.recv(HEADER).decode(FORMAT)
#         if msg_length:
#             msg_length = int(msg_length)
#             msg = conn.recv(msg_length).decode(FORMAT)
#             if msg == DISCONNECT_MESSAGE:
#                 connected = False

#             print(f"[{addr}] {msg}")
#             conn.send("Msg received".encode(FORMAT))

#     conn.close()

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

    #     text = request.form['text']
    # print('user:', text)
    # inputs = tokenizer(text, return_tensors="pt")
    # res = model.generate(**inputs)
    # reply = tokenizer.decode(res[0])
    # reply = reply.replace('<s>', '')
    # reply = reply.replace('</s>', '')
    # print('bot:', reply)
    # return my_form(text)

    # return render_template('index.html', async_mode=socket_.async_mode)

# @socket_.on('my_event', namespace='/test')
# def test_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']})

# @socket_.on('my_broadcast_event', namespace='/test')
# def test_broadcast_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']},
#          broadcast=True)

# @socket_.on('disconnect_request', namespace='/test')
# def disconnect_request():
#     @copy_current_request_context
#     def can_disconnect():
#         disconnect()

#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'Disconnected!', 'count': session['receive_count']},
#          callback=can_disconnect)


#if __name__ == '__main__':
    # socket_.run(app, debug=True)
    # app.run()
