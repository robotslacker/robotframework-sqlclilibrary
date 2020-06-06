# -*- coding: utf-8 -*-

from SQLCliLibrary.RunSQLCli import RunSQLCli
from SQLCliLibrary.LinkoopSQLParse import LinkoopSQLParse


class SQLCliLibrary(RunSQLCli, LinkoopSQLParse):
    """ RobotFrameWork 扩展库

    `SQLCliLibrary` 是RobotFrameWork的一个扩展库，通过这个扩展库，我们可以在Robot中利用SQLCli工具执行SQL脚本

    以下是在Robot中调用该扩展库的例子：
    ========================================================
    *** Settings ***
    Library           SQLCliLibrary

    *** Test Cases ***
    E101Test
        Execute SQL Script                   e101.sql    e101.log
    E102Test
        Logon And Execute SQL Script         admin/123456 e102.sql    e102.log
    E103Test
        SQLCli LoadDriver                    localtest\jdbcxxx.jar  com.xxx.xxx.jdbc.JdbcDriver
        SQLCli Connect                       user password
        SQLCli SubmitJob                     task1_sql 1 5
        SQLCli WaitJob

    关于脚本中文件名的写法：
    1： 具体的全路径文件名称，
    2： 当前目录下的文件名称
    3： 所有定义在T_SOURCE中的目录下的相同名称文件

    关于生成日志文件名的写法：
    1： 如果日志文件名是一个全路径名，则按照全路径名来生成文件
    2： 如果定义了T_WORK， 日志输出在T_WORK下
    3： 生成在当前工作目录下
    ========================================================
    SQLCli工具的详细信息，也可以参考： https://github.com/robotslacker/sqlcli/blob/master/Doc.md

    如何利用Robot来执行上述文件：
    $>  robot [test file]
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_DOC_FORMAT = 'TEXT'
    ROBOT_LIBRARY_VERSION = '0.0.19'