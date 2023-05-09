

import board
import busio
import binascii


from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
from adafruit_pn532.i2c import PN532_I2C


# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)

# Non-hardware reset/request with I2C
pn532 = PN532_I2C(i2c, debug=False)

# With I2C, we recommend connecting RSTPD_N (reset) to a digital pin for manual
# harware reset
# reset_pin = DigitalInOut(board.D6)
# On Raspberry Pi, you must also connect a pin to P32 "H_Request" for hardware
# wakeup! this means we don't need to do the I2C clock-stretch thing
# req_pin = DigitalInOut(board.D12)
# pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)


ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print("Waiting for RFID/NFC card to write to!")

key = b"\xFF\xFF\xFF\xFF\xFF\xFF"

while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    print(".", end="")
    # Try again if no card is available.
    if uid is not None:
        break

print("")

print("Found card with UID:", format(binascii.hexlify(uid)))
print("Authenticating block 4 ...")

authenticated = pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
if not authenticated:
    print("Authentication failed!")

# # Set 16 bytes of block to 0xFEEDBEEF
# data = bytearray(4)
# #data[0:16] = b"\xFE\xED\xBE\xEF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

block_choice = 12345678

# value = format(block_choice, 'x')

# while (6 > len(value)):
#     value = '0' + value
# data[0:4] = bytes.fromhex(value)
x = block_choice.to_bytes(16,"little")
print(x)

# # data[0:16] = bytes.fromhex(value)

# print(data)

# Write 16 byte block.
pn532.mifare_classic_write_block(4, x)
# Read block #6
print(
    "Wrote to block 4, now trying to read that data:",
    [hex(x) for x in pn532.mifare_classic_read_block(4)],
)