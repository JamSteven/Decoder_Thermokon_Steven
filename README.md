Vue d'ensemble / Overview
Ce projet déploie un décodeur Thermokon sur la passerelle Rakwireless WisGate pour traiter les données uplink des appareils via LoRaWAN.
This project deploys a Thermokon decoder on the Rakwireless WisGate gateway to process uplink data from devices via LoRaWAN.

Installation / How to Install
Commande / Command:
bash
Copier le code
wget -O - https://raw.githubusercontent.com/JamSteven/Decoder_Thermokon_Steven/main/bootstrap.sh | sh
Ce que fait la commande / What the Command Does:
Installe Python 3, unzip et paho-mqtt.
Installs Python 3, unzip, and paho-mqtt.

Télécharge et extrait les fichiers du décodeur depuis GitHub.
Downloads and extracts decoder files from GitHub.

Configure un service pour exécuter le décodeur au démarrage.
Configures a service to run the decoder at startup.

Démarre immédiatement le service.
Starts the service immediately.

Intégration / Integration
1. Création de l'Application / Creating the Application
Nom / Name: Thermokon.
2. Paramètres d'Intégration / Integration Parameters
Format du payload / Payload format: HEX string.
3. Ajout des Appareils / Adding Devices
Les appareils peuvent être ajoutés normalement, et le décodeur traitera automatiquement les données uplink.
Devices can be added normally, and the decoder will automatically process uplink data.
Vérification / Verifying
Pour consulter les logs :
To view the logs:

bash
Copier le code
cat /var/log/mqtt_decoder_service.log
Les logs afficheront les données décodées publiées sur :
The logs will show decoded data published to:
application/decoded/<devEUI>

Dépannage / Troubleshooting
Service non démarré ? / Service not running?
Démarrez manuellement :
Start manually:

bash
Copier le code
/etc/init.d/mqtt_decoder_service start
Réinstaller / Reinstall:
bash
Copier le code
wget -O - https://raw.githubusercontent.com/JamSteven/Decoder_Thermokon_Steven/main/bootstrap.sh | sh
