#!/usr/bin/python2.7
#
# Copyright (c) 2014 deathspawn
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#

# Import the necessary modules.
import os, mpd, time, random, itertools, sys, urllib2
from xml.dom import minidom

# Configurations for calling later...
api_folder = ".mpdcontrol"
# Not the same as the git README.md.
api_readme = "README"
# Config file.
api_config = "main.conf"
# Define working directory here. Default is .deathspawn.
configfolder = os.path.expanduser("~/")+"/.deathspawn/"+api_folder+"/"

readmefile = configfolder+api_readme
configfile = configfolder+api_config
confexamplefile = configfile+".example"

# Readme
# This is a different Readme from the Github version.
readmeversion = "1"
readmelist = ["version = "+readmeversion,
"""Coming soon."""]

configversion = "2"
exampleconfig = ["version = "+configversion,
"""# The line above is for internal version checks. Removing it will regenerate the conf.example only. This doesn't apply to the .conf.

# Random song limit. If you feel like killing your mpd server, raise this number.

randomlimit = 50

# If you plan on using the %albumwrap% variable, you can set the length here.

albumlength = 15

# Format Variables:
# %artist% = Artist
# %album% = Album
# %albumwrap% = Album shortened as defined by albumlength.
# %title% = Title

format = Listening to: %artist% - %title%
notplaying = Not listening to anything!

server = localhost
port = 6600
password = hackme

# If you are like me and have another mpd session up, define it here.
# This isn't functional yet.

enabled = False
server2 = localhost
port2 = 6601
password2 = hackmetoo"""]

# Argument catcher.
try:
    arguments = sys.argv[1]
except IndexError:
    exit("Error: Run "+sys.argv[0]+" -h for help.")

# Check to see if the config folder exists.
if not os.path.exists(configfolder):
    print "Making configuration folder at "+configfolder
    # Make the folder...
    os.makedirs(configfolder)

# Check to see if the readme exists.
if os.path.exists(readmefile):
    readmeopen = open(readmefile, "r")
    readmecheck = readmeopen.readline()
    readmeopen.close()
    # Version check.
    if readmecheck != "version = "+readmeversion+"\n":
        updatereadme = True
    else:
        updatereadme = False
else:
    updatereadme = True

# Make or remake readme.
if updatereadme == True:
    readmefilemake = open(readmefile, "w")
    for i in readmelist:
        readmefilemake.write(i+"\n")
    readmefilemake.close()

# If config doesn't exist, make it. No version check here, so your changes don't get overwritten.
if not os.path.exists(configfile):
    configfilemake = open(configfile, "w")
    for i in exampleconfig:
        configfilemake.write(i+"\n")
    configfilemake.close()

# Check to see if the config example exists
if os.path.exists(confexamplefile):
    exampleopen = open(confexamplefile, "r")
    examplecheck = exampleopen.readline()
    exampleopen.close()
    # Version check.
    if examplecheck != "version = "+configversion+"\n":
        updateconfig = True
    else:
        updateconfig = False
else:
    updateconfig = True

# Update the config if needed.
if updateconfig == True:
    examplefilemake = open(confexamplefile, "w")
    for i in exampleconfig:
        examplefilemake.write(i+"\n")
    examplefilemake.close()

# Used to get a config option.
def get_config(variable):
    config = open(configfile, "r")
    configlist = config.readlines()
    config.close()
    for i in configlist:
        try:
            splitpea = i.split(" = ")
        except IndexError:
            pass
        if splitpea:
            if splitpea[0] == variable:
                value = splitpea[1].rstrip("\n")
    return value

# MPD Connect function. Requires a server and port.
def mpd_connect(mpdserver, mpdport):
    mpd_client = mpd.MPDClient()
    mpd_client.connect(mpdserver, mpdport)
    return mpd_client

# First Check NP function.
def check_np():
    server = get_config("server")
    port = get_config("port")
    password = get_config("password")
    client = mpd_connect(server, port)
    if password != "None":
        client.password(password)
    nowplaying = client.currentsong()
    status = client.status()
    stats = client.stats()
    client.disconnect()
    return nowplaying, status, stats

# 2nd Check NP function.
def check_np2():
    server = get_config("server2")
    port = get_config("port2")
    password = get_config("password2")
    client = mpd_connect(server, port)
    if password != "None":
        client.password(password)
    nowplaying = client.currentsong()
    status = client.status()
    stats = client.stats()
    client.disconnect()
    return nowplaying, status, stats

# Random song function. Adds a # of songs.
def random_song(number):
    server = get_config("server")
    port = get_config("port")
    password = get_config("password")
    client = mpd_connect(server, port)
    client.password(password)
    songlist = client.list('file')
    for _ in itertools.repeat(None, number):
        songchoice = random.choice(songlist)
        client.add(songchoice)
        print "Added \""+songchoice+"\" to the playlist."
    client.disconnect()

# Internal commands can go here.
if arguments.find("h") != -1:
    print """
          -h - Prints this help output.
          -p - Prints the now playing info.
          -r # - Adds a number of random songs to the playlist. See config for cap option.
          -d - Debug. Prints the raw output for check_np()
    """
    exit(0)
# Any code that doesn't support multiple flags should end in an exit(0) and be before the multi-flag code.
if arguments.find("r") != -1:
    try:
        randomsongs = int(sys.argv[2])
    except IndexError:
        exit("Error: Run "+sys.argv[0]+" -h for help.")
    except ValueError:
        exit("Error: Run "+sys.argv[0]+" -h for help.")
    if randomsongs <= int(get_config("randomlimit")):
        random_song(randomsongs)
    else:
        exit("Error: Value is higher than randomlimit in config.")
if arguments.find("p") != -1:
    # Get some configuration items.
    albumlength = int(get_config("albumlength"))
    npstring = get_config("format")
    # Get information from servers.
    npquery = check_np()
    # Check if Server 2 is used.
    if get_config("enabled") == True:
        npquery2 = check_np2()
        npinfo2 = npquery2[0]
        status2 = npquery2[1]
    else:
        npinfo2 = ""
        status2 = ""
    npinfo = npquery[0]
    status = npquery[1]
    artist = npinfo.get("artist", "Unknown Artist")
    album = npinfo.get("album", "Unknown Album")
    albumwrap = (album[:15] + '...') if len(album) > 15 else album
    title = npinfo.get("title", "Unknown Title")
    # Replace the npstring variables.
    reply = npstring.replace("%artist%", artist).replace("%album%", album).replace("%albumwrap%", albumwrap).replace("%title%", title)
    if status.get("state", "Unknown") != "play":
        print get_config("notplaying")
    else:
        print reply
if arguments.find("d") != -1:
    npquery = check_np()
    print npquery