from database.DB_connect import DBConnect
from model.album import Album


class DAO:

    @staticmethod
    def getAlbums(dMin):  # trovo gli album che durano almeno dMin minuti
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select a.*, sum(t.Milliseconds)/1000/60 as dTot
                    from album a, track t
                    where a.AlbumId = t.AlbumId
                    group by a.AlbumId 
                    having dTot > %s"""
        cursor.execute(query, (dMin, ))  # dMin è in minuti
        result = []
        for row in cursor:
            result.append(Album(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMapAlbum):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """select distinctrow t1.AlbumId as a1, t2.AlbumId as a2
                    from track t1, track t2, playlisttrack p1, playlisttrack p2
                    where t2.TrackId = p2.TrackId and t1.TrackId = p1.TrackId
                    and p2.PlaylistId = p1.PlaylistId
                    and t1.AlbumId < t2.AlbumId """
        cursor.execute(query)
        result = []
        for row in cursor:
            if row["a1"] in idMapAlbum and row["a2"] in idMapAlbum:  # devo controllare che gli album ci siano nell'idmap che è creata sui nodi del grafo
                result.append((idMapAlbum[row["a1"]], idMapAlbum[row["a2"]]))  # avrei potuto anche fare il DTO arco, al cui interno mettevo i due album
        cursor.close()
        conn.close()
        return result
