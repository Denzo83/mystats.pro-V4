#!/usr/bin/env python3
"""
EasyStats HTML to JSON Parser - Pretty Good Basketball
Completely standalone parser for Pretty Good team
"""

import json
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path

# ============================================
# TEAM CONFIGURATION - PRETTY GOOD
# ============================================
TEAM_NAME = 'Pretty Good'
TEAM_SLUG = 'pretty-good'
TEAM_VARIANTS = ['pretty good', 'pretty-good', 'prettygood']
DATA_DIR = 'data/pretty-good'
# ============================================

class EasyStatsParser:
    def __init__(self):
        self.base_dir = Path(DATA_DIR)
        self.games_dir = self.base_dir / 'games'
        self.seasons_dir = self.base_dir / 'seasons'
        self.players_file = self.base_dir / 'players.json'
        self.records_file = self.base_dir / 'records.json'
        self.games_index_file = self.base_dir / 'games_index.json'
        self.seasons_meta_file = self.base_dir / 'seasons_meta.json'
        
        # Create directories
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.games_dir.mkdir(exist_ok=True)
        self.seasons_dir.mkdir(exist_ok=True)
        
        # Load existing data
        self.players = self._load_json(self.players_file, {})
        self.records = self._load_json(self.records_file, {'regular': {}, 'playoff': {}, 'all': {}})
        self.games_index = self._load_json(self.games_index_file, {})
        self.seasons_meta = self._load_json(self.seasons_meta_file, {})
    
    def _load_json(self, filepath, default):
        if filepath.exists():
            with open(filepath, 'r') as f:
                return json.load(f)
        return default
    
    def _save_json(self, filepath, data):
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def parse_date(self, date_str):
        try:
            dt = datetime.strptime(date_str.strip(), '%d %b %Y')
            return dt.strftime('%Y-%m-%d')
        except:
            return datetime.now().strftime('%Y-%m-%d')
    
    def parse_title(self, title):
        title = re.sub(r'-box-scores.*$', '', title)
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
        match = re.match(r'#(\d+)\s+(.+)', name_str.strip())
        if match:
            return match.group(1), match.group(2)
        return None, name_str.strip()
    
    def get_player_id(self, name):
        return name.replace('.', '').strip().lower().replace(' ', '-')
    
    def merge_player_data(self, number, name):
        player_id = self.get_player_id(name)
        
        if number in self.players:
            existing = self.players[number]
            if len(name) > len(existing.get('name', '')):
                existing['name'] = name
                existing['display_name'] = name
                existing['id'] = player_id
        else:
            self.players[number] = {
                'id': player_id,
                'display_name': name,
                'name': name,
                'number': number,
                'position': '',
                'teams': [TEAM_NAME],
                'images': {
                    'portrait': f'Assets/players/{player_id}.png'
                }
            }
    
    def calculate_derived_stats(self, stats):
        derived = {}
        fg = stats.get('fg', [0, 0])
        three_pt = stats.get('3pt', [0, 0])
        ft = stats.get('ft', [0, 0])
        
        if fg and three_pt:
            derived['2pt'] = [fg[0] - three_pt[0], fg[1] - three_pt[1]]
            derived['2pt_pct'] = round((derived['2pt'][0] / derived['2pt'][1] * 100), 1) if derived['2pt'][1] > 0 else 0.0
        
        derived['fg_pct'] = round((fg[0] / fg[1] * 100), 1) if fg and fg[1] > 0 else 0.0
        derived['3pt_pct'] = round((three_pt[0] / three_pt[1] * 100), 1) if three_pt and three_pt[1] > 0 else 0.0
        derived['ft_pct'] = round((ft[0] / ft[1] * 100), 1) if ft and ft[1] > 0 else 0.0
        
        oreb = stats.get('oreb', 0) or 0
        dreb = stats.get('dreb', 0) or 0
        derived['reb'] = oreb + dreb
        
        return derived
    
    def is_our_team(self, team_name):
        return any(variant in team_name.lower() for variant in TEAM_VARIANTS)
    
    def parse_html(self, html_file, is_playoff=False, force_season=None, opp_score=None):
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        title = soup.find('title')
        if not title:
            raise ValueError("No title found in HTML")
        
        game_info = self.parse_title(title.text)
        if not game_info:
            raise ValueError(f"Could not parse title: {title.text}")
        
        date_elem = soup.find('span', class_='detail')
        date = self.parse_date(date_elem.text) if date_elem else datetime.now().strftime('%Y-%m-%d')
        
        season_key = date[:4]
        
        if force_season:
            force_season = force_season.strip()
            season_match = re.match(r'(\d{4})\s*(.+)?', force_season)
            if season_match:
                season_key = season_match.group(1)
                season_suffix = season_match.group(2)
                if season_suffix:
                    season_display = f"{season_key} {season_suffix.strip().title()}"
                else:
                    season_display = f"{season_key} Season"
            else:
                season_display = force_season.title()
            
            self.seasons_meta[season_key] = {
                'key': season_key,
                'display_name': season_display
            }
            self._save_json(self.seasons_meta_file, self.seasons_meta)
        
        away_is_us = self.is_our_team(game_info['away_team'])
        home_is_us = self.is_our_team(game_info['home_team'])

        if away_is_us:
            is_home = False
            opponent = game_info['home_team']
        elif home_is_us:
            is_home = True
            opponent = game_info['away_team']
        else:
            print(f"⚠️  Warning: Neither team matches '{TEAM_NAME}'. Assuming away team is us.")
            is_home = False
            opponent = game_info['home_team']
        
        our_score = game_info['home_score'] if is_home else game_info['away_score']
        their_score = game_info['away_score'] if is_home else game_info['home_score']
        
        if opp_score is not None:
            their_score = opp_score
        
        stats_table = soup.find('table', id='stats')
        if not stats_table:
            raise ValueError("No stats table found")
        
        rows = stats_table.find_all('tr')[1:]
        
        player_stats = {}
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 2:
                continue
            
            player_name = cols[0].text.strip()
            number, name = self.extract_player_number(player_name)
            
            if not number:
                continue
            
            self.merge_player_data(number, name)
            
            if all(col.text.strip() == '-' for col in cols[1:]):
                continue
            
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
            
            derived = self.calculate_derived_stats(stats)
            stats.update(derived)
            
            player_stats[number] = stats
        
        game = {
            'date': date,
            'season': season_key,
            'opponent': opponent,
            'homeAway': 'home' if is_home else 'away',
            'score': {'us': our_score, 'them': their_score},
            'result': 'W' if our_score > their_score else 'L',
            'isPlayoff': is_playoff,
            'stats': player_stats
        }
        
        return game, date, opponent, season_key
    
    def save_game(self, game, date, opponent, season_key):
        opponent_slug = re.sub(r'[^a-z0-9]+', '-', opponent.lower()).strip('-')
        filename = f"{date}-{opponent_slug}.json"
        filepath = self.games_dir / filename
        
        self._save_json(filepath, game)
        print(f"✓ Saved game: {filepath}")
        
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
        self._save_json(self.games_index_file, self.games_index)
        
        return filepath
    
    def update_records(self):
        print(f"\nUpdating {TEAM_NAME} records...")
        
        stat_names = ['pts', 'reb', 'asst', 'stl', 'blk', 'to', 'fg', '3pt', 'ft', 'oreb', 'dreb', 'foul']
        
        for category in ['regular', 'playoff', 'all']:
            self.records[category] = {}
            for stat in stat_names:
                self.records[category][f'most_{stat}'] = {
                    'player': None, 'player_number': None, 'value': 0, 'date': None, 'opponent': None
                }
        
        for game_file in self.games_dir.glob('*.json'):
            game = self._load_json(game_file, {})
            game_type = 'playoff' if game.get('isPlayoff') else 'regular'
            game_date = game.get('date', '')
            
            for player_num, stats in game.get('stats', {}).items():
                player_name = self.players.get(player_num, {}).get('name', f"#{player_num}")
                
                for stat in stat_names:
                    value = stats.get(stat)
                    if isinstance(value, list):
                        value = value[0]
                    if value is None or value == 0:
                        continue
                    
                    record_key = f'most_{stat}'
                    
                    if value > self.records[game_type][record_key]['value']:
                        self.records[game_type][record_key] = {
                            'player': player_name, 'player_number': player_num,
                            'value': value, 'date': game_date, 'opponent': game['opponent']
                        }
                    
                    if value > self.records['all'][record_key]['value']:
                        self.records['all'][record_key] = {
                            'player': player_name, 'player_number': player_num,
                            'value': value, 'date': game_date, 'opponent': game['opponent']
                        }
        
        self._save_json(self.records_file, self.records)
        print(f"✓ Records updated")
    
    def update_season_stats(self):
        print(f"\nUpdating {TEAM_NAME} season statistics...")
        
        seasons = {}
        
        for game_file in self.games_dir.glob('*.json'):
            game = self._load_json(game_file, {})
            season_key = game.get('season', game['date'][:4])
            game_type = 'playoff' if game.get('isPlayoff') else 'regular'
            
            if season_key not in seasons:
                seasons[season_key] = {'regular': {}, 'playoff': {}, 'all': {}}
            
            for player_num, stats in game.get('stats', {}).items():
                for category in ['regular', 'playoff', 'all']:
                    if player_num not in seasons[season_key][category]:
                        seasons[season_key][category][player_num] = {
                            'gp': 0, 'pts': 0, 'reb': 0, 'asst': 0, 'stl': 0, 'blk': 0, 'to': 0, 'foul': 0,
                            'fg': [0, 0], '2pt': [0, 0], '3pt': [0, 0], 'ft': [0, 0], 'oreb': 0, 'dreb': 0
                        }
                
                for category in [game_type, 'all']:
                    ps = seasons[season_key][category][player_num]
                    ps['gp'] += 1
                    
                    for stat in ['pts', 'reb', 'asst', 'stl', 'blk', 'to', 'foul', 'oreb', 'dreb']:
                        if stats.get(stat):
                            ps[stat] += stats[stat]
                    
                    for stat in ['fg', '2pt', '3pt', 'ft']:
                        if stats.get(stat) and isinstance(stats[stat], list):
                            ps[stat][0] += stats[stat][0]
                            ps[stat][1] += stats[stat][1]
        
        for season_key, season_data in seasons.items():
            for category in ['regular', 'playoff', 'all']:
                for player_num, stats in season_data[category].items():
                    gp = stats['gp']
                    if gp > 0:
                        stats['ppg'] = round(stats['pts'] / gp, 1)
                        stats['rpg'] = round(stats['reb'] / gp, 1)
                        stats['apg'] = round(stats['asst'] / gp, 1)
                        stats['spg'] = round(stats['stl'] / gp, 1)
                        stats['bpg'] = round(stats['blk'] / gp, 1)
                        stats['tpg'] = round(stats['to'] / gp, 1)
                        stats['fpg'] = round(stats['foul'] / gp, 1)
                        stats['orebpg'] = round(stats['oreb'] / gp, 1)
                        stats['drebpg'] = round(stats['dreb'] / gp, 1)
                        
                        stats['fga_pg'] = round(stats['fg'][1] / gp, 1)
                        stats['3pa_pg'] = round(stats['3pt'][1] / gp, 1)
                        stats['fta_pg'] = round(stats['ft'][1] / gp, 1)
                        stats['2pa_pg'] = round(stats['2pt'][1] / gp, 1)
                        stats['fgm_pg'] = round(stats['fg'][0] / gp, 1)
                        stats['3pm_pg'] = round(stats['3pt'][0] / gp, 1)
                        stats['ftm_pg'] = round(stats['ft'][0] / gp, 1)
                        stats['2pm_pg'] = round(stats['2pt'][0] / gp, 1)
                        
                        stats['fg_pct'] = round((stats['fg'][0] / stats['fg'][1] * 100), 1) if stats['fg'][1] > 0 else 0.0
                        stats['2pt_pct'] = round((stats['2pt'][0] / stats['2pt'][1] * 100), 1) if stats['2pt'][1] > 0 else 0.0
                        stats['3pt_pct'] = round((stats['3pt'][0] / stats['3pt'][1] * 100), 1) if stats['3pt'][1] > 0 else 0.0
                        stats['ft_pct'] = round((stats['ft'][0] / stats['ft'][1] * 100), 1) if stats['ft'][1] > 0 else 0.0
            
            self._save_json(self.seasons_dir / f"{season_key}.json", season_data)
            print(f"✓ Updated season: {season_key}")
    
    def process_file(self, html_file, is_playoff=False, force_season=None, opp_score=None):
        print(f"\n{'='*50}")
        print(f"Processing for: {TEAM_NAME}")
        print(f"{'='*50}")
        print(f"File: {html_file}")
        if is_playoff:
            print("📍 PLAYOFF game")
        if force_season:
            print(f"📅 Season: {force_season}")
        if opp_score is not None:
            print(f"🏀 Opponent score: {opp_score}")
        
        game, date, opponent, season_key = self.parse_html(html_file, is_playoff, force_season, opp_score)
        self.save_game(game, date, opponent, season_key)
        self._save_json(self.players_file, self.players)
        print("✓ Updated players")
        self.update_records()
        self.update_season_stats()
        print(f"\n✓ Done!")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description=f'Parse EasyStats HTML for {TEAM_NAME}')
    parser.add_argument('html_file', help='EasyStats HTML export file')
    parser.add_argument('--playoff', action='store_true', help='Mark as playoff game')
    parser.add_argument('--season', type=str, default=None, help='Season (e.g., "2025 Spring")')
    parser.add_argument('--opp-score', type=int, default=None, help='Override opponent score')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.html_file):
        print(f"Error: File not found: {args.html_file}")
        return 1
    
    EasyStatsParser().process_file(args.html_file, args.playoff, args.season, args.opp_score)
    return 0


if __name__ == '__main__':
    exit(main())
