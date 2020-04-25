# rPI as a Ventivader UART peripherial
## Make your rPI behave as a  Ventivader UART peripherial
Based in: 
https://scribles.net/creating-ble-gatt-server-uart-service-on-raspberry-pi/
Be sure


## How to run it
### `python3 uart_peripheral.py`
### Type "start"(enter) in the terminal. This will start sending via BLE UART jsons in the Format
```
        {
        	"pressure": 1.2,
        	"volume": 3.4,
        	"flow":6.1
        }
```
### You could type any other text and it will be send via BLE UART TX (you could read the value using an iOS device running nRF Toolbox app. Read: https://scribles.net/creating-ble-gatt-server-uart-service-on-raspberry-pi/) 

## How to kill it
CMD + Z
`sudo systemctl restart bluetooth.service`

## How to develop iOS App
In order to develop an iOS you can start using this example:
iOS Example Project
https://github.com/adafruit/Basic-Chat