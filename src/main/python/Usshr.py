#!/usr/bin/python
# Usshr - A simple script to play media on the RaspberryPi over SSH.
# Credits: Jay Yeo - github.com/jay-yeo


import os
import re
import paramiko


# SSH Connection Class
class Connection:

    # Initialization
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
            print('ERROR: Message Not Sent!')

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
            print('ERROR: Message Not Sent!')

        client.close()


# Player Class
class Player:

    # Initialization
    def __init__(self, Connection, mediaDirectory):
        # Connection Details
        self.cnx = Connection
        self.directory = mediaDirectory
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

            # List all playable media files in mediaDirectory
            if command == 'l':

                self.listMovies()

            # Play Movie
            elif command == 'x':
                self.playMovie()

            # Quit
            elif command == 'q':
                print('Goodbye!')
                break
            # Incorrect Command
            else:
                print('Incorrect Command')

    # Play Function
    def play(self, videoURI):
        play_string = 'omxplayer --no-keys -o hdmi -b ' + '"' + str(self.directory + videoURI) + '" &'
        self.messenger.send(play_string)
        self.playbackControls()

    # Playback Controls
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
            list_string = "ls " + self.directory + " *.mkv *.mp4 *.avi *.mov .m4v"
            movie_list = self.messenger.sendReply(list_string)

            if movie_list:
                # Get list of video files
                for index, movie in enumerate(movie_list):
                    # Skip first entry which is the directory url - eg. "/home/pi/Videos"
                    if index > 0:
                        movieDetails = {"id": index, "movieURI": re.sub('\n', '', movie), "movieFile": os.path.basename(re.sub('\n', '', movie))}
                        self.playlist.append(movieDetails)

            # Display list of video files
            print('\nAll Movies:')
            if len(self.playlist) > 0:
                for movie in self.playlist:
                    outputString = str(movie["id"]) + ": " + movie["movieFile"]
                    print(outputString)
            else:
                print("No playable files in directory...")

            print('\n------------------')

    def playMovie(self):
        playable = False
        movieFile = ""
        movieInput = input('Enter Movie: ')

        for movie in self.playlist:
            if str(movie["id"]) == movieInput:
                movieFile = movie["movieURI"]
                playable = True

        if playable == True:
            print("\nStarting " + str(movieFile) + " ...")
            self.play(movieFile)
        else:
            print("Sorry, invalid movie selection. Try again!\n")

# Run Usshr Script
if __name__ == "__main__":

    # CONFIG - Add your device authorization details
    host = "192.168.0.1"
    port = 22
    user = "pi"
    password = "password"

    # New connection to RaspberryPi
    deviceConnection = Connection(host, port, user, password)

    # Directory containing media files
    mediaDirectory = "/home/pi/Videos"

    # Start playback
    Player(deviceConnection, mediaDirectory).playback()

