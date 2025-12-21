import React, { useState, useMemo, useEffect } from 'react';
import { BarChart3, Trophy, Users, Calendar, Moon, Sun, ChevronDown, ChevronUp, TrendingUp, AlertCircle } from 'lucide-react';

export default function BasketballStatsApp() {
  const [darkMode, setDarkMode] = useState(false);
  const [activeTab, setActiveTab] = useState('leaderboards');
  const [selectedSeason, setSelectedSeason] = useState('2025');
  const [gameType, setGameType] = useState('regular');
  const [statCategory, setStatCategory] = useState('ppg');
  const [expandedPlayer, setExpandedPlayer] = useState(null);
  
  // Navigation state
  const [currentView, setCurrentView] = useState('main'); // 'main', 'player', 'game'
  const [selectedPlayerNumber, setSelectedPlayerNumber] = useState(null);
  const [selectedGameId, setSelectedGameId] = useState(null);
  
  // Data state
  const [players, setPlayers] = useState<Record<string, any>>({});
  const [seasonStats, setSeasonStats] = useState<Record<string, any>>({});
  const [records, setRecords] = useState<Record<string, any>>({});
  const [games, setGames] = useState<any[]>([]);
  const [allGames, setAllGames] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load data on mount
  useEffect(() => {
    loadData(selectedSeason);
  }, [selectedSeason]);

  const loadData = async (season: string) => {
    try {
      setLoading(true);
      setError(null);

      // Helper function to fetch JSON files
      const fetchJSON = async (path: string) => {
        const response = await fetch(path);
        if (!response.ok) throw new Error(`Failed to fetch ${path}`);
        return response.json();
      };

      // Load players
      try {
        const playersData = await fetchJSON('data/players.json');
        setPlayers(playersData);
      } catch (e) {
        console.log('No players.json found, using empty data');
        setPlayers({});
      }

      // Load season stats
      try {
        const seasonData = await fetchJSON(`data/seasons/${season}.json`);
        setSeasonStats(seasonData);
      } catch (e) {
        console.log(`No season data for ${selectedSeason}`);
        setSeasonStats({});
      }

      // Load records
      try {
        const recordsData = await fetchJSON('data/records.json');
        setRecords(recordsData);
      } catch (e) {
        console.log('No records.json found');
        setRecords({});
      }

      // Load all games for the season
      try {
        // Load games index
        const gamesIndex = await fetchJSON('data/games_index.json');
        
        // Load each game file
        const loadedGames: Record<string, any> = {};
        for (const [gameId, gameInfo] of Object.entries(gamesIndex)) {
          // Check if game is from selected season
          if ((gameInfo as any).date && (gameInfo as any).date.startsWith(season)) {
            try {
              const gameData = await fetchJSON(`data/games/${(gameInfo as any).filename}`);
              loadedGames[gameId] = gameData;
            } catch (e) {
              console.log(`Could not load game: ${(gameInfo as any).filename}`);
            }
          }
        }
        
        setAllGames(loadedGames);
        setGames(Object.values(loadedGames));
      } catch (e) {
        console.log('No games data found');
        setGames([]);
        setAllGames({});
      }

      setLoading(false);
    } catch (err) {
      setError('Failed to load data. Make sure your data files are uploaded.');
      setLoading(false);
      console.error('Error loading data:', err);
    }
  };


  const statCategories = [
    { key: 'ppg', label: 'PPG', desc: 'Points Per Game' },
    { key: 'rpg', label: 'RPG', desc: 'Rebounds Per Game' },
    { key: 'apg', label: 'APG', desc: 'Assists Per Game' },
    { key: 'spg', label: 'SPG', desc: 'Steals Per Game' },
    { key: 'bpg', label: 'BPG', desc: 'Blocks Per Game' },
    { key: 'fg_pct', label: 'FG%', desc: 'Field Goal %' },
    { key: '3pt_pct', label: '3P%', desc: 'Three Point %' },
    { key: 'ft_pct', label: 'FT%', desc: 'Free Throw %' }
  ];

  const recordCategories = [
    { key: 'most_pts', label: 'Most Points', icon: '🔥' },
    { key: 'most_reb', label: 'Most Rebounds', icon: '🏀' },
    { key: 'most_asst', label: 'Most Assists', icon: '🎯' },
    { key: 'most_stl', label: 'Most Steals', icon: '👐' },
    { key: 'most_blk', label: 'Most Blocks', icon: '🛡️' },
    { key: 'most_3pt', label: 'Most 3-Pointers Made', icon: '🎯' },
    { key: 'most_fg', label: 'Most Field Goals Made', icon: '⛹️' }
  ];

  // Get top 3 records for a category
  const getTop3Records = (category: string) => {
    const allRecords: { player: any; value: any; date: any; opponent: any; gameId: string; }[] = [];
    
    // Collect all games and extract stats for this category
    Object.entries(allGames).forEach(([gameId, game]) => {
      Object.entries(game.stats || {}).forEach(([playerNum, stats]) => {
        const player = players[playerNum] || { name: `Player #${playerNum}`, number: playerNum };
        let value = (stats as Record<string, any>)[category.replace('most_', '')];
        
        // Handle array values (fg, 3pt, ft)
        if (Array.isArray(value)) {
          value = value[0];
        }
        
        if (value && value > 0) {
          allRecords.push({
            player: player.name,
            value: value,
            date: game.date,
            opponent: game.opponent,
            gameId: gameId
          });
        }
      });
    });
    
    // Sort by value and return top 3
    return allRecords
      .sort((a, b) => b.value - a.value)
      .slice(0, 3);
  };

  // Sort players by selected stat
  const sortedPlayers = useMemo(() => {
    if (!seasonStats[gameType]) return [];

    return Object.entries(seasonStats[gameType])
      .map(([num, stats]) => ({
        ...(players[num] || { name: `Player #${num}`, number: num }),
        ...(stats as Record<string, any>),
        number: num
      }))
      .filter(p => p.gp > 0)
      .sort((a, b) => (b[statCategory] || 0) - (a[statCategory] || 0));
  }, [seasonStats, gameType, statCategory, players]);

  const bgClass = darkMode ? 'bg-gray-900' : 'bg-gray-50';
  const cardClass = darkMode ? 'bg-gray-800 text-white' : 'bg-white text-gray-900';
  const textClass = darkMode ? 'text-gray-300' : 'text-gray-600';
  const borderClass = darkMode ? 'border-gray-700' : 'border-gray-200';
  const accentClass = 'bg-gradient-to-r from-blue-600 to-blue-400';

  // Calculate player career highs
  const getPlayerCareerHighs = (playerNum: string | number) => {
    const highs: Record<string, { value: number; game: { date: string; opponent: string; score: { us: number; them: number } } | null }> = {
      pts: { value: 0, game: null },
      reb: { value: 0, game: null },
      asst: { value: 0, game: null },
      stl: { value: 0, game: null },
      blk: { value: 0, game: null },
      fg: { value: 0, game: null },
      '3pt': { value: 0, game: null }
    };

    Object.entries(allGames).forEach(([gameId, game]) => {
      const stats = game.stats?.[playerNum];
      if (!stats) return;

      Object.keys(highs).forEach(stat => {
        let value = stats[stat];
        if (Array.isArray(value)) value = value[0];
        
        if (value && value > highs[stat].value) {
          highs[stat] = {
            value: value,
            game: {
              date: game.date,
              opponent: game.opponent,
              score: game.score
            }
          };
        }
      });
    });

    return highs;
  };

  // Get all games for a player
  const getPlayerGames = (playerNum: string | number) => {
    return Object.entries(allGames)
      .filter(([_, game]) => game.stats?.[playerNum])
      .map(([gameId, game]) => ({
        gameId,
        ...game,
        stats: game.stats[playerNum]
      }))
      .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
  };

  if (loading) {
    return (
      <div className={`min-h-screen ${bgClass} flex items-center justify-center`}>
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className={textClass}>Loading stats...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`min-h-screen ${bgClass} flex items-center justify-center p-4`}>
        <div className={`${cardClass} rounded-lg p-6 max-w-md`}>
          <AlertCircle className="text-red-500 mx-auto mb-4" size={48} />
          <h2 className="text-xl font-bold mb-2 text-center">No Data Found</h2>
          <p className={`${textClass} text-center mb-4`}>{error}</p>
          <p className={`${textClass} text-sm text-center`}>
            Please upload your data files or run the parser script first.
          </p>
        </div>
      </div>
    );
  }

  // Player Profile Page
  if (currentView === 'player' && selectedPlayerNumber) {
    const player = players[selectedPlayerNumber];
    const careerStats = seasonStats.all?.[selectedPlayerNumber] || {};
    const regularStats = seasonStats.regular?.[selectedPlayerNumber] || {};
    const playoffStats = seasonStats.playoff?.[selectedPlayerNumber] || {};
    const careerHighs = getPlayerCareerHighs(selectedPlayerNumber);
    const playerGames = getPlayerGames(selectedPlayerNumber);

    return (
      <div className={`min-h-screen ${bgClass} transition-colors duration-300`}>
        {/* Header */}
        <header className={`${accentClass} text-white shadow-lg`}>
          <div className="max-w-7xl mx-auto px-4 py-4">
            <button
              onClick={() => {
                setCurrentView('main');
                setSelectedPlayerNumber(null);
              }}
              className="flex items-center gap-2 mb-3 hover:opacity-80 transition-opacity"
            >
              <ChevronDown className="rotate-90" size={20} />
              <span>Back to Team</span>
            </button>
            <div className="flex items-center gap-4">
              <div className="w-20 h-20 rounded-full bg-white/20 flex items-center justify-center text-white font-bold text-2xl overflow-hidden">
                {player?.images?.portrait ? (
                  <img 
                    src={player.images.portrait} 
                    alt={player.name}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      const target = e.target as HTMLElement;
                      target.style.display = 'none';
                      target.parentElement!.innerHTML = `#${player?.number || selectedPlayerNumber}`;
                    }}
                  />
                ) : (
                  `#${player?.number || selectedPlayerNumber}`
                )}
              </div>
              <div>
                <h1 className="text-3xl font-bold">{player?.display_name || player?.name || `Player #${selectedPlayerNumber}`}</h1>
                <p className="text-blue-100">
                  #{player?.number || selectedPlayerNumber}
                  {player?.position && ` • ${player.position}`}
                </p>
              </div>
            </div>
          </div>
        </header>

        <div className="max-w-7xl mx-auto px-4 py-6">
          {/* Career Stats Overview */}
          <div className={`${cardClass} rounded-lg border ${borderClass} p-6 mb-6`}>
            <h2 className="text-2xl font-bold mb-4">Career Averages</h2>
            <div className="grid grid-cols-3 md:grid-cols-6 gap-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">{careerStats.ppg?.toFixed(1) || '0.0'}</div>
                <div className={`text-sm ${textClass}`}>PPG</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">{careerStats.rpg?.toFixed(1) || '0.0'}</div>
                <div className={`text-sm ${textClass}`}>RPG</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">{careerStats.apg?.toFixed(1) || '0.0'}</div>
                <div className={`text-sm ${textClass}`}>APG</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">{careerStats.fg_pct?.toFixed(1) || '0.0'}%</div>
                <div className={`text-sm ${textClass}`}>FG%</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">{careerStats['3pt_pct']?.toFixed(1) || '0.0'}%</div>
                <div className={`text-sm ${textClass}`}>3P%</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">{careerStats.gp || 0}</div>
                <div className={`text-sm ${textClass}`}>GP</div>
              </div>
            </div>
          </div>

          {/* Career Highs */}
          <div className={`${cardClass} rounded-lg border ${borderClass} p-6 mb-6`}>
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              <Trophy className="text-yellow-500" size={28} />
              Career Highs
            </h2>
            <div className="grid md:grid-cols-2 gap-4">
              {Object.entries(careerHighs).map(([stat, data]) => (
                <div key={stat} className={`p-4 rounded-lg border ${borderClass}`}>
                  <div className="flex justify-between items-start mb-2">
                    <div className="font-bold text-lg capitalize">{stat === '3pt' ? '3-Pointers' : stat}</div>
                    <div className="text-2xl font-bold text-blue-600">{data.value}</div>
                  </div>
                  {data.game && (
                    <div className={`text-sm ${textClass}`}>
                      <div>vs {data.game.opponent}</div>
                      <div>{data.game.date} • {data.game.score.us}-{data.game.score.them}</div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Splits */}
          <div className="grid md:grid-cols-2 gap-6 mb-6">
            <div className={`${cardClass} rounded-lg border ${borderClass} p-6`}>
              <h3 className="text-xl font-bold mb-4">Regular Season</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className={textClass}>Games</span>
                  <span className="font-bold">{regularStats.gp || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className={textClass}>PPG</span>
                  <span className="font-bold">{regularStats.ppg?.toFixed(1) || '0.0'}</span>
                </div>
                <div className="flex justify-between">
                  <span className={textClass}>RPG</span>
                  <span className="font-bold">{regularStats.rpg?.toFixed(1) || '0.0'}</span>
                </div>
                <div className="flex justify-between">
                  <span className={textClass}>APG</span>
                  <span className="font-bold">{regularStats.apg?.toFixed(1) || '0.0'}</span>
                </div>
              </div>
            </div>

            <div className={`${cardClass} rounded-lg border ${borderClass} p-6`}>
              <h3 className="text-xl font-bold mb-4">Playoffs</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className={textClass}>Games</span>
                  <span className="font-bold">{playoffStats.gp || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className={textClass}>PPG</span>
                  <span className="font-bold">{playoffStats.ppg?.toFixed(1) || '0.0'}</span>
                </div>
                <div className="flex justify-between">
                  <span className={textClass}>RPG</span>
                  <span className="font-bold">{playoffStats.rpg?.toFixed(1) || '0.0'}</span>
                </div>
                <div className="flex justify-between">
                  <span className={textClass}>APG</span>
                  <span className="font-bold">{playoffStats.apg?.toFixed(1) || '0.0'}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Game Log */}
          <div className={`${cardClass} rounded-lg border ${borderClass} p-6`}>
            <h2 className="text-2xl font-bold mb-4">Game Log</h2>
            <div className="space-y-3">
              {playerGames.length === 0 ? (
                <p className={`text-center py-8 ${textClass}`}>No games found</p>
              ) : (
                playerGames.map((game) => (
                  <button
                    key={game.gameId}
                    onClick={() => {
                      setSelectedGameId(game.gameId);
                      setCurrentView('game');
                    }}
                    className={`w-full p-4 rounded-lg border ${borderClass} hover:border-blue-500 transition-colors text-left`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <div className="font-bold">{game.result === 'W' ? '✅' : '❌'} vs {game.opponent}</div>
                        <div className={`text-sm ${textClass}`}>
                          {game.date} • {game.score.us}-{game.score.them}
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-blue-600">{game.stats.pts}</div>
                        <div className={`text-xs ${textClass}`}>PTS</div>
                      </div>
                    </div>
                    <div className="grid grid-cols-5 gap-2 text-sm">
                      <div className="text-center">
                        <div className="font-bold">{game.stats.reb || 0}</div>
                        <div className={textClass}>REB</div>
                      </div>
                      <div className="text-center">
                        <div className="font-bold">{game.stats.asst || 0}</div>
                        <div className={textClass}>AST</div>
                      </div>
                      <div className="text-center">
                        <div className="font-bold">{game.stats.fg?.[0] || 0}/{game.stats.fg?.[1] || 0}</div>
                        <div className={textClass}>FG</div>
                      </div>
                      <div className="text-center">
                        <div className="font-bold">{game.stats['3pt']?.[0] || 0}/{game.stats['3pt']?.[1] || 0}</div>
                        <div className={textClass}>3PT</div>
                      </div>
                      <div className="text-center">
                        <div className="font-bold">{game.stats.stl || 0}/{game.stats.blk || 0}</div>
                        <div className={textClass}>STL/BLK</div>
                      </div>
                    </div>
                  </button>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Box Score Page
  if (currentView === 'game' && selectedGameId) {
    const game = allGames[selectedGameId] as any;
    if (!game) {
      return (
        <div className={`min-h-screen ${bgClass} flex items-center justify-center`}>
          <div className={`${cardClass} rounded-lg p-6`}>
            <p>Game not found</p>
            <button
              onClick={() => {
                setCurrentView('main');
                setSelectedGameId(null);
              }}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg"
            >
              Back to Home
            </button>
          </div>
        </div>
      );
    }

    const teamStats = Object.entries(game.stats || {}).map(([num, stats]) => ({
      player: players[num] || { name: `Player #${num}`, number: num },
      stats
    }));

    return (
      <div className={`min-h-screen ${bgClass} transition-colors duration-300`}>
        {/* Header */}
        <header className={`${accentClass} text-white shadow-lg`}>
          <div className="max-w-7xl mx-auto px-4 py-4">
            <button
              onClick={() => {
                setCurrentView(selectedPlayerNumber ? 'player' : 'main');
                setSelectedGameId(null);
              }}
              className="flex items-center gap-2 mb-3 hover:opacity-80 transition-opacity"
            >
              <ChevronDown className="rotate-90" size={20} />
              <span>Back</span>
            </button>
            <div>
              <div className="text-sm text-blue-100 mb-1">{game.date}</div>
              <h1 className="text-3xl font-bold">
                Pretty Good {game.score.us} - {game.score.them} {game.opponent}
              </h1>
              <p className="text-blue-100 mt-1">
                {game.result === 'W' ? '✅ Win' : '❌ Loss'} • {game.homeAway === 'home' ? 'Home' : 'Away'}
              </p>
            </div>
          </div>
        </header>

        <div className="max-w-7xl mx-auto px-4 py-6">
          {/* Box Score */}
          <div className={`${cardClass} rounded-lg border ${borderClass} overflow-x-auto`}>
            <table className="w-full">
              <thead className={`${darkMode ? 'bg-gray-700' : 'bg-gray-100'} text-sm`}>
                <tr>
                  <th className="text-left p-3 sticky left-0 bg-inherit">Player</th>
                  <th className="p-3">PTS</th>
                  <th className="p-3">REB</th>
                  <th className="p-3">AST</th>
                  <th className="p-3">FG</th>
                  <th className="p-3">FG%</th>
                  <th className="p-3">3PT</th>
                  <th className="p-3">3P%</th>
                  <th className="p-3">FT</th>
                  <th className="p-3">FT%</th>
                  <th className="p-3">STL</th>
                  <th className="p-3">BLK</th>
                  <th className="p-3">TO</th>
                </tr>
              </thead>
              <tbody>
                {teamStats.map(({ player, stats }) => {
                  const s = stats as Record<string, any>;
                  return (
                  <tr key={player.number} className={`border-t ${borderClass} hover:bg-opacity-50 ${darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-50'}`}>
                    <td className="p-3 sticky left-0 bg-inherit">
                      <button
                        onClick={() => {
                          setSelectedPlayerNumber(player.number);
                          setCurrentView('player');
                        }}
                        className="font-bold hover:text-blue-600 transition-colors text-left"
                      >
                        #{player.number} {player.name}
                      </button>
                    </td>
                    <td className="p-3 text-center font-bold text-blue-600">{s.pts || 0}</td>
                    <td className="p-3 text-center">{s.reb || 0}</td>
                    <td className="p-3 text-center">{s.asst || 0}</td>
                    <td className="p-3 text-center">{s.fg?.[0] || 0}-{s.fg?.[1] || 0}</td>
                    <td className="p-3 text-center">{s.fg_pct?.toFixed(1) || '0.0'}%</td>
                    <td className="p-3 text-center">{s['3pt']?.[0] || 0}-{s['3pt']?.[1] || 0}</td>
                    <td className="p-3 text-center">{s['3pt_pct']?.toFixed(1) || '0.0'}%</td>
                    <td className="p-3 text-center">{s.ft?.[0] || 0}-{s.ft?.[1] || 0}</td>
                    <td className="p-3 text-center">{s.ft_pct?.toFixed(1) || '0.0'}%</td>
                    <td className="p-3 text-center">{s.stl || 0}</td>
                    <td className="p-3 text-center">{s.blk || 0}</td>
                    <td className="p-3 text-center">{s.to || 0}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen ${bgClass} transition-colors duration-300`}>
      {/* Header */}
      <header className={`${accentClass} text-white sticky top-0 z-50 shadow-lg`}>
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold">Pretty Good Basketball</h1>
              <p className="text-blue-100 text-sm">Team Statistics</p>
            </div>
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors"
              aria-label="Toggle dark mode"
            >
              {darkMode ? <Sun size={24} /> : <Moon size={24} />}
            </button>
          </div>
        </div>
      </header>

      {/* Filter Bar */}
      <div className={`${cardClass} sticky top-[72px] z-40 border-b ${borderClass} shadow-md`}>
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex flex-wrap gap-3 items-center justify-between">
            <div className="flex gap-2">
              <select
                value={selectedSeason}
                onChange={(e) => setSelectedSeason(e.target.value)}
                className={`px-3 py-2 rounded-lg border ${borderClass} ${cardClass} text-sm font-medium`}
              >
                <option value="2025">2025 Season</option>
                <option value="2024">2024 Season</option>
              </select>
              
              <select
                value={gameType}
                onChange={(e) => setGameType(e.target.value)}
                className={`px-3 py-2 rounded-lg border ${borderClass} ${cardClass} text-sm font-medium`}
              >
                <option value="regular">Regular Season</option>
                <option value="playoff">Playoffs</option>
                <option value="all">All Games</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
          {[
            { id: 'leaderboards', icon: TrendingUp, label: 'Leaderboards' },
            { id: 'records', icon: Trophy, label: 'Records' },
            { id: 'players', icon: Users, label: 'Players' },
            { id: 'games', icon: Calendar, label: 'Games' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium whitespace-nowrap transition-colors ${
                activeTab === tab.id
                  ? `${accentClass} text-white shadow-lg`
                  : `${cardClass} hover:opacity-80`
              }`}
            >
              <tab.icon size={18} />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Leaderboards Tab */}
        {activeTab === 'leaderboards' && (
          <div>
            {/* Stat Category Selector */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
              {statCategories.map(cat => (
                <button
                  key={cat.key}
                  onClick={() => setStatCategory(cat.key)}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    statCategory === cat.key
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                      : `border-transparent ${cardClass}`
                  }`}
                >
                  <div className="text-2xl font-bold text-blue-600">{cat.label}</div>
                  <div className={`text-xs ${textClass}`}>{cat.desc}</div>
                </button>
              ))}
            </div>

            {/* Leaderboard List */}
            {sortedPlayers.length === 0 ? (
              <div className={`${cardClass} rounded-lg border ${borderClass} p-8 text-center ${textClass}`}>
                <TrendingUp size={48} className="mx-auto mb-4 opacity-50" />
                <p>No stats available for this season yet.</p>
                <p className="text-sm mt-2">Add games using the parser script to see leaderboards.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {sortedPlayers.map((player, idx) => (
                  <div
                    key={player.number}
                    className={`${cardClass} rounded-lg border ${borderClass} p-4 hover:shadow-lg transition-shadow`}
                  >
                    <div className="flex items-center gap-4">
                      {/* Rank */}
                      <div className={`text-3xl font-bold ${idx < 3 ? 'text-blue-600' : textClass} w-12 text-center`}>
                        {idx + 1}
                      </div>

                      {/* Player Photo */}
                      <div className="w-16 h-16 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-bold text-xl flex-shrink-0 overflow-hidden">
                        {player.images?.portrait ? (
                          <img 
                            src={player.images.portrait} 
                            alt={player.name}
                            className="w-full h-full object-cover"
                            onError={(e) => {
                              const target = e.target as HTMLElement;
                              target.style.display = 'none';
                              target.parentElement!.innerHTML = `#${player.number}`;
                            }}
                          />
                        ) : (
                          `#${player.number}`
                        )}
                      </div>

                      {/* Player Info */}
                      <div className="flex-1 min-w-0">
                        <div className="font-bold text-lg truncate">{player.display_name || player.name}</div>
                        <div className={`text-sm ${textClass}`}>
                          {player.position && <span>{player.position} • </span>}
                          {player.gp} GP{player.teams ? ` • ${player.teams.join(', ')}` : ''}
                        </div>
                      </div>

                      {/* Stat Value */}
                      <div className="text-right">
                        <div className="text-3xl font-bold text-blue-600">
                          {typeof player[statCategory] === 'number' 
                            ? player[statCategory].toFixed(1) 
                            : '0.0'}
                        </div>
                        <div className={`text-xs ${textClass}`}>{statCategory.toUpperCase()}</div>
                      </div>
                    </div>

                    {/* Expandable Stats */}
                    <button
                      onClick={() => setExpandedPlayer(expandedPlayer === player.number ? null : player.number)}
                      className={`mt-3 w-full flex items-center justify-center gap-2 py-2 rounded ${darkMode ? 'bg-gray-700' : 'bg-gray-100'} text-sm hover:opacity-80 transition-opacity`}
                    >
                      {expandedPlayer === player.number ? (
                        <>Hide Details <ChevronUp size={16} /></>
                      ) : (
                        <>Show Details <ChevronDown size={16} /></>
                      )}
                    </button>

                    {expandedPlayer === player.number && (
                      <div className={`mt-3 pt-3 border-t ${borderClass} grid grid-cols-3 gap-3 text-sm`}>
                        <div className="text-center">
                          <div className={textClass}>PTS</div>
                          <div className="font-bold">{player.pts || 0}</div>
                        </div>
                        <div className="text-center">
                          <div className={textClass}>REB</div>
                          <div className="font-bold">{player.reb || 0}</div>
                        </div>
                        <div className="text-center">
                          <div className={textClass}>AST</div>
                          <div className="font-bold">{player.asst || 0}</div>
                        </div>
                        <div className="text-center">
                          <div className={textClass}>FG</div>
                          <div className="font-bold">{player.fg?.[0] || 0}/{player.fg?.[1] || 0}</div>
                        </div>
                        <div className="text-center">
                          <div className={textClass}>3PT</div>
                          <div className="font-bold">{player['3pt']?.[0] || 0}/{player['3pt']?.[1] || 0}</div>
                        </div>
                        <div className="text-center">
                          <div className={textClass}>FT</div>
                          <div className="font-bold">{player.ft?.[0] || 0}/{player.ft?.[1] || 0}</div>
                        </div>
                        <div className="text-center">
                          <div className={textClass}>STL</div>
                          <div className="font-bold">{player.stl || 0}</div>
                        </div>
                        <div className="text-center">
                          <div className={textClass}>BLK</div>
                          <div className="font-bold">{player.blk || 0}</div>
                        </div>
                        <div className="text-center">
                          <div className={textClass}>TO</div>
                          <div className="font-bold">{player.to || 0}</div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Records Tab */}
        {activeTab === 'records' && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold mb-4">Team Records</h2>
            
            {!records[gameType] || Object.keys(records[gameType]).length === 0 ? (
              <div className={`${cardClass} rounded-lg border ${borderClass} p-8 text-center ${textClass}`}>
                <Trophy size={48} className="mx-auto mb-4 opacity-50" />
                <p>No records available yet.</p>
                <p className="text-sm mt-2">Records will appear after processing games.</p>
              </div>
            ) : (
              recordCategories.map(({ key, label, icon }) => {
                const top3 = getTop3Records(key);
                if (top3.length === 0) return null;
                
                return (
                  <div key={key} className={`${cardClass} rounded-lg border ${borderClass} p-6`}>
                    <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                      <span className="text-2xl">{icon}</span>
                      {label}
                    </h3>
                    <div className="space-y-3">
                      {top3.map((record, idx) => (
                        <button
                          key={idx}
                          onClick={() => {
                            setSelectedGameId(record.gameId);
                            setCurrentView('game');
                          }}
                          className={`w-full flex items-center gap-4 p-4 rounded-lg border ${borderClass} hover:border-blue-500 transition-colors text-left`}
                        >
                          <div className={`text-3xl font-bold ${
                            idx === 0 ? 'text-yellow-500' : 
                            idx === 1 ? 'text-gray-400' : 
                            'text-amber-600'
                          } w-12 text-center`}>
                            {idx === 0 ? '🥇' : idx === 1 ? '🥈' : '🥉'}
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="font-bold text-lg truncate">{record.player}</div>
                            <div className={`text-sm ${textClass}`}>
                              vs {record.opponent} • {record.date}
                            </div>
                          </div>
                          <div className="text-4xl font-bold text-blue-600">{record.value}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                );
              })
            )}
          </div>
        )}

        {/* Players Tab */}
        {activeTab === 'players' && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold mb-4">Team Roster</h2>
            
            {Object.keys(players).length === 0 ? (
              <div className={`${cardClass} rounded-lg border ${borderClass} p-8 text-center ${textClass}`}>
                <Users size={48} className="mx-auto mb-4 opacity-50" />
                <p>No players registered yet.</p>
                <p className="text-sm mt-2">Players will appear after processing your first game.</p>
              </div>
            ) : (
              <div className="grid md:grid-cols-2 gap-4">
                {Object.values(players).map(player => {
                  const stats = seasonStats[gameType]?.[player.number] || {};
                  
                  return (
                    <button
                      key={player.number}
                      onClick={() => {
                        setSelectedPlayerNumber(player.number);
                        setCurrentView('player');
                      }}
                      className={`${cardClass} rounded-lg border ${borderClass} p-4 hover:border-blue-500 transition-all hover:shadow-lg text-left`}
                    >
                      <div className="flex items-center gap-4">
                        <div className="w-20 h-20 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white font-bold text-2xl flex-shrink-0 overflow-hidden">
                          {player?.images?.portrait ? (
                            <img 
                              src={player.images.portrait} 
                              alt={player.name}
                              className="w-full h-full object-cover"
                              onError={(e) => {
                                const target = e.target as HTMLElement;
                                target.style.display = 'none';
                                target.parentElement!.innerHTML = `#${player.number}`;
                              }}
                            />
                          ) : (
                            `#${player.number}`
                          )}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="font-bold text-xl truncate">{player.display_name || player.name}</div>
                          <div className={textClass}>
                            #{player.number}
                            {player.position && ` • ${player.position}`}
                          </div>
                          {player.teams && player.teams.length > 0 && (
                            <div className={`text-sm ${textClass} mt-1`}>
                              {player.teams.join(' • ')}
                            </div>
                          )}
                          {stats.gp > 0 && (
                            <div className="flex gap-3 mt-2 text-sm">
                              <div>
                                <span className="font-bold text-blue-600">{stats.ppg?.toFixed(1) || '0.0'}</span>
                                <span className={textClass}> PPG</span>
                              </div>
                              <div>
                                <span className="font-bold text-blue-600">{stats.rpg?.toFixed(1) || '0.0'}</span>
                                <span className={textClass}> RPG</span>
                              </div>
                              <div>
                                <span className="font-bold text-blue-600">{stats.apg?.toFixed(1) || '0.0'}</span>
                                <span className={textClass}> APG</span>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* Games Tab */}
        {activeTab === 'games' && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold mb-4">Game Log</h2>
            
            {Object.keys(allGames).length === 0 ? (
              <div className={`${cardClass} rounded-lg border ${borderClass} p-6 text-center ${textClass}`}>
                <Calendar size={48} className="mx-auto mb-4 opacity-50" />
                <p>No games found yet.</p>
                <p className="text-sm mt-2">Games will appear after processing with the parser script</p>
              </div>
            ) : (
              <div className="space-y-3">
                {Object.entries(allGames)
                  .filter(([_, game]) => {
                    if (gameType === 'regular') return !game.isPlayoff;
                    if (gameType === 'playoff') return game.isPlayoff;
                    return true;
                  })
                  .sort((a, b) => new Date(b[1].date) - new Date(a[1].date))
                  .map(([gameId, game]) => {
                    const totalPts = Object.values(game.stats || {}).reduce((sum, s) => sum + ((s as Record<string, any>).pts || 0), 0) as number;
                    
                    return (
                      <button
                        key={gameId}
                        onClick={() => {
                          setSelectedGameId(gameId);
                          setCurrentView('game');
                        }}
                        className={`w-full p-4 rounded-lg border ${borderClass} hover:border-blue-500 transition-all hover:shadow-lg text-left`}
                      >
                        <div className="flex justify-between items-start mb-3">
                          <div>
                            <div className="font-bold text-lg flex items-center gap-2">
                              {game.result === 'W' ? (
                                <span className="text-green-500">✅</span>
                              ) : (
                                <span className="text-red-500">❌</span>
                              )}
                              vs {game.opponent}
                            </div>
                            <div className={`text-sm ${textClass}`}>
                              {game.date} • {game.homeAway === 'home' ? 'Home' : 'Away'}
                              {game.isPlayoff && <span className="ml-2 px-2 py-0.5 bg-yellow-500 text-white text-xs rounded">PLAYOFF</span>}
                            </div>
                          </div>
                          <div className="text-right">
                            <div className={`text-2xl font-bold ${game.result === 'W' ? 'text-green-600' : 'text-red-600'}`}>
                              {game.score.us} - {game.score.them}
                            </div>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-3 gap-4 text-sm">
                          <div className={`text-center p-2 rounded bg-opacity-50 ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                            <div className="font-bold text-blue-600">{totalPts}</div>
                            <div className={textClass}>Team PTS</div>
                          </div>
                          <div className={`text-center p-2 rounded bg-opacity-50 ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                            <div className="font-bold text-blue-600">
                              {Object.values(game.stats || {}).reduce((sum, s) => sum + (s.reb || 0), 0)}
                            </div>
                            <div className={textClass}>Team REB</div>
                          </div>
                          <div className={`text-center p-2 rounded bg-opacity-50 ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                            <div className="font-bold text-blue-600">
                              {Object.values(game.stats || {}).reduce((sum, s) => sum + (s.asst || 0), 0)}
                            </div>
                            <div className={textClass}>Team AST</div>
                          </div>
                        </div>
                      </button>
                    );
                  })}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className={`${cardClass} border-t ${borderClass} mt-12 py-6`}>
        <div className={`max-w-7xl mx-auto px-4 text-center ${textClass}`}>
          <p>Pretty Good Basketball Team • Season Stats • Powered by EasyStats</p>
        </div>
      </footer>
    </div>
  );
}

function setPlayers(arg0: any) {
  throw new Error('Function not implemented.');
}
