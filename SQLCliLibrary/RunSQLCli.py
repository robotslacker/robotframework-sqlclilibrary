# -*- coding: UTF-8 -*-
import os
from sqlcli.main import SQLCli
from robot.api import logger
import shlex


class RunSQLCli(object):
    __BreakWithSQLerence  = False

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
    print("RunSQLCli. Please use this in RobotFramework.")
