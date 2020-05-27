# -*- coding: UTF-8 -*-
import os
import traceback

from sqlcli.main import SQLCli
from robot.api import logger
import shlex


class RunSQLCli(object):
    __BreakWithSQLerence = False

    __m_CliHandler__  = SQLCli(noconsole=True)

    def SQLCli_Connect(self, p_ConnString):
        """ 连接到数据库上
        输入参数：
             p_ConnString:        连接字符串，格式为:  user/Pass@jdbc.<driver_type><connect_type>://<host>:<port>/<service>
        返回值：
            无
        """
        self.__m_CliHandler__.DoSQL("CONNECT " + p_ConnString)

    def SQLCli_LoadDriver(self, p_DriverFile, p_DriverClass):
        """ 加载数据库驱动
        输入参数：
             p_DriverFile:        数据库驱动文件（Jar包） 的位置
             p_DriverClass：      数据库驱动类
        返回值：
            无
        """
        self.__m_CliHandler__.DoSQL("LOADDRIVER " + p_DriverFile + " " + p_DriverClass)

    def SQLCli_DoSQL(self, p_szSQLString):
        """ 执行SQL脚本
        输入参数：
             p_szSQLString:        具体的SQL语句
        返回值：
            无
        """
        self.__m_CliHandler__.DoSQL(p_szSQLString)

    def SQLCli_SubmitJOB(self, p_szScriptName, p_nCopies=1, p_nLoopCount=1):
        """ 提交任务到后台作业
        输入参数：
             p_szScriptName:        脚本的名称
             p_nCopies              并发执行的份数，默认为1
             p_nLoopCount           循环执行的次数，默认为1
        返回值：
            无
        """
        self.__m_CliHandler__.DoSQL("SUBMITJOB " + p_szScriptName + " " + str(p_nCopies) + " " + str(p_nLoopCount))

    def SQLCli_StartJOB(self, p_JobID="ALL"):
        """ 启动所有后台任务
        输入参数：
             p_JobID:        需要启动的JOBID，默认是启动所有尚未启动的任务
        返回值：
            无
        """
        self.__m_CliHandler__.DoSQL("STARTJOB " + str(p_JobID))

    def SQLCli_WaitJOB(self, p_JobID="ALL"):
        """ 等待JOB全部完成
        输入参数：
             p_JobID:        需要等待的JOBID，默认是等待全部JOB完成
        返回值：
            无
        """
        self.__m_CliHandler__.DoSQL("WAITJOB " + str(p_JobID))

    def SQLCli_Break_When_Error(self, p_BreakWithSQLError):
        """ 设置是否在遇到错误的时候中断该Case的后续运行
        输入参数：
             p_BreakWithSQLError:        是否在遇到SQL错误的时候中断，默认为不中断
        返回值：
            无

        如果设置为True，则SQLCli运行会中断，Case会被判断执行失败
        如果设置为False，则SQLCli运行不会中断，运行结果文件中有错误信息，供参考
        """
        if str(p_BreakWithSQLError).upper() == 'TRUE':
            self.__BreakWithSQLerence = True
            self.__m_CliHandler__.DoSQL("SET WHENEVER_SQLERROR EXIT")

    def Logon_And_Execute_SQL_Script(self, p_szLogonString, p_szSQLScript_FileName, p_szLogOutPutFileName = None):
        """执行SQL脚本
        输入参数：
            p_szLogonString                连接用户名，口令
            p_szSQLScript_FileName         脚本文件名称
            p_szLogOutPutFileName          结果日志文件名称, 如果没有提供，则默认和脚本同名的.log文件
        输出参数：
            无
        例子：
            Logon And Execute SQL Script     admin/123456 test.sql test.log
        """
        m_szSQLScript_FileName = None
        m_szLogOutPutFileName = None

        # 判断是否全路径名
        if os.path.exists(p_szSQLScript_FileName):
            m_szSQLScript_FileName = p_szSQLScript_FileName

        # 检查T_SOURCE目录
        if m_szSQLScript_FileName is None:
            if "T_SOURCE" in os.environ:
                T_SOURCE = os.environ["T_SOURCE"]
                m_T_SOURCE_environs = shlex.shlex(T_SOURCE)
                m_T_SOURCE_environs.whitespace = ','
                m_T_SOURCE_environs.quotes = "'"
                m_T_SOURCE_environs.whitespace_split = True
                for m_SourceDirectory in list(m_T_SOURCE_environs):
                    if os.path.exists(os.path.join(m_SourceDirectory, p_szSQLScript_FileName)):
                        m_szSQLScript_FileName = os.path.join(m_SourceDirectory, p_szSQLScript_FileName)
                        break
            else:
                logger.info("Skip T_SOURCE check. not defined.")

        # 如果还是没有找到文件，则异常错误
        if m_szSQLScript_FileName is None:
            raise RuntimeError("Script [" + p_szSQLScript_FileName + "] does not exist.")

        # 处理日志文件名
        if p_szLogOutPutFileName is None:
            if "T_WORK" in os.environ:
                m_szLogOutPutFileName = os.path.join(
                    os.environ["T_WORK"],
                    os.path.basename(p_szSQLScript_FileName).split('.')[0] + ".log")
            else:
                m_szLogOutPutFileName = os.path.join(
                    os.getcwd(),
                    os.path.basename(p_szSQLScript_FileName).split('.')[0] + ".log")

        if m_szLogOutPutFileName is None:
            m_log_dir = os.path.dirname(p_szLogOutPutFileName)
            if os.path.exists(m_log_dir):
                # 全路径名
                m_szLogOutPutFileName = p_szLogOutPutFileName
        if m_szLogOutPutFileName is None:
            if "T_WORK" in os.environ:
                m_szLogOutPutFileName = os.path.join(os.environ["T_WORK"], p_szLogOutPutFileName)
        if m_szLogOutPutFileName is None:
            m_szLogOutPutFileName = os.path.join(os.getcwd(), p_szLogOutPutFileName)

        cli = SQLCli(logon=p_szLogonString,
                     sqlscript=m_szSQLScript_FileName,
                     logfilename=m_szLogOutPutFileName,
                     breakwitherror=self.__BreakWithSQLerence)
        m_Result = cli.run_cli()
        if self.__BreakWithSQLerence and not m_Result:
            raise RuntimeError("SQL Execute failed.")

    def Execute_SQL_Script(self, p_szSQLScript_FileName, p_szLogOutPutFileName = None):
        """执行SQL脚本
        输入参数：
            p_szSQLScript_FileName         脚本文件名称
            p_szLogOutPutFileName          结果日志文件名称, 如果没有提供，则默认和脚本同名的.log文件
        输出参数：
            无
        例子：
            Execute SQL Script     test.sql test.log
        """
        self.Logon_And_Execute_SQL_Script(None, p_szSQLScript_FileName, p_szLogOutPutFileName)


if __name__ == '__main__':
    m_xxx = RunSQLCli()
    try:
        os.chdir("C:\\Work\\linkoop\\sqlcli\\")
        m_xxx.SQLCli_Break_When_Error(True)
        m_xxx.SQLCli_LoadDriver("localtest\\linkoopdb-jdbc-2.3.0.jar", "com.datapps.linkoopdb.jdbc.JdbcDriver")
        m_xxx.SQLCli_Connect("admin/123456@jdbc:linkoopdb:tcp://192.168.174.23:9105/ldb")
        m_xxx.SQLCli_SubmitJOB("stresstest\\q1.sql", 1 , 5)
        m_xxx.SQLCli_StartJOB("ALL")
        m_xxx.SQLCli_WaitJOB("ALL")

    except Exception as e:
        print('str(e):  ', str(e))
        print('repr(e):  ', repr(e))
        print('traceback.print_exc():\n%s' % traceback.print_exc())
        print('traceback.format_exc():\n%s' % traceback.format_exc())
    print("RunSQLCli. Please use this in RobotFramework.")
