# -*- coding: UTF-8 -*-
from sqlcli.main import SQLCli


class RunSQLCli(object):
    """
    *** Settings ***
    Library   SQLCliLibrary

    *** Testcases ***
    Execute_SQL_Script
        Execute SQL Script  SQLScript_FileName  LogOutPutFileName
    """
    @staticmethod
    def Execute_SQL_Script(p_szSQLScript_FileName, p_szLogOutPutFileName):
        """Execute sql script
        """
        cli = SQLCli(sqlscript=p_szSQLScript_FileName,
                     logfilename=p_szLogOutPutFileName)
        cli.run_cli()


if __name__ == '__main__':
    print("RunSQLCli. Please use this in RobotFramework.")
    RunSQLCli.Execute_SQL_Script("test.sql", "test.log")
