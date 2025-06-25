import discord
import os
import random
import json

#TODO
# 1.) Add functionality to allow a person to add/remove their own ops

class siege_bot(discord.Client):
    def __init__(self, message, client):
        self.client = client
        self.channel = message.channel
        self.player_stats = {}

        print("Siege Bot Initialized")
        print("Text Channel Detected: " + self.channel.name)

        self.bot_active = True
        self.drunksiege_active = False
        self.drunksiege_players = set()

    async def bot_pick(self, message):
        #splits message into 2 parts. First is command (!atk or !def), and second is player name.
        parts = message.strip().split(maxsplit = 1)

        if len(parts) < 2:
            await self.channel.send("Usage: !atk <player_name> or !def <player_name>")
            return
            
        command, player_name = parts
        command = command.lower()
        player_name = player_name.lower()

        #changes side to what the command specifies (either attack or defense)
        if (command == self.ATTACKER_PICK_COMMAND):
            side = "atk"
        elif (command == self.DEFENDER_PICK_COMMAND):
            side = "def"
        else:
            await self.channel.send("Side not found. Use '!atk' or '!def'")
            return

        #If valid side, calls operator_selection function to pick random op for that player on specified side.
        result = self.operator_selection(player_name, side)
        if result:
            await self.channel.send(result)
        else:
            await self.channel.send("Couldn't pick operator.")


    def operator_selection(self, player_name, side, selected_ops=None):
        try:
            #open json file (operators.json)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "operators.json")

            with open(file_path, "r") as f:
                data = json.load(f)

            # Check if player and side exist
            if player_name not in data:
                return f"Player name invalid: {player_name}."

            if side not in data[player_name]:
                return "Invalid side or no operators listed for side."

            ops = data[player_name][side]
            if not ops:
                return "Operator list is empty."
            
            #remove ops if already selected
            if selected_ops is not None:
                ops = [op for op in ops if list(op.keys())[0] not in selected_ops]

            #if op is valid, picks a random op and pulls from the json file.
            chosen_op = random.choice(ops)
            op_name, drink = list(chosen_op.items())[0]

            if selected_ops is not None:
                selected_ops.add(op_name)

            #counter to track drinks in a drunk siege session
            drink_type = drink.lower().strip()
            if player_name not in self.player_stats:
                self.player_stats[player_name] = {"sip": 0, "shot": 0, "shot(optional)": 0}

            if drink_type in self.player_stats[player_name]:
                self.player_stats[player_name][drink_type] += 1

            #displays the player's name, along with op and drink
            print(f"{player_name}'s random {side.upper()} op: {op_name} ({drink}).")
            return f"{player_name}'s random {side.upper()} operator is: {op_name} ({drink})"
        


        #error check, ensure if json can't be found it throws exception
        except FileNotFoundError:
            return "Error: JSON file not found."
        except Exception as e:
            return f"Unexpected error: {e}"

    def deactivate_siege_bot(self):
        self.bot_active = False
        self.drunksiege_players.clear()
        self.player_stats.clear()
        print("Siege Bot has been deactivated")


    async def drunk_siege(self, message):
        parts = message.strip().split(maxsplit = 1)
        ds_command = parts[0]

        #start drunk siege. Clears player set to ensure nobody is automatically joined.
        if ds_command == "!startdrunksiege":
            self.drunksiege_active = True

            #clear any active drunk siege players and their stats
            self.drunksiege_players.clear()
            self.player_stats.clear()
            await self.channel.send("Drunk siege activated. !join <playername> to join or !leave <playername> to leave.")

        elif ds_command == "!stopdrunksiege":
            self.drunksiege_players.clear()
            self.drunksiege_active = False
            await self.channel.send("Drunk siege deactivated.")

        #if player wants to join and enters command/their name.
        elif ds_command == "!join" and len(parts) == 2:
            player = parts[1].strip()
            self.drunksiege_players.add(player.lower())
            await self.channel.send(f"{player} has joined drunk siege.")

        #if player wants to leave and enters command/their name. Ensure player is already participating in drunk siege before they can be removed.
        elif ds_command == "!leave" and len(parts) == 2:
            player = parts[1].strip()
            if player in self.drunksiege_players:
                self.drunksiege_players.remove(player.lower())
                await self.channel.send(f"{player} has left the game.")
            else:
                await self.channel.send(f"{player} is not participating.")

        #displays currently joined players.
        elif ds_command == "!players":
            if not self.drunksiege_active:
                await self.channel.send("Drunk siege is not active.")
            elif not self.drunksiege_players:
                await self.channel.send("Nobody has joined drunk siege.")
            else:
                player_list = ", ".join(sorted(self.drunksiege_players))
                await self.channel.send(f"Drunk Siegers: {player_list}")

            #roll for everyone. Error check to start
        elif ds_command in ["!rollatk", "!rolldef"]:
            if not self.drunksiege_active:
                await self.channel.send("Drunk siege is not active. Please run !startdrunksiege to begin.")
                return
            
            side = "atk" if ds_command == "!rollatk" else "def"
            if not self.drunksiege_players:
                await self.channel.send("Where all the boys at, nobody joined.")

            #picks player's op and stores in result. If it can't pick op, send error message.
            results = []
            selected_operators = set()
            for player in sorted(self.drunksiege_players):
                result = self.operator_selection(player, side, selected_ops = selected_operators)
                results.append(result if result else f"{player}: Error picking op.")

            await self.channel.send("\n".join(results))
            print(results)

    async def command_handler(self, command):
        siege_bot_commands = [self.DRUNK_SIEGE_START_COMMAND, self.DRUNK_SIEGE_END_COMMAND, self.DRUNK_SIEGE_JOIN_COMMAND, self.DRUNK_SIEGE_LEAVE_COMMAND, self.GROUP_ATTACKER_ROLL_COMMAND, self.GROUP_DEFENDER_ROLL_COMMAND, self.DRUNK_SIEGE_ACTIVE_PLAYER_COMMAND]

        print(command)

        if not command.startswith("!"):
            return
        
        content = command.strip().lower()

        #have bot pick with !atk <playername> or !def <playername>
        if content.startswith(self.ATTACKER_PICK_COMMAND) or content.startswith(self.DEFENDER_PICK_COMMAND):
            await self.bot_pick(command)
        #checks to see if the listed commands were entered, then jumps to drunk_siege function.
        elif any(command.startswith(c) for c in siege_bot_commands):
            await self.drunk_siege(command)

        elif content == "!stopsiegebot":
            self.deactivate_siege_bot()
            await self.channel.send("Siege Bot Deactivated.")

        elif content == self.STATS_COMMAND:
            if not self.player_stats:
                await self.channel.send("No stats to display.")

            stats_message = []
            for player, stats in sorted(self.player_stats.items()):
                shots = stats.get("shot", 0)
                sips = stats.get("sip", 0)
                optional_shots = stats.get("shot(optional)", 0)
                stats_message.append(f"{player}: Shot(s): {shots}, Sip(s): {sips}, Optional Shot(s): {optional_shots}")

            await self.channel.send("\n".join(stats_message))

        else:
            await self.channel.send("Unknown Command.")
    
    # Initialization Variables
    client = None  # World Serpent Bot Client
    channel = None  # Message Text Channel
    bot_active = False  # Flag for bot's active status

    #constants
    ATTACKER_PICK_COMMAND = "!atk"
    DEFENDER_PICK_COMMAND = "!def"
    DRUNK_SIEGE_START_COMMAND = "!startdrunksiege"
    DRUNK_SIEGE_END_COMMAND = "!stopdrunksiege"
    DRUNK_SIEGE_JOIN_COMMAND = "!join"
    DRUNK_SIEGE_LEAVE_COMMAND = "!leave"
    DRUNK_SIEGE_ACTIVE_PLAYER_COMMAND = "!players"
    GROUP_ATTACKER_ROLL_COMMAND = "!rollatk"
    GROUP_DEFENDER_ROLL_COMMAND = "!rolldef"
    STATS_COMMAND = "!stats"