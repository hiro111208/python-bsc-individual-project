from unittest import TestCase
from player import Player
from resource import Resource
from strategy_profile import StrategyProfile

class StrategyProfileTest(TestCase):
    def setUp(self):
        player1 = Player(1,1.1)
        player2 = Player(2,4)
        self.players = {player1.id:player1,player2.id:player2}
        cost = {1:1,2:2}
        failure_probability = {1:0.01,2:0.26}
        resource1 = Resource(1, cost, failure_probability)
        resource2 = Resource(2, cost, failure_probability)
        self.resources = {resource1.id:resource1, resource2.id:resource2}
        self.strategies = {1:{1},2:{1,2}}
        self.profile = StrategyProfile(self.strategies, self.players, self.resources)

    def test_check_even(self):
        result = self.profile.check_even()
        expected = None
        self.assertEqual(expected, result)

    def test_get_congestion(self):
        result = self.profile.get_congestion(self.strategies)
        expected = {1:2,2:1}
        self.assertEqual(expected, result)

    def test_simulate_change(self):
        result = self.profile.simulate_change({1,2}, 1)
        expected = False
        self.assertEqual(expected, result)

    def test_calculate_utility(self):
        result = self.profile.calculate_utility(self.profile.players[2].id, self.profile.strategies[2], self.profile.congestion)
        expected = 4 * (1 - 0.01 * 0.26) - (1 + 2)
        #percentage_difference = abs((result - expected) / expected)
        #self.assertGreater(0.00001, percentage_difference)
        self.assertEqual(result, expected)

    def tearDown(self):
        del self.profile