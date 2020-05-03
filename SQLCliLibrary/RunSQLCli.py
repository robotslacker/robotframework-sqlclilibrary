# -*- coding: UTF-8 -*-
from sqlcli.main import SQLCli


class RunSQLCli(object):
    """
    *** Settings ***
    Library   SQLCliLibrary

    *** Testcases ***
    Execute_SQL_Script
        Execute SQL Script  p_szSQLScript_FileName  p_szLogOutPutFileName
    """


    def Execute_SQL_Script(self, p_szSQLScript_FileName, p_szLogOutPutFileName, *rest):
        cli = SQLCli(sqlscript=p_szSQLScript_FileName,
                     logfilename=p_szLogOutPutFileName)
        cli.run_cli()

    def keyword(self):
        pass

    def __init__(self):
        pass

def main():
    xx = RunSQLCli()
    xx.Execute_SQL_Script("aa.sql", "aa.txt")
    print("Hello World")


if __name__ == '__main__':
    main()
