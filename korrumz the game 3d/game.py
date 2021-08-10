from ursina import *
import threading, random, json
import multiplayer
from rpc import DiscordRPC
from objects import PlayerMe, Leaderboard

app = Ursina()
application.hot_reloader.hotkeys = {}

window.title = "korrumz the game 3d"
window.icon = "assets/korrumz.ico"
window.fullscreen = True
window.fps_counter.enabled = False
window.cog_button.enabled = False
window.exit_button.visible = False

player_me = None
leaderboard = Leaderboard()
discord_rpc = None

running = False

username_text = Text(text="Wpisz swój nick i wciśnij enter", origin=(0, 0), background=True)
username = InputField(y=-0.1)

def input(key):
    global running

    if not running and key == "enter":
        running = True
        run_game(username.text)
        destroy(username_text)
        destroy(username)
        time.sleep(1)

    elif not running and key == "escape":
        exit(0)

    if not running: return

    if key == "escape":
        multiplayer.ws.close()
        discord_rpc.running = False
        exit(0)

    elif key in ("tab", "tab hold"):
        if not leaderboard.visible:
            leaderboard.visible = True

    elif key == "tab up":
        if leaderboard.visible:
            leaderboard.visible = False

    elif key.split()[0] in ("w", "a", "s", "d"):
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

def run_game(username):
    global player_me, discord_rpc

    Sky(texture="assets/korrumz.png")
    Entity(model="plane", color=color.hex("202020"), collider="box", position=(1920 / 2, 0, 1080 / 2), scale=(1920, 0, 1080))
    Entity(model="cube", collider="box", position=(1920 / 2, 3 / 2, 0), scale=(1920, 3, 0))
    Entity(model="cube", collider="box", position=(0, 3 / 2, 1080 / 2), scale=(0, 3, 1080))
    Entity(model="cube", collider="box", position=(1920 / 2, 3 / 2, 1080), scale=(1920, 3, 0))
    Entity(model="cube", collider="box", position=(1920, 3 / 2, 1080 / 2), scale=(0, 3, 1080))
    Audio("assets/music/audio_epyk_muzik.ogg", autoplay=True, loop=True, volume=0.01)

    player_me = PlayerMe(username, random.randint(0, 1920), random.randint(0, 1080), random.randint(1, 20))
    discord_rpc = DiscordRPC(player_me, multiplayer)

    threading.Thread(target=multiplayer.run_multiplayer, args=(player_me, leaderboard, discord_rpc)).start()
    threading.Thread(target=discord_rpc.run).start()
    discord_rpc.update()

app.run()