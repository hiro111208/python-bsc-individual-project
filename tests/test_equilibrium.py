from unittest import TestCase
from player import Player
from resource import Resource
from equilibrium import Equilibrium

class Equilibrium(TestCase):
    def setUp(self):
        player1 = Player(1,1.1)
        player2 = Player(2,4)
        self.players = {player1.id:player1,player2.id:player2}
        cost = {1:1,2:2}
        failure_probability = {1:0.1,2:0.2}
        resource1 = Resource(1, cost, failure_probability)
        resource2 = Resource(2, cost, failure_probability)
        self.resources = {resource1.id:resource1, resource2.id:resource2}
        self.equilibrium = Equilibrium(self.players, self.resources)

    def test_step0(self):
        result = self.equilibrium
        expected = (2.96 + 0.089)
        self.assertEqual(result, expected)


    def tearDown(self):
        del self.equilibrium