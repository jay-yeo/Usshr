# Usshr

A simple script to play and control media on the RaspberryPi over SSH.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. Before you get started, make sure you have SSH running on the Raspberry Pi and have your access credentials ready.  

### Prerequisites
Installed on Raspbian is a command line media player, called OMXPlayer. 

First check to see if OMXPlayer is installed:

   ```omxplayer --version```

As of Raspian(Wheezy), OMXPlayer comes pre-bundled, however, for systems running older versions of Raspian, you may install OMXPlayer using the following command:

```sudo apt-get install omxplayer```

Lastly, please make sure the following python packages have been installed:

`sudo pip install paramiko`


### Installing

To install, zip or clone the project to a directory of your choice.

Using your favourite text editor, please open `Usshr.py` and edit the file to include your SSH access credentials.

```
# CONFIG - Add your device authorization details
    host = "192.168.0.1"
    port = 22
    user = "pi"
    password = "password"    
```

Usshr has been configured to use the default `/home/pi/Videos` directory to search for video files. To change this to a custom directory, please edit the following line of code:


```
# Directory containing media files
mediaDirectory = "/your/custom/directory"
```

## Using Usshr

Inside your deployed directory, enter the following command in the terminal to start Usshr script:

```python3 Usshr.py```

The script will launch in the terminal with the main menu. Functions and playback controls can be accessed using basic keystrokes from the terminal.

```
Usshr - Theatre
------------------
[x] Start Projector
[l] List Movies
[q] Quit

Enter Command:
```

## Built With

* [paramiko](http://www.paramiko.org/) - A Python implementation of SSHv2. 

## Authors

* **Jay Yeo** - *Initial work* - [jay-yeo](https://github.com/jay-yeo)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.