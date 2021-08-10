from ursina import *
import threading, random, json
import multiplayer
from rpc import DiscordRPC
from objects import PlayerMe, Leaderboard
from sys import exit

app = Ursina()

settings = json.load(open("settings/settings.json", "r"))

window.title = "korrumz the game 3d"
window.icon = "assets/korrumz.ico"
window.fullscreen = True
window.vsync = settings["vsync"]
window.fps_counter.enabled = False
window.cog_button.enabled = False
window.exit_button.visible = False

application.hot_reloader.hotkeys = {
    settings["fps_counter"]: lambda: setattr(window.fps_counter, "enabled", not window.fps_counter.enabled)
}

player_me = None
leaderboard = Leaderboard()
discord_rpc = None

running = False

username_text = Text(text="Wpisz swój nick i wciśnij enter", origin=(0, 0), background=True)
username = InputField(y=-0.1)

def sendloop():
    before = player_me.position

    while running and player_me.running:
        if not before == player_me.position:
            if player_me.position[0] < 0 or player_me.position[0] > 1920:
                player_me.position = (random.randint(0, 1920), 5, player_me.position[2])
            if player_me.position[2] < 0 or player_me.position[2] > 1080:
                player_me.position = (player_me.position[0], 5, random.randint(0, 1080))
            
            before = player_me.position

            data = {
                "event": "move",
                "data": {
                    "username": player_me.username,
                    "x": player_me.position[0],
                    "y": player_me.position[2]
                }
            }

            data = json.dumps(data)
            multiplayer.ws.send(data)

        time.sleep(0.044)

def input(key):
    global running

    if not running and key == "enter":
        running = True
        run_game(username.text)
        destroy(username_text)
        destroy(username)
        time.sleep(1)

    elif not running and key == settings["exit"]:
        running = False
        exit(0)

    if not running: return

    if key == settings["exit"]:
        multiplayer.ws.close()
        player_me.running = False
        discord_rpc.running = False
        exit(0)

    elif key in (settings["leaderboard"], settings["leaderboard"] + " hold"):
        if not leaderboard.visible:
            leaderboard.visible = True

    elif key == settings["leaderboard"] + " up":
        if leaderboard.visible:
            leaderboard.visible = False

def run_game(username):
    global player_me, discord_rpc

    Sky(texture="assets/korrumz.png")
    Entity(model="plane", color=color.hex("202020"), collider="box", position=(1920 / 2, 0, 1080 / 2), scale=(1920, 0, 1080))
    Entity(model="cube", collider="box", position=(1920 / 2, 10 / 2, 0), scale=(1920, 10, 0))
    Entity(model="cube", collider="box", position=(0, 10 / 2, 1080 / 2), scale=(0, 10, 1080))
    Entity(model="cube", collider="box", position=(1920 / 2, 10 / 2, 1080), scale=(1920, 10, 0))
    Entity(model="cube", collider="box", position=(1920, 10 / 2, 1080 / 2), scale=(0, 10, 1080))
    Audio("assets/music/audio_epyk_muzik.ogg", autoplay=True, loop=True, volume=0.01)

    player_me = PlayerMe(username, random.randint(0, 1920), random.randint(0, 1080), random.randint(1, 20))
    player_me.mouse_sensitivity = (settings["sensitivityX"], settings["sensitivityY"])
    discord_rpc = DiscordRPC(player_me, multiplayer)
    discord_rpc.enabled = settings["rpc_enabled"]

    threading.Thread(target=multiplayer.run_multiplayer, args=(player_me, leaderboard, discord_rpc)).start()
    threading.Thread(target=sendloop).start()
    threading.Thread(target=discord_rpc.run).start()
    discord_rpc.update()

app.run()