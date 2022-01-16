import redis
from redis import Connection

from api import yamlUtil


def connect():
    # 创建连接对象，设置基础数值
    connection = Connection(host="47.106.168.208", port=6379,
                            # db="python",
                            password=yamlUtil.read_yaml_bykeys("confid.yml", *["redis", "pwd"]))
    # 创建数据库连接池
    pool=redis.ConnectionPool(host="47.106.168.208", port=6379,
                            # db="python",
                            password=yamlUtil.read_yaml_bykeys("confid.yml", *["redis", "pwd"]))
    con=redis.Redis(connection_pool=pool)
    return con

def close(*connections):
    for c in connections:
        c.close()