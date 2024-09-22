Raspberry Pico W Workspace

In docker environment everything required to work with Pico W should be present inside conda environment named `domi`.

## How to work with ampy:

To list files on the Pico:
* ampy --port /dev/ttyUSB0 ls

To upload a file to the Pico:
* ampy --port /dev/ttyUSB0 put your_file.py

To download a file from the Pico:
* ampy --port /dev/ttyUSB0 get remote_file.py local_file.py

To remove a file from the Pico:
* ampy --port /dev/ttyUSB0 rm your_file.py

To run a Python script on the Pico:
* ampy --port /dev/ttyUSB0 run your_script.py
  * add -n to skip waiting for answer, required if program has infinite loop without output

Replace /dev/ttyUSB0 with the actual serial port of your Pico.
