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
        self.seasons_meta_file = self.base_dir / 'seasons_meta.json'
        
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
        self.seasons_meta = self.load_json(self.seasons_meta_file, {})
    
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
    
    def parse_html(self, html_file, is_playoff=False, force_season=None, opp_score=None):
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
        
        # Extract just the year from the date for the season key
        # The season name is stored separately in seasons_meta
        season_key = date[:4]  # Always use YYYY format for keys
        season_display = season_key  # Default display name
        
        # If a season name is specified, save it to meta
        if force_season:
            # Clean up the season name - extract just the display name
            # e.g., "2025 spring" or "2025spring" -> display as "2025 Spring"
            force_season = force_season.strip()
            
            # If the season contains a year and name like "2025 spring", parse them
            season_match = re.match(r'(\d{4})\s*(.+)?', force_season)
            if season_match:
                season_key = season_match.group(1)  # Use just the year as the key
                season_suffix = season_match.group(2)
                if season_suffix:
                    # Capitalize the season suffix (e.g., "spring" -> "Spring")
                    season_display = f"{season_key} {season_suffix.strip().title()}"
                else:
                    season_display = season_key
            else:
                # If no year in the string, use current year
                season_display = force_season.title()
            
            # Store the season display name in meta
            self.seasons_meta[season_key] = {
                'key': season_key,
                'display_name': season_display
            }
            self.save_json(self.seasons_meta_file, self.seasons_meta)
        
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
        
        # Override opponent score if provided via command line
        if opp_score is not None:
            their_score = opp_score
        
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
            'season': season_key,
            'opponent': opponent,
            'homeAway': 'home' if is_home else 'away',
            'score': {
                'us': our_score,
                'them': their_score
            },
            'result': 'W' if our_score > their_score else 'L',
            'isPlayoff': is_playoff,
            'stats': player_stats
        }
        
        return game, date, opponent, season_key
    
    def save_game(self, game, date, opponent, season_key):
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
            'season': season_key,
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
        stat_names = ['pts', 'reb', 'asst', 'stl', 'blk', 'to', 'fg', '3pt', 'ft', 'oreb', 'dreb', 'foul']
        
        for category in record_categories:
            self.records[category] = {}
            for stat in stat_names:
                self.records[category][f'most_{stat}'] = {
                    'player': None,
                    'player_number': None,
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
                            'player_number': player_num,
                            'value': value,
                            'date': game['date'],
                            'opponent': game['opponent']
                        }
                    
                    # Update all-time record
                    if value > self.records['all'][record_key]['value']:
                        self.records['all'][record_key] = {
                            'player': player_name,
                            'player_number': player_num,
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
            # Use the season key from game, falling back to year from date
            season_key = game.get('season', game['date'][:4])
            game_type = 'playoff' if game.get('isPlayoff') else 'regular'
            
            if season_key not in seasons:
                seasons[season_key] = {
                    'regular': {},
                    'playoff': {},
                    'all': {}
                }
            
            # Aggregate stats for each player
            for player_num, stats in game.get('stats', {}).items():
                # Initialize player if not exists
                for category in ['regular', 'playoff', 'all']:
                    if player_num not in seasons[season_key][category]:
                        seasons[season_key][category][player_num] = {
                            'gp': 0,  # games played
                            'pts': 0, 'reb': 0, 'asst': 0, 'stl': 0, 'blk': 0, 'to': 0, 'foul': 0,
                            'fg': [0, 0], '2pt': [0, 0], '3pt': [0, 0], 'ft': [0, 0],
                            'oreb': 0, 'dreb': 0
                        }
                
                # Add to appropriate category
                for category in [game_type, 'all']:
                    player_season = seasons[season_key][category][player_num]
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
        for season_key, season_data in seasons.items():
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
                        stats['orebpg'] = round(stats['oreb'] / gp, 1)
                        stats['drebpg'] = round(stats['dreb'] / gp, 1)
                        
                        # Calculate per game attempts
                        stats['fga_pg'] = round(stats['fg'][1] / gp, 1) if stats['fg'][1] > 0 else 0
                        stats['3pa_pg'] = round(stats['3pt'][1] / gp, 1) if stats['3pt'][1] > 0 else 0
                        stats['fta_pg'] = round(stats['ft'][1] / gp, 1) if stats['ft'][1] > 0 else 0
                        stats['2pa_pg'] = round(stats['2pt'][1] / gp, 1) if stats['2pt'][1] > 0 else 0
                        
                        # Calculate per game makes
                        stats['fgm_pg'] = round(stats['fg'][0] / gp, 1) if stats['fg'][0] > 0 else 0
                        stats['3pm_pg'] = round(stats['3pt'][0] / gp, 1) if stats['3pt'][0] > 0 else 0
                        stats['ftm_pg'] = round(stats['ft'][0] / gp, 1) if stats['ft'][0] > 0 else 0
                        stats['2pm_pg'] = round(stats['2pt'][0] / gp, 1) if stats['2pt'][0] > 0 else 0
                        
                        # Calculate percentages
                        stats['fg_pct'] = round((stats['fg'][0] / stats['fg'][1] * 100), 1) if stats['fg'][1] > 0 else 0
                        stats['2pt_pct'] = round((stats['2pt'][0] / stats['2pt'][1] * 100), 1) if stats['2pt'][1] > 0 else 0
                        stats['3pt_pct'] = round((stats['3pt'][0] / stats['3pt'][1] * 100), 1) if stats['3pt'][1] > 0 else 0
                        stats['ft_pct'] = round((stats['ft'][0] / stats['ft'][1] * 100), 1) if stats['ft'][1] > 0 else 0
            
            # Save season file
            season_file = self.seasons_dir / f"{season_key}.json"
            self.save_json(season_file, season_data)
            print(f"✓ Updated season: {season_key}")
    
    def process_file(self, html_file, is_playoff=False, force_season=None, opp_score=None):
        """Process a single HTML file"""
        print(f"\nProcessing: {html_file}")
        if is_playoff:
            print("📍 Marking as PLAYOFF game")
        if force_season:
            print(f"📅 Season: {force_season}")
        if opp_score is not None:
            print(f"🏀 Opponent score override: {opp_score}")
        
        try:
            # Parse HTML
            game, date, opponent, season_key = self.parse_html(html_file, is_playoff, force_season, opp_score)
            
            # Save game
            self.save_game(game, date, opponent, season_key)
            
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
  python easystats-parse.py game.html
  
  # Parse playoff game
  python easystats-parse.py game.html --playoff
  
  # Parse game for specific season
  python easystats-parse.py game.html --season "2025 Spring"
  
  # Parse playoff game for 2024 season with opponent score
  python easystats-parse.py game.html --playoff --season 2024 --opp-score 45
  
  # Parse game with opponent score (when not tracked in HTML)
  python easystats-parse.py game.html --opp-score 30
        """
    )
    
    parser_args.add_argument('html_file', help='EasyStats HTML export file')
    parser_args.add_argument('--playoff', action='store_true', 
                           help='Mark this game as a playoff game')
    parser_args.add_argument('--season', type=str, default=None,
                           help='Specify season (e.g., "2025 Spring", "2024 Fall")')
    parser_args.add_argument('--opp-score', type=int, default=None,
                           help='Override opponent score (when not tracked in HTML)')
    
    args = parser_args.parse_args()
    
    if not os.path.exists(args.html_file):
        print(f"Error: File not found: {args.html_file}")
        sys.exit(1)
    
    parser = EasyStatsParser()
    parser.process_file(args.html_file, is_playoff=args.playoff, force_season=args.season, opp_score=args.opp_score)
    
    print("\n" + "="*50)
    print("All data updated successfully!")
    print("="*50)

if __name__ == '__main__':
    main()
