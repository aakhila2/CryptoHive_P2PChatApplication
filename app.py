import socket
import threading

# Global set to store connected peers
peers = set()

# Global dictionary to store chat history
chat_history = {}

# Function to handle receiving messages
def receive_messages(server_socket):
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            message = client_socket.recv(1024).decode('utf-8').strip()
            print(f"\n📩 Received message: {message} from {client_address}")

            # ✅ Ensure message is properly formatted
            parts = message.split(' ', 2)
            if len(parts) < 3:
                print("⚠ Invalid message format received. Ignoring.")
                continue  # Skip invalid messages
            
            ip_port, team_name, msg = parts
            print(f"📌 Parsed - IP:Port: {ip_port}, Team: {team_name}, Message: {msg}")

            # ✅ If it's an exit message, remove only from active peers, but keep in chat history
            if msg.lower() == "exit":
                if ip_port in peers:
                    peers.discard(ip_port)  # ✅ Remove only from active peers
                    print(f"❌ {ip_port} disconnected")

                # ✅ Store a log of the disconnection in chat history
                if ip_port not in chat_history:
                    chat_history[ip_port] = []
                chat_history[ip_port].append(f"{team_name}: Peer {ip_port} exited.")

                continue  # Skip further processing


            # ✅ Ignore adding self to the active peers list
            if ip_port not in peers and ip_port != f"{server_ip}:{server_port}":
                peers.add(ip_port)
                print(f"✅ Added peer: {ip_port}")

            # ✅ Store received message in chat history
            if ip_port not in chat_history:
                chat_history[ip_port] = []
            chat_history[ip_port].append(f"{team_name}: {msg}")

        except Exception as e:
            print(f"❌ Error receiving message: {e}")

def send_message():
    ip = input("Enter the recipient's IP address (Press Enter for localhost): ").strip()
    if not ip:
        ip = "127.0.0.1"  # Default to localhost

    port = int(input("Enter the recipient's port number: "))
    message = input("Enter your message: ")

    peer_id = f"{ip}:{port}"  # Unique identifier for peer

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        try:
            s.connect((ip, port))
            formatted_msg = f"{server_ip}:{server_port} {team_name} {message}"
            s.sendall(formatted_msg.encode('utf-8'))
            print(f"✅ Message sent successfully to {peer_id}")

            # ❌ Remove automatic peer addition here
            # if peer_id not in peers:
            #     peers.add(peer_id)  # This line is removed

            # ✅ Store sent message in chat history
            if peer_id not in chat_history:
                chat_history[peer_id] = []
            chat_history[peer_id].append(f"You: {message}")

        except socket.gaierror:
            print("❌ Invalid IP address. Please check and try again.")
        except socket.timeout:
            print("❌ Connection timed out.")
        except Exception as e:
            print(f"❌ Failed to send message: {e}")


# Function to query connected peers
def query_peers():
    print(f"[DEBUG] Peers List: {peers}")
    if peers:
        print("\n🔥 Active Peers 🔥")
        for peer in peers:
            print(peer)
    else:
        print("\n🚫 No connected peers found!")

# Function to view chat history
def view_chat_history():
    if not chat_history:
        print("\n🗃 No chat history available!")
        return

    print("\n💬 Chat History 💬")
    for peer, messages in chat_history.items():
        print(f"\n📌 Chat with {peer}:")
        for msg in messages:
            print(f"   {msg}")

# Function to connect to active peers
def connect_to_peers():
    if not peers:
        print("🚫 No active peers to connect to.")
        return

    for peer in peers:
        ip, port = peer.split(":")
        
        # ✅ Avoid sending duplicate "Connection established" messages
        if peer in chat_history and any("Connection established" in msg for msg in chat_history[peer]):
            print(f"🔗 Already connected to {peer}, skipping...")
            continue  # Skip if already connected

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((ip, int(port)))

                connect_msg = f"{server_ip}:{server_port} {team_name} Connection established"
                s.sendall(connect_msg.encode('utf-8'))
                print(f"🔗 Connected to peer: {peer}")

                # ✅ Store the connection message only once
                if peer not in chat_history:
                    chat_history[peer] = []
                chat_history[peer].append(f"{team_name}: Connection established")

        except Exception as e:
            print(f"❌ Failed to connect to {peer}: {e}")

# Send mandatory messages to specified IPs
def send_mandatory_messages():
    mandatory_peers = [
        ("10.206.4.122", 1255),
        ("10.206.5.228", 6555)
    ]

    for ip, port in mandatory_peers:
        peer_id = f"{ip}:{port}"
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((ip, port))
                formatted_msg = f"{server_ip}:{server_port} {team_name} Hello from {team_name}"
                s.sendall(formatted_msg.encode('utf-8'))
                print(f"📨 Sent mandatory message to {peer_id}")

            # ✅ Manually add the mandatory peers to the peers list
            peers.add(peer_id)

        except Exception as e:
            print(f"⚠ Failed to send mandatory message to {peer_id}: {e}")

    print(f"ℹ Mandatory peers added: {peers}")

# Start server thread
server_port = int(input("Enter your port number: "))
team_name = input("Enter your team name : ")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", server_port))
server_socket.listen(5)

server_ip = socket.gethostbyname(socket.gethostname())  # Get the actual IP of the machine
print(f"🚀 Server listening on {server_ip}:{server_port}")

threading.Thread(target=receive_messages, args=(server_socket,), daemon=True).start()

send_mandatory_messages()

while True:
    print("\n***** Menu *****")
    print("1. Send message")
    print("2. Query active peers")
    print("3. Connect to active peers")
    print("4. View chat history")
    print("0. Quit")

    choice = input("Enter your choice: ")

    if choice == '1':
        send_message()
    elif choice == '2':
        query_peers()
    elif choice == '3':
        connect_to_peers()
    elif choice == '4':
        view_chat_history()
    elif choice == '0':
        print("👋 Notifying peers before exiting...")

        # ✅ Notify all peers before closing
        for peer in peers.copy():  
            ip, port = peer.split(":")
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(3)
                    s.connect((ip, int(port)))
                    exit_msg = f"{server_ip}:{server_port} {team_name} exit"
                    s.sendall(exit_msg.encode('utf-8'))
                    print(f"📤 Sent exit message to {peer}")
            except Exception:
                print(f"⚠ Could not notify {peer} (may already be offline)")

        print("👋 Exiting...")
        break  # Exit the program
    else:
        print("⚠ Invalid choice. Try again.")

server_socket.close()
