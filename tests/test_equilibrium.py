from unittest import TestCase
from player import Player
from resource import Resource
from equilibrium import Equilibrium

class EquilibriumTest(TestCase):
    def setUp(self):
        player1 = Player(1,4)
        player2 = Player(2,1.1)
        self.players = {player1.id:player1,player2.id:player2}
        cost = {1:1,2:2}
        failure_probability = {1:0.01,2:0.26}
        resource1 = Resource(1, cost, failure_probability)
        resource2 = Resource(2, cost, failure_probability)
        self.resources = {resource1.id:resource1, resource2.id:resource2}
        self.equilibrium = Equilibrium(self.players, self.resources)

    def test_step0(self):
        result = self.equilibrium.profile
        expected = 2.96 + 0.089
        self.assertEqual(result.social_utility, expected)

    def test_sigma_1(self):
        start = 1
        end = 0
        d = {1:{1,2,3},2:{4,5},3:{1}}
        result = self.equilibrium.sigma(start, end, d)
        self.assertEqual(result, 0)

    def tearDown(self):
        del self.equilibrium