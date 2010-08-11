@echo off

cd /d %~dp0

SET HOME=C:\Users\joamag
SET WORKSPACE_HOME=../../
python script.py %*
