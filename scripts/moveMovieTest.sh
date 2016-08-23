#!/bin/bash

cp -r moveMovieTestConfig.bak movieTest
TEST_DIR="$PWD/movieTest"
bash moveMovie.sh $TEST_DIR fakemovie_folder_rar rartest
bash moveMovie.sh $TEST_DIR fakemovie_folder normaltest
bash moveMovie.sh $TEST_DIR fakemovie_file filetest

TEST_OUT="`tree $TEST_DIR`"
CORRECT_OUT="`cat movieTestOut.txt`"
DIFF_OUT="`diff -q $TEST_DIR $TEST_OUT`" #report if files differ

if [ -s "$DIFF_OUT" ] #tests if file is zero size
then
  echo "FAILURE"
else
   echo "SUCCESS"
fi
rm -rf $TEST_DIR
