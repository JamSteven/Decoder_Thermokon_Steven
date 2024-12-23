#!/bin/sh

echo "=== [1/6] Vérification et configuration des dépôts OpenWrt ==="
if ! grep -q "wisgateos_base" /etc/opkg/distfeeds.conf; then
    echo "Configuration des dépôts manquante ou incorrecte. Mise à jour du fichier."
    # Sauvegarde du fichier de configuration existant
    if [ ! -f /etc/opkg/distfeeds.conf.bak ]; then
        cp /etc/opkg/distfeeds.conf /etc/opkg/distfeeds.conf.bak
    fi

    # Mise à jour des dépôts
    cat << EOF > /etc/opkg/distfeeds.conf
src/gz wisgateos_base https://downloads.openwrt.org/releases/21.02.1/packages/mipsel_24kc/base
src/gz wisgateos_packages https://downloads.openwrt.org/releases/21.02.1/packages/mipsel_24kc/packages
EOF
    echo "Dépôts OpenWrt configurés avec succès."
else
    echo "Les dépôts OpenWrt sont déjà configurés correctement."
fi

echo "=== [2/6] Mise à jour des dépôts et installation des dépendances ==="
opkg update
if [ $? -ne 0 ]; then
    echo "Erreur : Impossible de mettre à jour les dépôts. Vérifiez les URLs dans /etc/opkg/distfeeds.conf."
    exit 1
fi

opkg install python3 unzip python3-paho-mqtt || {
    echo "Certains paquets sont déjà installés ou une erreur est survenue."
    exit 1
}

echo "=== [3/6] Téléchargement et extraction du projet depuis GitHub ==="
wget -O /root/decoder_service.zip https://github.com/JamSteven/Decoder_Thermokon_Steven/archive/refs/heads/main.zip
if [ $? -ne 0 ]; then
    echo "Erreur : Échec du téléchargement du projet depuis GitHub."
    exit 1
fi

python3 -c "import zipfile; zipfile.ZipFile('/root/decoder_service.zip', 'r').extractall('/root/')" || {
    echo "Erreur : Impossible d'extraire le fichier ZIP."
    exit 1
}

if [ ! -d "/root/Decoder_Thermokon_Steven-main" ]; then
    echo "Erreur : Le répertoire extrait n'a pas été trouvé."
    exit 1
fi

mv /root/Decoder_Thermokon_Steven-main /root/decoder_service

echo "=== [4/6] Configuration des permissions ==="
chmod +x /root/decoder_service/install_decoder.sh

echo "=== [5/6] Exécution du script d'installation ==="
/root/decoder_service/install_decoder.sh
if [ $? -ne 0 ]; then
    echo "Erreur : Le script d'installation a échoué."
    exit 1
fi

echo "=== [6/6] Démarrage et activation du service MQTT Decoder ==="
if [ -f /etc/init.d/mqtt_decoder_service ]; then
    /etc/init.d/mqtt_decoder_service start
    /etc/init.d/mqtt_decoder_service enable
else
    echo "Erreur : Le fichier /etc/init.d/mqtt_decoder_service est introuvable."
fi

echo "=== Installation terminée avec succès ! ==="
