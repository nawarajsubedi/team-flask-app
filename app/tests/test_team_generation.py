import unittest
from unittest.mock import MagicMock
from app.services.team_generation_service import generate_balanced_teams

class TestGenerateBalancedTeams(unittest.TestCase):

    def setUp(self):
        self.players = [
            MagicMock(id=1, name="Player 1", skill_level=5),
            MagicMock(id=2, name="Player 2", skill_level=4),
            MagicMock(id=3, name="Player 3", skill_level=3),
            MagicMock(id=4, name="Player 4", skill_level=2),
            MagicMock(id=5, name="Player 5", skill_level=1),
        ]

    def test_balanced_teams_case_1(self):
        num_teams = 2
        team_info = [
            MagicMock(id=1, name="Team A"),
            MagicMock(id=2, name="Team B"),
        ]
        teams = generate_balanced_teams(self.players, num_teams, team_info)
        self.assertEqual(len(teams), num_teams)

    def test_balanced_teams_case_2(self):
        num_teams = 3
        team_info = [
            MagicMock(id=1, name="Team A"),
            MagicMock(id=2, name="Team B"),
            MagicMock(id=3, name="Team C"),
        ]
        teams = generate_balanced_teams(self.players, num_teams, team_info)
        self.assertEqual(len(teams), num_teams)

    def test_balanced_teams_case_3(self):
        self.players += [
            MagicMock(id=6, name="Player 6", skill_level=3),
            MagicMock(id=7, name="Player 7", skill_level=4),
            MagicMock(id=8, name="Player 8", skill_level=2),
        ]
        num_teams = 3
        team_info = [
            MagicMock(id=1, name="Team A"),
            MagicMock(id=2, name="Team B"),
            MagicMock(id=3, name="Team C"),
        ]
        teams = generate_balanced_teams(self.players, num_teams, team_info)
        self.assertEqual(len(teams), num_teams)

    def test_balanced_teams_case_4(self):
        num_teams = 2
        team_info = [
            MagicMock(id=1, name="Team A"),
            MagicMock(id=2, name="Team B"),
        ]
        teams = generate_balanced_teams(self.players, num_teams, team_info)
        # Check that teams have members distributed correctly
        self.assertTrue(all(len(team["members"]) > 0 for team in teams))

    def test_balanced_teams_case_5(self):
        self.players += [
            MagicMock(id=9, name="Player 9", skill_level=5),
            MagicMock(id=10, name="Player 10", skill_level=1),
        ]
        num_teams = 3
        team_info = [
            MagicMock(id=1, name="Team A"),
            MagicMock(id=2, name="Team B"),
            MagicMock(id=3, name="Team C"),
        ]
        teams = generate_balanced_teams(self.players, num_teams, team_info)

        # Calculate team weights based on returned structure
        team_weights = [
            sum(member["skill_level"] for member in team["members"]) for team in teams
        ]
        # Verify that the total skill levels of the teams are close
        self.assertLess(max(team_weights) - min(team_weights), 3)  # Adjust threshold as needed

if __name__ == "__main__":
    unittest.main()
