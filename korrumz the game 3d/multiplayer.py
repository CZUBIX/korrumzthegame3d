from ursina import *
import websocket, json
from objects import Player, Bug
from sys import exit

ws = websocket.WebSocketApp("wss://ws.korrumzthegame.cf")

players = []
bugs = []

def run_multiplayer(player_me, leaderboard, discord_rpc):
    global players, bugs

    def on_open(ws):
        data = {
            "event": "new player",
            "data": {
                "username": player_me.username,
                "x": player_me.x,
                "y": player_me.y,
                "canvasWidth": 5000,
                "canvasHeight": 5000,
                "imageNumber": player_me.image_number
            }
        }

        data = json.dumps(data)
        ws.send(data)

    def on_message(ws, msg):
        msg = json.loads(msg)
        data = msg["data"]
        p = None

        for player in players + [player_me]:
            if "username" in data and player.username == data["username"]:
                p = player

        if msg["event"] == "new player":
            players.append(Player(data["username"], data["x"], data["y"], data["pullRequests"], data["imageNumber"]))
            discord_rpc.update()

        elif msg["event"] == "new username":
            player_me.username = data["username"]
            discord_rpc.update()

        elif msg["event"] == "new image":
            player_me.image_number = data["imageNumber"]
            discord_rpc.update()

        elif msg["event"] == "move":
            p.position = (data["x"], 5, data["y"])
            if not p == player_me:
                p.username_object.position = (data["x"], 10, data["y"])

        elif msg["event"] == "new bug":
            bugs.append(Bug(data["x"], data["y"], data["imageNumber"]))

        elif msg["event"] == "pull request":
            b = None

            for bug in bugs:
                if (bug.position, bug.image_number) == (Vec3(data["bug"]["x"], 2, data["bug"]["y"]), data["bug"]["imageNumber"]):
                    b = bug
            
            bugs.remove(b)
            destroy(b)
            p.pull_requests = data["pullRequests"]

            discord_rpc.update()

        elif msg["event"] == "new gban":
            if data["username"] == player_me.username:
                ws.close()
                player_me.running = False
                discord_rpc.running = False

        elif msg["event"] == "player disconnected":
            players.remove(p)
            destroy(p.username_object)
            destroy(p)

            discord_rpc.update()

        leaderboard.text = "<scale:1.2>Pull requesty:<scale:1>\n\n" + "\n".join([f"{player.username if not player == player_me else player.username + ' (ty)'} {player.pull_requests}" for player in sorted(players + [player_me], reverse=True, key=lambda player: player.pull_requests)])
        leaderboard.create_background()

    ws.on_open = on_open
    ws.on_message = on_message
    ws.run_forever()