Thermokon Decoder Installation and Usage Guide
Overview
This repository provides a complete solution to deploy and manage the Thermokon decoder on your Rakwireless WisGate gateway. The decoder allows you to interpret and process data sent by Thermokon devices via LoRaWAN.

How to Install
To install the decoder service, run the following command in your gateway's terminal:

bash
Copier le code
wget -O - https://raw.githubusercontent.com/JamSteven/Decoder_Thermokon_Steven/main/bootstrap.sh | sh
This command will:

Install the necessary dependencies, including Python 3 and the required libraries.
Download and extract the decoder files from this GitHub repository.
Configure the MQTT decoder service to run automatically in the background.
Start the decoder service immediately after installation.
What the Script Does
Configures OPKG Repositories
Updates the package manager to access the correct OpenWrt repositories.

Installs Required Dependencies
Ensures Python 3, unzip, and paho-mqtt are installed for the decoder service to work.

Downloads and Extracts Decoder Files
Fetches the latest decoder files from GitHub and places them in /root/decoder_service.

Configures and Enables the Decoder Service
Creates an initialization script (mqtt_decoder_service) to run the decoder in the background and ensures it starts automatically on boot.

Starts the Decoder Service
Immediately launches the MQTT decoder service.

Integration Instructions
1. Creating the Application
When setting up your LoRaWAN application:

Name the application: Use the name Thermokon for the application. This ensures that the correct decoder is applied.
2. Integration Parameters
Set the payload format to HEX string.
This allows the decoder to interpret the raw data correctly.
3. Adding Devices
Devices can be added directly to the application. The decoder will automatically process their uplink data and publish the decoded payloads.
Verifying the Decoder
Once installed, the service will process incoming messages from the LoRaWAN application. You can verify the logs using:

bash
Copier le code
cat /var/log/mqtt_decoder_service.log
Logs will show decoded data published to MQTT topics like application/decoded/<devEUI>.

Troubleshooting
Service Not Running
Ensure the service is enabled and running:

bash
Copier le code
/etc/init.d/mqtt_decoder_service start
Decoder Logs
Check logs for errors:

bash
Copier le code
cat /var/log/mqtt_decoder_service.log
Reinstallation
If issues persist, reset the environment:

bash
Copier le code
wget -O - https://raw.githubusercontent.com/JamSteven/Decoder_Thermokon_Steven/main/bootstrap.sh | sh
FAQ
Q: Can I add products directly to the application?
Yes, devices can be registered normally within the Thermokon application, and the decoder will automatically process their uplinks.

Q: What should the integration parameter format be?
Set it to HEX string in the application integration settings.

Q: Does the script run automatically in the background?
Yes, the script sets up the decoder as a background service that runs on startup.

This README serves as a quick start guide for setting up and using the Thermokon decoder on your Rakwireless gateway.
