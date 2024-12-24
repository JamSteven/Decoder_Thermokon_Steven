import os
import sys

# Ajoutez le chemin avant les imports
sys.path.append('/root/decoder_service/decoders')

print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {os.environ.get('PYTHONPATH')}")
print(f"Files in /root/decoder_service/decoders: {os.listdir('/root/decoder_service/decoders')}")

import paho.mqtt.client as mqtt
import json
from thermokon_decoder import Decode  # Import direct après ajout au chemin

# Configuration
BROKER = "127.0.0.1"  # Adresse du broker MQTT
PORT = 1883  # Port par défaut
INPUT_TOPIC = "application/Thermokon/device/+/rx"
OUTPUT_TOPIC_PREFIX = "application/decoded/"

def on_message(client, userdata, msg):
    """Callback exécuté lors de la réception d'un message."""
    print(f"[MQTT] Message received on {msg.topic}: {msg.payload.decode(errors='ignore')}")
    try:
        # Analyse du message brut
        payload = json.loads(msg.payload.decode("utf-8", errors='ignore'))
        dev_eui = payload.get("devEUI", "unknown")
        f_port = payload.get("fPort", 0)
        data_hex = payload.get("data", "")
        data_bytes = bytes.fromhex(data_hex)

        # Décodage des données avec votre décodeur Thermokon
        decoded_data = Decode(f_port, data_bytes)

        # Préparation du topic et du message de sortie
        output_topic = f"{OUTPUT_TOPIC_PREFIX}{dev_eui}"
        output_payload = {
            "devEUI": dev_eui,
            "decoded_data": decoded_data
        }

        # Publication des données décodées
        client.publish(output_topic, json.dumps(output_payload))
        print(f"[MQTT] Decoded data published to {output_topic}: {output_payload}")

    except json.JSONDecodeError as jde:
        print(f"[ERROR] JSON decode error: {jde}")
    except Exception as e:
        print(f"[ERROR] Exception while processing message: {e}")

def main():
    """Point d'entrée principal du script."""
    # Vérification des dépendances nécessaires
    try:
        if not os.path.exists("/root/decoder_service/decoders/thermokon_decoder.py"):
            raise FileNotFoundError("Decoder file not found in the expected directory.")
    except FileNotFoundError as fnfe:
        print(f"[ERROR] {fnfe}")
        return

    # Création du client MQTT
    client = mqtt.Client()
    client.on_message = on_message

    # Connexion au broker et abonnement
    try:
        client.connect(BROKER, PORT, 60)
        client.subscribe(INPUT_TOPIC)
        print(f"[MQTT] Subscribed to topic: {INPUT_TOPIC}")
    except Exception as e:
        print(f"[ERROR] Failed to connect or subscribe: {e}")
        return

    # Boucle principale bloquante
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("[INFO] Script interrupted by user. Exiting...")
    except Exception as e:
        print(f"[ERROR] Unexpected exception: {e}")

if __name__ == "__main__":
    main()
