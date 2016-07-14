#Description:
#   handles kicking off torrent monitoring script and moves torrents to their
#   final resting places.
#
# Commands:
#   hubot awaken the beast [me] - Print out this month's calendar

#TODO how do i trigger the action to move the fucking file once it has been
#downloaded?
#I also don't know how to figure out if it has even finished copying yet.
#the program will also need to quit once it has finished copying.
{spawn} = require 'child_process'
HubotSlack = require 'hubot-slack'
base_folder = "/home/emby/movies"

module.exports = (robot) ->

  regex = /awaken the beast (.*) has been (.*)/i
  robot.listeners.push new HubotSlack.SlackBotListener robot, regex, (res) ->
    res.send "\nThe darkest part of my mind is reserved to The Beast."
    filename = res.match[1]
    python = spawn 'python', ['scripts/theBeast.py', "#{filename}", process.env.IFTTT_API_KEY]
    python.stdout.on 'data', (data) -> res.send data.toString().trim()
    python.stderr.on 'data', (data) -> res.send data.toString().trim()

  robot.respond /move (.*) a (.*) to (.*)/i, (res) ->
    res.send "cough"
    torrents_folder = res.match[1]
    type = res.match[2] # need to verify it is books / movies / music / tv_shows
    approved_folders = ["books", "movies", "music", "tv_shows"]

    if type not in approved_folders
      res.send "not an approved folder"
      return
    new_folder_name = res.match[3]

    src_folder = base_folder + "/torrents/" + torrents_folder
    rename_src = base_folder + "/torrents/" + new_folder_name
    dest_folder = base_folder + "/" + type + "/" + new_folder_name

    mkdir = spawn 'mkdir', ["-p", dest_folder]
    mkdir.stdout.on 'data', (data) -> res.send data.toString().trim()
    mkdir.stderr.on 'data', (data) -> res.send data.toString().trim()

    mv = spawn 'mv', [src_folder, rename_src]
    mv.stdout.on 'data', (data) -> res.send data.toString().trim()
    mv.stderr.on 'data', (data) -> res.send data.toString().trim()

    rsync = spawn 'rsync', ["-ar", rename_src + "/", dest_folder + "/"]
    rsync.stdout.on 'data', (data) -> res.send data.toString().trim()
    rsync.stderr.on 'data', (data) -> res.send data.toString().trim()

    #rm deletes it before it can be transferred
    #rm = spawn 'rm', ["-rf", rename_src]
    #rm.stdout.on 'data', (data) -> res.send data.toString().trim()
    #rm.stderr.on 'data', (data) -> res.send data.toString().trim()
    res.send "That was very... how we both... We both, together, equally destroyed that guy!"


  robot.respond /open the (.*) doors/i, (res) ->
    doorType = res.match[1]
    if doorType is "pod bay"
      res.reply "I'm afraid I can't let you do that."
    else
      res.reply "Opening #{doorType} doors"
