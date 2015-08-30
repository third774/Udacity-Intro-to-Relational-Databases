-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players ( name TEXT,
                     id SERIAL );

CREATE TABLE matches ( winner_id INT,
					 loser_id INT );

CREATE TABLE match_entries ( id SERIAL NOT NULL,
					 player_id INT NOT NULL,
					 opponent_id INT NOT NULL,
					 won BOOLEAN NOT NULL,
					 primary key (player_id, opponent_id) );