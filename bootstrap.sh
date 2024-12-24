#!/bin/sh

# Étape 1 : Nettoyage des fichiers précédents
echo "=== Nettoyage des fichiers précédents ==="
rm -rf /root/decoder_service /root/decoder_service.zip

# Étape 2 : Téléchargement et extraction
echo "=== Téléchargement et extraction des fichiers ==="
wget -O /root/decoder_service.zip https://github.com/JamSteven/Decoder_Thermokon_Steven/archive/refs/heads/main.zip || {
    echo "Erreur : Échec du téléchargement depuis GitHub."
    exit 1
}

if command -v unzip > /dev/null; then
    unzip /root/decoder_service.zip -d /root/ || {
        echo "Erreur : Échec de l'extraction avec unzip."
        exit 1
    }
else
    echo "unzip non trouvé. Installation en cours."
    opkg update && opkg install unzip || {
        echo "Erreur : Échec de l'installation d'unzip."
        exit 1
    }
    unzip /root/decoder_service.zip -d /root/ || {
        echo "Erreur : Échec de l'extraction après installation d'unzip."
        exit 1
    }
fi

mv /root/Decoder_Thermokon_Steven-main /root/decoder_service

# Étape 3 : Configuration des dépôts OPKG
echo "=== Configuration des dépôts OPKG ==="
cat << EOF > /etc/opkg/distfeeds.conf
src/gz wisgateos_base https://downloads.openwrt.org/releases/21.02.1/packages/mipsel_24kc/base
src/gz wisgateos_packages https://downloads.openwrt.org/releases/21.02.1/packages/mipsel_24kc/packages
EOF

# Étape 4 : Installation des dépendances
echo "=== Installation des dépendances ==="
opkg update
opkg install python3 python3-paho-mqtt unzip || {
    echo "Erreur : Échec de l'installation des dépendances."
    exit 1
}

# Étape 5 : Configuration du service
echo "=== Configuration du service MQTT Decoder ==="
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

# Étape 6 : Activation et démarrage du service
echo "=== Activation et démarrage du service MQTT Decoder ==="
/etc/init.d/mqtt_decoder_service enable
/etc/init.d/mqtt_decoder_service start || {
    echo "Erreur : Échec du démarrage du service MQTT Decoder."
    exit 1
}

echo "=== Installation terminée avec succès ! ==="
