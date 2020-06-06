# -*- coding: UTF-8 -*-
import os
from robot.api import logger
import re
import traceback
import jaydebeapi


class SQLException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message


class LinkoopSQLParse:
    objSQLConnection = None
    objSQLLists = list()
    objSQLReferenceLists = list()
    objSQLExecuteLists = list()
    jar_file = None
    driver_class = None
    db_url = None
    db_username = None
    db_password = None
    db_type = None
    db_driver_type = None
    db_host = None
    db_port = None
    db_service_name = None

    def Verify_LinkoopSQLAndComments(self, p_filename, p_username, p_password):
        """ 对LinkoopDB中， 处理合并SQL和注释的的脚本  """
        """
         输入参数：
              p_filename:        需要处理的脚本
              p_username：        数据库连接用户名
              p_password：        数据库连接口令
         返回值：
             无

         如果比对没有错误，正常结束
         如果比对发现错误，测试失败，抛出异常
         """
        # 连接数据库
        if "SQLCLI_CONNECTION_URL" in os.environ:
            # 从环境变量里头拼的连接字符串
            connect_parameters = [var for var in re.split(r'//|:|@|/', os.environ['SQLCLI_CONNECTION_URL']) if
                                  var]
            if len(connect_parameters) == 6:
                self.db_type = connect_parameters[1]
                self.db_driver_type = connect_parameters[2]
                self.db_host = connect_parameters[3]
                self.db_port = connect_parameters[4]
                self.db_service_name = connect_parameters[5]
                self.db_url = \
                    connect_parameters[0] + ':' + connect_parameters[1] + ':' + \
                    connect_parameters[2] + '://' + connect_parameters[3] + ':' + \
                    connect_parameters[4] + ':/' + connect_parameters[5]
            else:
                print("[" + str(connect_parameters) + "]")
                raise SQLException(
                    "Unexpeced env SQLCLI_CONNECTION_URL\n." +
                    "jdbc:[db type]:[driver type]://[host]:[port]/[service name]")

        if "SQLCLI_CONNECTION_JAR_NAME" in os.environ and \
                "SQLCLI_CONNECTION_CLASS_NAME" in os.environ:
            self.jar_file = os.environ["SQLCLI_CONNECTION_JAR_NAME"]
            self.driver_class = os.environ["SQLCLI_CONNECTION_CLASS_NAME"]
        else:
            raise SQLException(
                "Unexpeced env SQLCLI_CONNECTION_JAR_NAME and SQLCLI_CONNECTION_CLASS_NAME\n." +
                "Please set correct env first]")
        self.db_username = p_username
        self.db_password = p_password
        self.objSQLConnection = jaydebeapi.connect(
            self.driver_class, 'jdbc:' +
                               self.db_type + ":" + self.db_driver_type + "://" +
                               self.db_host + ":" + self.db_port + "/" + self.db_service_name,
            [self.db_username, self.db_password], self.jar_file, )

        #  清空之前的记录
        self.objSQLLists = list()
        self.objSQLReferenceLists = list()
        self.objSQLExecuteLists = list()

        fp = open(p_filename, 'r')
        contents = fp.readlines()
        fp.close()

        # 合并所有的字符串到一个完整的字符串中
        m_total_content = None
        for line in contents:
            if not m_total_content:
                m_total_content = line
            else:
                m_total_content = m_total_content + line
        m_total_content = m_total_content.strip()

        m_sql_start = 0
        m_total_length = len(m_total_content)
        while True:
            m_sql_end = m_sql_start + m_total_content[m_sql_start:].find('/*')
            if m_sql_end == -1:  # 剩下的部分全部是SQL，不过没用了
                # self.objSQLLists.append(m_total_content[m_sql_start:])
                break
            m_result_start = m_sql_end + 2
            m_result_end = m_result_start + m_total_content[m_result_start:].find('*/')
            if m_result_end == -1:  # 剩下的部分全部是RESULT，不过没用了
                # self.objSQLReferenceLists.append(m_total_content[m_result_start:])
                break
            self.objSQLLists.append(m_total_content[m_sql_start:m_sql_end].strip())
            self.objSQLReferenceLists.append(m_total_content[m_result_start:m_result_end].strip())
            m_sql_start = m_result_end + 2
            if m_sql_start >= m_total_length:
                break  # 后面已经没有内容了

        # 开始执行SQL文件
        niter = 0
        for sql_group in self.objSQLLists:
            # 每段可能有多个SQL
            sql_list = sql_group.split(';')
            # 计算的结果放置在字符串里头
            m_str_result = None
            for sql in sql_list:
                # 执行SQL语句，得到的结果是一个元祖列表
                cursor = None
                try:
                    cursor = self.objSQLConnection.cursor()
                    cursor.execute(sql)
                    sql_result = cursor.fetchall()

                    result = []
                    for row in sql_result:
                        m_row = []
                        for column in row:
                            if str(type(column)).find('JDBCClobClient') != -1:
                                m_row.append(column.getSubString(1, 20))
                            else:
                                m_row.append(column)
                        m_row = tuple(m_row)
                        result.append(m_row)
                    sql_result = result

                except Exception as e:
                    traceback.print_exc()

                    # 开始处理下一个SQL语句
                    niter = niter + 1

                    # 在输出结果中填写失败原因
                    if not m_str_result:
                        m_str_result = str(e)
                    else:
                        m_str_result = str(m_str_result) + str(e)
                else:
                    # 将sql_result中的列表变成分行打印
                    for m_row_info in sql_result:
                        m_str_row = None
                        for m_column_info in m_row_info:
                            if not m_str_row:
                                m_str_row = m_column_info
                            else:
                                m_str_row = str(m_str_row) + ','
                                if m_column_info:
                                    m_str_row = str(m_str_row) + str(m_column_info)
                                else:
                                    m_str_row = str(m_str_row) + 'null'
                        if not m_str_result:
                            m_str_result = m_str_row
                        else:
                            m_str_result = str(m_str_result) + '\n'
                            m_str_result = str(m_str_result) + str(m_str_row)
                finally:
                    # 关闭游标
                    if cursor:
                        cursor.close()

            # 运行结果放到结果列表中
            self.objSQLExecuteLists.append(m_str_result)
            # 开始处理下一个SQL语句
            niter = niter + 1

        # 开始比对文件结果
        n_check_successful = True
        for niter in range(len(self.objSQLReferenceLists)):
            if str(self.objSQLExecuteLists[niter]).strip() != str(self.objSQLReferenceLists[niter]).strip():
                logger.info("SQL> " + str(self.objSQLLists[niter]))
                logger.info("Current   Result: " + str(self.objSQLExecuteLists[niter]).strip())
                logger.info("Exepected Result: " + str(self.objSQLReferenceLists[niter]).strip())
                n_check_successful = False
                break
        if not n_check_successful:
            raise RuntimeError('Got Difference.')
        else:
            logger.info("Compare Successful")
        return n_check_successful
