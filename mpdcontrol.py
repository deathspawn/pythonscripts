#!/usr/bin/python3
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
import os, time, random, itertools, sys, logging, mpd
from xml.dom import minidom
from dateutil.relativedelta import relativedelta as rd
from configparser import RawConfigParser

# Configurations for calling later...
api_folder = "mpdcontrol"
# Config file.
api_config = "mpdcontrol.ini"
# Log file.
api_log = "mpdcontrol.log"
# Example file.
api_example = "example.ini"
# TODO: XDG_CONFIG_HOME environ
try:
    homedir = os.environ['XDG_CONFIG_HOME']
except KeyError:
    try:
        homedir = os.environ['HOME']
    except KeyError:
         homedir = os.path.expanduser("~")
# Define working directory here. Default is .deathspawn.
configfolder = homedir+"/.config/"+api_folder+"/"

configfile = configfolder+api_config
confexamplefile = configfolder+api_example
logfile = configfolder+api_log

# Thanks Stack Overflow.
class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

configversion = "4"
exampleconfig = """[version]
version = {version}
; The line above is for internal version checks. Removing it will regenerate the
; conf.example only. This doesn't apply to the .conf.

[format]
; Format Variables:
; {artist} = Artist
; {album} = Album
; {albumwrap} = Album shortened as defined by albumlength.
; {title} = Track title
; {elapsed} = Current position in song. Outputs as H:M:S if duration is an hour
;             or more. Outputs M:S if duration is under an hour.
; {duration} = Total time. Works the same as elapsed on output.
; {date} = Album date.
; {bitrate} = Outputs the bitrate as a number. You can add kbps after this tag.
; {khz} = Outputs khz as a number. Add khz after the tag if you want.
; {bits} = Outputs the bit as a number. Add -bit if you want.
; {channel} = Outputs the channels as a number. Add channels if you want.
; {extension} = File format. Gets from the file extension. May not work if
;            extension is missing.
; Warning! If you plan on using {}, please double them up like so: {{{extension}}} outputs to {flac} for example.
format = NP: {artist} - {title} ({album}) [{elapsed}/{duration}] ({date}) {{{bitrate}kbps | {khz}khz:{bits}-bit:{channels}-channel | {extension}}} ~MPDControl~
; If the album and artist are unknown, this will be a fallback. Shoutcast MP3
; streams often don't have an album/artist tag.
alternate = NP: {title}
notplaying = Not listening to anything!
; If you plan on using the %albumwrap% variable, you can set the length here.
albumlength = 15

; This is currently out of order!
[random]
; Random song limit. If you feel like killing your mpd server, raise this
; number.
randomlimit = 50

; You can add an infinite amount of servers. Just follow the same outline below.
; You could also name them, just don't use format or random. :)
; !! Please set a password on your server if you want to use this script. At the
; moment, there is no support for an empty password. Support may come in a later
; version.

[default]
server = 127.0.0.1
port = 0
password = hackme

[second]
server = 192.168.1.2
port = 0
password = hackme2""".replace("{version}", configversion)

# Argument catcher.
try:
    option = sys.argv[1]
except IndexError:
    exit("Error: Run "+sys.argv[0]+" help for help.")
try:
    servername = sys.argv[2]
except:
    servername = None

# Check to see if the config folder exists.
if not os.path.exists(configfolder):
    print("Making configuration folder at "+configfolder)
    # Make the folder...
    os.makedirs(configfolder)

# Make log file if it doesn't exist.
if not os.path.exists(logfile):
    open(logfile, 'a').close()

# Setup logger.
logger = logging.getLogger('mpdcontrol')
hdlr = logging.FileHandler(logfile)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
# Change log level here if needed.
logger.setLevel(logging.WARNING)

# Check to see if the config example exists
if os.path.exists(confexamplefile):
    parser = RawConfigParser()
    parser.read(confexamplefile)
    examplecheck = parser.get("version", "version")
    # Version check.
    if examplecheck != configversion:
        updateconfig = True
    else:
        updateconfig = False
else:
    updateconfig = True

# Update the config if needed.
if updateconfig == True:
    with open(confexamplefile, "w") as examplefilemake:
        for i in exampleconfig:
            examplefilemake.write(i)

# Used to get a config option.
def get_config(section, variable):
    parser = RawConfigParser()
    parser.read(configfile)
    return parser.get(section, variable)

# MPD Connect function. Requires a server and port.
def mpd_connect(mpdserver, mpdport):
    mpd_client = mpd.MPDClient()
    mpd_client.connect(mpdserver, mpdport)
    return mpd_client

# First Check NP function.
def check_np(server, port, password):
    client = mpd_connect(server, port)
    if password != "None":
        client.password(password)
    nowplaying = client.currentsong()
    status = client.status()
    stats = client.stats()
    client.disconnect()
    return nowplaying, status, stats


# Random song function. Adds a # of songs.
def random_song(number, server, port, password):
    client = mpd_connect(server, port)
    client.password(password)
    songlist = client.list('file')
    for _ in itertools.repeat(None, number):
        songchoice = random.choice(songlist)
        client.add(songchoice)
        print("Added \""+songchoice+"\" to the playlist.")
    client.disconnect()

# The good stuff.
try:
    if option.lower() == "help":
        print(
"""help - Prints this help output.
np <server> - Prints the now playing info. Include the name for the server according to the config.
nowplaying <server> - Same as np.
random <server> <number> - Out of order. Connection failures. :(
stats <server> - Prints stats for mpd database.
debug <server> - Debug. Prints the raw output for check_np()

Config directory is located at \""""+configfolder+"\".")
    elif option.lower() == "random":
        print("Out of order.")
#         if servername == None:
#             print("Missing server name. Error: Run "+sys.argv[0]+" help for help.")
#         else:
#             server = get_config(servername, "server")
#             port = get_config(servername, "port")
#             password = get_config(servername, "password")
#             try:
#                 randomsongs = int(sys.argv[3])
#             except IndexError:
#                 exit("Error: Run "+sys.argv[0]+" help for help.")
#             except ValueError:
#                 exit("Error: Run "+sys.argv[0]+" help for help.")
#             if randomsongs <= int(get_config("random", "randomlimit")):
#                 random_song(randomsongs, server, port, password)
#             else:
#                 exit("Error: Value is higher than randomlimit in config.")
    elif option.lower() == "np" or option.lower() == "nowplaying":
        if servername == None:
            print("Missing server name. Error: Run "+sys.argv[0]+" help for help.")
        else:
            server = get_config(servername, "server")
            port = get_config(servername, "port")
            password = get_config(servername, "password")
            albumlength = int(get_config("format", "albumlength"))
            npquery = check_np(server, port, password)
            npinfo = npquery[0]
            status = npquery[1]
            artist = npinfo.get("artist", "Unknown Artist")
            album = npinfo.get("album", "Unknown Album")
            albumwrap = (album[:15] + '...') if len(album) > 15 else album
            title = npinfo.get("title", "Unknown Title")
            bitrate = status.get("bitrate", "?")
            audioraw = status.get("audio", "?")
            filepath = npinfo.get("file", "?.unknown")
            try:
                filename, fileextension = os.path.splitext(filepath)
            except:
                fileextension = ".unknown"
            extension = fileextension.lstrip(".")
            if audioraw != "?":
                audiolist = audioraw.split(":")
                audiochannels = audiolist[2]
                audiobits = audiolist[1]
                audiokhz = audiolist[0]
            else:
                audiochannels = audioraw
                audiobits = audioraw
                audiokhz = audioraw
            durationsec = int(float(status.get("duration", "0")))
            if durationsec <= 3599:
                duration = time.strftime('%M:%S', time.gmtime(durationsec))
            else:
                duration = time.strftime('%H:%M:%S', time.gmtime(durationsec))
            elapsedsec = int(float(status.get("elapsed", "0")))
            if durationsec <= 3599:
                elapsed = time.strftime('%M:%S', time.gmtime(elapsedsec))
            else:
                elapsed = time.strftime('%H:%M:%S', time.gmtime(elapsedsec))
            date = npinfo.get("date", "?")
            if album != "Unknown Album" and artist != "Unknown Artist":
                npstring = get_config("format", "format")
                reply = npstring.format_map(SafeDict(artist=artist, album=album, albumwrap=albumwrap, title=title, bitrate=bitrate, duration=duration, elapsed=elapsed, extension=extension, date=date, bits=audiobits, khz=audiokhz, channels=audiochannels))
            else:
                npstring = get_config("format", "alternate")
                reply = npstring.format_map(SafeDict(artist=artist, album=album, albumwrap=albumwrap, title=title, bitrate=bitrate, duration=duration, elapsed=elapsed, extension=extension, date=date, bits=audiobits, khz=audiokhz, channels=audiochannels))
            if status.get("state", "Unknown") != "play":
                print(get_config("format", "notplaying"))
            else:
                print(reply)
    elif option.lower() == "stats":
        if servername == None:
            print("Error: Missing server name. Run "+sys.argv[0]+" help for help.")
        else:
            server = get_config(servername, "server")
            port = get_config(servername, "port")
            password = get_config(servername, "password")
            npquery = check_np(server, port, password)
            stats = npquery[2]
            songs = stats.get("songs")
            artists = stats.get("artists")
            albums = stats.get("albums")
            playtime = stats.get("db_playtime")
            fmt = '{0.days} days, {0.hours} hours, {0.minutes} minutes, {0.seconds} seconds'
            human_playtime = fmt.format(rd(seconds=int(playtime)))
            human_playtime = str(human_playtime)
            print("MPD Database Stats: "+songs+" songs, "+artists+" artists, "+albums+" albums. Total Playtime: "+human_playtime+".")
    elif option.lower() == "debug":
        if servername == None:
            print("Error: Missing server name. Run "+sys.argv[0]+" help for help.")
        else:
            server = get_config(servername, "server")
            port = get_config(servername, "port")
            password = get_config(servername, "password")
            npquery = check_np(server, port, password)
            print(npquery)
except:
    if not os.path.exists(configfile):
        print("Please make a "+api_config+" in \""+configfolder+"\". There is a "+api_example+" provided for you there.")
    else:
        logger.error("We have a problem...", exc_info=1)
        print("Error: This has been logged to \""+logfile+"\". Run "+sys.argv[0]+" help for help.")
