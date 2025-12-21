#!/usr/bin/env python3
"""
Helper script to import existing player data into the new format
Merges old player data with current players.json while preserving stats
"""

import json
from pathlib import Path

def import_players(old_players_file, base_dir='data'):
    """Import players from old JSON format"""
    
    base_dir = Path(base_dir)
    players_file = base_dir / 'players.json'
    
    # Load old players data
    with open(old_players_file, 'r') as f:
        old_players = json.load(f)
    
    # Load existing players.json if it exists
    if players_file.exists():
        with open(players_file, 'r') as f:
            current_players = json.load(f)
    else:
        current_players = {}
    
    # Merge players
    for old_player in old_players:
        number = str(old_player['number'])
        
        if number in current_players:
            # Update existing player with additional info
            current_players[number].update({
                'id': old_player['id'],
                'display_name': old_player['display_name'],
                'name': old_player['name'],
                'position': old_player.get('position', ''),
                'images': old_player.get('images', {})
            })
            
            # Merge teams (keep unique)
            old_teams = old_player.get('teams', [])
            current_teams = current_players[number].get('teams', [])
            merged_teams = list(set(current_teams + old_teams))
            current_players[number]['teams'] = merged_teams
        else:
            # Add new player
            current_players[number] = {
                'id': old_player['id'],
                'display_name': old_player['display_name'],
                'name': old_player['name'],
                'number': number,
                'position': old_player.get('position', ''),
                'teams': old_player.get('teams', []),
                'images': old_player.get('images', {})
            }
    
    # Save updated players.json
    with open(players_file, 'w') as f:
        json.dump(current_players, f, indent=2)
    
    print(f"✓ Updated players.json with {len(old_players)} players")
    print(f"✓ Total players now: {len(current_players)}")
    
    # Print summary
    print("\nPlayer Summary:")
    for number, player in sorted(current_players.items(), key=lambda x: int(x[0])):
        teams_str = ', '.join(player.get('teams', []))
        pos_str = f" ({player.get('position', 'N/A')})" if player.get('position') else ""
        print(f"  #{number:2s} - {player['display_name']:20s}{pos_str:10s} - {teams_str}")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python import_players.py <old_players.json>")
        print("Example: python import_players.py old_players.json")
        sys.exit(1)
    
    old_players_file = sys.argv[1]
    
    if not Path(old_players_file).exists():
        print(f"Error: File not found: {old_players_file}")
        sys.exit(1)
    
    import_players(old_players_file)
    print("\n✅ Import complete!")

if __name__ == '__main__':
    main()
