# Pretty Good Basketball Stats - Quick Start 🏀

## 📦 Complete Package

You now have a **professional basketball statistics website** with:

✅ **Player Pages** - Individual profiles with career stats, highs, and game logs
✅ **Box Scores** - Detailed game statistics for every match
✅ **Leaderboards** - Sort by any stat category (PPG, RPG, APG, etc.)
✅ **Top 3 Records** - Best performances in each category
✅ **Mobile Optimized** - Perfect for viewing on phones
✅ **Dark Mode** - Easy on the eyes
✅ **Auto Stats** - All calculations handled automatically
✅ **Photo Support** - Player portraits with fallback to jersey numbers

## 🚀 5-Minute Setup

### 1. Install Python Dependency
```bash
pip install beautifulsoup4
```

### 2. Create Project Structure
```bash
mkdir basketball-stats
cd basketball-stats
mkdir -p data/games data/seasons assets/players
```

### 3. Add Your Files
- Copy `parse_easystats.py` to the folder
- Copy `import_players.py` to the folder (optional)
- Copy `fix_player_numbers.py` to the folder (if needed)
- Save the React website as `index.html`

### 4. Import Existing Player Data (Optional)
If you have photos/positions from an old project:
```bash
python import_players.py old_players.json
```

### 5. Process Your First Game
```bash
python parse_easystats.py "your-game-file.html"
```

### 6. Deploy to GitHub Pages
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/basketball-stats.git
git push -u origin main
```

Enable GitHub Pages in repo Settings → Pages → Deploy from `main` branch.

**Your site will be live at:** `https://YOUR_USERNAME.github.io/basketball-stats/`

## 📱 What You Get

### Main Features

**🏆 Leaderboards**
- Sort by 8 stat categories
- Filter by Regular/Playoff/All
- Expandable player cards with detailed stats
- Shows games played and team affiliations

**🥇 Records Page**
- Top 3 for each stat category
- Medal indicators (🥇🥈🥉)
- Click any record to view the game
- Updates automatically

**👥 Player Profiles**
- Career averages (PPG, RPG, APG, FG%, 3P%, GP)
- Career highs for all stats
- Regular season vs Playoff splits
- Complete game log
- Click games to see box scores

**📊 Box Scores**
- Full game statistics table
- All shooting percentages calculated
- Click player names to see their profile
- Shows game result, date, score

**📅 Games Tab**
- Full season game log
- Filter by Regular/Playoff/All
- Team totals preview
- Click to view box score

### Tracked Stats

**Per Game:**
- Points (PTS)
- Rebounds (REB) - Total, Offensive, Defensive
- Assists (AST)
- Steals (STL)
- Blocks (BLK)
- Turnovers (TO)
- Fouls (F)
- Games Played (GP)

**Shooting:**
- Field Goals (FG, 2PT, 3PT) - Made/Attempted
- Free Throws (FT) - Made/Attempted
- All Percentages (FG%, 2P%, 3P%, FT%)

## 🎨 Customization

### Colors
Edit the React component to change from Royal Blue:
- Replace `blue-600`, `blue-500`, `blue-400`
- Options: `indigo`, `purple`, `pink`, `red`, `orange`, `yellow`, `green`, `teal`, `cyan`

### Player Photos
Place images in `assets/players/` using player ID format:
- `kyle-denzin.png`
- `josh-todd.png`
- Site works with or without photos!

### Team Name
Edit the header in `index.html`:
```javascript
<h1 className="text-2xl font-bold">Your Team Name</h1>
```

## 🔄 Workflow

### After Each Game

1. **Export from EasyStats** (HTML file)
2. **Run Parser:**
   ```bash
   python parse_easystats.py "game-file.html"
   ```
3. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Added game vs Opponent"
   git push
   ```
4. **Wait 5-10 minutes** for GitHub Pages to update

### Mark Playoff Games

Edit the game JSON:
```bash
nano data/games/2025-12-16-opponent.json
```

Change `"isPlayoff": false` to `"isPlayoff": true`

Then re-run parser to update aggregates.

## 🎯 Pro Tips

1. **Import your old data first** before processing new games to preserve photos/positions
2. **Commit after each game** so you can track history
3. **Use the mapping script** if EasyStats numbers don't match real jerseys
4. **Check the website locally** by opening `index.html` before pushing
5. **Add player positions** in `players.json` for better roster display

## 📂 File Structure Explained

```
basketball-stats/
├── data/
│   ├── games/              # Individual game files
│   │   └── 2025-12-16-opponent.json
│   ├── seasons/            # Aggregated season stats
│   │   └── 2025.json
│   ├── players.json        # Player registry
│   ├── records.json        # Team records
│   └── games_index.json    # Game index (auto-generated)
├── assets/
│   └── players/            # Player photos
│       ├── kyle-denzin.png
│       └── josh-todd.png
├── parse_easystats.py      # Main parser
├── import_players.py       # Import old data
├── fix_player_numbers.py   # Fix jersey numbers
└── index.html              # Website
```

## 💡 Common Issues & Solutions

**"No data found"** → Run the parser script first

**Wrong jersey numbers** → Use `fix_player_numbers.py` with mapping file

**Photos not showing** → Check file paths and names match player IDs

**Stats seem wrong** → Re-run parser to recalculate everything

**Website not updating** → Clear browser cache, wait 10 minutes for GitHub Pages

**Player shows twice** → Check for duplicate entries in `players.json`

## 🎓 Advanced Features

### Multi-Team Support
Players can be on multiple teams (e.g., Pretty Good + Chuckers Chuckers). The system tracks this automatically.

### Manual Edits
You can manually edit any JSON file to:
- Update player positions
- Fix incorrect stats
- Change team names
- Add custom fields

After manual edits, re-run the parser to recalculate aggregates.

### Backup Your Data
```bash
# Create backup before major changes
cp -r data data_backup_$(date +%Y%m%d)
```

## 📞 Quick Reference

**Add game:** `python parse_easystats.py "game.html"`

**Import players:** `python import_players.py old_players.json`

**Fix numbers:** `python fix_player_numbers.py mapping.json`

**Deploy:** `git add . && git commit -m "Update" && git push`

---

## 🎉 You're Ready!

Everything is set up and ready to go. Just:
1. Process your games
2. Push to GitHub
3. Share your stats site with the team!

**Your teammates will love being able to check their stats anytime on their phones!** 📱🏀
