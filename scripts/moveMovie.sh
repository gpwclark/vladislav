#!/bin/bash

#TODO why is everything destroyed
#TODO some movies are not in folders

# USAGE:
# bash moveMovie.sh ~/mytorrentfolder snatch_ERP_HDRIP_720P Snatch\ \(2000\)

# TODO RESTRICT USE OF TRAILING SLASHES
BASE_FOLDER=$1
echo "base folder: $BASE_FOLDER"
FILE_NAME=$2
echo "file name: $FILE_NAME"
NEW_FOLDER_NAME="$3/"
echo "new folder name: $NEW_FOLDER_NAME"
TORRENT_FOLDER="$BASE_FOLDER/torrents/"
echo "torrent folder name: $NEW_FOLDER_NAME"
TYPE_FOLDER="$BASE_FOLDER/movies/"
echo "type folder name: $NEW_FOLDER_NAME"


# SRC_FOLD="BASE_FOLDER/torrents/snatch_ERP_HDRIP_720P"
# RENAMED_SRC_FOLD="$BASE_FOLDER/torrents/Snatch (2000)"
# DEST_FOLDER="$BASE_FOLDER/movies/Snatch (2000)"

SRC_FOLD="$TORRENT_FOLDER$FILE_NAME"
echo "src folder name: $SRC_FOLD"
RENAMED_SRC_FOLD="$TORRENT_FOLDER$NEW_FOLDER_NAME"
echo "renamed_src folder name: $RENAMED_SRC_FOLD"
DEST_FOLDER="$TYPE_FOLDER$NEW_FOLDER_NAME"
echo "dest folder name: $DEST_FOLDER"
FOLDER_SUFFIX="folder"

# mkdir -p base/movies/Snatch (2000)
# mv base/torrents/snatch_ERP_HDRIP_720P base/torrents/Snatch (2000)
# rsync -ar base/torrents/Snatch (2000) base/movies/Snatch (2000) --remove-source-files
# find base/torrents/Snatch (2000)/ -depth -type d -empty -delete

if [ -f "$SRC_FOLD" ]
then
  FOLDER_NAME="$SRC_FOLD$FOLDER_SUFFIX"
  mkdir -p $FOLDER_NAME
  mv $SRC_FOLD $FOLDER_NAME
  SRC_FOLD="$FOLDER_NAME"
fi

bash unrarall/unrarall --clean=rar $SRC_FOLD
mkdir -p $DEST_FOLDER
mv $SRC_FOLD $RENAMED_SRC_FOLD
rsync -ar $RENAMED_SRC_FOLD $DEST_FOLDER --remove-source-files

#TODO will find command work if the file wasn't a folder
find $RENAMED_SRC_FOLD -depth -type d -empty -delete

# after this command runs we need to check for a few things...
# 1. the RENAMED_SRC_FOLD is gone.
# 2. the dest_folder exists is non-empty
# 3. message individual who requested media and ask them to let you know
#    if something isn't working quite right.
