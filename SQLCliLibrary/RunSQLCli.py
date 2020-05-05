# -*- coding: UTF-8 -*-
from sqlcli.main import SQLCli


class RunSQLCli(object):

    @staticmethod
    def Execute_SQL_Script(p_szSQLScript_FileName, p_szLogOutPutFileName):
        """执行SQL脚本
        输入参数：
            p_szSQLScript_FileName         脚本文件名称
            p_szLogOutPutFileName          结果日志文件名称
        输出参数：
            无
        """
        cli = SQLCli(sqlscript=p_szSQLScript_FileName,
                     logfilename=p_szLogOutPutFileName)
        cli.run_cli()


if __name__ == '__main__':
    print("RunSQLCli. Please use this in RobotFramework.")
    RunSQLCli.Execute_SQL_Script("test.sql", "test.log")
