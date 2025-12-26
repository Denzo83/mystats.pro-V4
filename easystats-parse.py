#!/usr/bin/env python3
"""
EasyStats HTML to JSON Parser
Parses EasyStats basketball HTML exports and updates JSON data files
"""

import json
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path

class EasyStatsParser:
    def __init__(self, base_dir='data'):
        self.base_dir = Path(base_dir)
        self.players_file = self.base_dir / 'players.json'
        self.games_dir = self.base_dir / 'games'
        self.records_file = self.base_dir / 'records.json'
        self.seasons_dir = self.base_dir / 'seasons'
        self.games_index_file = self.base_dir / 'games_index.json'
        
        # Create directories if they don't exist
        self.base_dir.mkdir(exist_ok=True)
        self.games_dir.mkdir(exist_ok=True)
        self.seasons_dir.mkdir(exist_ok=True)
        
        # Load existing data
        self.players = self.load_json(self.players_file, {})
        self.records = self.load_json(self.records_file, {
            'regular': {},
            'playoff': {},
            'all': {}
        })
        self.games_index = self.load_json(self.games_index_file, {})
    
    def load_json(self, filepath, default):
        """Load JSON file or return default if doesn't exist"""
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return default
    
    def save_json(self, filepath, data):
        """Save data to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def parse_date(self, date_str):
        """Parse date string like '16 Dec 2025' to YYYY-MM-DD"""
        try:
            dt = datetime.strptime(date_str.strip(), '%d %b %Y')
            return dt.strftime('%Y-%m-%d')
        except:
            return datetime.now().strftime('%Y-%m-%d')
    
    def parse_title(self, title):
        """Parse title: 'Team1 Score1 at Team2 Score2' or similar"""
        # Remove "box-scores" suffix if present
        title = re.sub(r'-box-scores.*$', '', title)
        
        # Pattern: "Team1 Score1 at Team2 Score2"
        match = re.match(r'(.+?)\s+(\d+)\s+at\s+(.+?)\s+(\d+)', title)
        if match:
            return {
                'away_team': match.group(1).strip(),
                'away_score': int(match.group(2)),
                'home_team': match.group(3).strip(),
                'home_score': int(match.group(4))
            }
        return None
    
    def parse_stat_value(self, stat_str):
        """Parse stat string like '4-16' to [made, attempted]"""
        if not stat_str or stat_str == '-':
            return None
        
        if '-' in stat_str:
            parts = stat_str.split('-')
            return [int(parts[0]), int(parts[1])]
        
        try:
            return int(stat_str)
        except:
            return None
    
    def extract_player_number(self, name_str):
        """Extract player number from '#1 R. Ogle' format"""
        match = re.match(r'#(\d+)\s+(.+)', name_str.strip())
        if match:
            return match.group(1), match.group(2)
        return None, name_str.strip()
    
    def get_player_id(self, name, number):
        """Generate player ID from name"""
        # Remove periods and convert to lowercase
        name_clean = name.replace('.', '').strip().lower()
        # Replace spaces with hyphens
        return name_clean.replace(' ', '-')
    
    def merge_player_data(self, number, name):
        """Merge new player data with existing, preserving extra fields"""
        player_id = self.get_player_id(name, number)
        
        # If player exists, update teams list but keep other data
        if number in self.players:
            existing = self.players[number]
            # Keep all existing fields
            # Just update the name if it's more complete
            if len(name) > len(existing.get('name', '')):
                existing['name'] = name
                existing['display_name'] = name
                existing['id'] = player_id
        else:
            # Create new player entry
            self.players[number] = {
                'id': player_id,
                'display_name': name,
                'name': name,
                'number': number,
                'position': '',  # Can be manually updated
                'teams': [],
                'images': {
                    'portrait': f'Assets/players/{player_id}.png'
                }
            }
    
    def calculate_derived_stats(self, stats):
        """Calculate derived stats like 2PT, FG%, etc."""
        derived = {}
        
        # Extract made/attempted values
        fg = stats.get('fg', [0, 0])
        three_pt = stats.get('3pt', [0, 0])
        ft = stats.get('ft', [0, 0])
        
        if fg and three_pt:
            # Calculate 2PT (FG - 3PT)
            derived['2pt'] = [fg[0] - three_pt[0], fg[1] - three_pt[1]]
            derived['2pt_pct'] = round((derived['2pt'][0] / derived['2pt'][1] * 100), 1) if derived['2pt'][1] > 0 else 0
        
        # Calculate percentages
        derived['fg_pct'] = round((fg[0] / fg[1] * 100), 1) if fg and fg[1] > 0 else 0
        derived['3pt_pct'] = round((three_pt[0] / three_pt[1] * 100), 1) if three_pt and three_pt[1] > 0 else 0
        derived['ft_pct'] = round((ft[0] / ft[1] * 100), 1) if ft and ft[1] > 0 else 0
        
        # Total rebounds
        oreb = stats.get('oreb', 0) or 0
        dreb = stats.get('dreb', 0) or 0
        derived['reb'] = oreb + dreb
        
        return derived
    
    def parse_html(self, html_file, is_playoff=False, force_season=None):
        """Parse EasyStats HTML file and extract game data"""
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        # Extract game info
        title = soup.find('title')
        if not title:
            raise ValueError("No title found in HTML")
        
        game_info = self.parse_title(title.text)
        if not game_info:
            raise ValueError(f"Could not parse title: {title.text}")
        
        # Get date
        date_elem = soup.find('span', class_='detail')
        date = self.parse_date(date_elem.text) if date_elem else datetime.now().strftime('%Y-%m-%d')
        
        # Override season if specified
        if force_season:
            year = date[:4]  # Get current year from date
            date = date.replace(year, force_season)
        
        # Determine if our team is home or away (Pretty good is our team)
        our_team = "Pretty good"  # Standardized team name
        our_team_variants = ["pretty good", "pretty-good"]
        away_is_us = any(variant in game_info['away_team'].lower() for variant in our_team_variants)
        home_is_us = any(variant in game_info['home_team'].lower() for variant in our_team_variants)

        # Determine which one we are
        if away_is_us:
            is_home = False
            opponent = game_info['home_team']
        elif home_is_us:
            is_home = True
            opponent = game_info['away_team']
        else:
            # Neither team name matches - use default
            is_home = False
            opponent = game_info['home_team']   
                 
        opponent = game_info['away_team'] if is_home else game_info['home_team']
        our_score = game_info['home_score'] if is_home else game_info['away_score']
        their_score = game_info['away_score'] if is_home else game_info['home_score']
        
        # Parse stats table
        stats_table = soup.find('table', id='stats')
        if not stats_table:
            raise ValueError("No stats table found")
        
        rows = stats_table.find_all('tr')[1:]  # Skip header row
        
        player_stats = {}
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 2:
                continue
            
            # Extract player info
            player_name = cols[0].text.strip()
            number, name = self.extract_player_number(player_name)
            
            if not number:
                continue
            
            # Update players registry with merge logic
            self.merge_player_data(number, name)
            
            # Add team if not already listed
            if our_team not in self.players[number]['teams']:
                self.players[number]['teams'].append(our_team)
            
            # Check if player DNP (all stats are '-')
            if all(col.text.strip() == '-' for col in cols[1:]):
                continue
            
            # Parse stats (order from HTML: fg, fg%, 3pt, 3pt%, ft, ft%, oreb, dreb, foul, stl, to, blk, asst, pts)
            stats = {
                'fg': self.parse_stat_value(cols[1].text.strip()),
                '3pt': self.parse_stat_value(cols[3].text.strip()),
                'ft': self.parse_stat_value(cols[5].text.strip()),
                'oreb': self.parse_stat_value(cols[7].text.strip()),
                'dreb': self.parse_stat_value(cols[8].text.strip()),
                'foul': self.parse_stat_value(cols[9].text.strip()),
                'stl': self.parse_stat_value(cols[10].text.strip()),
                'to': self.parse_stat_value(cols[11].text.strip()),
                'blk': self.parse_stat_value(cols[12].text.strip()),
                'asst': self.parse_stat_value(cols[13].text.strip()),
                'pts': self.parse_stat_value(cols[14].text.strip())
            }
            
            # Calculate derived stats
            derived = self.calculate_derived_stats(stats)
            stats.update(derived)
            
            player_stats[number] = stats
        
        # Create game object
        game = {
            'date': date,
            'opponent': opponent,
            'homeAway': 'home' if is_home else 'away',
            'score': {
                'us': our_score,
                'them': their_score
            },
            'result': 'W' if our_score > their_score else 'L',
            'isPlayoff': is_playoff,  # Use the parameter instead of default False
            'stats': player_stats
        }
        
        return game, date, opponent
    
    def save_game(self, game, date, opponent):
        """Save game to appropriate JSON file"""
        # Create filename: YYYY-MM-DD-opponent.json
        opponent_slug = re.sub(r'[^a-z0-9]+', '-', opponent.lower()).strip('-')
        filename = f"{date}-{opponent_slug}.json"
        filepath = self.games_dir / filename
        
        self.save_json(filepath, game)
        print(f"✓ Saved game: {filepath}")
        
        # Update games index
        game_id = filename.replace('.json', '')
        self.games_index[game_id] = {
            'filename': filename,
            'date': date,
            'opponent': opponent,
            'score': game['score'],
            'result': game['result'],
            'isPlayoff': game['isPlayoff']
        }
        self.save_json(self.games_index_file, self.games_index)
        
        return filepath
    
    def update_records(self):
        """Update records from all games"""
        print("\nUpdating records...")
        
        # Initialize record structures
        record_categories = ['regular', 'playoff', 'all']
        stat_names = ['pts', 'reb', 'asst', 'stl', 'blk', 'to', 'fg', '3pt', 'ft']
        
        for category in record_categories:
            self.records[category] = {}
            for stat in stat_names:
                self.records[category][f'most_{stat}'] = {
                    'player': None,
                    'value': 0,
                    'date': None,
                    'opponent': None
                }
        
        # Process all games
        for game_file in self.games_dir.glob('*.json'):
            game = self.load_json(game_file, {})
            game_type = 'playoff' if game.get('isPlayoff') else 'regular'
            
            for player_num, stats in game.get('stats', {}).items():
                player_name = self.players.get(player_num, {}).get('name', f"#{player_num}")
                
                # Check each stat for records
                for stat in stat_names:
                    value = stats.get(stat)
                    
                    # Handle array values (fg, 3pt, ft) - use made shots
                    if isinstance(value, list):
                        value = value[0]
                    
                    if value is None or value == 0:
                        continue
                    
                    record_key = f'most_{stat}'
                    
                    # Update game type specific record
                    if value > self.records[game_type][record_key]['value']:
                        self.records[game_type][record_key] = {
                            'player': player_name,
                            'value': value,
                            'date': game['date'],
                            'opponent': game['opponent']
                        }
                    
                    # Update all-time record
                    if value > self.records['all'][record_key]['value']:
                        self.records['all'][record_key] = {
                            'player': player_name,
                            'value': value,
                            'date': game['date'],
                            'opponent': game['opponent']
                        }
        
        self.save_json(self.records_file, self.records)
        print("✓ Records updated")
    
    def update_season_stats(self):
        """Aggregate season statistics"""
        print("\nUpdating season statistics...")
        
        seasons = {}
        
        # Process all games
        for game_file in self.games_dir.glob('*.json'):
            game = self.load_json(game_file, {})
            year = game['date'][:4]  # Extract year
            game_type = 'playoff' if game.get('isPlayoff') else 'regular'
            
            if year not in seasons:
                seasons[year] = {
                    'regular': {},
                    'playoff': {},
                    'all': {}
                }
            
            # Aggregate stats for each player
            for player_num, stats in game.get('stats', {}).items():
                # Initialize player if not exists
                for category in ['regular', 'playoff', 'all']:
                    if player_num not in seasons[year][category]:
                        seasons[year][category][player_num] = {
                            'gp': 0,  # games played
                            'pts': 0, 'reb': 0, 'asst': 0, 'stl': 0, 'blk': 0, 'to': 0, 'foul': 0,
                            'fg': [0, 0], '2pt': [0, 0], '3pt': [0, 0], 'ft': [0, 0],
                            'oreb': 0, 'dreb': 0
                        }
                
                # Add to appropriate category
                for category in [game_type, 'all']:
                    player_season = seasons[year][category][player_num]
                    player_season['gp'] += 1
                    
                    # Sum counting stats
                    for stat in ['pts', 'reb', 'asst', 'stl', 'blk', 'to', 'foul', 'oreb', 'dreb']:
                        value = stats.get(stat, 0)
                        if value:
                            player_season[stat] += value
                    
                    # Sum shooting stats
                    for stat in ['fg', '2pt', '3pt', 'ft']:
                        value = stats.get(stat)
                        if value and isinstance(value, list):
                            player_season[stat][0] += value[0]
                            player_season[stat][1] += value[1]
        
        # Calculate averages and percentages for each season
        for year, season_data in seasons.items():
            for category in ['regular', 'playoff', 'all']:
                for player_num, stats in season_data[category].items():
                    gp = stats['gp']
                    if gp > 0:
                        # Calculate averages
                        stats['ppg'] = round(stats['pts'] / gp, 1)
                        stats['rpg'] = round(stats['reb'] / gp, 1)
                        stats['apg'] = round(stats['asst'] / gp, 1)
                        stats['spg'] = round(stats['stl'] / gp, 1)
                        stats['bpg'] = round(stats['blk'] / gp, 1)
                        stats['tpg'] = round(stats['to'] / gp, 1)
                        stats['fpg'] = round(stats['foul'] / gp, 1)
                        
                        # Calculate percentages
                        stats['fg_pct'] = round((stats['fg'][0] / stats['fg'][1] * 100), 1) if stats['fg'][1] > 0 else 0
                        stats['2pt_pct'] = round((stats['2pt'][0] / stats['2pt'][1] * 100), 1) if stats['2pt'][1] > 0 else 0
                        stats['3pt_pct'] = round((stats['3pt'][0] / stats['3pt'][1] * 100), 1) if stats['3pt'][1] > 0 else 0
                        stats['ft_pct'] = round((stats['ft'][0] / stats['ft'][1] * 100), 1) if stats['ft'][1] > 0 else 0
            
            # Save season file
            season_file = self.seasons_dir / f"{year}.json"
            self.save_json(season_file, season_data)
            print(f"✓ Updated season: {year}")
    
    def process_file(self, html_file, is_playoff=False, force_season=None):
        """Process a single HTML file"""
        print(f"\nProcessing: {html_file}")
        if is_playoff:
            print("📍 Marking as PLAYOFF game")
        if force_season:
            print(f"📅 Forcing season: {force_season}")
        
        try:
            # Parse HTML
            game, date, opponent = self.parse_html(html_file, is_playoff, force_season)
            
            # Save game
            self.save_game(game, date, opponent)
            
            # Save updated players
            self.save_json(self.players_file, self.players)
            print("✓ Updated players registry")
            
            # Update aggregated data
            self.update_records()
            self.update_season_stats()
            
            print(f"\n✓ Successfully processed {html_file}")
            
        except Exception as e:
            print(f"\n✗ Error processing {html_file}: {str(e)}")
            raise

def main():
    import sys
    import argparse
    
    # Set up argument parser
    parser_args = argparse.ArgumentParser(
        description='Parse EasyStats HTML exports and update basketball statistics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse regular season game (default)
  python parse_easystats.py game.html
  
  # Parse playoff game
  python parse_easystats.py game.html --playoff
  
  # Parse game for specific season
  python parse_easystats.py game.html --season 2024
  
  # Parse playoff game for 2024 season
  python parse_easystats.py game.html --playoff --season 2024
        """
    )
    
    parser_args.add_argument('html_file', help='EasyStats HTML export file')
    parser_args.add_argument('--playoff', action='store_true', 
                           help='Mark this game as a playoff game')
    parser_args.add_argument('--season', type=str, default=None,
                           help='Specify season year (default: auto-detect from game date)')
    
    args = parser_args.parse_args()
    
    if not os.path.exists(args.html_file):
        print(f"Error: File not found: {args.html_file}")
        sys.exit(1)
    
    parser = EasyStatsParser()
    parser.process_file(args.html_file, is_playoff=args.playoff, force_season=args.season)
    
    print("\n" + "="*50)
    print("All data updated successfully!")
    print("="*50)

if __name__ == '__main__':
    main()