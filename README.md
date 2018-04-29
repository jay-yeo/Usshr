# Usshr

**A simple script to play and control media on the RaspberryPi over SSH.**

<p>The script opens a simple commandline interface and allows you to play and control media on your RaspberryPi. This basic script if perfect for situations where you need to remotely control content playing via the RaspberryPi.<p>

**Installation + Configuration**
<p>To install, zip or clone the project to a directory of your choice.</p> 
<p>Using your favourite text editor, please open `Usshr.py` and edit the file to include your access credentials inside `if __name__ == "__main__"`.</p>

```
# CONFIG - Add your device authorization details
    host = "192.168.0.1"
    port = 22
    user = "pi"
    password = "password"    
```
Usshr has been configured to use the default `/home/pi/Videos` directory to search for video files. To change this to a custom directory, please edit the following line of code:

```
mediaDirectory = "/your/custom/directory"
```

<p>Finally, please check that the following python packages have been installed:
<br>`sudo pip install paramiko`</p>