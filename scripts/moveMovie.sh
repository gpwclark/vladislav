#!/bin/bash

#TODO make sure rsync has trailling slashes since these are folders
#TODO some movies are not in folders
#TODO some movies are rar'ed UGH.

# USAGE:
# bash moveMovie.sh ~/mytorrentfolder snatch_ERP_HDRIP_720P Snatch (2000)
BASE_FOLDER=$1
FILE_NAME=$2
NEW_FOLDER_NAME="$3/"
TORRENT_FOLDER="$BASE_FOLDER/torrents/"
TYPE_FOLDER="$BASE_FOLDER/movies/"


# SRC_FOLD="BASE_FOLDER/torrents/snatch_ERP_HDRIP_720P"
# RENAMED_SRC_FOLD="$BASE_FOLDER/torrents/Snatch (2000)"
# DEST_FOLDER="$BASE_FOLDER/movies/Snatch (2000)"

SRC_FOLD="$TORRENT_FOLDER$FILENAME"
RENAMED_SRC_FOLD="$TORRENT_FOLDER$NEW_FOLDER_NAME"
DEST_FOLDER="$TYPE_FOLDER$NEW_FOLDER_NAME"

# mkdir -p base/movies/Snatch (2000)
# mv base/torrents/snatch_ERP_HDRIP_720P base/torrents/Snatch (2000)
# rsync -ar base/torrents/Snatch (2000) base/movies/Snatch (2000) --remove-source-files
# find base/torrents/Snatch (2000)/ -depth -type d -empty -delete

mkdir -p $DEST_FOLDER
mv $SRC_FOLD $RENAMED_SRC_FOLD
rsync -ar $RENAMED_SRC_FOLD $DEST_FOLDER --remove-source-files
find $RENAMED_SRC_FOLD -depth -type d -empty -delete
