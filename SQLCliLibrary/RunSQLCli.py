# -*- coding: UTF-8 -*-
import os
import sys
import traceback

from sqlcli.main import SQLCli
from robot.api import logger
import shlex


class RunSQLCli(object):
    __BreakWithSQLerence = False              # 是否遇到SQL错误就退出，默认是不退出
    __EnableConsoleOutPut = False             # 是否关闭在Console上的显示，默认是不关闭
    __SQLMapping = None                       # 映射文件列表

    __m_CliHandler__ = SQLCli(HeadlessMode=True)

    def SQLCli_Connect(self, p_ConnString):
        """ 连接到数据库 """
        """
        输入参数：
             p_ConnString:        连接字符串，格式为:  user/Pass@jdbc.<driver_type><connect_type>://<host>:<port>/<service>
        返回值：
            无
        """
        self.__m_CliHandler__.DoSQL("CONNECT " + p_ConnString)

    def SQLCli_LoadDriver(self, p_DriverFile, p_DriverClass):
        """ 加载数据库驱动 """
        """
        输入参数：
             p_DriverFile:        数据库驱动文件（Jar包） 的位置
             p_DriverClass：      数据库驱动类
        返回值：
            无
        """
        self.__m_CliHandler__.DoSQL("LOADDRIVER " + p_DriverFile + " " + p_DriverClass)

    def SQLCli_DoSQL(self, p_szSQLString):
        """ 执行SQL脚本 """
        """
        输入参数：
             p_szSQLString:        具体的SQL语句
        返回值：
            无
        """
        self.__m_CliHandler__.DoSQL(p_szSQLString)

    def SQLCli_SubmitJOB(self, p_szScriptName, p_nCopies=1, p_nLoopCount=1):
        """ 提交任务到后台作业 """
        """
        输入参数：
             p_szScriptName:        脚本的名称
             p_nCopies              并发执行的份数，默认为1
             p_nLoopCount           循环执行的次数，默认为1
        返回值：
            无
        """
        self.__m_CliHandler__.DoSQL("SUBMITJOB " + p_szScriptName + " " + str(p_nCopies) + " " + str(p_nLoopCount))

    def SQLCli_StartJOB(self, p_JobID="ALL"):
        """ 启动所有后台任务 """
        """
        输入参数：
             p_JobID:        需要启动的JOBID，默认是启动所有尚未启动的任务
        返回值：
            无
        """
        self.__m_CliHandler__.DoSQL("STARTJOB " + str(p_JobID))

    def SQLCli_WaitJOB(self, p_JobID="ALL"):
        """ 等待JOB全部完成  """
        """
        输入参数：
             p_JobID:        需要等待的JOBID，默认是等待全部JOB完成
        返回值：
            无
        """
        self.__m_CliHandler__.DoSQL("WAITJOB " + str(p_JobID))

    def SQLCli_Break_When_Error(self, p_BreakWithSQLError):
        """ 设置是否在遇到错误的时候中断该Case的后续运行  """
        """
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
        if str(p_BreakWithSQLError).upper() == 'FALSE':
            self.__BreakWithSQLerence = False
            self.__m_CliHandler__.DoSQL("SET WHENEVER_SQLERROR CONTINUE")

    def SQLCli_Enable_ConsoleOutput(self, p_ConsoleOutput):
        """ 设置是否在在屏幕上显示SQL的执行过程  """
        """
        输入参数：
             p_ConsoleOutput:        是否在在屏幕上显示SQL的执行过程， 默认是不显示
        返回值：
            无

        如果设置为True，则所有SQL执行的过程不仅仅会记录在日之内，也会显示在控制台上
        如果设置为False，则所有SQL执行的过程仅仅会记录在日之内，不会显示在控制台上
        """
        if str(p_ConsoleOutput).upper() == 'TRUE':
            self.__EnableConsoleOutPut = True
        if str(p_ConsoleOutput).upper() == 'FALSE':
            self.__EnableConsoleOutPut = False

    def SQLCli_Set_SQLMAPPING(self, p_szSQLMapping):
        """ 设置SQLMAPPING文件  """
        """
        输入参数：
             p_szSQLMapping:        SQLMAPPING文件，如果包括多个文件，用，分割
        返回值：
            无
        """
        self.__SQLMapping = p_szSQLMapping

    def Logon_And_Execute_SQL_Script(self, p_szLogonString, p_szSQLScript_FileName, p_szLogOutPutFileName=None):
        """ 执行SQL脚本  """
        """
        输入参数：
            p_szLogonString                连接用户名，口令
            p_szSQLScript_FileName         脚本文件名称
            p_szLogOutPutFileName          结果日志文件名称, 如果没有提供，则默认和脚本同名的.log文件
        输出参数：
            无
        例子：
            Logon And Execute SQL Script     admin/123456 test.sql test.log
        """
        try:
            m_szSQLScript_FileName = None

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
            # 如果没有提供文件名， 有T_WORK，   日志是T_WORK下和SQL同名的.log文件
            # 如果没有提供文件名， 没有T_WORK， 日志是当前目录下和SQL同名的.log文件
            # 如果提供了文件名，   并且是全路径名， 用提供的名字
            # 如果提供了文件名，   但不是全路径名，有T_WORK下，在T_WORK下生成提供的文件名
            # 如果提供了文件名，   但不是全路径名，没有T_WORK下，在当前目录下生成提供的文件名
            if p_szLogOutPutFileName is None:
                if "T_WORK" in os.environ:
                    m_szLogOutPutFileName = os.path.join(
                        os.environ["T_WORK"],
                        os.path.basename(p_szSQLScript_FileName).split('.')[0] + ".log")
                    m_szLogOutPutFullFileName = os.path.join(os.environ["T_WORK"], m_szLogOutPutFileName)
                else:
                    m_szLogOutPutFileName = os.path.join(
                        os.getcwd(),
                        os.path.basename(p_szSQLScript_FileName).split('.')[0] + ".log")
                    m_szLogOutPutFullFileName = os.path.join(os.getcwd(), m_szLogOutPutFileName)
            else:
                if os.path.exists(os.path.dirname(p_szLogOutPutFileName)):
                    # 全路径名
                    m_szLogOutPutFullFileName = p_szLogOutPutFileName
                else:
                    if "T_WORK" in os.environ:
                        m_szLogOutPutFullFileName = os.path.join(os.environ["T_WORK"], p_szLogOutPutFileName)
                    else:
                        m_szLogOutPutFullFileName = os.path.join(os.getcwd(), p_szLogOutPutFileName)

            sys.__stdout__.write('\n')                    # 打印一个空行，好保证在Robot上Console显示不错行
            logger.info('===== Execute   [' + m_szSQLScript_FileName + '] ========')
            logger.info('===== LogFile   [' + m_szLogOutPutFullFileName + '] ========')
            logger.info('===== BreakMode [' + str(self.__BreakWithSQLerence) + '] ========')
            sys.__stdout__.write('===== Execute   [' + m_szSQLScript_FileName + '] ========\n')
            sys.__stdout__.write('===== LogFile   [' + m_szLogOutPutFullFileName + '] ========\n')
            sys.__stdout__.write('===== BreakMode [' + str(self.__BreakWithSQLerence) + '] ========\n')
            sys.__stdout__.write('===== Starting .....\n')
            if not self.__EnableConsoleOutPut:
                myConsole = None
                myHeadLessMode = True
                mylogger = None
            else:
                myConsole = sys.__stdout__
                myHeadLessMode = False
                mylogger = logger
            cli = SQLCli(logon=p_szLogonString,
                         sqlscript=m_szSQLScript_FileName,
                         logfilename=m_szLogOutPutFullFileName,
                         Console=myConsole,
                         HeadlessMode=myHeadLessMode,
                         logger=mylogger,
                         sqlmap=self.__SQLMapping,
                         breakwitherror=self.__BreakWithSQLerence)
            m_Result = cli.run_cli()
            sys.__stdout__.write('===== End SQLCli with result [' + str(m_Result) + '] \n')
            if self.__BreakWithSQLerence and not m_Result:
                # 如果日志信息少于30K，则全部打印
                m_Results = []
                with open(m_szLogOutPutFullFileName, "rb") as f:
                    size = f.seek(0, 2)
                    if size < 30 * 1024:  # 如果文件不足30K，则全部读入
                        # 回到文件开头
                        f.seek(0, 0)
                        for row in f.readlines():
                            m_Results.append(row.decode('utf-8'))
                    else:
                        # 回到文件开头
                        f.seek(0, 0)
                        m_ReadBuf = f.readlines(10 * 1024)
                        for row in m_ReadBuf[0:10]:
                            m_Results.append(row.decode('utf-8'))
                        m_Results.append(" .......................   ")
                        # 来到文件末尾
                        f.seek(- 20 * 1024, 2)
                        m_ReadBuf = f.readlines()
                        for row in m_ReadBuf[-30:]:
                            m_Results.append(row.decode('utf-8'))
                sys.__stdout__.write(' =====  SQL Break with Error ========\n')
                logger.info(' =====  SQL Break with Error ========')
                for row in m_Results:
                    sys.__stdout__.write(row)
                    logger.info(row.replace("\n", ""))
                logger.info(' =====  SQL Break with Error ========')
                sys.__stdout__.write(' =====  SQL Break with Error ========\n')
                raise RuntimeError("SQL Execute failed.")
        except RuntimeError as ex:
            raise ex
        except Exception as ex:
            logger.info('str(e):  ', str(ex))
            logger.info('repr(e):  ', repr(ex))
            logger.info('traceback.print_exc():\n%s' % traceback.print_exc())
            logger.info('traceback.format_exc():\n%s' % traceback.format_exc())
            raise RuntimeError("SQL Execute failed.")

    def Execute_SQL_Script(self, p_szSQLScript_FileName, p_szLogOutPutFileName=None):
        """ 执行SQL脚本  """
        """
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
    pass
