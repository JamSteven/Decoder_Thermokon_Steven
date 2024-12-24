import paho.mqtt.client as mqtt
import json

def u16_to_s16(u16):
    """Convert unsigned 16-bit integer to signed 16-bit integer."""
    s16 = u16 & 0xFFFF
    if s16 & 0x8000:
        s16 = -(0x10000 - s16)
    return s16

def u8_to_s8(u8):
    """Convert unsigned 8-bit integer to signed 8-bit integer."""
    s8 = u8 & 0xFF
    if s8 & 0x80:
        s8 = -(0x100 - s8)
    return s8

def voltage_to_battery_percentage(voltage):
    if voltage < 2.0:
        min_voltage = 1.0
        max_voltage = 1.5
        absolute_max_voltage = 1.9

        if voltage < min_voltage:
            percentage = 0
        elif max_voltage <= voltage <= absolute_max_voltage:
            percentage = 100
        elif voltage > absolute_max_voltage:
            percentage = 100
        else:
            percentage = ((voltage - min_voltage) / (max_voltage - min_voltage)) * 100
    else:
        min_voltage = 2.7
        max_voltage = 3.6
        absolute_max_voltage = 4.0

        if voltage < min_voltage:
            percentage = 0
        elif max_voltage <= voltage <= absolute_max_voltage:
            percentage = 100
        elif voltage > absolute_max_voltage:
            percentage = 100
        else:
            percentage = ((voltage - min_voltage) / (max_voltage - min_voltage)) * 100

    percentage = round(percentage / 20) * 20
    percentage = max(0, min(100, percentage))
    return percentage

def Decode(fPort, bytes):
    LPP_CONSTANTS = {
        0x0000: "PARSER",
        0x0001: "DUMMY",
        0x0010: "TEMP",
        0x0011: "RHUM",
        0x0012: "CO2",
        0x0013: "VOC",
        0x0030: "ATM_P",
        0x0031: "DP",
        0x0032: "FLOW",
        0x0040: "VISIBLE_LIGHT",
        0x0041: "OCCU0",
        0x0050: "REED0",
        0x0051: "CONDENSATION",
        0x0054: "VBAT",
        0x0063: "SETPOINT",
        0x8540: "VBAT_HI_RES",
        0x9410: "OCCU1",
        0x9500: "REED1",
        0x9510: "CONDENSATION_RAW",
        0xC000: "DEV_KEY",
        0xC100: "CMD",
        0xC103: "LEARN",
        0xC105: "BAT_TYPE",
        0xC106: "HEARTBEAT",
        0xC108: "MEAS_INTERVAL",
        0xC10A: "CNT_MEAS",
        0xC10B: "BIN_LATENCY",
        0xC120: "TLF_MODE",
        0xC121: "TLF_ONTIME",
        0xC123: "TLF_INTERVAL_0",
        0xC125: "TLF_INTERVAL_1",
        0xC127: "TLF_INTERVAL_2",
        0xC129: "TLF_INTERVAL_3",
        0xC12B: "TLF_INTERVAL_4",
        0xC12D: "TLF_INTERVAL_5",
        0xC134: "LED_MODE",
        0xC135: "LED_ONTIME",
        0xC136: "LED_INTERVAL_0",
        0xC137: "LED_INTERVAL_1",
        0xC138: "LED_INTERVAL_2",
        0xC139: "LED_INTERVAL_3",
        0xC230: "FORCED_UPLINK"
    }

    decoded = {}
    temp_vbat = None
    i = 0

    while i < len(bytes):
        if bytes[i] <= 0x7F:
            lpp = bytes[i]
            i += 1
        else:
            if i + 1 < len(bytes):
                lpp = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            else:
                break

        if lpp in LPP_CONSTANTS:
            key = LPP_CONSTANTS[lpp]
            if key == "PARSER" and i + 1 < len(bytes):
                decoded[key] = u16_to_s16((bytes[i] << 8) | bytes[i + 1])
                i += 2
            elif key == "DUMMY" and i < len(bytes):
                decoded[key] = u8_to_s8(bytes[i])
                i += 1
            elif key == "TEMP" and i + 1 < len(bytes):
                decoded[key] = u16_to_s16((bytes[i] << 8) | bytes[i + 1]) / 10.0
                i += 2
            elif key == "RHUM" and i < len(bytes):
                decoded[key] = bytes[i]
                i += 1
            elif key == "CO2" and i + 1 < len(bytes):
                decoded[key] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            elif key == "VOC" and i + 1 < len(bytes):
                decoded[key] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            elif key == "ATM_P" and i + 1 < len(bytes):
                decoded[key] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            elif key == "DP" and i + 1 < len(bytes):
                decoded[key] = u16_to_s16((bytes[i] << 8) | bytes[i + 1])
                i += 2
            elif key == "FLOW" and i + 1 < len(bytes):
                decoded[key] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            elif key == "VISIBLE_LIGHT" and i + 1 < len(bytes):
                decoded[key] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            elif key == "OCCU0" and i < len(bytes):
                decoded["OCCU0_STATE"] = bytes[i] & 0x01
                decoded["OCCU0_CNT"] = bytes[i] >> 1
                i += 1
            elif key == "REED0" and i < len(bytes):
                decoded["REED0_STATE"] = bytes[i] & 0x01
                decoded["REED0_CNT"] = bytes[i] >> 1
                i += 1
            elif key == "CONDENSATION" and i + 1 < len(bytes):
                decoded["CONDENSATION_STATE"] = bytes[i] >> 7
                decoded["CONDENSATION_RAW"] = ((bytes[i] & 0x7F) << 8) | bytes[i + 1]
                i += 2
            elif key == "VBAT" and i < len(bytes):
                temp_vbat = bytes[i] * 20
                i += 1
            elif key == "SETPOINT" and i < len(bytes):
                decoded[key] = bytes[i]
                i += 1
            elif key == "VBAT_HI_RES" and i + 1 < len(bytes):
                decoded[key] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            elif key == "OCCU1" and i < len(bytes):
                decoded["OCCU1_STATE"] = bytes[i] & 0x01
                decoded["OCCU1_CNT"] = bytes[i] >> 1
                i += 1
            elif key == "REED1" and i < len(bytes):
                decoded["REED1_STATE"] = bytes[i] & 0x01
                decoded["REED1_CNT"] = bytes[i] >> 1
                i += 1
            elif key == "CONDENSATION_RAW" and i + 1 < len(bytes):
                decoded[key] = u16_to_s16((bytes[i] << 8) | bytes[i + 1])
                i += 2
            elif key == "DEV_KEY" and i + 1 < len(bytes):
                decoded[key] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            elif key == "CMD" and i + 1 < len(bytes):
                decoded[key] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            elif key == "LEARN" and i < len(bytes):
                decoded[key] = bytes[i]
                i += 1
            elif key == "BAT_TYPE" and i + 1 < len(bytes):
                decoded[key] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            elif key == "HEARTBEAT" and i + 1 < len(bytes):
                decoded[key] = ((bytes[i] << 8) | bytes[i + 1]) * 60000
                i += 2
            elif key == "MEAS_INTERVAL" and i + 1 < len(bytes):
                decoded[key] = ((bytes[i] << 8) | bytes[i + 1]) * 1000
                i += 2
            elif key == "CNT_MEAS" and i + 1 < len(bytes):
                decoded[key] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            elif key == "BIN_LATENCY" and i + 1 < len(bytes):
                decoded[key] = ((bytes[i] << 8) | bytes[i + 1]) * 1000
                i += 2
            elif key == "TLF_MODE" and i < len(bytes):
                decoded[key] = bytes[i]
                i += 1
            elif key == "TLF_ONTIME" and i + 1 < len(bytes):
                decoded[key] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            elif key.startswith("TLF_INTERVAL") and i + 1 < len(bytes):
                interval_index = (lpp - 0xC123) // 2
                decoded[f"TLF_INTERVAL_{interval_index}"] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            elif key == "LED_MODE" and i < len(bytes):
                decoded[key] = bytes[i]
                i += 1
            elif key == "LED_ONTIME" and i + 1 < len(bytes):
                decoded[key] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            elif key.startswith("LED_INTERVAL") and i + 1 < len(bytes):
                led_interval_index = (lpp - 0xC136) // 2
                decoded[f"LED_INTERVAL_{led_interval_index}"] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            elif key == "FORCED_UPLINK" and i + 1 < len(bytes):
                decoded[key] = (bytes[i] << 8) | bytes[i + 1]
                i += 2
            else:
                i += 1  # Advance for unknown keys without crashing
        else:
            print(f"Unknown LPP type: {hex(lpp)}")
            break

    if temp_vbat is not None:
        decoded["VBAT"] = temp_vbat
        decoded["PBAT"] = voltage_to_battery_percentage(temp_vbat / 1000.0)

    return decoded

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload.decode("utf-8"))

    dev_eui = payload.get("devEUI", "unknown")
    f_port = payload.get("fPort", 0)
    data = bytes.fromhex(payload.get("data", ""))
    rx_info = payload.get("rxInfo", [{}])[0]

    decoded_data = Decode(f_port, data)

    result = {
        "devEUI": dev_eui,
        "decoded_data": decoded_data,
        "metadata": {
            "loRaSNR": rx_info.get("loRaSNR"),
            "rssi": rx_info.get("rssi"),
            "frequency": payload.get("txInfo", {}).get("frequency"),
            "dr": payload.get("txInfo", {}).get("dr")
        }
    }

    output_topic = f"application/decoded/{dev_eui}"
    client.publish(output_topic, json.dumps(result))
    print(f"Donn..es d..cod..es publi..es sur {output_topic}: {result}")

def main():
    mqtt_broker = "localhost"
    mqtt_port = 1883
    input_topic = "application/Thermokon/device/+/rx"

    client = mqtt.Client()
    client.on_message = on_message

    client.connect(mqtt_broker, mqtt_port, 60)
    client.subscribe(input_topic)

    print(f"Abonn.. au topic : {input_topic}")
    client.loop_forever()

if __name__ == "__main__":
    main()

