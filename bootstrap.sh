#!/bin/sh

# Étape 1 : Installation de `unzip` si non présent
if ! command -v unzip > /dev/null; then
    echo "=== Installing unzip ==="
    opkg update
    opkg install unzip || {
        echo "Failed to install unzip. Exiting."
        exit 1
    }
fi

# Étape 2 : Configuration des dépôts OPKG
echo "=== Configuring opkg repositories ==="
cat << EOF > /etc/opkg/distfeeds.conf
src/gz wisgateos_base https://downloads.openwrt.org/releases/21.02.1/packages/mipsel_24kc/base
src/gz wisgateos_packages https://downloads.openwrt.org/releases/21.02.1/packages/mipsel_24kc/packages
EOF

# Étape 3 : Mise à jour des dépôts et installation des dépendances
echo "=== Updating repositories and installing dependencies ==="
opkg update && opkg install python3 python3-paho-mqtt || {
    echo "Failed to install dependencies."
    exit 1
}

# Étape 4 : Téléchargement des fichiers depuis GitHub
echo "=== Downloading decoder service files from GitHub ==="
rm -rf /root/decoder_service /root/decoder_service.zip
wget -O /root/decoder_service.zip https://github.com/JamSteven/Decoder_Thermokon_Steven/archive/refs/heads/main.zip || {
    echo "Failed to download files from GitHub."
    exit 1
}

# Étape 5 : Extraction des fichiers
echo "=== Extracting decoder service files ==="
unzip /root/decoder_service.zip -d /root/ || {
    echo "Failed to unzip files."
    exit 1
}

mv /root/Decoder_Thermokon_Steven-main /root/decoder_service
chmod +x /root/decoder_service/mqtt_decoder_service.py

# Étape 6 : Configuration du service
echo "=== Configuring MQTT decoder service ==="
cat << 'EOF' > /etc/init.d/mqtt_decoder_service
#!/bin/sh /etc/rc.common
START=99
STOP=10
SCRIPT_PATH="/root/decoder_service/mqtt_decoder_service.py"
LOG_FILE="/var/log/mqtt_decoder_service.log"

start() {
    echo "Starting MQTT Decoder Service..."
    export PYTHONPATH=/root/decoder_service/decoders
    python3 $SCRIPT_PATH > $LOG_FILE 2>&1 &
}

stop() {
    echo "Stopping MQTT Decoder Service..."
    pkill -f "$SCRIPT_PATH"
}
EOF

chmod +x /etc/init.d/mqtt_decoder_service

# Étape 7 : Activation et démarrage du service
echo "=== Enabling and starting MQTT decoder service ==="
/etc/init.d/mqtt_decoder_service enable
/etc/init.d/mqtt_decoder_service start

echo "=== Installation completed successfully ==="
