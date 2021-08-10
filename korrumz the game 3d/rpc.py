from discordsdk import Discord, CreateFlags, Activity
import time

class DiscordRPC:
    def __init__(self, player_me, multiplayer):
        self.app_id = 874435457038053447

        self.player_me = player_me
        self.multiplayer = multiplayer

        self.app = Discord(self.app_id, CreateFlags.default)
        self.activity_manager = self.app.get_activity_manager()

        self.running = True

    def update(self):
        activity = Activity()
        activity.details = f"{self.player_me.username}, {self.player_me.pull_requests} pull requestów"
        activity.state = "www.korrumzthegame.cf"
        activity.assets.large_image = "korrumz"
        activity.assets.large_text = "korrumz the game 3d"
        activity.assets.small_image = f"player{self.player_me.image_number}"
        activity.assets.small_text = self.player_me.username
        activity.party.size.current_size = len(self.multiplayer.players) + 1
        activity.party.size.max_size = 100

        self.activity_manager.update_activity(activity, lambda x: x)

    def run(self):
        while self.running:
            time.sleep(1 / 10)
            self.app.run_callbacks()