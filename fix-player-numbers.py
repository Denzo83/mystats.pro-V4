#!/usr/bin/env python3
"""
Helper script to create a mapping between EasyStats numbers and actual jersey numbers
This is useful when the app exports different numbers than the players actually wear

Usage:
1. Create a mapping file (mapping.json) with format:
   {
     "1": "14",   // EasyStats shows #1, but player actually wears #14 (Rhys Ogle)
     "11": "24",  // EasyStats shows #11, but player actually wears #24 (Josh Todd)
     "28": "28",  // Correct already
     "37": "37"   // Correct already
   }

2. Run: python fix_player_numbers.py mapping.json

This will update all game files and regenerate stats with correct numbers.
"""

import json
from pathlib import Path
import shutil
from datetime import datetime

def create_backup(base_dir='data'):
    """Create backup of data folder"""
    base_dir = Path(base_dir)
    backup_dir = Path(f'data_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    
    shutil.copytree(base_dir, backup_dir)
    print(f"✓ Created backup: {backup_dir}")
    return backup_dir

def load_mapping(mapping_file):
    """Load number mapping from JSON file"""
    with open(mapping_file, 'r') as f:
        mapping = json.load(f)
    
    print("\nNumber Mapping:")
    for old, new in mapping.items():
        print(f"  #{old} → #{new}")
    
    return mapping

def remap_game_file(game_file, mapping):
    """Remap player numbers in a game file"""
    with open(game_file, 'r') as f:
        game = json.load(f)
    
    # Remap stats
    new_stats = {}
    for old_num, stats in game['stats'].items():
        new_num = mapping.get(old_num, old_num)
        new_stats[new_num] = stats
    
    game['stats'] = new_stats
    
    # Save updated game
    with open(game_file, 'w') as f:
        json.dump(game, f, indent=2)

def remap_players_file(players_file, mapping):
    """Remap player numbers in players.json"""
    with open(players_file, 'r') as f:
        players = json.load(f)
    
    new_players = {}
    for old_num, player in players.items():
        new_num = mapping.get(old_num, old_num)
        player['number'] = new_num
        new_players[new_num] = player
    
    with open(players_file, 'w') as f:
        json.dump(new_players, f, indent=2)

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python fix_player_numbers.py <mapping.json>")
        print("\nExample mapping.json:")
        print('''{
  "1": "14",
  "11": "24",
  "2": "11",
  "5": "5",
  "10": "15",
  "28": "28",
  "37": "37",
  "43": "43"
}''')
        sys.exit(1)
    
    mapping_file = sys.argv[1]
    
    if not Path(mapping_file).exists():
        print(f"Error: Mapping file not found: {mapping_file}")
        sys.exit(1)
    
    # Create backup
    print("Creating backup...")
    backup_dir = create_backup()
    
    # Load mapping
    mapping = load_mapping(mapping_file)
    
    # Get confirmation
    response = input("\nThis will update all game files and players.json. Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Aborted.")
        sys.exit(0)
    
    base_dir = Path('data')
    
    # Remap all game files
    print("\nUpdating game files...")
    games_dir = base_dir / 'games'
    game_count = 0
    for game_file in games_dir.glob('*.json'):
        remap_game_file(game_file, mapping)
        game_count += 1
        print(f"  ✓ {game_file.name}")
    
    # Remap players.json
    print("\nUpdating players.json...")
    players_file = base_dir / 'players.json'
    if players_file.exists():
        remap_players_file(players_file, mapping)
        print("  ✓ players.json")
    
    print(f"\n✅ Updated {game_count} game files")
    print("\nNext steps:")
    print("1. Run the parser again to regenerate season stats and records")
    print("2. Backup saved to:", backup_dir)

if __name__ == '__main__':
    main()
