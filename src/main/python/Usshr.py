#!/usr/bin/python
# Usshr - A simple script to play media on the RaspberryPi over SSH.
# Credits: Jay Yeo - github.com/jay-yeo

import os
import re
import paramiko

# SSH Connection Class
class Connection:

    # Constructor
    def __init__(self, hostname, portNum, username, password):
        self.host = hostname
        self.port = portNum
        self.user = username
        self.pwd = password


# SSH Messaging Functions Class
class Messenger:

    # Initialization
    def __init__(self, Connection):
        self.Connection = Connection

    # Send message
    def send(self, message):

        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.WarningPolicy)

            client.connect(self.Connection.host, port=self.Connection.port, username=self.Connection.user, password=self.Connection.pwd)

            # Send SSH Command
            stdin, stdout, stderr = client.exec_command(message)

        except:
            print('Fuck!')

        client.close()

    # Send message and return reply
    def sendReply(self, message):

        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.WarningPolicy)

            client.connect(self.Connection.host, port=self.Connection.port, username=self.Connection.user, password=self.Connection.pwd)

            # Send SSH Command
            stdin, stdout, stderr = client.exec_command(message)
            reply = stdout.readlines()

            return reply
        except:
            print('Fuck!')

        client.close()


# Player Class
class Player:

    # Initialization
    def __init__(self, Connection, mediaDirectory):
        # Connection Details
        self.cnx = Connection
        self.dir = mediaDirectory
        self.messenger = Messenger(self.cnx)
        self.playlist = []

    def playback(self):
        print("Usshr - Theatre")
        print('------------------')

        command = ""

        # Start a loop that runs until the user enters the value for 'quit'.
        while command != 'q':

            # Give all the choices in a series of print statements.
            print('[x] Start Projector')
            print('[l] List Movies')
            print('[q] Quit')
            print("")

            # Ask for the user's choice.
            command = input('Enter Command: ')
            if command == 'l':

                self.listMovies()

            # Play Movies
            elif command == 'x':
                movieInput = input('Enter Movie: ')

                for movie in self.playlist:
                    if str(movie["id"]) == movieInput:
                        print("Starting " + str(movie["movieFile"]) + " ...")
                        self.play(movie["movieURI"])
                    else:
                        print("Invalid Movie ID. Try again!")

            # Quit
            elif command == 'q':
                print('Goodbye!')
                break
            # Incorrect Command
            else:
                print('Incorrect Command')

    # Play Function
    def play(self, videoURL):

        play_string = 'omxplayer --no-keys -o hdmi -b ' + '"' + str(videoURL) + '" &'
        self.messenger.send(play_string)
        self.playbackControls()

    # Terminal Playback Controls
    def playbackControls(self):

        # Give the user some context.
        print('------------------')
        print('Playback Controls:')

        # Set an initial value for choice other than the value for 'quit'.
        command = ""

        # Start a loop that runs until the user enters the value for 'quit'.
        while command != "q":

            # Command choices
            print("[p] Pause")
            print("[q] Quit")

            # Ask for user choice
            command = input("\nEnter Command: ")

            # Respond to user choice
            if command == "p":
                self.messenger.send("dbuscontrol.sh pause")
                print("Pausing Playback\n")
            elif command == "q":
                self.messenger.send("pkill omxplayer")
                print("Goodbye!\n")
            else:
                print("Incorrect Command\n")

    # List Movies
    def listMovies(self):

            # Clear old list data
            self.playlist.clear()

            # Get directory list
            list_string = "ls " + self.dir + " *.mkv *.mp4"
            movie_list = self.messenger.sendReply(list_string)

            # Get list of video files
            for index, movie in enumerate(movie_list):
                if index > 0:
                    movieDetails = {"id": index, "movieURI": re.sub('\n', '', movie), "movieFile": os.path.basename(re.sub('\n', '', movie))}
                    self.playlist.append(movieDetails)

            # Display list of video files
            print('\nAll Movies:')
            for movie in self.playlist:
                outputString = str(movie["id"]) + ": " + movie["movieFile"]
                print(outputString)

            print('\n------------------')
            return self.playlist


# Run Script
if __name__ == "__main__":

    # CONFIG - Add your device authorization details
    host = "192.168.0.87"
    port = 22
    user = "pi"
    password = "Budap3st1!"

    # New connection to RaspberryPi
    deviceConnection = Connection(host, port, user, password)
    mediaDirectory = "/home/pi/Videos"

    # Start playback
    Player(deviceConnection, mediaDirectory).playback()

