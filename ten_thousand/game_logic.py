import random
from collections import Counter

class GameLogic:

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
        kept_dice = [int(x) for x in user_input]
        dice_to_reroll = len(roll_tuple) - len(kept_dice)
        return kept_dice, dice_to_reroll

    def quit_game(self):
        print(f'Thanks for playing. You earned {self.game_score}')
        self.keep_playing = False

    def roll_logic(self, dice=6):
        print(f'Rolling {dice} dice...')
        roll = self.roll_dice(dice)
        roll_str = [str(x) for x in roll]
        print(f"*** {' '.join(roll_str)} ***")
        user_kept = input('Enter dice to keep, or (q)uit:')
        if user_kept == 'q':
            self.quit_game()
        kept_dice, dice_to_reroll = self.kept_dice(user_kept, roll)
        self.round_dice.extend(kept_dice)
        print(
            f'You have {self.calculate_score(self.round_dice)} unbanked points and {dice_to_reroll} dice remaining\n(r)oll again, (b)ank your points or (q)uit:')
        choice = input(f'> ')
        if choice == 'r':
            self.roll_logic(dice_to_reroll)
        elif choice == 'b':
            print(f'You banked {self.calculate_score(self.round_dice)} points in round {self.round}')
            self.game_score += self.calculate_score(self.round_dice)
            print(f'Total score is {self.game_score} points')
            self.round += 1
            self.round_logic()
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

    def play(self):
        while self.keep_playing:
            print('Welcome to Ten Thousand\n(y)es to play or (n)o to decline')
            play_prompt = input('> ')
            if play_prompt == 'y':
                self.round_logic()
            else:
                self.quit_game()