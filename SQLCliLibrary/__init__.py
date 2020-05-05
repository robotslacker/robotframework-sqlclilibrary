# -*- coding: utf-8 -*-

from SQLCliLibrary.RunSQLCli import RunSQLCli


class SQLCliLibrary(RunSQLCli):
    """ RobotFrameWork 扩展库

    `SQLCliLibrary` 是RobotFrameWork的一个扩展库，通过这个扩展库，我们可以在Robot中利用SQLCli工具执行SQL脚本

    以下是在Robot中调用该扩展库的例子：
    ========================================================
    *** Settings ***
    Library           SQLCliLibrary

    *** Test Cases ***
    E101Test
        Execute SQL Script         e101.sql    e101.log
    E102Test
        Execute SQL Script         e102.sql    e102.log
    ========================================================

    如何利用Robot来执行上述文件：
    $>  robot [test file]
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_DOC_FORMAT = 'TEXT'
    ROBOT_LIBRARY_VERSION = '0.0.6'