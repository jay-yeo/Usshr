# Usshr

A simple script to play and control media on the RaspberryPi over SSH.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. Before you get started, make sure you have SSH running on the Raspberry Pi and have your access credentials ready.  

### Prerequisites

Please check that the following python packages have been installed:
<br>`sudo pip install paramiko`


### Installing

To install, zip or clone the project to a directory of your choice.
<br><br>Using your favourite text editor, please open `Usshr.py` and edit the file to include your access credentials inside `if __name__ == "__main__"`.

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

Inside your deployed directory, enter the following command in the terminal:
<br>```python3 Usshr.py```

## Built With

* [paramiko](http://www.paramiko.org/) - A Python implementation of SSHv2. 

## Authors

* **Jay Yeo** - *Initial work* - [jay-yeo](https://github.com/jay-yeo)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* The Great Architect of the Universe
