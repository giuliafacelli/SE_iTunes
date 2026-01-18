from database.DB_connect import DBConnect
from model.album import Album

class DAO:
    @staticmethod
    def get_album_duration(duration_min):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT a.id, a.title, a.artist_id, SUM(t.milliseconds)/60000 AS duration
                FROM album a, track t
                WHERE a.id = t.album_id
                GROUP BY a.id, a.title, a.artist_id
                HAVING duration > %s
                """

        cursor.execute(query,(duration_min,))

        for row in cursor:
            album = Album(**row)
            result.append(album)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_album_playlist_map(albums):
        conn = DBConnect.get_connection()
        result = {a: set() for a in albums}
        album_ids = tuple(a.id for a in albums)
        if not album_ids:
            return result

        cursor = conn.cursor(dictionary=True)
        query = f"""
                SELECT t.album_id, t.id, p.playlist_id
                FROM track t, playlist_track p
                WHERE t.id = p.track_id
                AND t.album_id IN {album_ids}
                """

        cursor.execute(query)

        for row in cursor:
            album = next((a for a in albums if a.id == row['album_id']), None)
            if album:
                result[album].add(row['playlist_id'])
        cursor.close()
        conn.close()
        return result
