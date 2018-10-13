import mysql.connector
from contextlib import closing
from . import models

conn = None


def init(connection):
    global conn
    conn = connection


class ModelNotFoundException(Exception):
    pass


class CVideoFetcher(object):
    """Static class for interfacing with the database"""

    global conn

    @staticmethod
    def serialize_all(c_videos):
        """Utility method for serializing multiple CVideos

        Arguments:
            list - List of CVideos

        Returns:
            list - List of dictionaries representing serialized CVideos
        """
        serialized = []
        if c_videos:
            for cv in c_videos:
                serialized.append(cv.serialize())
            return serialized
        else:
            return None

    @staticmethod
    def fetch_all():
        """Fetches all partial models.CVideo's (only id and title) from the
           database.

        Returns:
            A list of all partial models.CVideo's
        """
        with closing(conn.cursor()) as cur:
            cur.execute("""SELECT id, title FROM c_videos""")
            rows = cur.fetchall()

        cvideos = []
        for r in rows:
            cvideos.append(models.CVideo(r[0], r[1]))

        return cvideos

    @staticmethod
    def fetch_by_id(id):
        """Fetches a complete models.CVideo from the database

        Arguments:
            id - The id of the model.CVideo

        Returns:
            CVideo - the requested CVideo

        Raises:
            ModelNotFoundException - if the requested model is not found

        """
        with closing(conn.cursor()) as cur:
            cur.execute("""SELECT id, title, description, resolution_w, \
                    resolution_h, size, uri, path
                    FROM c_videos WHERE id=%s LIMIT 0, 1""", (id,))
            rows = cur.fetchone()

        if rows:
            r = rows
            return models.CVideo.full(r[0], r[1], r[2], (r[3], r[4]), r[5],
                                      r[6], r[7])
        else:
            raise ModelNotFoundException
