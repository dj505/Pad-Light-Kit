import board
import busio
import digitalio
import time
import ipaddress
import wifi
from adafruit_httpserver import Server, Request, Response, POST
import socketpool
import re
import json
import binascii

uart = busio.UART(board.GP4, board.GP5, baudrate=9600)

# Wifi stuff
ssid = "dkpepper"
pswd = "7808607880"
ip = "10.0.0.234"

ipv4 =  ipaddress.IPv4Address(ip)
netmask =  ipaddress.IPv4Address("255.255.255.0")
gateway =  ipaddress.IPv4Address("10.0.0.1")
wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)
#  connect to your SSID
wifi.radio.connect(ssid, pswd)

print("Connected to WiFi")
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

def webpage():
    html = f"""
    <!DOCTYPE html>
        <html>
            <head>
                <meta http-equiv="Content-type" content="text/html;charset=utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <script>
                  document.addEventListener("DOMContentLoaded", function() {{
                    var DL = document.getElementById('DL');
                    var UL = document.getElementById('UL');
                    var CN = document.getElementById('CN');
                    var UR = document.getElementById('UR');
                    var DR = document.getElementById('DR');

                    function handleFileUpload(event) {{
                      event.preventDefault();
                      const file = event.target.files[0];
                      const boardID = event.currentTarget.ID
                      const reader = new FileReader();

                      reader.onload = function() {{
                        const base64Image = reader.result.split(',')[1];
                        console.log(base64Image);
                        sendImageToServer(base64Image, boardID);
                      }};
                      reader.readAsDataURL(file);
                    }};

                    function sendImageToServer(base64Image, ID) {{
                      const data = {{
                        image: base64Image,
                        boardID: ID
                      }};

                      const jsonData = JSON.stringify(data);

                      console.log(jsonData);

                      // Send the POST request
                      fetch('http://{ip}', {{
                        method: 'POST',
                        mode: 'cors',
                        headers: {{
                          'Content-Type': 'application/json'
                        }},
                        body: jsonData
                      }})
                      .then(response => response.json())
                      .then(result => {{
                        // Handle the response from the server
                        console.log('Server response:', result);
                      }})
                      .catch(error => {{
                        // Handle any errors
                        console.error('Error:', error);
                      }});
                    }};

                    DL.addEventListener('change', handleFileUpload);
                    DL.ID = "DL"
                    UL.addEventListener('change', handleFileUpload);
                    UL.ID = "UL"
                    CN.addEventListener('change', handleFileUpload);
                    CN.ID = "CN"
                    UR.addEventListener('change', handleFileUpload);
                    UR.ID = "UR"
                    DR.addEventListener('change', handleFileUpload);
                    DR.ID = "DR"
                  }});
                </script>
            </head>
            <body>
                <title>Pad Light Kit Thing :)</title>
                <h1>Overkill Pad Light Kit File Upload</h1>
                <form id="uploadForm">
                    <label for="DL">DownLeft Pattern</label><br>
                    <input type="file" id="DL"><br><br>
                    <label for="UL">UpLeft Pattern</label><br>
                    <input type="file" id="UL"><br><br>
                    <label for="CN">Center Pattern</label><br>
                    <input type="file" id="CN"><br><br>
                    <label for="UR">UpRight Pattern</label><br>
                    <input type="file" id="UR"><br><br>
                    <label for="DR">DownRight Pattern</label><br>
                    <input type="file" id="DR"><br><br>
                    <button>Upload</button>
                </form>
                <p id="opTag"></p>
            </body>
        </html>
    """
    return html

def decode_image(data):
    image = binascii.a2b_base64(data)
    return image

def uart_write(boardid, imagedata):
    n = 32
    strbytes = bytearray(f"<{boardid},{imagedata}>")
    bytechunks = [strbytes[i:i + n] for i in range(0, len(strbytes), n)]
    print(bytechunks)
    print(f"Writing UART Data")
    for chunk in bytechunks:
        print(chunk)
        uart.write(chunk)
        time.sleep(0.2)
    return True

@server.route("/")
def base(request: Request):
    return Response(request, f"{webpage()}", content_type='text/html')

@server.route("/", POST)
def buttonpress(request: Request):
    #  get the raw text
    request_content = request.json()
    print(request_content)
    image = decode_image(request_content["image"])
    boardid = request_content["boardID"]
    print("Starting UART write...")
    if uart_write(boardid, image):
        print("Finished UART write")

    return Response(request, f"{webpage()}", content_type='text/html')

print("starting server...")
# startup the server
try:
    server.start(str(wifi.radio.ipv4_address))
    print("Listening on http://%s:80" % wifi.radio.ipv4_address)
#  if the server fails to begin, restart the pico w
except OSError:
    time.sleep(5)
    print("restarting...")
    microcontroller.reset()

ping_address = ipaddress.ip_address("8.8.4.4")
clock = time.monotonic()
while True:
    try:
        if (clock + 30) < time.monotonic():
            if wifi.radio.ping(ping_address) is None:
                # print("Disconnected!")
                continue
            else:
                # print("Still connected")
                continue

            clock = time.monotonic()
        server.poll()
    except Exception as e:
        print(e)
        continue
