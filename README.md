# Machine Statistics Collection System

## Overall Objective

Implements architecture and design of a network based machine statistics collection system.

## Functional Requirements

The system allows collection of machine statistics in an intranet environment. The system implements the
following specifications.
### Client Script
1. This script will be uploaded and executed to 100s of machines in the intranet. These machines are meant to be monitored for system level statistics like memory usage, CPU usage, total uptime and windows security event logs (in case of windows OS).
2. When executed, the client script collects the statistics and return them to the server script for cumulation.
3. The client script must encrypt the data before returning it to server.
### Server Script
1. Installed on a single central machine in the same intranet.
2. Each client is configured in a server config xml file something like this
	<client ip=’127.0.0.1’ port=’22’ username=’user’ password=’password’ mail="asa@asda.com">
		<alert type="memory" limit="50%" />
		<alert type="cpu" limit="20%" />
	</client>
3. When executed, the server script should connect to each client using ssh, upload the client script in a temp directory, execute it and get the response.
4. After receiving the response from the client script, server script should decode it and stores it into a relational database along with client ip. This collected data is consumed by another application, that is out of scope, but you may design the database table yourself.
5. The server based upon the "alert" configuration of each client sends a mail notification. The notification is sent to the client configured email address using SMTP. Use a simple text mail format with some detail about the alert. event logs must be sent via email every time without any condition.

## Other Technical and Non-functional Requirements

- Paramiko has been used for ssh communication.
- Win32api has been used for statistics.
- SMTP ie smtplib has been used to send emails. 
- Pycrypto has been used for encryption purposes.

## Running 

### Requirements

- Python 2.7
- Make sure you have pip (pip --version)
- Pip install virtualenv to install virtual environment
- Virtualenv wrapper
- Git 

Clone the repository into a directory of your own choice.

`git clone https://github.com/SamwelOpiyo/machine_statistics_collection_system.git`
`cd machine_statistics_collection_system`

Then, to run:

- `mkvirtualenv machine_statistics` create a virtual environment
- Install requirements: `pip install -r /Source/requirements.txt` (you almost certainly want to do this in a virtualenv).
- Create Database: `python Create_Database.py`
- Start the ssh service in Linux: `systemctl start ssh`
- Run the System: `python Server_Script.py`
