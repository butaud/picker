import sys

sys.path.append('./models')

from models.picker import Picker
from soccer import models as soccer

def output(message):
    print(message)

def output_quarter_roster(quarter_roster):
    output("      " + quarter_roster.goalie)
    for bank in [quarter_roster.defenders, quarter_roster.midfielders, quarter_roster.forwards]:
        output("     ".join(bank))

def output_roster(game_roster):
    for i in range(4):
        output("====== Q" + str(i + 1) + " =====")
        output_quarter_roster(game_roster.quarter_rosters[i])

def main():
    players = ["Asher", "Ransom", "Jacob", "Zeke", "Nolan", "Kylas", "Timothy", "Peter", "Aiden", "Owen", "Cyrus", "Marc", "Jude", "Elias"]
    constraints = [\
        soccer.MinimumGoodPlayersConstraint(["Jacob", "Zeke", "Nolan", "Kylas", "Ransom"], 2),\
        soccer.UniqueQuartersConstraint(),\
        soccer.PlayingTimeConstraint(players, 2),\
        soccer.PlayerPositionVarietyConstraint(players, 2),\
    ]
    heuristics = [\
        soccer.PositionPreferenceHeuristic({\
            'Asher': soccer.PositionPreference({'defender': 1, 'forward': -1, 'goalie': -1}),\
            'Timothy': soccer.PositionPreference({'goalie': 5}),\
            'Jacob': soccer.PositionPreference({'forward': 1}),\
            'Zeke': soccer.PositionPreference({'defender': -1, 'goalie': -1}),\
            'Peter': soccer.PositionPreference({'defender': 1, 'goalie': 5}),\
            'Aiden': soccer.PositionPreference({'defender': 1}),\
            'Cyrus': soccer.PositionPreference({'defender': -1, 'goalie': -1}),\
            'Marc': soccer.PositionPreference({'defender': 1}),\
            'Elias': soccer.PositionPreference({'defender': 1, 'forward': -1})\
        })\
    ]
    generator = soccer.GameRosterGenerator(players)

    picker = Picker(generator, constraints, heuristics)
    picker.output_func = output
    picker.choices_to_compare = 30
    roster = picker.pick()

    if roster is not None:
        output_roster(roster)
    else:
        print("No roster found")
    

if __name__ == "__main__":
    main()