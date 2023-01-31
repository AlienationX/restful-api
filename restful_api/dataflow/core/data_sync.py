#!/usr/bin/python3

from loguru import logger
from datetime import datetime
from itertools import chain

# from pyhive import hive
from impala import dbapi
import psycopg2


class DataChannels:
    
    def __init__(self, source_config, sink_config, commit_num=1000):
        # model_name = __import__(model_str, globals(), locals(), fromlist=[resource], level=1)
        
        driver_map = {
            # "mysql": MySQLdb.connect(**sink_config.config),
            # "oracle": "cx_Oracle.connect()",
            # "mssql": pymssql.connect(**source_config.config),
            # "postgres": psycopg2.connect(**source_config["config"]),
            "greenplum": psycopg2.connect(**sink_config["config"]),
            # "hive": hive.connect(**source_config["config"]),
            "impala": dbapi.connect(**source_config["config"]),
        }

        self.source_conn = driver_map[source_config["driver"]]
        self.sink_conn = driver_map[sink_config["driver"]]
        self.source_cur = self.source_conn.cursor()
        self.sink_cur = self.sink_conn.cursor()
        self.commit_num = commit_num
        self.start_time = datetime.now()
        print(self.start_time)  # __init__ 比 __enter__ 优先执行
    
    def get_conn(self):
        pass
    
    def get_convert_dtype(self, data_type):
        type_map = {
            "string": "varchar(127)",
            "tinyint": "int",
            "int": "int",
            "bigint": "bigint",
            "float": "float",
            "double": "numeric(38,4)",
            "decimal": "numeric",
        }
        for key in type_map.keys():
            if key in data_type:
                return data_type.replace(key, type_map[key])
        print(f"{data_type} ==> varchar(100)")
        return "varchar(100)"
    
    def create_sink_table(self, source_table, sink_table):
        """ col_name, data_type, comment """
        sql = f"describe {source_table}"
        logger.info(sql)
        self.source_cur.execute(sql)
        
        cols = []
        for row in self.source_cur.fetchall():
            cols.append("    {:<30} {}".format(row[0], self.get_convert_dtype(row[1])))
        
        create_sql = f"create table if not exists {sink_table} (\n" + \
            ",\n".join(cols) + \
            "\n)"
        logger.info("\n" + create_sql)
        self.sink_cur.execute(create_sql)
            
    def insert(self, source_table, sink_table):
        """ in memory 内存中执行 """
        
        self.create_sink_table(source_table, sink_table)
        
        s = datetime.now()
        sql = f"select * from {source_table} limit 1234"
        logger.info(sql)
        self.source_cur.execute(sql)

        rows = self.source_cur.fetchall()  # 返回list，触发计算
        logger.info(f"execute sql elapsed time {(datetime.now() - s).seconds}s")
        row_count = len(rows)
        logger.info("{} total rows: {}".format(source_table, row_count))
        if row_count == 0:
            logger.info(f"{source_table} no data, skip.")
            return
        
        # 读取数据执行sql成功后才执行删除数据
        del_sql = f"truncate table {sink_table}"
        logger.info(del_sql)
        self.sink_cur.execute(del_sql)
        self.sink_cur.execute("set optimizer to off")
            
        # col_count = len([col[0] for col in self.source_cur.description])
        col_count = len(rows[0])
        placeholders = ("%s," * col_count)[:-1]
        n_placeholders = f"({placeholders})," * self.commit_num
        # print(n_placeholders)
        
        # from psycopg2.extras import execute_values, execute_batch
        # from psycopg2.pool import SimpleConnectionPool, ThreadedConnectionPool
        # conn_pool = ThreadedConnectionPool(
        #     minconn=5, 
        #     maxconn=20,
        #     dbname="test",
        #     user="dw_rw",
        #     password="Yxsj@123",
        #     host="10.63.82.191",
        #     port="5432"
        # )
        # conn = conn_pool.getconn()
        # cur = conn.cursor()
        # cur.execute(f"truncate table {sink_table}")
        # cur.execute("set optimizer to off")
        
        i = 0
        start_time = datetime.now()
        logger.info("starting insert ......")
        while row_count > i:
            j = i + self.commit_num
            if j > row_count:
                n_placeholders = f"({placeholders})," * (row_count + self.commit_num - j)
                j = row_count
                
            # self.sink_cur.executemany("insert into {} values ({})".format(sink_table, ("%s," * col_count)[:-1]), rows[i:j])
            # self.sink_conn.commit()
            # print("insert into {} values ({})".format(sink_table, ("%s," * col_count)[:-1]), data)
            # print(self.sink_cur.query)     # 查看上一条执行的脚本，greenplum的executemany还是单条执行?
            
            one_data = list(chain.from_iterable(rows[i:j]))  # 二维列表转一维列表
            # print(one_data)
            self.sink_cur.execute("insert into {} values {}".format(sink_table, n_placeholders[:-1]), one_data)
            
            # 批量提交数据execute_values性能大于executemany，测试后并没有
            # execute_values(cur, "insert into {} values %s".format(sink_table), rows[i:j])
            # execute_batch(cur, "insert into {} values ({})".format(sink_table, ("%s," * col_count)[:-1]), rows[i:j])
            
            # self.sink_conn.commit()
            elapsed_time = datetime.now() - start_time
            duration = 1 if elapsed_time.seconds == 0 else elapsed_time.seconds
            speed = int(j / duration)
            progress = "{:.2f}".format(j / row_count * 100)
            logger.info(f"insert into {sink_table} {j}({progress}%) data succeed, speed {speed} records/s, elapsed time {elapsed_time}")
  
            i += self.commit_num
    
    def insert_with_iter(self, source_table, sink_table):
        """ iter 迭代器, 内存不够的时候推荐使用该方法 """
        
        self.create_sink_table(source_table, sink_table)
        
        s = datetime.now()
        sql = f"select * from {source_table} limit 1234"
        logger.info(sql)
        self.source_cur.execute(sql)

        logger.info(f"execute sql elapsed time {(datetime.now() - s).seconds}s")
        
        # 读取数据执行sql成功后才执行删除数据
        del_sql = f"truncate table {sink_table}"
        logger.info(del_sql)
        self.sink_cur.execute(del_sql)
        self.sink_cur.execute("set optimizer to off")
            
        # print(self.source_cur.description)
        col_count = len([col[0] for col in self.source_cur.description])
        placeholders = ("%s," * col_count)[:-1]
        # n_placeholders = f"({placeholders})," * self.commit_num
        # print(n_placeholders)
        
        i = 0
        start_time = datetime.now()
        logger.info("starting insert ......")
        while True:
            data = self.source_cur.fetchmany(self.commit_num)
            n = len(data)
            j = i + n
            if data:
                one_data = list(chain.from_iterable(data))  # 二维列表转一维列表
                # print(one_data)
                n_placeholders = f"({placeholders})," * n
                self.sink_cur.execute("insert into {} values {}".format(sink_table, n_placeholders[:-1]), one_data)
                
                elapsed_time = datetime.now() - start_time
                duration = 1 if elapsed_time.seconds == 0 else elapsed_time.seconds
                speed = int(j / duration)
                # progress = "{:.2f}".format(j / row_count * 100)
                logger.info(f"insert into {sink_table} {j} data succeed, speed {speed} records/s, elapsed time {elapsed_time}")
            else:
                break
            i += n

    def __enter__(self):
        logger.debug("init at " + str(datetime.now()))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.source_cur:
            self.source_cur.close()
            logger.debug(str(self.source_cur) + " cursor closed")
        if self.sink_cur:
            self.sink_cur.close()
            logger.debug(str(self.sink_cur) + " cursor closed")
        if self.source_conn:
            self.source_conn.commit()
            self.source_conn.close()
            logger.debug(str(self.source_conn) + " connect closed")
        if self.sink_conn:
            self.sink_conn.commit()
            self.sink_conn.close()
            logger.debug(str(self.sink_conn) + " connect closed")
        logger.info(f"Total time: {datetime.now() - self.start_time}s")


if __name__ == "__main__":
    source_db_config = {
        # "driver": "hive",
        # "config": {
        #     "host": "10.63.82.207",
        #     "username": "work",
        #     "password": "TwkdFNAdS1nIikzk",
        #     "database": "default",
        #     "port": 10000,
        #     "auth": "LDAP",
        # }
        "driver": "impala",
        "config": {
            "host": "10.63.82.218",
            "user": "work",
            "password": "TwkdFNAdS1nIikzk",
            "database": "default",
            "port": 21050,
            "auth_mechanism": "LDAP",
        }
    }
    sink_db_config = {
        "driver": "greenplum",
        "config": {
            "host": "10.63.82.191",
            "user": "dw_rw",
            "password": "Yxsj@123",
            "database": "test",
            "port": 5432
        }
    }
    with DataChannels(source_db_config, sink_db_config, 10) as channels:
        channels.insert_with_iter("medical_yongfu.src_yb_master_info", "medical.test_yb_master_info")