#Description:
#   handles kicking off torrent monitoring script and moves torrents to their
#   final resting places.
#
# Commands:
#   vlad awaken the beast [file] has been ... - start theBeast.py monitoring [file]
#   vlad move [file] to [dir] - move specified file one of the dirs books/movies/music/tv_shows

{spawn} = require 'child_process'
HubotSlack = require 'hubot-slack'
base_folder = "/home/emby/movies"

module.exports = (robot) ->

  regex = /awaken the beast (.*) has been (.*)/i
  robot.listeners.push new HubotSlack.SlackBotListener robot, regex, (res) ->
    res.send "\nThe darkest part of my mind is reserved to The Beast."
    filename = res.match[1]
    python = spawn 'python', ['scripts/theBeast.py', "#{filename}", process.env.IFTTT_API_KEY, "/home/emby/movies/torrents/"]
    python.stdout.on 'data', (data) -> res.send data.toString().trim()
    python.stderr.on 'data', (data) -> res.send data.toString().trim()

#TODO needs to adhere to new .torrent file naming std.
  robot.respond /move (.*) album (.*) artist (.*)/i, (res) ->
    approved_folders = ["music"]
    file = res.match[1]
    album = res.match[2]
    artist = res.match[2]
    type = "music"

    if type not in approved_folders
      res.send "not an approved folder"
      return

    src_folder = base_folder + "/torrents/" + file 
    rename_src = base_folder + "/torrents/" + album 
    dest_folder = base_folder + "/" + type + "/" + artist
    album_folder = base_folder + "/" + type + "/" + artist + "/" + album

    mkdir = spawn 'mkdir', ["-p", album_folder]
    mkdir.stdout.on 'data', (data) -> res.send data.toString().trim()
    mkdir.stderr.on 'data', (data) -> res.send data.toString().trim()

    mv = spawn 'mv', [src_folder, rename_src]
    mv.stdout.on 'data', (data) -> res.send data.toString().trim()
    mv.stderr.on 'data', (data) -> res.send data.toString().trim()

    rsync = spawn 'rsync', ["-ar", rename_src + "/", album_folder + "/", "--remove-source-files"]
    rsync.stdout.on 'data', (data) -> res.send data.toString().trim()
    rsync.stderr.on 'data', (data) -> res.send data.toString().trim()

    find = spawn 'find', [src_folder, "-depth", "-type", "d" , "-empty", "-delete"]
    find.stdout.on 'data', (data) -> res.send data.toString().trim()
    find.stderr.on 'data', (data) -> res.send data.toString().trim()

    rmdir = spawn 'rmdir', [base_folder + "/torrents/" + rename_src]
    rmdir.stdout.on 'data', (data) -> res.send data.toString().trim()
    rmdir.stderr.on 'data', (data) -> res.send data.toString().trim()

    #rm deletes it before it can be transferred
    #rm = spawn 'rm', ["-rf", rename_src]
    #rm.stdout.on 'data', (data) -> res.send data.toString().trim()
    #rm.stderr.on 'data', (data) -> res.send data.toString().trim()
    res.send "That was very... how we both... We both, together, equally destroyed that file!"

#TODO need to remove the folder after it has been moved.
#TODO need to add tests in case file is not in folder OR it is RARed
#TODO needs to adhere to new naming standards
  robot.respond /move (.*) a (.*) to (.*)/i, (res) ->
    res.send "cough"
    file = res.match[1]
    type = res.match[2] # need to verify it is books / movies / tv_shows
    approved_folders = ["books", "movies", "tv_shows"]

    if type not in approved_folders
      res.send "not an approved folder"
      return
    new_folder_name = res.match[3]

    src_folder = base_folder + "/torrents/" + file 
    rename_src = base_folder + "/torrents/" + new_folder_name
    dest_folder = base_folder + "/" + type + "/" + new_folder_name

    mkdir = spawn 'mkdir', ["-p", dest_folder]
    mkdir.stdout.on 'data', (data) -> res.send data.toString().trim()
    mkdir.stderr.on 'data', (data) -> res.send data.toString().trim()

    mv = spawn 'mv', [src_folder, rename_src]
    mv.stdout.on 'data', (data) -> res.send data.toString().trim()
    mv.stderr.on 'data', (data) -> res.send data.toString().trim()

    rsync = spawn 'rsync', ["-ar", rename_src + "/", dest_folder + "/", "--remove-source-files"]
    rsync.stdout.on 'data', (data) -> res.send data.toString().trim()
    rsync.stderr.on 'data', (data) -> res.send data.toString().trim()

    find = spawn 'find', [src_folder, "-depth", "-type", "d" , "-empty", "-delete"]
    find.stdout.on 'data', (data) -> res.send data.toString().trim()
    find.stderr.on 'data', (data) -> res.send data.toString().trim()

    #rm deletes it before it can be transferred
    #rm = spawn 'rm', ["-rf", rename_src]
    #rm.stdout.on 'data', (data) -> res.send data.toString().trim()
    #rm.stderr.on 'data', (data) -> res.send data.toString().trim()
    res.send "That was very... how we both... We both, together, equally destroyed that file!"


  robot.respond /open the (.*) doors/i, (res) ->
    doorType = res.match[1]
    if doorType is "pod bay"
      res.reply "I'm afraid I can't let you do that."
    else
      res.reply "Opening #{doorType} doors"
