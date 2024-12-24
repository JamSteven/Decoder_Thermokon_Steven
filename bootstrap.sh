#!/bin/sh

# Nettoyage
rm -rf /root/decoder_service /root/decoder_service.zip

# Téléchargement et extraction
wget -O /root/decoder_service.zip https://github.com/JamSteven/Decoder_Thermokon_Steven/archive/refs/heads/main.zip
unzip /root/decoder_service.zip -d /root/
mv /root/Decoder_Thermokon_Steven-main /root/decoder_service

# Configuration des dépôts OPKG
cat << EOF > /etc/opkg/distfeeds.conf
src/gz wisgateos_base https://downloads.openwrt.org/releases/21.02.1/packages/mipsel_24kc/base
src/gz wisgateos_packages https://downloads.openwrt.org/releases/21.02.1/packages/mipsel_24kc/packages
EOF

# Installation des dépendances
opkg update
opkg install python3 unzip python3-paho-mqtt

# Configuration du service
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
/etc/init.d/mqtt_decoder_service enable
/etc/init.d/mqtt_decoder_service start

echo "Installation terminée avec succès !"
