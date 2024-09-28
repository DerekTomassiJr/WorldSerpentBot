import discord
import random

class cs_bot():
    def __init__(self, message):
        self.channel = message.channel
        self.voice_channel = message.author.voice.channel

        # logging channel information
        print("CS Bot Object Created!")
        print("Text Channel Detected: " + self.channel.name)
        print("User Active Voice Channel Detected: " + self.voice_channel.name)

    def private_match(self, player_count):
        self.player_count = player_count

        print("Generating Teams...")
        users = self.voice_channel.members
        random.shuffle(users)

        # Error handling
        if (users == None):
            print("No Valid Players Found!!!")
            print("Terminating Game!")
            return None

        # Splitting the teams
        half_index = round(len(users) / 2)
        team_t = users[:half_index]
        team_ct = users[half_index:]
        
        print("T Side Team: ", team_t)
        print("CT Side Team: ", team_ct)
        game_setup = True

        await self.channel.send("T Side:")
        for member in team_t:
            await self.channel.send(member.name)

        await self.channel.send("CT Side:")
        for member in team_ct:
            await self.channel.send(member.name)

    def start_match(self):
        for member in team_t:
            member.move_to(TEAM_T_VC, VC_MOVE_REASON)

        for member in team_ct:
            member.move_to(TEAM_CT_VC, VC_MOVE_REASON)

    def command_handler(self, command):
        if (self.PRIVATE_MATCH_COMMAND in command):
            player_count = command[16:]
            self.private_match(int(player_count))
        elif (self.command == CONFIRM_TEAMS_COMMAND and game_setup):
            self.start_match()

    # Initialization Variables
    player_count = 0 # num of players in game
    game_setup = False # flag for match status
    team_t = [] # Team 1
    team_ct = [] # Team 2
    channel = None # message text channel
    voice_channel = None # user's active voice channel

    # Constants
    TEAM_T_VC = 1277807619872002099 # T Side Voice Channel
    TEAM_CT_VC = 1277807683168374795 # CT Side Voice Channel
    VC_MOVE_REASON = "CS Private Match" # Audit Log Move Reason
    PRIVATE_MATCH_COMMAND = "!csprivatematch"
    CONFIRM_TEAMS_COMMAND = "!csconfirmteams"


        
