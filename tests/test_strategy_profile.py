from unittest import TestCase
from player import Player
from resource import Resource
from strategy_profile import StrategyProfile

class StrategyProfileTest(TestCase):
    def setUp(self):
        player1 = Player(1,1.1)
        player2 = Player(2,4)
        self.__players = {player1.get_id():player1,player2.get_id():player2}
        cost = {1:1,2:2}
        failure_probability = {1:0.01,2:0.26}
        resource1 = Resource(1, cost, failure_probability)
        resource2 = Resource(2, cost, failure_probability)
        self.__resources = {resource1.get_id():resource1, resource2.get_id():resource2}
        self.__strategies = {1:{1},2:{1,2}}
        self.__profile = StrategyProfile(self.__strategies, self.__players, self.__resources)

    def test_check_even(self):
        result = self.__profile.check_even()
        expected = None
        self.assertEqual(expected, result)

    def test_get_congestion(self):
        result = self.__profile.get_congestion()
        expected = {1:2,2:1}
        self.assertEqual(expected, result)

    def test_simulate_change(self):
        result = self.__profile.simulate_change({1,2}, 1)
        expected = False
        self.assertEqual(expected, result)

    def test_calculate_utility(self):
        result = self.__profile.calculate_utility(2, self.__profile.get_strategies()[2], self.__profile.get_congestion())
        expected = 4 * (1 - 0.01 * 0.26) - (1 + 2)
        self.assertEqual(result, expected)

    def tearDown(self):
        del self.__profile