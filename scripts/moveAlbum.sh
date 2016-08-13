#!/bin/bash

FILE_NAME=$1
ALBUM=$2
ARTIST=$3
TYPE=music

#approved_folders = ["music"]
#file = res.match[1]
#album = res.match[2]
#artist = res.match[2]
#type = "music"
#
#if type not in approved_folders
#  res.send "not an approved folder"
#  return
#
#src_folder = base_folder + "/torrents/" + file 
#rename_src = base_folder + "/torrents/" + album 
#dest_folder = base_folder + "/" + type + "/" + artist
#album_folder = base_folder + "/" + type + "/" + artist + "/" + album
#
#mkdir = spawn 'mkdir', ["-p", album_folder]
#mkdir.stdout.on 'data', (data) -> res.send data.toString().trim()
#mkdir.stderr.on 'data', (data) -> res.send data.toString().trim()
#
#mv = spawn 'mv', [src_folder, rename_src]
#mv.stdout.on 'data', (data) -> res.send data.toString().trim()
#mv.stderr.on 'data', (data) -> res.send data.toString().trim()
#
#rsync = spawn 'rsync', ["-ar", rename_src + "/", album_folder + "/", "--remove-source-files"]
#rsync.stdout.on 'data', (data) -> res.send data.toString().trim()
#rsync.stderr.on 'data', (data) -> res.send data.toString().trim()
#
#find = spawn 'find', [src_folder, "-depth", "-type", "d" , "-empty", "-delete"]
#find.stdout.on 'data', (data) -> res.send data.toString().trim()
#find.stderr.on 'data', (data) -> res.send data.toString().trim()
#
#rmdir = spawn 'rmdir', [base_folder + "/torrents/" + rename_src]
#rmdir.stdout.on 'data', (data) -> res.send data.toString().trim()
#rmdir.stderr.on 'data', (data) -> res.send data.toString().trim()
#
##rm deletes it before it can be transferred
##rm = spawn 'rm', ["-rf", rename_src]
##rm.stdout.on 'data', (data) -> res.send data.toString().trim()
##rm.stderr.on 'data', (data) -> res.send data.toString().trim()
#res.send "That was very... how we both... We both, together, equally destroyed that file!"
