# -*- coding: UTF-8 -*-
from sqlcli.main import SQLCli


class SQLCliLibrary(object):
    """
    *** Settings ***
    Library   SQLCliLibrary

    *** Testcases ***
    Execute_SQL_Script
        Execute SQL Script  p_szSQLScript_FileName  p_szLogOutPutFileName
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_DOC_FORMAT = 'HTML'
    ROBOT_LIBRARY_VERSION = '0.0.2'

    def Execute_SQL_Script(self, p_szSQLScript_FileName, p_szLogOutPutFileName, *rest):
        cli = SQLCli(sqlscript=p_szSQLScript_FileName,
                     logfilename=p_szLogOutPutFileName)
        cli.run_cli()

    def keyword(self):
        pass

    def __init__(self):
        pass

def main():
    xx = SQLCliLibrary()
    xx.Execute_SQL_Script("aa.sql", "aa.txt")
    print("Hello World")


if __name__ == '__main__':
    main()
