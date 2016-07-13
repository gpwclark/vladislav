#Description:
#   Prints out this month's ASCII calendar.
#
# Commands:
#   hubot calendar [me] - Print out this month's calendar

{spawn} = require 'child_process'
module.exports = (robot) ->

  robot.respond /who/i, (res) ->
    who = spawn 'who'
    who.stdout.on 'data', (data) -> res.send data.toString().trim()
    who.stderr.on 'data', (data) -> res.send data.toString().trim()
