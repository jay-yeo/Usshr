#!/usr/bin/python
# Usshr - A simple script to play media on the RaspberryPi over SSH.
# Credits: Jay Yeo - github.com/jay-yeo

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

# SSH Messaging Functions Class
class Messenger:

    # Constructor
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

            print('Command Sent!')
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

            print('Command Sent!')
            return reply
        except:
            print('Fuck!')

        client.close()


# Player Class
class Player:

    # Constructor
    def __init__(self, Connection):
        # Connection Details
        self.cnx = Connection
        self.messenger = Messenger(self.cnx)


    # Play Function
    def play(self, videoURL):

        #play_string = 'omxplayer --no-keys -o hdmi -b ' + '"' + str(videoURL) + '" &'
        self.messenger.send(videoURL)
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
            command = input("Command: ")

            # Respond to user choice
            if command == "p":
                self.messenger.send("dbuscontrol.sh pause")
                print("Pausing Playback")
            elif command == "q":
                self.messenger.send("pkill omxplayer")
                print("Goodbye!")
            else:
                print("Incorrect Command")

#Run Script
if __name__ == "__main__":
    print("Usshr - Theatre")

    # CONFIG - Add your device authorization details
    host = "192.168.0.87"
    port = 22
    user = "pi"
    password = "Budap3st1!"

    piConnection = Connection(host, port, user, password)

    Player(piConnection).play("video")

    # Start a loop that runs until the user enters the value for 'quit'.
    # while command != 'q':
    #
    #     # Give all the choices in a series of print statements.
    #     print('[x] Start Projector')
    #     print('[l] List Movies')
    #     print('[q] Quit')
    #
    #     # Ask for the user's choice.
    #     command = input('Command: ')
    #
    #     # List Movies
    #     if command == 'l':
    #         list_string = "find *.mkv *.mp4 /media/pi/VIDEO/ "
    #         movie_list = sshMessenger(cxDetails, list_string,reply=True)
    #         print('All Movies:')
    #         if '.mkv' or '.mp4' in movie_list:
    #         for movie in movie_list:
    #             print(movie)
    #         print(movie_list)
    #     # Play Movies
    #     elif command == 'x':
    #         movie = raw_input('Enter Movie: ')
    #         print('Starting "' + str(movie) + '"')
    #         play(movie)
    #         playbackCTRL()
    #     # Quit
    #     elif command == 'q':
    #         print('Goodbye!')
    #         break
    #     # Incorrect Command
    #     else:
    #         print('Incorrect Command')