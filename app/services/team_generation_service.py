def calculate_team_weight(team):
    """Calculate the total skill level of a team."""
    return sum(player.skill_level for player in team)


def swap_players(teams, max_swaps=100, threshold=1):
    """Balance teams by swapping players to minimize skill difference."""
    swaps = 0
    while swaps < max_swaps:
        # Calculate total skill for each team
        team_weights = [calculate_team_weight(team) for team in teams]
        min_weight = min(team_weights)
        max_weight = max(team_weights)

        # Stop if teams are balanced enough
        if max_weight - min_weight <= threshold:
            break

        # Identify teams with min and max weights
        min_team_index = team_weights.index(min_weight)
        max_team_index = team_weights.index(max_weight)

        made_swap = False  # Track if a swap was made

        for player_from_max in teams[max_team_index][:]:  # Use a copy of the list
            for player_from_min in teams[min_team_index][:]:  # Use a copy of the list
                # Perform the swap
                teams[max_team_index].remove(player_from_max)
                teams[min_team_index].remove(player_from_min)
                teams[max_team_index].append(player_from_min)
                teams[min_team_index].append(player_from_max)

                # Check new weights after the swap
                new_min_weight = calculate_team_weight(teams[min_team_index])
                new_max_weight = calculate_team_weight(teams[max_team_index])

                # If the swap improves balance, keep it; otherwise, revert
                if abs(new_max_weight - new_min_weight) < abs(max_weight - min_weight):
                    swaps += 1
                    made_swap = True  # A swap was made
                    break  # Break out of inner loop
                else:
                    # Revert the swap
                    teams[max_team_index].remove(player_from_min)
                    teams[min_team_index].remove(player_from_max)
                    teams[max_team_index].append(player_from_max)
                    teams[min_team_index].append(player_from_min)

            if made_swap:
                break  # Exit the outer loop if a swap was made

        if not made_swap:
            # No beneficial swaps were made, exit the loop to avoid infinite loop
            break

    return teams


def generate_balanced_teams(players, num_teams, team_info):
    """Generate balanced teams from a list of players and include team ID and name."""
    # Sort players by skill level (high to low)
    players.sort(key=lambda p: p.skill_level, reverse=True)

    # Initialize teams with IDs and names
    teams = {team['id']: {"name": team['name'], "members": []} for team in team_info}

    # Distribute top players across teams
    for i in range(num_teams):
        if players:
            team_id = list(teams.keys())[i]
            teams[team_id]["members"].append(players.pop(0))

    # Round-robin distribution of remaining players
    for i, player in enumerate(players):
        team_index = i % num_teams
        team_id = list(teams.keys())[team_index]
        teams[team_id]["members"].append(player)

    # Balance teams
    balanced_teams = swap_players([team["members"] for team in teams.values()])

    # Convert players to a JSON-serializable format
    return [
        {
            "id": team_id,
            "name": teams[team_id]["name"],
            "members": [
                {
                    "id": player.id,
                    "name": player.name,
                    "skill_level": player.skill_level,
                }
                for player in balanced_teams[i]
            ],
        }
        for i, team_id in enumerate(teams.keys())
    ]
