# HA Tenda 4G09 Custom Integration

Local integration for collecting data and managing the **Tenda TG09** router.

It communicates directly with the router over HTTP on your local network and uses a Telnet connection to retrieve signal information from the modem.

---

## Features

| Entity | Type | Description |
| ------ | ---- | ----------- |
| Device name | `sensor` | Name of the device |
| WAN connection | `binary_sensor` | Indicates whether the WAN connection is active |
| WAN IP address | `sensor` | Wide Area Network IP address |
| LAN IP address | `sensor` | Local area network IP address |
| LAN MAC address | `sensor` | MAC address of the local network interface |
| Internet status | `sensor` | Current internet connection status |
| SIM card status | `sensor` | Current SIM card status |
| Connection type | `sensor` | Type of network connection |
| Connected clients | `sensor` | Number of connected clients |
| Operating mode | `sensor` | Operating mode of the device |
| Signal strength | `sensor` | Cellular signal strength indicator |
| Mobile Country Code | `sensor` | Country code of the mobile network |
| Mobile Network Code | `sensor` | Code identifying the mobile network operator |
| Upload speed | `sensor` | Data upload speed |
| Download speed | `sensor` | Data download speed |
| Total data usage | `sensor` | Total mobile data usage in megabytes |
| Cell ID | `sensor` | Identifier of the connected cellular network cell |
| Physical Cell ID | `sensor` | Physical identifier of the LTE cell |
| Radio Access Technology | `sensor` | Radio access technology, such as LTE or 5G |
| Duplex Mode | `sensor` | Duplex mode, such as FDD or TDD |
| LTE Band | `sensor` | LTE frequency band |
| Uplink Bandwidth | `sensor` | Uplink bandwidth |
| Downlink Bandwidth | `sensor` | Downlink bandwidth |
| RSRP | `sensor` | Reference Signal Received Power; measures LTE/5G signal strength in dBm |
| RSRQ | `sensor` | Reference Signal Received Quality; indicates signal quality in dB |
| RSSI | `sensor` | Received Signal Strength Indicator; measures total received signal power in dBm |
| SINR | `sensor` | Signal-to-Interference-plus-Noise Ratio; measures signal quality relative to interference and noise in dB |

---

## Installation

### Manual

- Copy the custom_components/tenda_mesh/ folder into the config/custom_components/ directory of your Home Assistant installation.
- Restart Home Assistant.
- Navigate to Settings → Devices & Services → Add Integration.
- Search for Tenda 4G09 and follow the setup wizard to complete the configuration.

## Configuration

| Field                | Description                      | Default |
| -------------------- | -------------------------------- | ------- |
| **Router Ip**        | The router IP address            | —       |
| **Password**         | Router administrator password    | —       |
| **Refresh interval** | Data polling interval in seconds | 30      |
