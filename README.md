# WakeOnLAN GUI 🚀

WakeOnLAN GUI is a simple web-based interface for sending Wake-on-LAN (WOL) packets to power on computers remotely over your local network. It is designed to be easy to deploy and use, with persistent storage for your device list.

## ✨ Features
- 🖥️ Web interface to manage and wake devices
- 💾 Persistent storage using SQLite
- 🐳 Easy deployment with Docker

## 🚦 Getting Started

### 🛠️ Prerequisites
- Docker and Docker Compose installed on your system

### 🏗️ Running with Docker Compose
1. Clone this repository or create a directory for your configuration.
2. Create a `docker-compose.yml` file as shown below.
3. Start the service:
   ```sh
   docker-compose up -d
   ```
4. Open your browser and go to `http://localhost:5000` (or the port configured by the app).

### 📄 Example `docker-compose.yml`
```yaml
services:
  deploy:
    image: jairf/wakeonlan_gui:latest
    container_name: wakeonlan_gui
    network_mode: host
    restart: unless-stopped
    volumes:
      - ./database.sqlite:/server/database.sqlite
```

- ⚠️ `network_mode: host` is required for sending WOL packets on the local network.
- 💾 The SQLite database is persisted to `./database.sqlite` on your host.

## 🖱️ Usage
1. Access the web interface in your browser.
2. Add devices by specifying their MAC address and a name.
3. Click the wake button to send a WOL packet to a device.

## 📝 Notes
- 💡 Make sure your target devices are configured to accept Wake-on-LAN packets.
- 🌐 The app must run on the same local network as the devices you want to wake.

## 📄 License
MIT License
