import asyncio
import board
import digitalio
import neopixel
import struct

matrix = neopixel.NeoPixel(board.GP0, 25, brightness=1, auto_write=False)

sensor = digitalio.DigitalInOut(board.GP4)
sensor.direction = digitalio.Direction.INPUT
sensor.pull = digitalio.Pull.UP # Active low for testing purposes. Will be updated later.

frame_delay = 0.05 # Animation timing; adjust to change playback speed

# Bitmap reading (with padding)
# Most of this is magic. I barely understand it, but it does what it needs to do
with open("bitmap/image.bmp", "rb") as f:
    # Read the file header
    f.seek(10)
    offset = struct.unpack("<i", f.read(4))[0]

    # Read the image header
    f.seek(18)
    width, height = struct.unpack("<ii", f.read(8))

    # Create a 2D array to store the pixel data
    pixels = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]

    # Go to the pixel data
    f.seek(offset)

    # Read the pixel data
    for row in range(height - 1, -1, -1):
        for col in range(width):
            blue = ord(f.read(1))
            green = ord(f.read(1))
            red = ord(f.read(1))
            pixels[row][col] = (red, green, blue)

        # Calculate the number of padding bytes
        padding = (4 - (width * 3) % 4) % 4
        # Read the padding bytes and discard them
        f.read(padding)

pixels = sum(pixels, []) # Hacky magic to flatten the 2D list into a 1D list, because it doesn't need to be 2D.
                         # Will fix this later. Unless you're reading this, in which case it's a permanent feature now
frames = []
for i in range(0, len(pixels), 25): # Spritesheets should be vertical columns of 5x5 sprites for this project, or 25 "pixels" per sprite.
    frames.append(pixels[i:i + 25]) # This splits the list into 25 "pixel" long frames.

ctrl = asyncio.Event()
ctrl.clear()
animation_task = None

async def animate():
    matrix.brightness = 0.25
    while True:
        i = 0
        for frame in frames:
            for dot in frame:
                matrix[i] = dot
                i = 0 if (i+1) > 24 else i+1 # Necessary to prevent an index error
            matrix.show()
            await asyncio.sleep(frame_delay)
        await asyncio.sleep(0)

async def idle():
    i = 0
    for dot in frames[0]:
        matrix[i] = dot
        i = 0 if (i+1) > 24 else i+1
    matrix.brightness = 0.05
    matrix.show()

async def ctrl_detect():
    global animation_task
    while True:
        if not sensor.value:
            ctrl.set()
        else:
            ctrl.clear()
            if animation_task is not None:
                animation_task.cancel()
                animation_task = None
                idle_task = asyncio.create_task(idle())
                await idle_task
        await asyncio.sleep(0)

async def main():
    global animation_task
    idle_task = asyncio.create_task(idle())
    ctrl_task = asyncio.create_task(ctrl_detect())
    while True:
        if ctrl.is_set():
            if animation_task is None or animation_task.is_cancelled():
                animation_task = asyncio.create_task(animate())
            try:
                await animation_task
            except asyncio.CancelledError:
                pass
        else:
            await idle_task
        await asyncio.sleep(0)
    await asyncio.gather(ctrl_task, idle_task, animate_task)

asyncio.run(main())
