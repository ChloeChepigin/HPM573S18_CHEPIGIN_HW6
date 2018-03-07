#Question 3 Part 1 looking at the owner's perspective

import numpy as np
import scr.FigureSupport as figureLibrary
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
        self._get_reward = 250 - 100*self._countWins
        return self._get_reward

    def get_probability_loss(self):
        """ returns the probability of a loss """
        count_loss = 0
        if self._get_reward < 0:
                count_loss = 1
        elif self._get_reward >= 0:
            count_loss = 0
        return count_loss


class SetOfGames:
    def __init__(self, id, prob_head, n_games):
        self._id=id
        self._gameRewards = []  # create an empty list where rewards will be stored
        self._probloss = []     # create an empty list where probability of losses will be stored

        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())
            # store the probability of loss
            self._probloss.append(game.get_probability_loss())

    def simulate(self):
        return GameOutcomes(self)

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def get_rewards(self):
        """ returns all the rewards from all game to later be used for creation of histogram """
        return self._gameRewards

    def get_max(self):
        """ returns maximum reward"""
        return max(self._gameRewards)

    def get_min(self):
        """ returns minimum reward"""
        return min(self._gameRewards)

    def get_probability_loss(self):
        """ returns the probability of a loss """
        return self._probloss



class GameOutcomes:
    def __init__(self, simulated_set):
        self._simulatedGameSet = simulated_set

        # summary statistics of game rewards
        self._sumStat_gameReward = Stat.SummaryStat('game rewards', self._simulatedGameSet.get_rewards())
        # summary statistics of probability of loss
        self._sumStat_prob_loss = Stat.SummaryStat('prob of loss', self._simulatedGameSet.get_probability_loss())

    def get_reward_list(self):
        return self._simulatedGameSet.get_rewards()

    def get_ave_reward(self):
        return self._sumStat_gameReward.get_mean()

    def get_prob_loss(self):
        return self._sumStat_prob_loss.get_mean()

    def get_CI_prob_loss(self, alpha):
        return self._sumStat_prob_loss.get_t_CI(alpha)

    def get_CI_game_rewards(self, alpha):
        """
        :param alpha: confidence level
        :return: t-based confidence interval
        """
        return self._sumStat_gameReward.get_t_CI(alpha)


# Calculate expected reward of 1000 games
trial = SetOfGames(id=1, prob_head=0.5, n_games=1000)
SimGame = trial.simulate()
print("The average expected reward is:", trial.get_ave_reward())


# HW 5 Problem 2: Find the probability of a loss
print("The probability of a single game yielding a loss is:", trial.get_probability_loss())


# HW 6 Question 1
print('95% CI of game rewards', SimGame.get_CI_game_rewards(0.05))
print('95% CI of prob loss', SimGame.get_CI_prob_loss(0.05))


# Because in the case of the owner we are considering the steady state, as we have a large enough sample size,
# we can look at the confidence intervals retrieved from question 1



