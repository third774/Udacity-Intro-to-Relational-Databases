#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Database connection
DB = []

## Get posts from database.
def GetAllPosts():
    conn = psycopg2.connect("dbname=forum")
    cur = conn.cursor()

    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''

    post_query = """
    SELECT * FROM posts
    ORDER BY time DESC;
    """

    cur.execute(post_query)

    posts = cur.fetchall()

    allowed_tags = ['h2', 'br']

    posts = [{'content': str(bleach.clean(row[0], allowed_tags)), 'time': str(row[1])} for row in posts]
    #posts.sort(key=lambda row: row['time'], reverse=True)
    cur.close()
    conn.close()

    return posts

## Add a post to the database.
def AddPost(content):
    conn = psycopg2.connect("dbname=forum")
    cur = conn.cursor()

    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''

    cur.execute("INSERT INTO posts (content) VALUES (%s)", (bleach.clean(content),))
    
    conn.commit()

    cur.close()
    conn.close()
    #t = time.strftime('%c', time.localtime())
    #DB.append((t, content))