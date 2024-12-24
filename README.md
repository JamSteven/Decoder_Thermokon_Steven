THERMOKON Decoder
Description
Ce projet déploie un décodeur Thermokon sur la passerelle Rakwireless WisGate pour traiter les données uplink des appareils via LoRaWAN.
This project deploys a Thermokon decoder on the Rakwireless WisGate gateway to process uplink data from devices via LoRaWAN.

Installation / How to Install
Connexion à la passerelle / Connect to the Gateway

Se connecter en SSH à la passerelle.
Connect to the gateway via SSH.
Identifiant : root, Mot de passe : celui défini lors de la configuration initiale.
Username: root, Password: the one set during the initial setup.
Créer une Application / Create an Application

Nom de l'application : Thermokon.
Application name: Thermokon.
Paramètres d'intégration : HEX string.
Integration parameters: HEX string.
Exécuter la Commande / Run the Command
Copiez et collez cette commande dans le terminal :
Copy and paste this command into the terminal:

bash
Copier le code
wget -O - https://raw.githubusercontent.com/JamSteven/Decoder_Thermokon_Steven/main/bootstrap.sh | sh
