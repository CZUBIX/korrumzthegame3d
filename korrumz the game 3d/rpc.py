from discordsdk import Discord, CreateFlags, Activity
import time

class DiscordRPC:
    def __init__(self, player_me, multiplayer):
        self.app_id = 874435457038053447
        self.enabled = True

        self.player_me = player_me
        self.multiplayer = multiplayer

        self.app = Discord(self.app_id, CreateFlags.default)
        self.activity_manager = self.app.get_activity_manager()

        self.activity = Activity()
        self.activity.details = f"{self.player_me.username}, {self.player_me.pull_requests} pull requestów"
        self.activity.state = "www.korrumzthegame.cf"
        self.activity.assets.large_image = "korrumz"
        self.activity.assets.large_text = "korrumz the game 3d"
        self.activity.assets.small_image = f"player{self.player_me.image_number}"
        self.activity.assets.small_text = self.player_me.username
        self.activity.party.size.current_size = len(self.multiplayer.players) + 1
        self.activity.party.size.max_size = 100
        self.activity.timestamps.start = time.time()

        self.running = True

    def update(self):
        if self.enabled:
            self.activity.details = f"{self.player_me.username}, {self.player_me.pull_requests} pull requestów"
            self.activity.party.size.current_size = len(self.multiplayer.players) + 1

            self.activity_manager.update_activity(self.activity, lambda x: x)

    def run(self):
        while self.running:
            time.sleep(1 / 10)
            self.app.run_callbacks()
