# Cards = a dictionary that maps each card to a list of values (updated by __init__())
#   last element = availability of that card, which is checked by update_avialability each time card is dealt
# Cards_keys = a list of all cards that can be dealt, list decreases once update_availability removes a card
# deal_card -> randomly choses a key, returns a dictionary of the key and its list (exculding last element), calls update availability
# update_availability -> updates number of times card is used and pops the card out if number of times = 4

from random import choice
class Deck:
    Cards = {}
    Cards_keys = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', "Q", "K"]
    
    def __init__(self):
        for card_key_index in range(len(self.Cards_keys)):
            if card_key_index == 0: # for ace
                self.Cards[self.Cards_keys[card_key_index]] = [1, 11, 0]
            elif card_key_index < 10: # for 2 - 10
                self.Cards[self.Cards_keys[card_key_index]] = [self.Cards_keys[card_key_index], 0]
            else: # for J, Q, K
                self.Cards[self.Cards_keys[card_key_index]] = [10, 0]
        # print(self.Cards)
            
    def deal_card(self):
        card_key_dealt = choice(self.Cards_keys)
        card_dealt_dict = {card_key_dealt:self.Cards[card_key_dealt][:-1]}
        self.update_availability(card_key_dealt)
        return card_dealt_dict
    
    def update_availability(self, card_key):
        if self.Cards[card_key][-1] == 3:
            self.Cards_keys.remove(card_key)
            return
        self.Cards[card_key][-1] += 1
        
# Favour = Deck()
# while True:
    # print(Favour.deal_card(), Favour.Cards_keys)
    

# player_cards = dictionary --> containing list of cards_dictionaries that have been dealt to him----this is to enable splitting
#   first element = stay boolean. if false, the stack can hit else the stack will be skipped
#   2nd element = list of sums (sum1 --> sum if 'A' == 1 and sum2 = sum if 'A' == 11)
# player_bet = bets player has made
# player_split = determines if player has split already or not
# __init__() ----> assigns the deck common to all players, initializes the player_cards dict
# player_turn ---> encapsulating function that calls all functions for each stack of split cards
#   check if split is available
#   
# player_hit ---> calls the deck, deals a card, update player_cards
# player_split----> carries out a split
# player_double_down ----> carries out a double down
# player_card_sum ---> returns sum of values of player_cards so player can decide on a hit or stay, decides if a player has a black jack


## Note----> in control class, make sure when dealing first 2 cards to call player.hit(stack_1)
class Player:
    
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.player_cards = {"stack_1":[False, [0]]}
        self.player_bet = 1
        self.player_split = False
        self.ace_card_present = False
        self.turn = True # player can have a turn
        self.bust = {}
        self.print_initial = f"~~~~~| {self.name} ---> "
    
    def player_hit(self, stack_to_hit):
        card_dealt = self.deck.deal_card()
        self.player_cards[stack_to_hit].append(card_dealt)
        self.player_card_sum(stack_to_hit)
        # print(self.player_cards)
        
    def player_turn(self):
        
        print(self.print_initial + "It's your turn!")
        
        # Split or not
        if self.player_split == False and len(self.player_cards) == 1 and len(self.player_cards["stack_1"][2:]) == 2 and self.player_cards["stack_1"][2] == self.player_cards["stack_1"][3]:
            split_or_not = input(self.print_initial + "1st and 2nd cards are similar. Will you split? (y or n) ")
            if split_or_not == "y":
                self.split()
                player_split = True
        
        for stack in self.player_cards:
            stay_bool = self.player_cards[stack][0]
            if stay_bool == False:
                while True:
                    hit_or_stay_or_dd = input(self.print_initial+ "press h to hit, s to stay, dd to double down: ")
                    if hit_or_stay_or_dd == "h":
                        self.player_hit(stack)
                        break
                    elif hit_or_stay_or_dd == "dd":
                        self.double_down(stack)
                        break  
                    else:
                        self.player_cards[stack][0] = True
                        break
        self.update_turn() 
    
    
    def split(self):
        self.player_cards["stack_2"] = [False, [self.player_cards["stack_1"][1][0]]] + self.player_cards["stack_1"][-1]
        self.player_cards["stack_1"] = self.player_cards["stack_1"][:3]
    
    def double_down(self, stack_to_dd):
        if len(self.player_cards[stack_to_dd][2:]) == 2 and (value in [9, 10, 11] for value in self.player_cards[stack_to_dd][1]):
            self.player_bet += 1
            self.player_hit(stack_to_dd)
            self.player_cards[stack_to_dd][0] = True
    
    def player_card_sum(self, stack):
        new_card_dict = self.player_cards[stack][-1]; full_stacks = 0
        for index in range(len(self.player_cards[stack][1])):
            self.player_cards[stack][1][index] += list(new_card_dict.values())[0][0]
        if list(new_card_dict.keys()) == ['A'] and self.ace_card_present == False:
            self.player_cards[stack][1].append(self.player_cards[stack][1][0] + list(new_card_dict.values())[0][1] - list(new_card_dict.values())[0][0])
            self.ace_card_present = True # prevent this from occuring with 2nd ace
        return
    
    def update_turn(self):
        length = len(self.player_cards.keys())
        tlength = 0
        for stack in self.player_cards:
            self.bust[stack] = []
            if self.player_cards[stack][0] == False:
                for value in self.player_cards[stack][1]:
                    if value not in range(21):
                        self.bust[stack].append(value)
                        # self.player_cards[stack][1].remove(value)
                if len(self.bust[stack]) == len(self.player_cards[stack][1]):
                    self.player_cards[stack][0] = True
                    tlength += 1
            else:
                tlength += 1
        if tlength == length:
            self.turn = False


# A rectangular frame that has card name at top left and bottom right
# ,________,
# |        |
# | J      |
# |        |
# |     J  |
# |________|
# print_column ---> Each row prints the card for every player
# get_cards ---> iterate over player_name and stacks
# print_card_column(card letter/number) ----> print respective columns for a single card
# card_index: keeps track of the number of columns of rows of cards to be printed
# players: all the players in the game
# dealer = players[0]

class Board:
    players = []
    number_of_rows = 1
    
    def print_column(self, dealer=False):
        present_index = 0; card_column_index = 0
        self.print_player_names()
        
        if dealer == False:
            deal = 3
        else:
            deal = 2
            
        while present_index < self.number_of_rows:
            for player in self.players:
                for stack in player.player_cards:
                    stack_length = len(player.player_cards[stack][2:])
                    if present_index == 0 and stack_length > self.number_of_rows:
                        self.number_of_rows = len(player.player_cards[stack][2:])
                    
                    if self.players.index(player) != 0 and present_index < stack_length:
                        present_card = player.player_cards[stack][2+present_index] 
                        self.print_card_column(card_column_index, list(present_card.keys())[0])
                    # for the dealer
                    elif self.players.index(player) == 0 and present_index < stack_length-(deal-2):
                        present_card = player.player_cards[stack][deal+present_index] 
                        self.print_card_column(card_column_index, list(present_card.keys())[0])
                    elif self.players.index(player) != 0 and present_index >= stack_length or self.players.index(player) == 0 and present_index >= stack_length-(deal-2):
                        print("            ",end="\t")
            print()
            card_column_index += 1
            if card_column_index == 6:
                present_index += 1
                card_column_index = 0  
    
    def print_player_names(self):
        for player in self.players:
            if len(player.player_cards) == 1:
                print(player.name.center(13,"_"), end="   ")
            else:
                print(player.name.center(26,"_"), end="   ")
        print()
                
    
    def print_card_column(self, column, card_letter):
        if column == 0:
            print(",________,", end="\t")
        elif column == 1 or column == 3:
            print("|        |", end='\t')
        elif column == 2:
            if len(str(card_letter))== 1:
                print(f"| {card_letter}      |", end='\t')
            else:
                print(f"| {card_letter}     |", end="\t")
        elif column == 4:
            if len(str(card_letter))==1:
                print(f"|     {card_letter}  |", end='\t')
            else:
                print(f"|     {card_letter} |", end='\t')
        else:
            print("|________|", end='\t')
            
    def add_player(self, player_object):
        self.players.append(player_object)

#### Board Test
# player1 = Player("Regubris")
# player2 = Player("Zenabre")
# player3 = Player("Ant")
# game_board = Board(); game_board.add_player(player1); game_board.add_player(player2); game_board.add_player(player3)

# player1.player_hit("stack_1"); player2.player_hit("stack_1"); player3.player_hit("stack_1")
# game_board.print_column()
# player1.player_hit("stack_1"); player2.player_hit("stack_1");player3.player_hit("stack_1")
# game_board.print_column()
# player1.player_turn(); player2.player_turn(); player3.player_turn(); game_board.print_column()


# players --> taken from board\
#   players[0] = dealer
# player_board_initialize ----> inputs number of players, each player's name, initialize board, store players in a players' list
    # Dealer initializer will create Player dealer object
    # Dealer hidden card
# check_black_jack ----> checks for black_jack after each player's turn
# function to do first 2 hits
# function to check_black_jack
# function to do rest of game
# 
class Control:
    deck = Deck()
    dealer = Player("Dealer", deck)
    players = [dealer]
    board = Board()
    board.players = [dealer]
    
    def get_players(self):
        while True:
            try:
                number_of_players = abs(int(input("How many players are playing? ")))
            except TypeError:
                print("Enter a positive number!")
            break
        for num in range(number_of_players):
            player_name = input(f"Enter player{num+1}'s name: ")
            new_player = Player(player_name, self.deck)
            self.players.append(new_player)
            self.board.add_player(new_player)
    
    def check_black_jack(self):
        for player in self.players[1:]:
            for stack in player.player_cards:
                if 21 in player.player_cards[stack][1]:
                    print("\n````````` {name} has black Jack!! `````````\n".format(name=player.name))
                    player.player_cards[stack][0] = True
    
    def start_game(self):
        time_index = 0 
        while time_index < 2:
            for player in self.players:
                player.player_hit("stack_1")
            time_index += 1
        self.board.print_column()
            
    def run_game(self):
        self.check_black_jack()
        players_in_game = 1
        while players_in_game > 0:
            players_in_game = 0
            for player in self.players[1:]:
                player.player_turn()
                self.board.print_column()
                if player.turn == True:
                    players_in_game += 1
        self.dealer_sum = self.dealer_choice()
        self.board.print_column(dealer=True)
        self.game_results()
        
        
    def dealer_choice(self):
        totals_1 = [x for x in self.players[0].player_cards["stack_1"][1]]
        self.players[0].player_hit("stack_1")
        totals_2 = self.players[0].player_cards["stack_1"][1]
        final_totals = []
        
        for total in totals_1:
            if total >= 16:
                final_totals.append(total)
            else:
                 final_totals.append(totals_2[totals_1.index(total)])
                 
        if max(final_totals) <= 21:
            to_return =  max(final_totals)
        else:
            final_totals.sort()
            to_return = final_totals[0]
        if to_return in totals_1:
            self.players[0].player_cards["stack_1"].pop()
        return to_return
            
            
    
    def game_results(self):
        print("~~~~~~~| Dealer cards sum = ", self.dealer_sum)
        
        if self.dealer_sum > 21:
            print("!! Dealer |---> LOSER !!")
        for player in self.players[1:]:
            for stack in player.player_cards:
                for total in player.player_cards[stack][1]:
                    print(f"~~~~~~~| {player.name} sum = {total} ---> ", end="")
                    if total > 21:
                        print(" !! ``BUSTED' !!")
                    elif total == 21:
                        print("!! ``BLACKJACK' !!")
                    elif self.dealer_sum < 21:
                        if total > self.dealer_sum:
                            print("!! ``WINNER' !!")
                        elif total < self.dealer_sum:
                            print("!! ``LOSER' !!")
                        else:
                            print("!! ``PUSH' !!")
                    else:
                        print("!! ``WINNER' !!")
            print()
### Control TEst
blackjack = Control()
blackjack.get_players()
blackjack.start_game()
blackjack.run_game()
