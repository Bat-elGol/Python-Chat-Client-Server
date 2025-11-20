# Python-Chat-Client-Server
This project implements a **multi-threaded** client–server chat system using Python and TCP socket programming. It allows multiple users to communicate in real-time and logs the chat history.

---

## Project Files
- `chat_server.py` – Server-side program  
- `chat_client.py` – Client-side program  
- `System_Overview_and_Code_Structure.pdf` – Full system explanation  
- `Installation_and_Execution_Guide.pdf` – Step-by-step installation guide  
- `Input_Output_Examples.pdf` – Usage examples  

---

## How to Run
- Run the server first: python chat_server.py
- Run the client (open multiple terminals for multiple users): python chat_client.py
   
Note: Ensure the client is configured to connect to the correct IP address and port (Default: 127.0.0.1:12345).

---

## System Overview
The project uses a TCP client–server architecture:

**Server:**

- Uses threading to handle multiple clients simultaneously
- Broadcasts messages to all connected users
- Logs all activity (connections, messages) to a text file
- 
**Client:**
  
- Connects to the server using TCP
- Sends messages and receives real-time updates
- Runs in multiple terminals for multiple users

---

## Technologies
- Python 3
- TCP Socket Programming
- Threading & Concurrency
- File I/O (logging)
