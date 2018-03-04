import numpy as np
import scr.FigureSupport as figureLibrary
import scr.StatisticalClasses as PathCls
import scr.StatisticalClasses as Stat

class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250


class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = []  # create an empty list where rewards will be stored
        self._probloss = []     # creat an empty list where probability of losses will be stored

        self._sumStat_meanRewards = None
        self._sumStat_meanProbLoss = None

        # summary statistics of game rewards
        self._sumStat_gameReward = Stat.SummaryStat('game rewards', self._gameRewards.get_reward())

        # summary statistics of probability of loss
        self._sumStat_prob_loss = Stat.SummaryStat('prob of loss', self._probloss.get_probability_loss())

        # summary statistics of mean game rewards
        self._sumStat_meanRewards = Stat.SummaryStat('mean rewards', self._gameRewards())


        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())


    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def get_PI_game_rewards(self, alpha):
        return self._sumStat_meanRewards.get_t_CI(alpha)

    def get_reward_list(self):
        """ returns all the rewards from all game to later be used for creation of histogram """
        return self._gameRewards


    def get_prob_loss(self):
        count_loss = 0
        for value in self._gameRewards:
            if value < 0:
                count_loss += 1
        return count_loss / len(self._gameRewards)

    def get_PI_prob_loss(self, alpha):
        return self._sumStat_meanProbLoss.get_t_CI(alpha)


# calculate expected reward of 10 games
trial = SetOfGames(prob_head=0.5, n_games=10)

# find the probability of a loss
print("The probability of a single game yielding a loss is:", trial.get_probability_loss())

# HW 6 question 3
print('95% CI of game rewards', trial.get_PI_game_rewards(0.05))
print ('95% CI probability of loss', trial.get_PI_prob_loss(0.05))
