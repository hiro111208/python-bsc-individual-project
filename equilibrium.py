from strategy_profile import StrategyProfile

class Equilibrium():

    def __init__(players, resources):
        self.k = len(players)
        self.xD = dict() # key; int, value; int
        self.xA = dict() # key; int, value; int
        self.x = dict() # key; int, value; int

        self.players = players
        self.resources = resources
        #print(self.step0())

    def calculate_marginal_benefit(self, player, congestion, number_of_resources):
        return player.benefit * (self.resources[0].get_failure_probability(congestion)**(number_of_resources))

    def calculate_marginal_cost(self, congestion):
        return self.resources[0].get_cost(congestion)/(1-self.resources[0].get_failure_probability(congestion))

    def sigma(start, end, collection: dict) -> float:
        sum = 0
        for i in range(start, end + 1):
            sum += collection[i]
        return sum

    def step0(self): # done
        player = min(self.players, key=lambda x:x.benefit)
        if self.calculate_marginal_benefit(player, len(self.players), len(self.resources)-1) >= self.calculate_marginal_cost(len(self.players)): # player with the lowest benefit
            print(f'Found equilibrium')
            return even_profiles[k][0]
        else:
            self.k -= 1
            self.step1()

    def step1(self): # done
        for player in self.players:
            XD = []
            for x in range(1, len(self.resources)+1):
                if self.calculate_marginal_benefit(player, k, x-1) >= self.calculate_marginal_cost(k):
                    XD.append(x)
            if XD == []:
                self.xD[player.id] = 0
            else:
                # self.xD.append(max(X))
                self.xD[player.id] = max(XD)
        if sum(self.xD.values()) < self.k * len(self.resources):
            self.k -= 1
            self.step2()
        else:
            self.step3()

    def step2(self): # done
        if self.k == 0:
            #strategy_profiles = self.strategy_profiles
            strategies = dict()
            resource_index = 1
            for player in self.players:
                if self.xD[player.id] > 0:
                    strategy = set()
                    for i in range(resource_index, self.xD[player.id] + 1):
                        strategy.add(self.resources[i])
                    resource_index += self.xD[player.id]
                    strategies[player.id] = strategy
                    #strategy_profiles = list(filter(lambda x: len(x.strategies[player]) == self.xD[player]))
                else:
                    strategies[player.id] = set()
                    #strategy_profiles = list(filter(lambda x: x.strategies[player] == set()))
            #return strategy_profiles[0]
            return StrategyProfile(strategies, self.players, self.resources)
        else:
            self.step1()

    def step3(self):
        for player in self.players:
            XA = []
            for x in range(len(self.resources)):
                if self.calculate_marginal_benefit(player, k, x) <= self.calculate_marginal_cost(k+1):
                    XA.append(x)
            if XA == []:
                xA[player.id] = len(self.resources)
            else:
                xA[player.id] = min(XA)
        if sum(xA.values()) > self.k * len(self.resources) or any(xA[player.id] > xD[player.id] for player in self.players):
            self.step5(strategy_profile) # k*-even, post-addition D-stable profile
        else:
            self.step4()

    def step4(self): # needs research about strategy profile, profile is k*-even, D-stable
        d = dict()
        strategies = {key:set() for key in self.players}
        for i in range(1, len(self.players) + 1):
            d[i] = self.k * len(self.resources) - self.sigma(1, i, strategies) - self.sigma(i, n + 1, self.xA)
            r = min([self.xD[i], self.xA[i] + d[i]])
            strategy = set()
            for i in range(resource_index, r + 1):
                strategy.add(self.resources[i])
            resource_index = (resource_index + r) % len(self.resources)
            strategies[self.players[i]] = strategy # needs to be fixed to link strategy and player
        return StrategyProfile(strategies, self.players, self.resources)

    def step5(self): # needs research in the same way as step4, profile is k*-even D-stable not A-stable
        for player in self.players:
            X = []
            for x in range(1, len(self.resources) + 1):
                if self.calculate_marginal_benefit(player, k, x - 1) <= self.calculate_marginal_cost(k + 1):
                    X.append(x)
            if X == []:
                self.x[player.id] = 0
            else:
                self.x[player.id] = max(X)
        resource_index = 1
        strategies = {key:set() for key in self.players}
        for i in range(1, len(self.players) + 1):
            if self.k * len(self.resources) - self.sigma(1, i, strategies) > 0:
                r = min([self.x[i], self.k * len(self.resources) - self.sigma(1, i, strategies)])
                strategy = set()
                for i in range(resource_index, r + 1):
                    strategy.add(self.resources[i])
                resource_index = (resource_index + r) % len(self.resources)
                strategies[player.id] = strategy # needs to be fixed to link strategy and player
            else:
                strategies[player.id] = set() # needs to be fixed to link strategy and player
        self.step6(StrategyProfile(strategies, self.players, self.resources))

    def step6(self, strategy_profile): # done
        # a_move_players = []
        a_move_resources = [] # M(sigma)
        for player in self.players:
            # option = {x: strategy_profile.get_congestion()[x] for x in strategy_profile.get_congestion() if x not in strategies[player]}
            option = {key:value for key, value in strategy_profile.congestion.items() if not key in strategy_profile.strategies[player]}
            light_resource = min(option, key=option.get) # option must be dict
            if strategy_profile.simulate_change(strategy_profile.strategies[player].add(light_resource), player):
                #a_move_players.append(player)
                #a_move_resources.append(light_resource)
                a_move_resources[player] = light_resource
        if len(a_move_resources) == 0:
            # the profile is confirmed to be A-stable
            return strategy_profile
        else:
            self.step7(strategy_profile, a_move_resources)

    def step7(self, strategy_profile, a_move_resources): # done
        a_move_player, light_resource_a = min(a_move_resources.items(), key=lambda x: x[1])
        if light_resource == min(strategy_profile.congestion.items(), key=lambda x: x[1])[0]
            # one step addition
            strategies[a_move_player] = strategies[a_move_player].update({light_resource})
        else:
            # two step addition
            light_resource_b = min(strategy_profile.congestion, key=strategy_profile.congestion.get)
            player_j = [key for key, value in strategy_profile.strategies.items() if light_resource_a in value and not light_resource_b in value][0]
            strategies[a_move_player] = strategies[a_move_player].update({light_resource_a})
            strategies[player_j] = strategies[player_j].difference_update({light_resource_a})
            strategies[player_j] = strategies[player_j].update({light_resource_b})
        self.step6(StrategyProfile(strategies, self.players, self.resources))