import random
import datetime

from constraints import Constraint
from heuristics import Heuristic
from generators import Generator

class GameRosterGenerator(Generator):
    def __init__(self, players):
        self.players = players
        random.seed(datetime.datetime.now())
    
    def generate(self):
        first_half_players = list(self.players)
        second_half_players = list(self.players)
        while len(first_half_players) < 2 * 7:
            spots_to_fill = 2 * 7 - len(first_half_players)
            first_half_players += random.sample(self.players, min(len(self.players), spots_to_fill))
            second_half_players += random.sample(self.players, min(len(self.players), spots_to_fill))
        
        random.shuffle(first_half_players)
        random.shuffle(second_half_players)

        game_players = first_half_players + second_half_players
        
        quarters = []
        for i in range(4):
            goalie = game_players.pop()
            defenders = [game_players.pop(), game_players.pop()]
            midfielders = [game_players.pop(), game_players.pop()]
            forwards = [game_players.pop(), game_players.pop()]
            quarters.append(QuarterRoster(goalie, defenders, midfielders, forwards))
            
        return GameRoster(quarters)

class GameRoster:
    def __init__(self, quarter_rosters):
        self.quarter_rosters = quarter_rosters
    
    def __eq__(self, other):
        if isinstance(other, GameRoster):
            return self.quarter_rosters == other.quarter_rosters
        return False
    
    def __neq__(self, other):
        return not self.__eq__(other)

    def get_all_players(self):
        retval = set()
        for roster in self.quarter_rosters:
            retval = retval.intersection(roster.get_all_players())
        return retval

class QuarterRoster:
    def __init__(self, goalie, defs, mids, fwds):
        self.goalie = goalie
        self.defenders = set(defs)
        self.midfielders = set(mids)
        self.forwards = set(fwds)
    
    def __eq__(self, other):
        if isinstance(other, QuarterRoster):
            return \
                self.goalie == other.goalie and \
                self.defenders == other.defenders and \
                self.midfielders == other.midfielders and \
                self.forwards == other.forwards
        else:
            return False
    
    def __neq__(self, other):
        return not self.__eq__(other)
    
    def get_all_players(self):
        return set([self.goalie]).union(self.defenders).union(self.midfielders).union(self.forwards)
    
    def get_all_players_and_positions(self):
        return set([(self.goalie, 'goalie')] + \
            [(p, 'defender') for p in self.defenders] + \
            [(p, 'midfielder') for p in self.midfielders] + \
            [(p, 'forward') for p in self.forwards])
    
    def get_position_of_player(self, player):
        if self.goalie == player:
            return 'goalie'
        if player in self.defenders:
            return 'defender'
        if player in self.midfielders:
            return 'midfielder'
        if player in self.forwards:
            return 'forward'
        return False

class PositionPreference:
    def __init__(self, preference_dict):
        self.preference_dict = preference_dict
    
    def get_score(self, position):
        if position in self.preference_dict.keys():
            return self.preference_dict[position]
        else:
            return 0

class PlayingTimeConstraint(Constraint):
    def __init__(self, players, minimum_quarters):
        self.players = players
        self.minimum_quarters = minimum_quarters
    
    def is_met(self, game_roster):
        player_quarters = dict()
        for player in self.players:
            player_quarters[player] = ''
        
        for i in range(len(game_roster.quarter_rosters)):
            for p in game_roster.quarter_rosters[i].get_all_players():
                player_quarters[p] += str(i + 1)
            
        min_time = 4
        max_time = 0

        for p in player_quarters.keys():
            quarters_played = player_quarters[p]
            num = len(quarters_played)
            if num < self.minimum_quarters:
                return False
            
            if quarters_played in ('12', '34', '14'):
                return False
            
            min_time = min(min_time, num)
            max_time = max(max_time, num)
        
        if max_time > min_time + 1:
            return False
        return True


class MinimumGoodPlayersConstraint(Constraint):
    def __init__(self, good_players, minimum):
        self.good_players = set(good_players)
        self.minimum = minimum
    
    def is_met(self, game_roster):
        for roster in game_roster.quarter_rosters:
            if len(self.good_players.intersection(roster.get_all_players())) < self.minimum:
               return False
        return True

class UniqueQuartersConstraint(Constraint):
    def is_met(self, game_roster):
        for i in range(4):
            for j in range(i + 1, 4):
                thisq = game_roster.quarter_rosters[i]
                otherq = game_roster.quarter_rosters[j]
                if thisq is otherq:
                    return False
        return True

class PlayerPositionVarietyConstraint(Constraint):
    def __init__(self, players, minimum_positions):
        self.players = players
        self.minimum_positions = 2
    
    def is_met(self, game_roster):
        player_positions = dict()
        for player in self.players:
            player_positions[player] = set()
        
        for i in range(len(game_roster.quarter_rosters)):
            for (player, position) in game_roster.quarter_rosters[i].get_all_players_and_positions():
                player_positions[player].add(position)
        
        for player in self.players:
            if len(player_positions[player]) < self.minimum_positions:
                return False
        return True
        
        

class PositionPreferenceHeuristic(Heuristic):
    def __init__(self, preferences):
        self.preferences = preferences

    def _calc_unweighted_score(self, game_roster):
        score = 0
        for q in game_roster.quarter_rosters:
            score += self._calc_quarter_score(q)
        return score
            
    def _calc_quarter_score(self, quarter_roster):
        score = 0
        for (player, position) in quarter_roster.get_all_players_and_positions():
            score += self._calc_player_preference(player, position)
        return score

    def _calc_player_preference(self, player, position):
        if player not in self.preferences.keys():
            return 0
        return self.preferences[player].get_score(position)
        
        

