# ha-bobcatminer
<p align="center">
  <img alt="VS Code in action" src="https://user-images.githubusercontent.com/366855/164951482-a8c1107d-8be7-4f8d-9c9b-838f36bbbe15.png">
</p>

## Introduction
This is a Home Assistant integration for the Bobcat Helium Miner, allowing you to monitor your Bobcat miner's state including sync gap, temperature and public IP.

## Installation

Numerous installation options are available.

## HACS (Recommended)

You can install the integration through HACS directly. The integration can also be updated through HACS.

## Custom Integration Wheels
Add a file called `bobcatminer.json` in your `custom_components` directory with the following content.

```json
{
  "name": "Bobcat Miner",
  "owner": ["@ardevd"],
  "manifest": "https://raw.githubusercontent.com/ardevd/ha-bobcatminer/main/custom_components/bobcatminer/manifest.json",
  "url": "https://github.com/ardevd/ha-bobcatminer/"
}
```

## Manual
1. Download this repo by either of the following method
- `git clone https://github.com/ardevd/ha-bobcatminer`
- Download https://github.com/ardevd/ha-bobcatminer/archive/refs/heads/master.zip
2. Copy or link this repo into Home Assistant `custom_components` directory

## Configuration
Click "Add integration" from Home Assistant, search "Bobcat Miner", click to add.

Enter the IP address asssociated with the Bobcat miner. The diagnoser needs to be accessible from Home Assistant for the integration to work.

After setting up, miner status should be available in Home Assistant.


