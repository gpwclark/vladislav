#Description:
#   Prints out this month's ASCII calendar.
#
# Commands:
#   hubot calendar [me] - Print out this month's calendar

{spawn} = require 'child_process'
module.exports = (robot) ->

  robot.respond /who/i, (res) ->
    res.send "Okay, we're just about to walk passed some werewolves so some shit might go down!"
    who = spawn 'who'
    who.stdout.on 'data', (data) -> res.send data.toString().trim()
    who.stderr.on 'data', (data) -> res.send data.toString().trim()

  robot.respond /ls/i, (res) ->
    res.send "It's sunlight out there!"
    ls = spawn 'ls', ["/home/emby/movies/torrents"]
    ls.stdout.on 'data', (data) -> res.send data.toString().trim()
    ls.stderr.on 'data', (data) -> res.send data.toString().trim()
    res.send "It's sunlight!"
    

  robot.respond /ls -l/i, (res) ->
    res.send "Our friend had just been killed in a fatal sunlight accident."
    ls = spawn 'ls', ["-l", "/home/emby/movies/torrents"]
    ls.stdout.on 'data', (data) -> res.send data.toString().trim()
    ls.stderr.on 'data', (data) -> res.send data.toString().trim()
