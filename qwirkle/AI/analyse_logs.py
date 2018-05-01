import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from _ast import Num
from numba.tests.npyufunc.test_ufunc import dtype


def logs():
    for file in os.listdir('analysis'):
        with open('analysis/' + file, 'rb') as f:
            yield pickle.load(f)


def plot_distribution_of_game_lengths():
    lengths = []
    for log in logs():
        scores = log['score of move']
        lengths.append(len(scores))
    mu = np.mean(lengths)
    sigma = np.std(lengths)
    n, bins, patches = plt.hist(lengths, density=False,
                                facecolor='g', alpha=0.75)
    plt.xlabel('Turns')
    plt.ylabel('Frequency')
    plt.title('Histogram of Qwirkle game lengths')
    plt.text(47, 17, r'$\mu={},\ \sigma={}$'.format(mu, sigma))
    #plt.axis([40, 160, 0, 0.03])
    plt.grid(True)
    plt.show()


def plot_tiles_on_board():
    tiles = [[] for i in range(70)]
    for log in logs():
        tiles_on_board = log['tiles on board at start of round']
        for i, num in enumerate(tiles_on_board):
            tiles[i].append(num)
    averages = []
    stds = []
    for round in tiles:
        if round:
            averages.append(np.mean(round))
            stds.append(np.std(round))
        elif False:
            averages.append(0)
            stds.append(0)
    plt.plot(averages)
    plt.plot(np.array(averages)+np.array(stds))
    plt.plot(np.array(averages)-np.array(stds))
    plt.plot(stds)
    plt.grid(True)
    plt.show()


def plot_tiles_played():
    tiles_played = [[] for i in range(108)]
    for log in logs():
        tiles_on_board = log['tiles on board at start of round']
        played = log['tiles played in move']
        for a, tiles_in_move in zip(tiles_on_board, played):
            tiles_played[a].append(tiles_in_move)
    averages = []
    stds = []
    for round in tiles_played:
        if round:
            averages.append(np.mean(round))
            stds.append(np.std(round))
        else:
            averages.append(np.NaN)
            stds.append(np.NaN)
    plt.plot(averages)
    plt.plot(stds)
    plt.grid(True)
    plt.show()


def plot_score():
    tiles_played = [[] for i in range(108)]
    for log in logs():
        tiles_on_board = log['tiles on board at start of round']
        scores = log['score of move']
        for a, score in zip(tiles_on_board, scores):
            tiles_played[a].append(score)
    averages = []
    stds = []
    for round in tiles_played:
        if round:
            averages.append(np.mean(round))
            stds.append(np.std(round))
        else:
            averages.append(np.NaN)
            stds.append(np.NaN)
    plt.plot(averages)
    plt.plot(stds)
    plt.grid(True)
    plt.show()


def plot_num_max_score_moves():
    lengths = []
    for log in logs():
        num_moves = np.array(log['number of legal moves of max score for hand'], dtype='float')
        scores = np.array(log['score of move'])
        indexes = np.where(scores == 0)[0]
        num_moves[indexes] = -1
        lengths.extend(list(num_moves))
    mu = np.mean(lengths)
    sigma = np.std(lengths)
    n, bins, patches = plt.hist(lengths,
                                bins=np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                               11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                                               21, 22, 23, 24, 25, 26, 27, 28, 29, 30])-0.5,
                                density=True, facecolor='g', alpha=0.75)
    plt.xlabel('Number of moves')
    plt.ylabel('Frequency')
    plt.title('Histogram of number of legal moves of max score')
    plt.text(47, 17, r'$\mu={},\ \sigma={}$'.format(mu, sigma))
    #plt.axis([40, 160, 0, 0.03])
    plt.grid(True)
    plt.show()


def unique_tiles_on_hand():
    tiles = [[] for i in range(7)]
    for log in logs():
        unique_tiles_on_hand = log['unique tiles on hand']
        scores = np.array(log['score of move'])

        for unique, score in zip(unique_tiles_on_hand, scores):
            tiles[unique].append(score)
    averages = []
    stds = []
    for round in tiles:
        if round:
            averages.append(np.mean(round))
            stds.append(np.std(round))
        elif False:
            averages.append(0)
            stds.append(0)
    plt.plot([1, 2, 3, 4, 5, 6], averages)
    plt.plot([1, 2, 3, 4, 5, 6], stds)
    plt.grid(True)
    plt.show()


def unique_tiles_on_hand_no_zeros():
    tiles = [[] for i in range(7)]
    for log in logs():
        unique_tiles_on_hand = log['unique tiles on hand']
        scores = np.array(log['score of move'])

        for unique, score in zip(unique_tiles_on_hand, scores):
            if score > 0:
                tiles[unique].append(score)
    averages = []
    stds = []
    for round in tiles:
        if round:
            averages.append(np.mean(round))
            stds.append(np.std(round))
        elif False:
            averages.append(0)
            stds.append(0)
    plt.plot([1, 2, 3, 4, 5, 6], averages)
    plt.plot([1, 2, 3, 4, 5, 6], stds)
    plt.grid(True)
    plt.show()


def plot_forbidden_positions():
    tiles_played = [[] for i in range(108)]
    for log in logs():
        tiles_on_board = log['tiles on board at start of round']
        forbidden = log['completely forbidden positions']
        for a, forbidden_positions_in_move in zip(tiles_on_board, forbidden):
            tiles_played[a].append(forbidden_positions_in_move)
    averages = []
    stds = []
    for round in tiles_played:
        if round:
            averages.append(np.mean(round))
            stds.append(np.std(round))
        else:
            averages.append(np.NaN)
            stds.append(np.NaN)
    plt.plot(averages)
    plt.plot(stds)
    plt.grid(True)
    plt.show()


def plot_playable_positions():
    tiles_played = [[] for i in range(108)]
    for log in logs():
        tiles_on_board = log['tiles on board at start of round']
        forbidden = log['playable positions total']
        for a, forbidden_positions_in_move in zip(tiles_on_board, forbidden):
            tiles_played[a].append(forbidden_positions_in_move)
    averages = []
    stds = []
    for round in tiles_played:
        if round:
            averages.append(np.mean(round))
            stds.append(np.std(round))
        else:
            averages.append(np.NaN)
            stds.append(np.NaN)
    plt.plot(averages)
    plt.plot(stds)
    plt.grid(True)
    plt.show()


def plot_legal_moves_sfa_tiles_on_board():
    tiles_played = [[] for i in range(108)]
    for log in logs():
        tiles_on_board = log['tiles on board at start of round']
        moves = log['number of legal moves for hand']
        for a, num_moves in zip(tiles_on_board, moves):
            tiles_played[a].append(num_moves)
    averages = []
    stds = []
    max_so_far = 0
    for round in tiles_played:
        if round:
            max_so_far = max(max_so_far, max(round))
            averages.append(np.mean(round))
            stds.append(np.std(round))
        else:
            averages.append(np.NaN)
            stds.append(np.NaN)
    print(max_so_far)
    plt.plot(averages)
    plt.plot(stds)
    plt.grid(True)
    plt.show()


def plot_score_distribution():
    scores = []
    for log in logs():
        score = log['score of move']
        scores.extend(score)
    mu = np.mean(scores)
    sigma = np.std(scores)
    n, bins, patches = plt.hist(scores,
                                bins=np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20, 21, 22, 23, 24, 25, 30])-0.5,
                                density=True, facecolor='g', alpha=0.75)
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.title('Histogram of Qwirkle scores per turn')
    plt.text(47, 17, r'$\mu={},\ \sigma={}$'.format(mu, sigma))
    #plt.axis([40, 160, 0, 0.03])
    plt.grid(True)
    plt.show()


# plot_distribution_of_game_lengths()
# plot_tiles_on_board()
# plot_tiles_played()
# plot_score()
# plot_num_max_score_moves()
# unique_tiles_on_hand()
# unique_tiles_on_hand_no_zeros()
# plot_forbidden_positions()
plot_playable_positions()
# plot_legal_moves_sfa_tiles_on_board()
# plot_score_distribution()