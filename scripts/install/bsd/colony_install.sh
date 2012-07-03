#!/bin/sh
# -*- coding: utf-8 -*-

# Hive Colony Framework
# Copyright (c) 2008-2012 Hive Solutions Lda.
#
# This file is part of Hive Colony Framework.
#
# Hive Colony Framework is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Colony Framework is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.

# __author__    = João Magalhães <joamag@hive.pt>
# __version__   = 1.0.0
# __revision__  = $LastChangedRevision$
# __date__      = $LastChangedDate$
# __copyright__ = Copyright (c) 2008-2012 Hive Solutions Lda.
# __license__   = GNU General Public License (GPL), Version 3

# the base http address from where the colony installation
# is going to be downloaded
BASE_ADDRESS="http://hivesolutions.dyndns.org/integration_public"

# the binary path to be used to create the dynamic
# links for colony
BIN_PATH=/usr/bin

# the temporary path to be used to store the temporary
# files downloaded
TMP_PATH=/tmp

# in case the target path is not defined
# iterates over all the given command line options
# to parsed them and change the script state
while getopts "rht:" option; do
    # switches over the option value
    case $option in
        r)
            # sets the replace (files) flag
            REPLACE="true"
        ;;
        h)
            # prints an information message
            echo "USAGE: colony_web_install [-r] [-h] [-t target_path]"

            # exits the installation
            exit
        ;;
        t)
            # sets the target path from the
            # option value
            TARGET_PATH=$OPTARG
        ;;
    esac
done

# in case the target path is not defined
# a default one must be used
if [ -z "$TARGET_PATH" ]; then
    # prints an information message
    echo "No target path defined using the current path (.)"

    # sets the default  target path
    TARGET_PATH="."
fi

# in case the target colony path already
# exists
if [ -e "$TARGET_PATH/colony" ]; then
    # prints an information message
    echo "Target path ($TARGET_PATH/colony) already exists"

    # in case the replace flag is set
    # (the current installation must be removed)
    if [ -n "$REPLACE" ]; then
        # prints an information message
        echo "Removing existing installation ($TARGET_PATH/colony)..."

        # removes the existing instalation
        rm -rf "$TARGET_PATH/colony"
    # otherwise the replace flag is not set
    # and no replacement is going to occur
    else
        # exits the installation
        exit
    fi
fi

# prints an information message
echo "Downloading installation files (may take a while)..."

# retrieves the various colony base files
wget "$BASE_ADDRESS/LATEST_SUCCESS.build" -O "$TMP_PATH/colony.build" -o /dev/null
wget "$BASE_ADDRESS/LATEST_SUCCESS/resources/colony_1.0.0_all.zip" -O "$TMP_PATH/colony_1.0.0_all.zip" -o /dev/null
wget "$BASE_ADDRESS/LATEST_SUCCESS/resources/colony-base-plugins_1.0.0_all.zip" -O "$TMP_PATH/colony-base-plugins_1.0.0_all.zip" -o /dev/null
wget "$BASE_ADDRESS/LATEST_SUCCESS/resources/colony-base-containers_1.0.0_all.zip" -O "$TMP_PATH/colony-base-containers_1.0.0_all.zip" -o /dev/null

# retrieves the build number from the the colony
# repository file
BUILD="$(cat $TMP_PATH/colony.build)"

# print an information message
echo "Deploying colony build $BUILD"

# prints an information message
echo "Unziping the base colony files..."

# unzips the colony base file, the colony
# base plugins file and the base containers file
unzip "$TMP_PATH/colony_1.0.0_all.zip" -d "$TARGET_PATH" > /dev/null
unzip "$TMP_PATH/colony-base-plugins_1.0.0_all.zip" -d "$TARGET_PATH" > /dev/null
unzip "$TMP_PATH/colony-base-containers_1.0.0_all.zip" -d "$TARGET_PATH" > /dev/null

# prints an information message
echo "Deploying plugin and containers files into colony..."

# executes the deployment script to deploy the various
# base cpx files
"$TARGET_PATH/colony/scripts/bsd/colony_deploy.sh" --flush > /dev/null 2> /dev/null

# iterates over all the script elements to create their
# appropriate symbolic link references
for ELEMENT in colony colony_deploy colony_log; do
    # checks if the element symbolic link already exists
    # in the system
    if ! [ -e "$BIN_PATH/$ELEMENT" ]; then
        # prints an information message
        echo "Creating symbolic link ($BIN_PATH/$ELEMENT)..."

        # creates the symbolic link for the python execution script
        ln -s "$TARGET_PATH/colony/scripts/bsd/$ELEMENT.sh" "$BIN_PATH/$ELEMENT"
    # otherwise no symbolic link is created
    else
        # prints an information message
        echo "No symbolic created ($BIN_PATH/$ELEMENT) link exists..."
    fi
done

# prints an information message
echo "Removing the temporary files..."

# removes all temporary files
rm "$TMP_PATH/colony.build"
rm "$TMP_PATH/colony_1.0.0_all.zip"
rm "$TMP_PATH/colony-base-plugins_1.0.0_all.zip"
rm "$TMP_PATH/colony-base-containers_1.0.0_all.zip"

# prints an information message
echo "Finished colony web install"
