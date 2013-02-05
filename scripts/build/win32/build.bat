:: turns off the echo
@echo off

:: sets the version string constant value
set VERSION=1.0.1

:: sets the various global related name values
:: (going to be used for file construction)
set NAME=colony-%VERSION%
set NAME_RAW=colony-%VERSION%-raw
set NAME_SRC=colony-%VERSION%-src
set ID=pt.hive.colony

:: sets the directory to be used as the base
:: for the retrieval of the development tools
if not defined DEV_HOME set DEV_HOME=\dev

:: sets the various path related global
:: variable with relative names
set CURRENT_DIR=%cd%
set BUILD_DIR=%CURRENT_DIR%\build
set REPO_DIR=%BUILD_DIR%\repo
set TARGET_DIR=%BUILD_DIR%\target
set TEMP_DIR=%TARGET_DIR%\tmp
set RESULT_DIR=%TARGET_DIR%\result
set DIST_DIR=%TARGET_DIR%\dist
set BASE_DIR=%REPO_DIR%
set SRC_DIR=%BASE_DIR%\src

:: creates the various directories that are going to be
:: used during the build process
mkdir %BUILD_DIR%
mkdir %REPO_DIR%
mkdir %TARGET_DIR%
mkdir %TEMP_DIR%
mkdir %RESULT_DIR%
mkdir %DIST_DIR%

:: moves the current working directory to the build directory
:: so that all the generated files are placed there
cd %BUILD_DIR%

:: clones the repository to retrieve the source code
:: for compilation, the command is run using the call
:: operator so that it avoid exiting the current process
call git clone git://github.com/hivesolutions/colony.git %REPO_DIR% --quiet

:: in case the previous command didn't exit properly
:: must return immediately with the error
if %ERRORLEVEL% neq 0 ( cd %CURRENT_DIR% && exit /b %ERRORLEVEL% )

:: removes the internal git repository directory to avoid
:: extra files in source distribution
rmdir /q /s %REPO_DIR%\.git
del /q /f %REPO_DIR%\.gitignore

:: removes the extra (non source files) from the source
:: distribution directory
del /q /f %REPO_DIR%\TODO.md
del /q /f %REPO_DIR%\INTERNAL.md

:: copies the current repository as the source directory
:: into a temporary directory to be used latter
xcopy /q /y /a /e /k %REPO_DIR% %TEMP_DIR%\%NAME_SRC%\

:: copies the current repository source as the source directory
:: into a temporary directory to be used latter and also copies
:: it as the result from the build process
xcopy /q /y /a /e /k %REPO_DIR%\src %RESULT_DIR%\
xcopy /q /y /a /e /k %REPO_DIR%\src %TEMP_DIR%\%NAME%\

:: changes the current directory to the repository directory
:: to run a series of tests and build steps
cd %REPO_DIR%

:: runs the unit testing scripts to ensure that there is no
:: problem in the build process
python setup.py test

:: in case the previous command didn't exit properly
:: must return immediately with the error
if %ERRORLEVEL% neq 0 ( cd %CURRENT_DIR% && exit /b %ERRORLEVEL% )

:: runs the source distribution package using the setuptools
:: utility to provide a good distribution package
python setup.py process sdist

:: in case the previous command didn't exit properly
:: must return immediately with the error
if %ERRORLEVEL% neq 0 ( cd %CURRENT_DIR% && exit /b %ERRORLEVEL% )

:: runs the colony admin build command to generate the
:: appropriate package file for the colony container
call colony_admin build src\colony_container.json

:: in case the previous command didn't exit properly
:: must return immediately with the error
if %ERRORLEVEL% neq 0 ( cd %CURRENT_DIR% && exit /b %ERRORLEVEL% )

:: changes the name of the source distribution file in
:: order to avoid any name collision then copies it
:: and the colony package file to the distribution directory
move %REPO_DIR%\dist\%NAME%.zip dist\%NAME%_pypi.zip
xcopy /q /y /k dist\%NAME%_pypi.zip %DIST_DIR%
xcopy /q /y /k %ID%.ccx %DIST_DIR%

:: copies the complete set of result contents into the
:: raw tar file in order to be used in capsule construction
cd %RESULT_DIR%
tar -cf %NAME_RAW%.tar *
move %NAME_RAW%.tar %DIST_DIR%

:: changes the directory in order to group the files and then
:: returns the "original" build directory
cd %TEMP_DIR%
zip -qr %NAME%.zip %NAME%
tar -cf %NAME%.tar %NAME%
gzip -c %NAME%.tar > %NAME%.tar.gz
zip -qr %NAME_SRC%.zip %NAME_SRC%
tar -cf %NAME_SRC%.tar %NAME_SRC%
gzip -c %NAME_SRC%.tar > %NAME_SRC%.tar.gz
move %NAME%.zip %DIST_DIR%
move %NAME%.tar %DIST_DIR%
move %NAME%.tar.gz %DIST_DIR%
move %NAME_SRC%.zip %DIST_DIR%
move %NAME_SRC%.tar %DIST_DIR%
move %NAME_SRC%.tar.gz %DIST_DIR%
cd %BUILD_DIR%

echo Building capsule setup package...

:: runs the capsule process adding the viriatum group file
:: to it in order to create the proper intaller
capsule clone %DIST_DIR%\%NAME%.exe
capsule extend %DIST_DIR%\%NAME%.exe Colony "Colony Framework" %DIST_DIR%\%NAME_RAW%.tar

:: runs the checksums on the various elements of the setup
:: dir then copies the result into the setu directory
cd %DIST_DIR%
for %%F in (*) do (
    md5sum %%F > %TEMP_DIR%\%%F.md5
)
md5sum * > %TEMP_DIR%\MD5SUMS
move %TEMP_DIR%\*.md5 %DIST_DIR%
move %TEMP_DIR%\MD5SUMS %DIST_DIR%
cd %BUILD_DIR%

:: removes the directories that are no longer required
:: for the build
rmdir /q /s %TEMP_DIR%

:: moves back to the current directory (back to the base)
cd %CURRENT_DIR%
