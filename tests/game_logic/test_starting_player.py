from qwirkle.game_logic.game import Game


def test_one_player():
    player = MockPlayer(1)
    result = Game.determine_starting_player([player])
    assert player == result


def test_two_first_best():
    player1 = MockPlayer(2)
    player2 = MockPlayer(1)
    result = Game.determine_starting_player([player1, player2])
    assert player1 == result


def test_two_second_best():
    player1 = MockPlayer(1)
    player2 = MockPlayer(2)
    result = Game.determine_starting_player([player1, player2])
    assert player2 == result


def test_three_1_2_3():
    player1 = MockPlayer(1)
    player2 = MockPlayer(2)
    player3 = MockPlayer(3)
    players = [player1, player2, player3]
    result = Game.determine_starting_player(players)
    assert player3 == result


def test_three_3_2_1():
    player1 = MockPlayer(3)
    player2 = MockPlayer(2)
    player3 = MockPlayer(1)
    players = [player1, player2, player3]
    result = Game.determine_starting_player(players)
    assert player1 == result


def test_three_1_2_1():
    player1 = MockPlayer(1)
    player2 = MockPlayer(2)
    player3 = MockPlayer(1)
    players = [player1, player2, player3]
    result = Game.determine_starting_player(players)
    assert player2 == result


def test_three_1_2_2():
    player1 = MockPlayer(1)
    player2 = MockPlayer(2)
    player3 = MockPlayer(2)
    players = [player1, player2, player3]
    result = Game.determine_starting_player(players)
    assert result in [player2, player3]


class MockPlayer():
    def __init__(self, starting_score):
        self.hand = MockHand(starting_score)


class MockHand():
    def __init__(self, starting_score):
        self.score = starting_score

    def starting_score(self):
        return self.score
