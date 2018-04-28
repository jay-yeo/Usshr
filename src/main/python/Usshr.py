#!/usr/bin/python
# Usshr - A simple script to play media on the RaspberryPi over SSH.
# By Jay Yeo - github.com/jay-yeo

import os
import paramiko

# SSH Connection Class
class Connection:

    # Constructor
    def __init__(self, hostname, portNum, username, password):
        self.host = hostname
        self.port = portNum
        self.user = username
        self.pwd = password


# SSH Message Transport
def sshMessenger(Connection, message, reply):

    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)

        client.connect(Connection.host, port=Connection.port, username=Connection.user, password=Connection.pwd)

        # Send SSH Command
        stdin, stdout, stderr = client.exec_command(message)

        # Terminal Reply
        if reply == True:
            reply = stdout.readlines()
            return reply

        print('Command Sent!')
    except:
        print('Fuck!')

    client.close()


# Play Function
def play(video):

    video_dir = '/media/pi/VIDEO/YouTube/'
    video_url = video_dir + video

    play_string = 'omxplayer --no-keys -o hdmi -b ' + '"' + str(video_url) + '" &'
    return sshMessenger(play_string,reply=False)

# Terminal Playback Controls
def playbackCTRL():

    # Give the user some context.
    print('------------------')
    print('Playback Controls:')

    # Set an initial value for choice other than the value for 'quit'.
    command = ''

    # Start a loop that runs until the user enters the value for 'quit'.
    while command != 'q':

        # Command choices
        print('[p] Pause')
        print('[q] Quit')

        # Ask for user choice
        command = raw_input('Command: ')

        # Respond to user choice
        if command == 'p':
            sshMessenger('dbuscontrol.sh pause', reply=False)
            print('Pausing Playback')
        elif command == 'q':
            sshMessenger('pkill omxplayer',reply=False)
            print('Goodbye!')
        else:
            print('Incorrect Command')

#Run Script
if __name__ == '__main__':
    print('PiTube - Theatre')

    # CONFIG - Add your details
    host = "localhost"
    port = 22
    user = "yourUsername"
    password = "yourPassword"

    cxDetails = Connection(host, port, user, password)

    command = ''

    # Start a loop that runs until the user enters the value for 'quit'.
    while command != 'q':

        # Give all the choices in a series of print statements.
        print('[x] Start Projector')
        print('[l] List Movies')
        print('[q] Quit')

        # Ask for the user's choice.
        command = raw_input('Command: ')

        # List Movies
        if command == 'l':
            list_string = "find *.mkv *.mp4 /media/pi/VIDEO/ "
            movie_list = sshMessenger(cxDetails, list_string,reply=True)
            print('All Movies:')
            if '.mkv' or '.mp4' in movie_list:
            for movie in movie_list:
                print(movie)
            print(movie_list)
        # Play Movies
        elif command == 'x':
            movie = raw_input('Enter Movie: ')
            print('Starting "' + str(movie) + '"')
            play(movie)
            playbackCTRL()
        # Quit
        elif command == 'q':
            print('Goodbye!')
            break
        # Incorrect Command
        else:
            print('Incorrect Command')