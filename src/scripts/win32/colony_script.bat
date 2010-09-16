:: Hive Colony Framework
:: Copyright (C) 2008 Hive Solutions Lda.
::
:: This file is part of Hive Colony Framework.
::
:: Hive Colony Framework is free software: you can redistribute it and/or modify
:: it under the terms of the GNU General Public License as published by
:: the Free Software Foundation, either version 3 of the License, or
:: (at your option) any later version.
::
:: Hive Colony Framework is distributed in the hope that it will be useful,
:: but WITHOUT ANY WARRANTY; without even the implied warranty of
:: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
:: GNU General Public License for more details.
::
:: You should have received a copy of the GNU General Public License
:: along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

:: __author__    = João Magalhães <joamag@hive.pt>
:: __version__   = 1.0.0
:: __revision__  = $LastChangedRevision: 7693 $
:: __date__      = $LastChangedDate: 2010-03-25 08:40:31 +0000 (qui, 25 Mar 2010) $
:: __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
:: __license__   = GNU General Public License (GPL), Version 3

:: turns off the echo
@echo off

:: sets the temporary variables
set RELATIVE_PATH=../../
set SCRIPT_NAME=script.py

:: executes the initial python script with
:: the provided arguments
python %~dp0/%RELATIVE_PATH%/%SCRIPT_NAME% %*

:: exits the process
exit /b %ERRORLEVEL%
