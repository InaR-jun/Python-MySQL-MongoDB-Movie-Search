import pymysql
from contextlib import contextmanager
from local_settings1 import MYSQL_CONFIG


@contextmanager
def get_mysql_connection():
    """
    Creates and manages a connection to a MySQL database.
    Automatically closes the connection and cursor.
    """
    connection = None
    try:
        connection = pymysql.connect(**MYSQL_CONFIG)
        yield connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        yield None
    finally:
        if connection:
            connection.close()


def get_all_genres():
    """
    Returns a list of all genres from the database.
    """
    with get_mysql_connection() as connection:
        if connection is None:
            return []
        with connection.cursor() as cursor:
            cursor.execute("SELECT category_id, name FROM category ORDER BY name")
            return cursor.fetchall()

def get_min_max_years():
    """
    Returns the minimum and maximum years of release for movies.
    """
    with get_mysql_connection() as connection:
        if connection is None:
            return None, None
        with connection.cursor() as cursor:
            cursor.execute("SELECT MIN(release_year), MAX(release_year) FROM film")
            return cursor.fetchone()

def search_by_keyword(keyword, limit=10, offset=0):
    """
    Searches for movies by title, limiting the results.
    """
    with get_mysql_connection() as connection:
        if connection is None:
            return []
        with connection.cursor() as cursor:
            query = """
            SELECT title, release_year
            FROM film
            WHERE title LIKE %s
            ORDER BY title
            LIMIT %s OFFSET %s;
            """
            cursor.execute(query, (f"%{keyword}%", limit, offset))
            return cursor.fetchall()

def search_by_genre_and_years(genre_id, start_year, end_year, limit=10, offset=0):
    """
    Searches for films by genre and year range.
    """
    with get_mysql_connection() as connection:
        if connection is None:
            return []
        with connection.cursor() as cursor:
            query = """
            SELECT f.title, f.release_year
            FROM film AS f
            JOIN film_category AS fc ON f.film_id = fc.film_id
            WHERE fc.category_id = %s AND f.release_year BETWEEN %s AND %s
            ORDER BY f.title
            LIMIT %s OFFSET %s;
            """
            cursor.execute(query, (genre_id, start_year, end_year, limit, offset))
            return cursor.fetchall()

def check_exact_title_match(keyword):
    """
    Checks if the keyword is an exact match for any film title.
    """
    with get_mysql_connection() as connection:
        if connection is None:
            return False
        with connection.cursor() as cursor:
            query = "SELECT COUNT(*) FROM film WHERE title = %s;"
            cursor.execute(query, (keyword,))
            count = cursor.fetchone()[0]
            return count > 0