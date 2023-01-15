import random
from collections import Counter

class GameLogic:

    def __init__(self):
        self.keep_playing = True
        self.game_score = 0
        self.round_dice = []
        self.round = 1

    @staticmethod
    def calculate_score(roll):
        score = 0
        pairs = 0
        straight =0
        count = Counter()
        for num in roll:
            count[num] += 1

        for num in range(1, 7):
            if count[num] == 1:
                if num == 1:
                    score += 100
                    straight += 1
                elif num == 5:
                    score += 50
                    straight += 1
                else:
                    straight += 1
            elif count[num] == 2:
                if num == 1:
                    score += 200
                    pairs += 1
                elif num == 5:
                    score += 100
                    pairs += 1
                else:
                    pairs += 1
            elif count[num] > 2:
                if num == 1:
                    score += 1000 * (count[num] - 2)
                if num > 1 :
                    score += 100 * num * (count[num] -2)

        if pairs == 3 or straight == 6:
            return 1500
        else:
            return score

    @staticmethod
    def roll_dice(number_dice):
        roll = []
        for i in range(number_dice):
            roll.append(random.randint(1,6))
        return tuple(roll)

    @staticmethod
    def kept_dice(user_input, roll_tuple):
        kept_dice = tuple([int(x) for x in user_input])
        dice_to_reroll = len(roll_tuple) - len(kept_dice)
        return kept_dice, dice_to_reroll

    @staticmethod
    def get_scorers(roll):
        return tuple([x for x in roll if x in [1, 5]])

    @staticmethod
    def validate_keepers(roll, keepers):
        roll_ctr = Counter()
        keepers_ctr = Counter()
        for num in roll:
            roll_ctr[num] += 1
        for num in keepers:
            keepers_ctr[num] += 1

        for key in keepers_ctr:
            if key not in roll_ctr:
                print(roll_ctr)
                print(keepers_ctr)
                return False
            if keepers_ctr[key] > roll_ctr[key]:
                print(roll_ctr)
                print(keepers_ctr)
                return False
        return True

    def quit_game(self):
        print(f'Thanks for playing. You earned {self.game_score}')
        self.keep_playing = False

    @staticmethod
    def print_roll(roll):
        roll_str = [str(x) for x in roll]
        print(f"*** {' '.join(roll_str)} ***")

    def roll_validation(self, roll):
        self.print_roll(roll)
        user_kept = input('Enter dice to keep, or (q)uit: ')
        if user_kept == 'q':
            self.quit_game()
            kept_dice = []
            dice_to_reroll = 0
            quit_game = True
            return kept_dice, dice_to_reroll, quit_game

        else:
            kept_dice, dice_to_reroll = self.kept_dice(user_kept, roll)
            quit_game = False
            if self.calculate_score(kept_dice) == 1500 or len(self.get_scorers(roll)) == 6:
                dice_to_reroll = 6
            if not self.validate_keepers(roll, kept_dice):
                print("Cheater!!! Or possibly made a typo...")
                self.roll_validation(roll)
            return kept_dice, dice_to_reroll, quit_game

    def round_end(self):
        print(f'You banked {self.calculate_score(self.round_dice)} points in round {self.round}')
        self.game_score += self.calculate_score(self.round_dice)
        print(f'Total score is {self.game_score} points')
        self.round += 1
        self.round_logic()

    def zilcher(self, roll):
        if self.calculate_score(roll) == 0:
            self.print_roll(roll)
            print('''
          ****************************************
          **        Zilch!!! Round over         **
          ****************************************
                      ''')
            self.round += 1
            self.round_logic()

    def roll_logic(self, dice=6):
        print(f'Rolling {dice} dice...')
        roll = self.roll_dice(dice)
        self.zilcher(roll)
        kept_dice, reroll_dice, quit_game = self.roll_validation(roll)
        if quit_game:
            return
        self.round_dice.extend(kept_dice)

        print(
            f'You have {self.calculate_score(self.round_dice)} unbanked points and {reroll_dice} dice remaining\n(r)oll again, (b)ank your points or (q)uit:')
        choice = input(f'> ')

        if choice == 'r':
            self.roll_logic(reroll_dice)
        elif choice == 'b':
            self.round_end()
        elif choice == 'q':
            self.quit_game()

    def round_logic(self):
        self.round_dice = []
        if self.game_score >= 10000:
            print(f'You won the game with a score of {self.game_score}!!')
            again = input('Play again? (y)es or (n)o')
            if again == 'y':
                self.play()
            else:
                self.quit_game()

        print(f'Starting round {self.round}')
        self.roll_logic()

    def play(self, num_rounds=20):
        while self.keep_playing and self.round < num_rounds:
            print('Welcome to Ten Thousand\n(y)es to play or (n)o to decline')
            play_prompt = input('> ')
            if play_prompt == 'y':
                self.round_logic()
            else:
                self.quit_game()