import discord
import random
from CSBotFiles import cs_bot_queue

class cs_bot(discord.Client):
    def __init__(self, message, client):
        self.channel = message.channel
        self.client = client

        try:
            self.voice_channel = message.author.voice.channel
            
            # logging channel information
            print("CS Bot Object Created!")
            print("Text Channel Detected: " + self.channel.name)
            print("User Active Voice Channel Detected: " + self.voice_channel.name)
            
            self.bot_active = True
        except:
            print("No Voice Channel Detected!")
            self.deactivate_cs_bot()

    def create_private_match_message(self):
        pm_message = "=== T Side ===\n"
        for member in self.team_t:
            pm_message += (member.name + "\n")
        
        pm_message += "\n=== CT Side ===\n"
        for member in self.team_ct:
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
        self.team_t = users[:half_index]
        self.team_ct = users[half_index:]
        
        print("T Side Team: ", self.team_t)
        print("CT Side Team: ", self.team_ct)
        self.game_setup = True

        return self.create_private_match_message()

    async def start_match(self):
        print("Starting Match")

        TEAM_T_VC = self.client.get_channel(self.TEAM_T_VC_ID)
        TEAM_CT_VC = self.client.get_channel(self.TEAM_CT_VC_ID)

        for member in self.team_t:
            await member.move_to(TEAM_T_VC)
        print("Moved T Members")

        for member in self.team_ct:
            await member.move_to(TEAM_CT_VC)
        print("Moved CT Members")

        await self.channel.send("Match Started")

    def end_match(self):
        if (self.game_setup or self.match_started):
            self.game_setup = False
            self.match_started = False
            return "Ended Current Game"
        else:
            return """A game has not been created\n
                   Use the !csprivatematch command to start a game"""
                   
    async def handle_cs_queue_command(self, command):
        if (command == self.START_CS_QUEUE_COMMAND):
            if (self.cs_queue != None):
                await self.channel.send("Cannot Start a CS Queue as one is in progress.")
                return
            
            self.cs_queue = cs_bot_queue.cs_bot_queue()
            
            if (self.cs_queue.active):
                await self.channel.send("CS Queue Started!")
            else:
                await self.channel.send("CS Queue did not initialize properly!")
                self.cs_queue = None
                
            return
        
        if (command == self.STOP_CS_QUEUE_COMMAND):
            if (self.cs_queue == None):
                await self.channel.send("A CS Queue has not been started.")
                return
            
            self.cs_queue = None
            await self.channel.send("CS Queue successfully stopped.")
            return
            
        if (self.cs_queue == None):
            await self.channel.send(f"CS Queue is not initialized. Please start the csqueue with {self.START_CS_QUEUE_COMMAND}")
        
        try:
            await self.channel.send(self.cs_queue.command_parser(command))
        except Exception as e:
            await self.channel.send(f"{e}")
            
    def deactivate_cs_bot(self):
        self.bot_active = False
        print("Bot has been deactivate ")

    async def command_handler(self, command):
        print(command)
        print(self.game_setup)
        print(self.team_ct)
        
        # Determine if the command is cs queue command first
        if (command == self.START_CS_QUEUE_COMMAND or command == self.STOP_CS_QUEUE_COMMAND or command.startswith(self.CS_QUEUE_COMMAND)):
            await self.handle_cs_queue_command(command)
            return
        
        if (command == self.PRIVATE_MATCH_COMMAND or command == self.REROLL_TEAMS_COMMAND):
            await self.channel.send(self.private_match())
        elif (command == self.CONFIRM_TEAMS_COMMAND and self.game_setup):
            await self.start_match()
        elif (command == self.END_GAME_COMMAND):
            self.deactivate_cs_bot()
            await self.channel.send(self.end_match())
        elif (command == self.STOP_BOT_COMMAND):
            self.deactivate_cs_bot()
            await self.channel.send("CS Bot Deactivated!")
        else:
            await self.channel.send("Command Not Found")


    # Initialization Variables
    client = None # World Serpent Bot Client
    bot_active = False # Tracking for whether the bot should be terminated
    player_count = 0 # num of players in game
    game_setup = False # flag for game status
    match_started = False # flag for match status
    team_t = [] # Team 1
    team_ct = [] # Team 2
    channel = None # message text channel
    voice_channel = None # user's active voice channel
    cs_queue = None # cs bot queue object

    # Constants
    TEAM_T_VC_ID = 1277807619872002099 # T Side Voice Channel
    TEAM_CT_VC_ID = 1277807683168374795 # CT Side Voice Channel
    
    PRIVATE_MATCH_COMMAND = "!csprivatematch"
    CONFIRM_TEAMS_COMMAND = "!csconfirmteams"
    REROLL_TEAMS_COMMAND = "!csreroll"
    END_GAME_COMMAND = "!csendgame"
    
    START_CS_QUEUE_COMMAND = "!startcsqueue"
    STOP_CS_QUEUE_COMMAND = "!stopcsqueue"
    CS_QUEUE_COMMAND = "!csbotqueue"

    STOP_BOT_COMMAND = "!stopcsbot"
