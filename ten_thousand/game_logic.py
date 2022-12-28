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