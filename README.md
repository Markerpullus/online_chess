# online_chess
An online chess game made with pygame and socket that can be played on a single computer or across multiple computers on the same local area network

--IMPORTANT--
You can customize the server ip and port in the imports/ip.py file. If you are running the server and the players on the same computer, just set the "server_ip" equal to "127.0.0.1"(set by default). If you are playing across multiple devices, set the "server_ip" to the private ip address of the computer that you wish to be the server computer, which you can get by typing "ipconfig" in terminal on windows or "ifconfig" on unix-based OS's. A minimum of two computers is required for online mode to work.

--WARNING--
In order for this game to work across computers, make sure that your firewall if set to not block connections from private network. I have experienced this and found out about it.
