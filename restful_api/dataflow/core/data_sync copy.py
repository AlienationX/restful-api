class TwoDB:
    def __init__(self, cursor_type='list'):
        mssql_db_config = {
            # 'host': '10.15.1.11',
            # 'user': 'warmsoft_read',
            # 'password': 'Awq123456',
            # 'database': 'pms',
            # 'port': 2121,
            # 'charset': 'utf8',

            'host': '192.168.99.1',
            'user': 'sa',
            'password': 'qazwsx12345!@#$%',
            'database': 'warmmedreport',
            'port': 1433,
            'charset': 'utf8',

            # 'host': '180.169.226.158',
            # 'user': 'sa',
            # 'password': 'Aibier1177%',
            # 'database': 'FnlPetCtr',
            # 'port': 1433,
            # 'charset': 'utf8',
        }
        mysql_db_config = {
            # 'host': 'localhost',
            # 'user': 'root',
            # 'password': 'root',
            # 'database': 'sanbengzi',
            # 'port': 3306,
            # 'charset': 'utf8',
            'host': 'rm-m5e2m5gr559b3s484.mysql.rds.aliyuncs.com',
            'user': 'writer',
            'password': 'HH$writer',
            'database': 'sanbengzi',
            'port': 3306,
            'charset': 'utf8',
        }
        self.mssql_conn = pymssql.connect(**mssql_db_config)
        self.mysql_conn = pymysql.connect(**mysql_db_config)
        if cursor_type == 'list':
            self.mssql_cur = self.mssql_conn.cursor()
            self.mysql_cur = self.mysql_conn.cursor()
        elif cursor_type == 'dict':
            self.mssql_cur = self.mssql_conn.cursor(as_dict=True)
            self.mysql_cur = self.mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)
        else:
            raise Exception('cursor type error !')

    def __enter__(self):
        logging.debug("exec __enter__")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.mssql_cur:
            self.mssql_cur.close()
        if self.mysql_cur:
            self.mysql_cur.close()
        if self.mssql_conn:
            self.mssql_conn.commit()
            self.mssql_conn.close()
        if self.mysql_conn:
            self.mysql_conn.commit()
            self.mysql_conn.close()
        logging.debug("connect closed")


def db_conn_test():
    pass


def get_all_tables():
    sql = "select name from sys.tables where name <> 'SysLogs' order by name"
    with TwoDB() as twodb:
        twodb.mssql_cur.execute(sql)
        rows = twodb.mssql_cur.fetchall()
    all_tables = [x[0] for x in rows]
    logging.info(all_tables)
    return all_tables


def create_table(table_name):
    print "start"
    sql = """select t.name as table_name,
                   s.name as column_name,
                   case when s1.name in ('int','tinyint','bigint','date','datetime','text') then s1.name
                        when s1.name in ('char','varchar') then s1.name + '(' + case when s.max_length<0 then '8000' else cast(s.max_length as varchar(10)) end +')'
                        when s1.name in ('nchar''nvarchar') then substring(s1.name,2,len(s1.name)) + '(' + case when s.max_length<0 then '8000' else cast(s.max_length as varchar(10)) end +')'
                        when s1.name='money' then 'decimal(18,2)'
                        when s1.name='timestamp' then 'blob'
                        else 'varchar(255)' end as column_type,
                   s1.name as raw_type,
                   s.max_length as raw_length,
                   s.precision as raw_precision,
                   s.*
              from sys.tables t
              left join sys.columns s on t.object_id=s.object_id
              left join sys.types s1 on s.user_type_id=s1.user_type_id
              where t.type='U' and t.name='{table_name}'
              order by t.name,s.column_id
              """.format(table_name=table_name)
    drop_script = "drop table if exists `{}`".format(table_name)
    create_script = "create table if not exists `{table_name}` (".format(table_name=table_name)
    with TwoDB('dict') as twodb:
        twodb.mssql_cur.execute(sql)
        rows = twodb.mssql_cur.fetchall()
        for row in rows:
            create_script += "`{0}` {1},".format(row['column_name'], row['column_type'])
        create_script = create_script[:-1]
        create_script += ") ENGINE=InnoDB CHARSET=utf8;"
        create_script = create_script.lower()
        logging.info(drop_script)
        logging.info(create_script)
        twodb.mysql_cur.execute(drop_script)
        twodb.mysql_cur.execute(create_script)
    logging.info("{} has been created".format(table_name))


# def insert_date(self, table_name):
#     """一次insert全部数据，数据量大的话会很慢很慢，卡死状态"""
#     sql = "select * from {}".format(table_name)
#     self.mssql_cur_list.execute(sql)
#     rows = self.mssql_cur_list.fetchall()
#     rows_count = self.mssql_cur_list.rowcount
#     if rows_count == 0:
#         logging.info("{} no data, skip.".format(table_name))
#         return
#     logging.info("{} total rows: {}".format(table_name, rows_count))
#     cols_count = len(rows[0])
#     self.mysql_cur_dict.execute("truncate table {}".format(table_name))
#     effect_rows = self.mysql_cur_dict.executemany("insert into {} values ({})".format(table_name, ("%s," * cols_count)[:-1]), rows)
#     logging.info("insert into {} {} data succeeded".format(table_name, effect_rows))


def insert_data_batch(table_name):
    """
    串行 total：367311
    commit_num=1000    2:16
    commit_num=10000   2:04
    """
    sql = "select * from {}".format(table_name)
    with TwoDB() as twodb:
        twodb.mssql_cur.execute(sql)
        rows = twodb.mssql_cur.fetchall()
        rows_count = twodb.mssql_cur.rowcount
        if rows_count == 0:
            logging.info("{} no data, skip.".format(table_name))
            return
        logging.info("{} total rows: {}".format(table_name, rows_count))
        cols_count = len(rows[0])
        twodb.mysql_cur.execute("truncate table `{}`".format(table_name))
        # for i in range(0,rows_count,self.commit_num):
        #     j=i+self.commit_num
        #     if j > rows_count:
        #         j = rows_count
        #     effect_rows = self.mysql_cur_dict.executemany("insert into {} values ({})".format(table_name, ("%s," * cols_count)[:-1]), rows[i:j])
        #     logging.info("insert into {} {} data succeeded".format(table_name, effect_rows))
        i = 0
        while rows_count > i:
            j = i + _commit_num
            if j > rows_count:
                j = rows_count
            twodb.mysql_cur.executemany("insert into `{}` values ({})".format(table_name, ("%s," * cols_count)[:-1]), rows[i:j])
            twodb.mysql_conn.commit()
            logging.info("insert into {} {}({}%) data succeeded".format(table_name, j, '%0.0f' % (float(j) / rows_count * 100)))
            i += _commit_num


# """数据并行插入，有表锁，搁浅"""
# def get_rows(table_name):
#     sql = "select * from {}".format(table_name)
#     with TwoDB() as twodb:
#         twodb.mssql_cur.execute(sql)
#         rows = twodb.mssql_cur.fetchall()
#         rows_count = twodb.mssql_cur.rowcount
#         if rows_count == 0:
#             logging.info("{} no data, skip.".format(table_name))
#             return
#     logging.info("{} total rows: {}".format(table_name, rows_count))
#     return rows
#
#
# def insert_data_tmp(rows, rows_count, i):
#     cols_count = len(rows[0])
#     with TwoDB() as twodb:
#         j = i + _commit_num
#         if j > rows_count:
#             j = rows_count
#         twodb.mysql_cur.executemany("insert into {} values ({})".format(table_name, ("%s," * cols_count)[:-1]), rows[i:j])
#         twodb.mysql_conn.commit()
#         logging.info("insert into {} {}({}%) data succeeded".format(table_name, j, '%0.0f' % (float(j) / rows_count * 100)))
#
#
# def insert_data_batch_parallel(rows):
#     rows_count = len(rows)
#     p = Pool(_process_num)
#     for i in range(0, rows_count, _commit_num):
#         p.apply_async(func=insert_data_tmp, args=(rows, rows_count, i,))
#     p.close()
#     p.join()

def create_and_insert(table_name):
    create_table(table_name)
    insert_data_batch(table_name)


def insert_log():
    sql = """create table if not exists data_sync_log (
                id int,
                dt char(10),
                start_time varchar(50),
                end_time varchar(50),
                exec_time varchar(50),
                message varchar(200),
                sign char(1)
              )"""
    max_sql = "select max(id) from data_sync_log"
    with TwoDB() as twodb:
        twodb.mysql_cur.execute(sql)
        twodb.mysql_cur.execute(max_sql)
        max_id = twodb.mysql_cur.fetchone()[0]
        if max_id is None:
            max_id = 1
        else:
            max_id += 1
        start_time = datetime.datetime.now()
        twodb.mysql_cur.execute("insert into data_sync_log(id,dt,start_time) values({},'{}','{}')".format(max_id, start_time.strftime("%Y-%m-%d"), start_time))
    logging.info("start insert data_sync_log")
    return max_id, start_time


def update_log(max_id, start_time):
    end_time = datetime.datetime.now()
    exec_time = (end_time - start_time).seconds
    m, s = divmod(exec_time, 60)
    h, m = divmod(m, 60)
    exec_time = "%02d:%02d:%02d" % (h, m, s)
    with TwoDB() as twodb:
        twodb.mysql_cur.execute("update data_sync_log set end_time='{}',exec_time='{}',message='{}',sign={} where id={}".format(end_time, exec_time, "成功，详细日志所在路径" + log_name.replace('\\','\\\\'), 1, max_id))
    logging.info("insert data_sync_log end")


if __name__ == "__main__":
    # for table_name in get_all_tables():
    #     create_table(table_name)
    #     insert_data_batch(table_name)
    #     # rows = get_rows(table_name)
    #     # insert_data_batch_parallel(rows)
    max_id, start_time = insert_log()
    p = Pool(_process_num)
    for table_name in get_all_tables():
        p.apply_async(func=create_and_insert, args=(table_name,))
    p.close()
    p.join()
    update_log(max_id, start_time)
    logging.info("--------------------------end--------------------------\n")