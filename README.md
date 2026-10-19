# Tenda 4G09 Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/b-proszkowiec/ha-tenda-4g09.svg)](https://github.com/b-proszkowiec/ha-tenda-4g09/releases)

A custom integration for Home Assistant to monitor and control Tenda 4G09 LTE routers. It provides sensors for connection status, data usage, connected clients, and advanced LTE signal metrics (if supported by your firmware via Telnet).

## Features

- 🌐 **WAN/LTE Status:** Monitor internet connection status.
- 📊 **Data Usage:** Track your data limit and current usage.
- 📱 **Connected Devices:** See online clients with their IP, MAC, and upload/download speeds.
- 📶 **LTE Signal Metrics:** Detailed tracking of RSSI, RSRP, RSRQ, and SINR (requires Telnet support on the router).

| Entity                  | Type            | Description                                                                                               |
| ----------------------- | --------------- | --------------------------------------------------------------------------------------------------------- |
| Device name             | `sensor`        | Name of the device                                                                                        |
| WAN connection          | `binary_sensor` | Indicates whether the WAN connection is active                                                            |
| WAN IP address          | `sensor`        | Wide Area Network IP address                                                                              |
| LAN IP address          | `sensor`        | Local area network IP address                                                                             |
| LAN MAC address         | `sensor`        | MAC address of the local network interface                                                                |
| Internet status         | `sensor`        | Current internet connection status                                                                        |
| SIM card status         | `sensor`        | Current SIM card status                                                                                   |
| Connection type         | `sensor`        | Type of network connection                                                                                |
| Connected clients       | `sensor`        | Number of connected clients                                                                               |
| Operating mode          | `sensor`        | Operating mode of the device                                                                              |
| Signal strength         | `sensor`        | Cellular signal strength indicator                                                                        |
| Mobile Country Code     | `sensor`        | Country code of the mobile network                                                                        |
| Mobile Network Code     | `sensor`        | Code identifying the mobile network operator                                                              |
| Upload speed            | `sensor`        | Data upload speed                                                                                         |
| Download speed          | `sensor`        | Data download speed                                                                                       |
| Total data usage        | `sensor`        | Total mobile data usage in megabytes                                                                      |
| Cell ID                 | `sensor`        | Identifier of the connected cellular network cell                                                         |
| Physical Cell ID        | `sensor`        | Physical identifier of the LTE cell                                                                       |
| Radio Access Technology | `sensor`        | Radio access technology, such as LTE or 5G                                                                |
| Duplex Mode             | `sensor`        | Duplex mode, such as FDD or TDD                                                                           |
| LTE Band                | `sensor`        | LTE frequency band                                                                                        |
| Uplink Bandwidth        | `sensor`        | Uplink bandwidth                                                                                          |
| Downlink Bandwidth      | `sensor`        | Downlink bandwidth                                                                                        |
| RSRP                    | `sensor`        | Reference Signal Received Power; measures LTE/5G signal strength in dBm                                   |
| RSRQ                    | `sensor`        | Reference Signal Received Quality; indicates signal quality in dB                                         |
| RSSI                    | `sensor`        | Received Signal Strength Indicator; measures total received signal power in dBm                           |
| SINR                    | `sensor`        | Signal-to-Interference-plus-Noise Ratio; measures signal quality relative to interference and noise in dB |

---

## Installation

### Method 1: HACS (Recommended)

1. Open Home Assistant and navigate to **HACS**.
2. Click on **Integrations** -> **3 dots (top right)** -> **Custom repositories**.
3. Add repository URL: `https://github.com/b-proszkowiec/ha-tenda-4g09` and select category **Integration**.
4. Click **Download** and restart Home Assistant.

### Method 2: Manual

1. Download the latest release.
2. Copy the `custom_components/tenda_4g09` folder to your Home Assistant `custom_components` directory.
3. Restart Home Assistant.

---

## Configuration

1. In Home Assistant, go to **Settings** -> **Devices & Services**.
2. Click **Add Integration** and search for **Tenda 4G09**.
3. Enter your router's IP address (default: `192.168.0.1`) and admin password.

---

## Dashboard Examples

Here are some ready-to-use Lovelace cards to make your dashboard look great.

### 1. Connected Devices List

A dynamic list showing all connected clients, their speeds, and device types based on their name.
<br><br>

<p align="center">
  <img src="https://github.com/b-proszkowiec/ha-tenda-4g09/blob/cards/custom_components/cards/devices_card.webp" alt="Connected Devices Example" width="400">
</p>

<details>
  <summary><b>Click to expand Card Configuration (YAML)</b></summary>

```yaml
{% set devices = state_attr('sensor.tenda_4g09_connected_clients', 'devices') or [] %}
  <div style="text-align:center; margin-bottom:12px;">
    <span style="font-size:28px; font-weight:bold;">
    {{ devices | count }}
    </span>
    <span style="opacity:0.7;">
    devices online
    </span>
  </div>

{% if devices %}
  {% for device in devices %}
  <div style="
    padding: 12px;
    margin: 8px 0;
    border-radius: 12px;
    background: rgba(127,127,127,0.10);
  ">
  <div style="font-size: 17px; font-weight: bold;">
    {% if 'TV' in device.name | upper %}
      {% set mark = "📺" %}
    {% elif 'DESKTOP' in device.name | upper or 'PC' in device.name | upper %}
      {% set mark = "🖥️" %}
    {% elif 'HOMEASSISTANT' in device.name | upper %}
      {% set mark = "🏠" %}
    {% elif 'PHONE' in device.name | upper or 'IPHONE' in device.name | upper %}
        {% set mark = "📱" %}
    {% else %}
      {% set mark = "💻" %}
    {% endif %}

    {{ mark }} {{ device.name }} ({{ device.ip }} / {{ device.mac }} )
  </div>

  <div style="font-size:13px; opacity:0.7; margin-top:4px;">
    <span>⬆️ {{ device.upload_speed }} kB/s</span>
    <span>⬇️ {{ device.download_speed }} kB/s</span>
  </div>
  {% if device.guest %}
  <div style="margin-top:6px; font-size:12px;">
    👤 Guest network
  </div>
  {% endif %}

  {% if device.blocked %}
  <div>
    🚫 Blocked
  </div>
  {% endif %}
  </div>
  {% endfor %}

{% else %}
  <div style="text-align:center; padding:20px; opacity:0.6;">
  📭 No connected devices
  </div>
{% endif %}
```

</details>

### 2. Advanced LTE Signal Charts

A beautiful 2x2 grid showing the quality of your LTE connection.

> ⚠️ **Requirements:** You must have the [ApexCharts Card](https://github.com/RomRider/apexcharts-card) installed via HACS frontend to use this card.

<br><br>

<p align="center">
  <img src="https://github.com/b-proszkowiec/ha-tenda-4g09/blob/cards/custom_components/cards/signal_card.webp" alt="Signal Parameters Example" width="700">
</p>

<details>
  <summary><b>Click to expand Card Configuration (YAML)</b></summary>

```yaml
type: grid
columns: 2
square: false
cards:
  - type: custom:apexcharts-card
    header:
      show: true
      title: RSSI (Received Signal Strength)
      show_states: true
    graph_span: 12h
    yaxis:
      - min: -100
        max: -60
    apex_config:
      grid:
        strokeDashArray: 2
        borderColor: "#808080"
        opacity: 0.3
      annotations:
        yaxis:
          - "y": -70
            y2: -50
            borderColor: transparent
            fillColor: "#16A34A"
            opacity: 0.15
          - "y": -90
            y2: -70
            borderColor: transparent
            fillColor: "#EAB308"
            opacity: 0.15
          - "y": -110
            y2: -90
            borderColor: transparent
            fillColor: "#DC2626"
            opacity: 0.15
    series:
      - entity: sensor.tenda_4g09_rssi
        name: RSSI avg
        type: line
        curve: straight
        group_by:
          duration: 10min
          func: avg
      - entity: sensor.tenda_4g09_rssi
        name: RSSI
        type: line
        opacity: 0.3
        stroke_width: 1

  - type: custom:apexcharts-card
    header:
      show: true
      title: RSRP (Reference Signal Power)
      show_states: true
    graph_span: 12h
    yaxis:
      - min: -115
        max: -80
    apex_config:
      grid:
        strokeDashArray: 2
        borderColor: "#808080"
        opacity: 0.3
      annotations:
        yaxis:
          - "y": -90
            y2: -70
            borderColor: transparent
            fillColor: "#16A34A"
            opacity: 0.15
          - "y": -110
            y2: -90
            borderColor: transparent
            fillColor: "#EAB308"
            opacity: 0.15
          - "y": -125
            y2: -110
            borderColor: transparent
            fillColor: "#DC2626"
            opacity: 0.15
    series:
      - entity: sensor.tenda_4g09_rsrp
        name: RSRP avg
        type: line
        curve: straight
        group_by:
          duration: 10min
          func: avg
      - entity: sensor.tenda_4g09_rsrp
        name: RSRP
        type: line
        opacity: 0.3
        stroke_width: 1

  - type: custom:apexcharts-card
    header:
      show: true
      title: RSRQ (Reference Signal Quality)
      show_states: true
    graph_span: 12h
    yaxis:
      - min: -18
        max: -8
    apex_config:
      grid:
        strokeDashArray: 2
        borderColor: "#808080"
        opacity: 0.3
      annotations:
        yaxis:
          - "y": -10
            y2: 0
            borderColor: transparent
            fillColor: "#16A34A"
            opacity: 0.15
          - "y": -15
            y2: -10
            borderColor: transparent
            fillColor: "#EAB308"
            opacity: 0.15
          - "y": -20
            y2: -15
            borderColor: transparent
            fillColor: "#DC2626"
            opacity: 0.15
    series:
      - entity: sensor.tenda_4g09_rsrq
        name: RSRQ avg
        type: line
        curve: straight
        group_by:
          duration: 10min
          func: avg
      - entity: sensor.tenda_4g09_rsrq
        name: RSRQ
        type: line
        opacity: 0.3
        stroke_width: 1

  - type: custom:apexcharts-card
    header:
      show: true
      title: SINR (Signal-to-Noise Ratio)
      show_states: true
    graph_span: 12h
    yaxis:
      - min: -10
        max: 30
    apex_config:
      grid:
        strokeDashArray: 2
        borderColor: "#808080"
        opacity: 0.3
      annotations:
        yaxis:
          - "y": 20
            y2: 30
            borderColor: transparent
            fillColor: "#16A34A"
            opacity: 0.15
          - "y": 0
            y2: 20
            borderColor: transparent
            fillColor: "#EAB308"
            opacity: 0.15
          - "y": -10
            y2: 0
            borderColor: transparent
            fillColor: "#DC2626"
            opacity: 0.15
    series:
      - entity: sensor.tenda_4g09_sinr
        name: SINR avg
        type: line
        curve: straight
        group_by:
          duration: 10min
          func: avg
      - entity: sensor.tenda_4g09_sinr
        name: SINR
        type: line
        opacity: 0.3
        stroke_width: 1
```

</details>

### 3. Support & Contributions

If you find a bug or want to suggest an improvement, feel free to open an issue or create a Pull Request on GitHub.
