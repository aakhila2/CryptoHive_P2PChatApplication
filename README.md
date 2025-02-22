# Peer-To-Peer Chat Application

## Team Details 

Team Name : **CryptoHive**

Team Members : 
- Akella Akhila, 230001005, CSE
- Kommireddy Jayanthi, 230001041, CSE
- Parimi Sunitha, 230001061, CSE

## Introduction

Peer-to-Peer (P2P) Chat Application enables simultaneous sending and receiving of messages between multiple peers using TCP. The program supports querying and retrieving a list of peers with which a node has communicated. Multiple instances of the program can be run in separate terminal environments to form a P2P chat network.

## Features

- Simultaneous sending and receiving of messages using threads.

- Both server and client functionalities on the same port.

- Maintains a list of active and previously connected peers.

- Query active peers.

- View complete chat history for each node.

- Supports dynamic runtime configuration of IP addresses and ports.

## Execution 

Tip: Opening several terminal windows to run multiple instances of the program helps with a better visual of the peer-to-peer functionality.

### Initialising

- You give a port number and your team name. Team name is used when a message is sent to other peers, and port number is used in all the specified operations.

- After you input your team name and port number, mandatory messages are sent to 2 sets of IP addresses and ports :

     IP: 10.206.4.122, PORT : 1255
     IP: 10.206.5.228, PORT : 6555
  
- Then, you will see a menu with 5 different options. Below, we explain each option in detail.

  Menu : 
1. Send message
2. Query active peers
3. Connect to active peers
4. View chat history
 0. Quit

### ✉️Send Message

- You send a message by choosing **1** from the menu.

- Then, you should enter the receipent's IP address and port number; and then type your message. You'll get the output "message sent successfully" along with the receipent's IP and port number.

- Your message to the receipent looks in this format :

  <IP ADDRESS:PORT> <team name> <your message>

- Here our client by default depends on ephemeral port, hence our client port will be some random number which will be printed in continuition to the format mentioned above.

- From that received message, we will extract sender's IP address, port number, message, team name.

- When a peer, say **peer1** sends a message to another peer, say **peer2** then **peer2 will recognize peer1 as an active peer and stores its IP address and port number in query active peers**, but peer1 doesn't recognize peer2 as an active peer until it receives a message from peer2.

- Another option available after choosing **1** is **exit**. When an "exit" message is sent by peer1 to peer2, then terminal 2 will show that peer1 got disconnected and peer1 gets removed from query active list of peer2. 

### 👤Query Active Peers

- By choosing choice **2**, it displays the active peers recognized by that peer.

### 👥Connect To Active Peers 

- When you choose **3**, your peer tries to connect with the active peers recognized by it.

- If any of the peers is offline, then it won't get connected; else a connection is established.

- A message will be sent to the peers with which the connection is established, and the terminal of your peer shows the established connections with other peers.

### 💬View Chat - A Special Feature

- When the number **4** is chosen from the menu, then that particular peer's complete chat history with all the active peers will be displayed.

### 👋🏻Quit

- When **0** is chosen in peer1's terminal, then "notifying all peers before exitting" will be displayed in peer1's terminal and an exit message will be sent to all the connected peers.

- All the connected peers will receive the message and disconnecting with peer1 message will be shown in their terminals.



All these operations are demonstarted and the corresponding screenshots are available in the **Screenshots** floder.
