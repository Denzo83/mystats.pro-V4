# Pretty Good Basketball Stats - Setup Guide

## 🎉 NEW FEATURES

### Individual Player Pages
- Click any player from the roster to see their full profile
- View career highs for all stat categories
- See season splits (Regular vs Playoffs)
- Complete game log with all stats
- Click games in player profile to see full box score

### Box Score Pages
- Click any game to see detailed box scores
- Full stats table with all categories
- Click player names in box score to go to their profile
- Easy navigation back to previous pages

### Enhanced Records Page
- **Top 3 records** for each stat category (was only #1)
- Medal icons (🥇🥈🥉) for top 3
- Click any record to view that game's box score
- Records update automatically after each game

## 📁 Project Structure

```
basketball-stats/
├── data/
│   ├── games/           # Individual game JSON files
│   ├── seasons/         # Season aggregate stats
│   ├── players.json     # Player registry
│   ├── records.json     # Team records
│   └── games_index.json # Index of all games (auto-generated)
├── parse_easystats.py   # Parser script
├── index.html           # Your website (React app)
└── easystats_exports/   # Put your HTML exports here
```

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Install Python dependencies
pip install beautifulsoup4
```

### Step 2: Set Up Directory Structure

```bash
mkdir basketball-stats
cd basketball-stats
mkdir data data/games data/seasons easystats_exports
```

### Step 3: Add the Parser Script

Save the `parse_easystats.py` script to your `basketball-stats` folder.

### Step 4: Process Your First Game

```bash
# Copy your EasyStats HTML export to the folder
cp "Macho men vs Pretty good box-scores-16 Dec 2025.html" easystats_exports/

# (Optional) Import existing player data first
python import_players.py old_players.json

# Run the parser
python parse_easystats.py "easystats_exports/Macho men vs Pretty good box-scores-16 Dec 2025.html"
```

### Step 5: Deploy Website to GitHub Pages

1. **Create a new GitHub repository** called `basketball-stats`

2. **Initialize git in your folder:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/basketball-stats.git
   git push -u origin main
   ```

3. **Enable GitHub Pages:**
   - Go to your repo → Settings → Pages
   - Source: Deploy from branch
   - Branch: `main` / `root`
   - Save

4. **Your site will be live at:**
   `https://YOUR_USERNAME.github.io/basketball-stats/`

## 📊 Using the Parser

### Initial Setup (If You Have Existing Data)

```bash
# 1. Import your old player data (positions, photos, etc.)
python import_players.py old_players.json

# 2. This preserves:
#    - Player photos/images
#    - Positions (G, F, C, etc.)
#    - Display names
#    - Team affiliations
```

### After Each Game

```bash
# 1. Export game from EasyStats app (as HTML)
# 2. Save to easystats_exports folder
# 3. Run parser
python parse_easystats.py "easystats_exports/GAME_FILE.html"

# 4. Commit and push to GitHub
git add .
git commit -m "Added game vs Opponent on DATE"
git push
```

### Marking Playoff Games

Edit the game JSON file and change `"isPlayoff": false` to `"isPlayoff": true`:

```bash
# Edit the game file
nano data/games/2025-12-16-opponent.json

# Change the line:
"isPlayoff": true

# Commit changes
git add .
git commit -m "Marked game as playoff"
git push
```

Then re-run the parser to update aggregates:
```bash
python parse_easystats.py "easystats_exports/GAME_FILE.html"
```

## 🖼️ Adding Player Photos

### Method 1: Using Existing Player Data (Recommended)

If you have an old players JSON file with photo paths:

1. Save your old players JSON as `old_players.json`

2. Run the import script:
   ```bash
   python import_players.py old_players.json
   ```

3. This will:
   - Merge positions and photo paths
   - Preserve existing stats
   - Combine team lists
   - Update display names

### Method 2: Manual Setup

1. Create folder structure:
   ```bash
   mkdir -p assets/players
   ```

2. Add photos with naming convention:
   - `assets/players/kyle-denzin.png` (player ID format)
   - Or manually edit `players.json` to update paths

3. Player JSON structure:
   ```json
   {
     "37": {
       "id": "kyle-denzin",
       "display_name": "Kyle Denzin",
       "name": "Kyle Denzin",
       "number": "37",
       "position": "G/F",
       "teams": ["Pretty good", "Chuckers chuckers"],
       "images": {
         "portrait": "assets/players/kyle-denzin.png"
       }
     }
   }
   ```

4. The website will automatically:
   - Try to load the image
   - Fall back to jersey number if image fails
   - Work with or without photos

### Photo Requirements

- **Format**: PNG, JPG, or WEBP
- **Size**: 400x400px recommended (will be displayed as circular)
- **Naming**: Use player ID (lowercase, hyphens) like `kyle-denzin.png`
- Photos are optional - site works great without them!

## 🎨 Customizing Colors

The site uses Tailwind's blue color scheme by default. To customize:

**Change primary color:**
- Replace `blue-600`, `blue-500`, `blue-400` with your color
- Options: `indigo`, `purple`, `pink`, `red`, `orange`, `yellow`, `green`, `teal`, `cyan`

**Royal Blue specifically:**
- Use `blue-700` for darker royal blue
- Use `blue-600` for medium royal blue
- Use `blue-400` for lighter blue accents

## 📱 Mobile Optimization Features

The site includes:
- ✅ Responsive design (mobile-first)
- ✅ Touch-friendly buttons (48px minimum)
- ✅ Sticky headers that stay visible while scrolling
- ✅ Dark mode toggle
- ✅ Swipeable tabs
- ✅ Collapsible player details
- ✅ Optimized for 320px+ screens

## 📈 Data Files Explained

### `players.json`
```json
{
  "1": {
    "name": "R. Ogle",
    "number": "1",
    "teams": ["Pretty good", "Chuckers chuckers"]
  }
}
```

### `games/2025-12-16-opponent.json`
```json
{
  "date": "2025-12-16",
  "opponent": "Opponent Name",
  "homeAway": "home",
  "score": { "us": 75, "them": 68 },
  "result": "W",
  "isPlayoff": false,
  "stats": {
    "1": {
      "fg": [8, 15],
      "3pt": [2, 6],
      "ft": [3, 4],
      "pts": 21,
      "reb": 8,
      "asst": 5,
      // ... all other stats
    }
  }
}
```

### `seasons/2025.json`
```json
{
  "regular": {
    "1": {
      "gp": 10,
      "pts": 180,
      "ppg": 18.0,
      "fg": [70, 150],
      "fg_pct": 46.7,
      // ... all aggregated stats
    }
  },
  "playoff": { /* same structure */ },
  "all": { /* combined */ }
}
```

### `records.json`
```json
{
  "regular": {
    "most_pts": {
      "player": "R. Ogle",
      "value": 35,
      "date": "2025-12-16",
      "opponent": "Team X"
    }
  }
}
```

## 🔧 Troubleshooting

**Parser errors:**
- Make sure the HTML file is from EasyStats
- Check that player names use `#NUMBER Name` format
- Verify the title format: "Team1 Score at Team2 Score"

**Wrong Jersey Numbers:**
If EasyStats exports show different numbers than players actually wear:

1. Create `mapping.json`:
   ```json
   {
     "1": "14",
     "11": "24"
   }
   ```

2. Run the fix script:
   ```bash
   python fix_player_numbers.py mapping.json
   ```

3. Re-run parser to regenerate stats

**Website not updating:**
- GitHub Pages can take 5-10 minutes to update
- Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- Check browser console for errors

**Photos not showing:**
- Check file paths match exactly
- Verify images are in `assets/players/` folder
- Make sure filenames use player ID format (lowercase-with-hyphens)
- Images should be in your GitHub repo

**Stats not calculating:**
- Make sure you run the parser after adding/editing games
- The parser updates all aggregates automatically

## 📞 Support

For issues with:
- **EasyStats app:** Contact EasyStats support
- **Parser script:** Check the error message, ensure HTML format matches
- **Website display:** Check browser console (F12)

## 🎯 Future Enhancements

Consider adding:
- Shot charts (if you track shot locations)
- Head-to-head player comparisons
- Game-by-game player progression charts
- Export stats to CSV
- Search functionality
- Advanced stats (PER, TS%, etc.)
- Player photo uploads
- Season-by-season comparison
- Team vs team comparison for games against same opponent

## 🆕 Navigation Features

### Player Pages
- Click any player card in the roster
- View full career stats, highs, and game log
- Click games in their log to see box score
- Navigate back with the back button

### Box Score Pages  
- Click any game from the games tab
- Click player names to go to their profile
- Full stats table with all shooting stats
- Shows game result, date, and score

### Records Page
- Now shows **Top 3** for each category
- Click any record to view that game
- Medal indicators for 1st, 2nd, 3rd place

## 📝 Notes

- The parser automatically detects which team is "Pretty good" vs opponent
- Players who appear in multiple teams (like Chuckers chuckers) are tracked separately
- DNPs (Did Not Play) are automatically filtered out
- All percentages are calculated automatically
- Games Played (GP) is tracked for accurate averages

---

**Made with ❤️ for Pretty Good Basketball Team**
