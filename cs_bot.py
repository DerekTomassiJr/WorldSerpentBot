import discord
import random

class cs_bot():
    
    # Initialization Variables
    player_count = 0 # num of players in game
    game_setup = False # flag for match status
    team_t = [] # Team 1
    team_ct = [] # Team 2

    # Constants
    TEAM_T_VC = 1277807619872002099
    TEAM_CT_VC = 1277807683168374795
    VC_MOVE_REASON = "CS Private Match"

    def __init__(self, message):
        self.channel = message.channel
        self.voice_channel = message.author.voice.channel

    def private_match(player_count):
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

        teams = [team_t, team_ct]
        return teams

    def start_match():
        for member in team_t:
            member.move_to(TEAM_T_VC, VC_MOVE_REASON)

        for member in team_ct:
            member.move_to(TEAM_CT_VC, VC_MOVE_REASON)

    def command_handler(command):
        if ("!csprivatematch" in command):
            player_count = command[16:]
            self.private_match(int(player_count))
        elif (command == "!csconfirmteams" and game_setup):
            self.start_match()


        
