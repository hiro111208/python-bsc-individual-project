from unittest import TestCase
from cglf import CGLF
from player import Player
from resource import Resource
from strategy_profile import StrategyProfile

class CGLFTest(TestCase):
    def setUp(self):
        player1 = Player(1,1.1)
        player2 = Player(2,4)
        self.players = {player1.id:player1,player2.id:player2}
        cost = {1:1,2:2}
        failure_probability = {1:0.01,2:0.26}
        resource1 = Resource(1, cost, failure_probability)
        resource2 = Resource(2, cost, failure_probability)
        self.resources = {resource1.id:resource1, resource2.id:resource2}
        self.cglf = CGLF(self.players, self.resources)

    def test_set_strategy_set(self):
        result = self.cglf.set_strategy_set(self.resources)
        expected = [set(), {1}, {2}, {1,2}]
        self.assertEqual(result, expected)

    # Since eac
    def test_build_strategy_profiles(self):
        profiles = self.cglf.build_strategy_profiles()
        result = {profile.social_utility for profile in profiles}
        expected = {StrategyProfile({1:{}, 2:{}}, self.players, self.resources).social_utility, 
                    StrategyProfile({1:{1}, 2:{}}, self.players, self.resources).social_utility,
                    StrategyProfile({1:{2}, 2:{}}, self.players, self.resources).social_utility,
                    StrategyProfile({1:{1,2}, 2:{}}, self.players, self.resources).social_utility,
                    StrategyProfile({1:{}, 2:{1}}, self.players, self.resources).social_utility,
                    StrategyProfile({1:{1}, 2:{1}}, self.players, self.resources).social_utility,
                    StrategyProfile({1:{2}, 2:{1}}, self.players, self.resources).social_utility,
                    StrategyProfile({1:{1,2}, 2:{1}}, self.players, self.resources).social_utility,
                    StrategyProfile({1:{}, 2:{2}}, self.players, self.resources).social_utility,
                    StrategyProfile({1:{1}, 2:{2}}, self.players, self.resources).social_utility,
                    StrategyProfile({1:{2}, 2:{2}}, self.players, self.resources).social_utility,
                    StrategyProfile({1:{1,2}, 2:{2}}, self.players, self.resources).social_utility,
                    StrategyProfile({1:{}, 2:{1,2}}, self.players, self.resources).social_utility,
                    StrategyProfile({1:{1}, 2:{1,2}}, self.players, self.resources).social_utility,
                    StrategyProfile({1:{2}, 2:{1,2}}, self.players, self.resources).social_utility,
                    StrategyProfile({1:{1,2}, 2:{1,2}}, self.players, self.resources).social_utility}
        self.assertEqual(result, expected)


    def tearDown(self):
        del self.cglf