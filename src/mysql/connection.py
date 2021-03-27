import mysql.connector.pooling


def make_pool_party(dbconfig):
    return mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool",
                                     pool_size=20,
                                     **dbconfig)
