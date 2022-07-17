# ha-bobcatminer
![ha-bobcatminer](https://user-images.githubusercontent.com/366855/164951518-b39a20b9-0040-4b42-a727-916d2852cd30.png)

## Introduction
This is a Home Assistant integration for the Bobcat Helium Miner, allowing you to monitor your Bobcat miner's state including running state, temperature and public IP.

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
