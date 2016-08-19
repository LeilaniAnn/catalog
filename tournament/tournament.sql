-- Connect to the database after dropping
DROP DATABASE tournament;
CREATE DATABASE tournament;
\c tournament


-- Drops all views and tables inside db

DROP VIEW IF EXISTS standings;
DROP VIEW IF EXISTS wins;
DROP VIEW IF EXISTS losses;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

-- Create Table
CREATE TABLE players (id SERIAL primary key, name TEXT);
CREATE TABLE matches (winner INT references players(id), 
					 loser INT references players(id));

-- Creating Views to simplify repetitive queries
-- Left join allows players to show up even with 0 matches
CREATE VIEW wins AS
	SELECT players.id, players.name, count(matches.winner) AS wins
	FROM players
		LEFT JOIN matches ON players.id = matches.winner
	GROUP BY players.id, players.name;

CREATE VIEW losses AS
	SELECT players.id, players.name, count(matches.loser) AS losses
	FROM players
		LEFT JOIN matches ON players.id = matches.loser
	GROUP BY players.id, players.name;

-- Player standings row 
-- [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
CREATE VIEW standings AS
	SELECT players.id, players.name, wins.wins, 
	wins.wins + losses.losses AS matches
	FROM players
		LEFT JOIN wins ON players.id = wins.id
		LEFT JOIN losses ON players.id = losses.id
	GROUP BY players.id, players.name, wins.wins, losses.losses
	ORDER BY wins desc;