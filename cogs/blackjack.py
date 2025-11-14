import random
import discord
from discord.ext import commands

#init
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)


#Start logic

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
#default ace value at 11, but user can choose ultimately.
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

class BlackjackGame:

    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False
        self.player_ace_choices = []  # Track player's ace values, defaulted at 11.

    def create_deck(self):
        deck = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def deal_card(self, hand):
        hand.append(self.deck.pop())
    
    def hand_value(self, hand):
        value = 0
        aces = 0
        for card in hand:
            rank = card[0]
            if rank == 'A':
                value += 11
                aces += 1
            else:
                value += values[rank]
        
        # Adjust for aces if value > 21 to ensure the user does not bust.
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    #Alternates dealing cards between player and dealer
    def start_game(self):
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)

    def hit(self):
        self.deal_card(self.player_hand)
        if self.hand_value(self.player_hand) > 21:
            return "You busted!"
        return None


    #REMINDER - Dealer plays after player stands, but also is forced to stand on 17+.
    def dealer_plays(self):
        while self.hand_value(self.dealer_hand) < 17:
            self.deal_card(self.dealer_hand)
        self.game_over = True

    def result(self):
        player_value = self.hand_value(self.player_hand)
        dealer_value = self.hand_value(self.dealer_hand)

        if player_value > 21:
            return "You busted! Dealer wins."
        elif dealer_value > 21:
            return "Dealer busted! You win!"
        elif player_value == dealer_value:
            return "Push!"
        else:
            return "Dealer Wins."

    def format_hand(self, hand):
        return ', '.join([f"{rank} of {suit}" for rank, suit in hand])
    
    #checks for aces
    def has_ace(self, hand):
        return any(card[0] == 'A' for card in hand)
    
    #Sets future ace evaluation, but downgrades to 1 if >21.
    def set_ace_value(self, value):
        for i, card in enumerate(self.player_hand):
            if card[0] == 'A':
                self.player_ace_values[i] = value
#-----Bot Cog Logic -----
games = {}

class Blackjack(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.games = {} #Tracks game by user id

#Handles start of game, and shows first set of cards
    @commands.command(name='blackjack', help='Start a game of Blackjack', brief='Play Blackjack', aliases=['bj'])
    async def start_blackjack(self, ctx):
        if ctx.author.id in self.games:
            return await ctx.send("You already have a game running! Use !hit or !stand.")

        game = BlackjackGame()
        game.start_game()
        self.games[ctx.author.id] = game

        #Formats the hands for readability
        player_hand_formatted = game.format_hand(game.player_hand)
        dealer_visible_card = f"{game.dealer_hand[0][0]} of {game.dealer_hand[0][1]}"

        await ctx.send("Game started! Dealing cards...\n\n"
                        f"Your Hand: {player_hand_formatted} (Value: {game.hand_value(game.player_hand)})\n" 
                        f"Dealer's Hand: {dealer_visible_card}, Face Down Card ")

        await ctx.send("Game Started")
        if game.has_ace(game.player_hand):
            await ctx.send("You have an Ace! You can choose its value with !ace 1 or !ace 11.")

#Handles player hitting
    @commands.command(name='hit', help='Take another card', brief='Hit')
    async def hit(self, ctx):
        game = self.games.get(ctx.author.id)
        if not game:
            return await ctx.send("Start a game by typing !blackjack")
    
        message = game.hit()
        hand_value = game.hand_value(game.player_hand)
    
        last_drawn = game.player_hand[-1]
        formatted_card = f"{last_drawn[0]} of {last_drawn[1]}"

        await ctx.send(f"You drew a card!\n" f"You Drew {formatted_card}\n" f"Your Hand: {game.format_hand(game.player_hand)} (Value: {hand_value})")

    # set ace value manually if drawn when hit
        if game.has_ace(game.player_hand):
            await ctx.send("You have an Ace! You can choose its value with !ace 1 or !ace 11.")

        if message:
            await ctx.send(message)
            del self.games[ctx.author.id]

    @commands.command(name='stand', help='End your turn', brief='Stand')
    async def stand(self, ctx):
        game = self.games.get(ctx.author.id)
        if not game:
            return await ctx.send("No game running! Start one with !blackjack")
    
        game.dealer_plays()
        result_message = game.result()
        
        player_hand_formatted = game.format_hand(game.player_hand)
        dealer_hand_formatted = game.format_hand(game.dealer_hand)

        await ctx.send(f"Final Hands:\n"
        f"Your Hand: {player_hand_formatted} (Value: {game.hand_value(game.player_hand)})\n"
        f"Dealer's Hand: {dealer_hand_formatted} (Value: {game.hand_value(game.dealer_hand)})\n"
        f"{result_message}")

        del self.games[ctx.author.id]

    @commands.command(name='ace', help='Set the value of an Ace (1 or 11)', brief='Set Ace Value')
    async def set_ace(self, ctx, value: int):
        game = self.games.get(ctx.author.id)
        if not game:
            return await ctx.send("No game running! Start one with !blackjack")
    
        if not value.isdigit():
            return await ctx.send("Please provide a valid number (1 or 11).")

        if value not in [1, 11]:
            return await ctx.send("Invalid value! Please choose 1 or 11.")
    
        game.set_ace_value(value)
        await ctx.send(f"Ace value set to {value}. Your hand value is now {game.hand_value(game.player_hand)}.")

async def setup(bot):
    await bot.add_cog(Blackjack(bot))