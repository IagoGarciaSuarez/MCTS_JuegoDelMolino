# from fastapi import WebSocket
# destUri = "ws://127.0.0.1:8000/ws/"

# ws = WebSocket(destUri)

# ws.send('hello world')
# r = ws.receive()
# print(r)


import websocket
import json

destUri = "ws://127.0.0.1:8000/newgame"

def on_msg(ws, msg):
    print(msg)
    msg = json.loads(msg)
    if msg["success"]:
        print('bien')
    else:
        print('mal')
    ws.close()
def on_close():
    print('bye')
def on_open(ws):
    print("ANTES DE ENVIAR")
    ws.send('{"greet": "hello world"}')
    print("ENVIADO")

ws = websocket.WebSocketApp(destUri, on_message=on_msg, on_open=on_open)
ws.run_forever()