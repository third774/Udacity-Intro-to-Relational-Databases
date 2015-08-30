#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    #"""Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    #"""Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    query = """
    DELETE FROM match_entries;
    """
    cur.execute(query)
    conn.commit()

    cur.close()
    conn.close()


def deletePlayers():
    #"""Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    query = """
    DELETE FROM players;
    """
    cur.execute(query)
    conn.commit()

    cur.close()
    conn.close()

def countPlayers():
    #"""Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    query = """
    SELECT count(*) as num
    FROM players;
    """
    cur.execute(query)
    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return count

def registerPlayer(name):
    # """Adds a player to the tournament database.
  
    # The database assigns a unique serial id number for the player.  (This
    # should be handled by your SQL database schema, not in your Python code.)
  
    # Args:
    #   name: the player's full name (need not be unique).
    # """

    conn = connect()
    cur = conn.cursor()

    cur.execute('INSERT INTO players (name) VALUES (%s)', (bleach.clean(name),))
    conn.commit()

    cur.close()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    
    # This query is used with match_entries schema

    # query = """
    # SELECT match_entries.player_id, players.name, count(case when match_entries.won = TRUE then 1 else null end) as wins, count(match_entries.player_id) as num_matches
    # FROM match_entries
    # INNER JOIN players
    # ON players.id = match_entries.player_id
    # GROUP BY match_entries.player_id, players.name
    # ORDER BY wins DESC;
    # """

    # Query below used old matches schema
    # 
    query = """
    SELECT players.id, players.name, count(matches.winner_id) as wins, count(match_part.no_matches)
    FROM players LEFT JOIN matches
    ON players.id = matches.winner_id
    LEFT JOIN match_part
    ON players.id = match_part.player_id
    GROUP BY players.id
    ORDER BY wins DESC;
    """
    
    cur.execute(query)
    count = cur.fetchall()

    cur.close()
    conn.close()

    return count



def reportMatch(winner, loser):
    # """Records the outcome of a single match between two players.

    # Args:
    #   winner:  the id number of the player who won
    #   loser:  the id number of the player who lost
    # """
    conn = connect()
    cur = conn.cursor()

    cur.execute('INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)', (winner, loser))
    conn.commit()

    cur.close()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    pairing = []
    
    i = 0
    for each in standings[::2]:
        pairing.append((standings[i][0],standings[i][1],standings[i+1][0],standings[i+1][1]),)
        print pairing
        i += 2

    return pairing