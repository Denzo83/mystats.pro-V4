# Basketball Stats - Multi-Team Setup

## Teams

| Team | HTML File | Parser | Data Folder |
|------|-----------|--------|-------------|
| Pretty Good | `pretty-good.html` | `prettygoodparser.py` | `data/pretty-good/` |
| Chuckers Chuckers | `chuckers-chuckers.html` | `chuckersparser.py` | `data/chuckers-chuckers/` |
| Just Jokic-ing | `just-jokic-ing.html` | `justjokicingparser.py` | `data/test teams/just-jokic-ing/` |
| Board Man Gets Paid | `board-man-gets-paid.html` | `boardmangetspaidparser.py` | `data/test teams/board-man-gets-paid/` |

## Folder Structure

```
├── index.html                      # Landing page - team selection
├── pretty-good.html                # Pretty Good stats viewer
├── chuckers-chuckers.html          # Chuckers Chuckers stats viewer
├── just-jokic-ing.html             # Just Jokic-ing stats viewer
├── board-man-gets-paid.html        # Board Man Gets Paid stats viewer
│
├── Assets/
│   ├── teams/
│   │   ├── pretty-good-logo.png
│   │   ├── chuckers-chuckers-logo.png
│   │   ├── just-jokic-ing-logo.png
│   │   └── board-man-gets-paid-logo.png
│   └── players/
│       └── player-name.png
│
└── data/
    ├── pretty-good/                # Pretty Good team data
    │   ├── players.json
    │   ├── seasons_meta.json
    │   ├── records.json
    │   ├── games_index.json
    │   ├── seasons/
    │   │   └── 2025.json
    │   └── games/
    │       └── 2025-12-16-opponent.json
    │
    ├── chuckers-chuckers/          # Chuckers Chuckers team data
    │   └── (same structure)
    │
    └── test teams/                 # Test teams folder
        ├── just-jokic-ing/         # Just Jokic-ing team data
        │   └── (same structure)
        │
        └── board-man-gets-paid/    # Board Man Gets Paid team data
            └── (same structure)
```

## Parser Usage

### Pretty Good
```bash
python prettygoodparser.py game.html --season "2025 Spring"
python prettygoodparser.py game.html --season "2025 Spring" --playoff
python prettygoodparser.py game.html --season "2025 Spring" --opp-score 30
```

### Chuckers Chuckers
```bash
python chuckersparser.py game.html --season "2025 Spring"
```

### Just Jokic-ing
```bash
python justjokicingparser.py game.html --season "2025 Spring"
```

### Board Man Gets Paid
```bash
python boardmangetspaidparser.py game.html --season "2025 Spring"
```

## Adding a New Team

1. Copy any parser file (e.g., `prettygoodparser.py`) to `newteamparser.py`
2. Edit the team configuration at the top:
   ```python
   TEAM_NAME = 'New Team Name'
   TEAM_SLUG = 'new-team-name'
   TEAM_VARIANTS = ['new team name', 'new-team-name', 'newteamname']
   DATA_DIR = 'data/new-team-name'
   ```
3. Copy any team HTML file to `new-team-name.html`
4. Add the team to `TEAM_CONFIG` in the HTML file
5. Add a card for the new team in `index.html`

## Notes

- Each team has completely separate data - no stats carryover between teams
- Each team has its own `players.json` - same player on multiple teams exists in each file
- Team logos go in `Assets/teams/[team-slug]-logo.png`
- Player images go in `Assets/players/[player-id].png`
- The "test teams" folder name has a space - parsers handle this automatically
