#Description:
#   Prints out this month's ASCII calendar.
#
# Commands:
#   hubot calendar [me] - Print out this month's calendar

#TODO how do i trigger the action to move the fucking file once it has been
#downloaded?
#I also don't know how to figure out if it has even finished copying yet.
#the program will also need to quit once it has finished copying.
{spawn} = require 'child_process'
HubotSlack = require 'hubot-slack'

module.exports = (robot) ->

  regex = /awaken the beast (.*) has been (.*)/i
  robot.listeners.push new HubotSlack.SlackBotListener robot, regex, (res) ->
    filename = res.match[1]
    python = spawn 'python', ['scripts/theBeast.py', "#{filename}", process.env.IFTTT_API_KEY]
    python.stdout.on 'data', (data) -> res.send data.toString().trim()
    python.stderr.on 'data', (data) -> res.send data.toString().trim()
    res.send "\nThe darkest part of my mind is reserved to The Beast."

  robot.respond /open the (.*) doors/i, (res) ->
    doorType = res.match[1]
    if doorType is "pod bay"
      res.reply "I'm afraid I can't let you do that."
    else
      res.reply "Opening #{doorType} doors"
