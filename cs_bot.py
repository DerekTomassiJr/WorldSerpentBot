import discord
import random

class cs_bot():
    def __init__(self, message):
        self.channel = message.channel

        try:
            self.voice_channel = message.author.voice.channel
        except:
            print("No Voice Channel Detected!")

        # logging channel information
        print("CS Bot Object Created!")
        print("Text Channel Detected: " + self.channel.name)
        print("User Active Voice Channel Detected: " + self.voice_channel.name)

    def create_private_match_message(self, team_t, team_ct):
        pm_message = "=== T Side ===\n"
        for memeber in team_t:
            pm_message += (member.name + "\n")
        
        pm_message += "\n=== CT Side ===\n"
        for member in team_ct:
            pm_message += (member.name + "\n")
        
        pm_message += "\n"
        pm_message += "Type !csconfirmteams to confirm teams\n"
        pm_message += "Type !csreroll to reroll teams"
        
        return pm_message

    def private_match(self):
        if (self.match_started):
            return "A match is currently in progress"
        
        self.player_count = len(self.voice_channel.members)

        print("Generating Teams...")
        users = self.voice_channel.members
        random.shuffle(users)

        # Error handling
        if (users == None):
            print("No Valid Players Found!!!")
            print("Terminating Game!")
            return """No Users Found in Voice Chat or User is not in Voice Chat!!!\n
                    Game Not Created!"""

        # Splitting the teams
        half_index = round(len(users) / 2)
        team_t = users[:half_index]
        team_ct = users[half_index:]
        
        print("T Side Team: ", team_t)
        print("CT Side Team: ", team_ct)
        game_setup = True

        return self.create_private_match_message(team_t, team_ct)

    def start_match(self):
        print("Starting Match")

        for member in team_t:
            member.move_to(TEAM_T_VC, VC_MOVE_REASON)
        print("Moved T Members")

        for member in team_ct:
            member.move_to(TEAM_CT_VC, VC_MOVE_REASON)
        print("Moved CT Members")

        return "Match Started"

    def end_match(self):
        if (game_setup or match_started):
            game_setup = False
            match_started = False
            return "Ended Current Game"
        else:
            return """A game has not been created\n
                   Use the !csprivatematch command to start a game"""

    def command_handler(self, command):
        print(command)
        print(self.game_setup)
        print(self.team_ct)
        
        if (command == self.PRIVATE_MATCH_COMMAND or command == self.REROLL_TEAMS_COMMAND):
            return self.private_match()
        elif (command == self.CONFIRM_TEAMS_COMMAND and self.game_setup):
            return self.start_match()
        elif (command == self.END_GAME_COMMAND):
            return self.end_match()
        else:
            return "Command Not Found"


    # Initialization Variables
    player_count = 0 # num of players in game
    game_setup = False # flag for game status
    match_started = False # flag for match status
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
    REROLL_TEAMS_COMMAND = "!csreroll"
    END_GAME_COMMAND = "!csendgame"
