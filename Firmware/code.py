import asyncio
import board
import digitalio
import neopixel
import struct

matrix = neopixel.NeoPixel(board.GP0, 25, brightness=1, auto_write=False)

sensor = digitalio.DigitalInOut(board.GP4)
sensor.direction = digitalio.Direction.INPUT
sensor.pull = digitalio.Pull.DOWN

frame_delay = 0.05 # Time between frames. Adjust to change playback speed
idle_brightness = 0.125
anim_brightness = 1

# Bitmap reading (with padding)
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
for i in range(0, len(pixels), 25):
    pixels[i + 5:i + 10] = pixels[i + 5:i + 10][::-1]   # The LED matrix is wired in alternating rows.
    pixels[i + 15:i + 20] = pixels[i + 15:i + 20][::-1] # As such, every 2nd "row" of each frame needs
    frames.append(pixels[i:i + 25])                     # to be mirrored.

ctrl = asyncio.Event() # Event to communicate whether the lights should be on or off to every async process
ctrl.clear() # Clear the event, so it's set as "False"
animation_task = None # Define the animation task as a global varbiale for ease of use. Don't cancel me for this, async is hard :(

async def animate(): # Self explanatory. Loops while animating
    matrix.brightness = anim_brightness
    while True:
        i = 0
        for frame in frames: # Loop through every frame, each made up of a 25 element long list holding the colour values for each pixel
            for dot in frame: # Loop through the colour values
                matrix[i] = dot # Assign the colour value to every LED in the matrix (actually just a strip of 25 LEDs chopped up, so we can treat it as one strip)
                i = 0 if (i+1) > 24 else i+1 # Necessary to prevent an index error
            matrix.show()
            await asyncio.sleep(frame_delay) # Async sleep, to make sure other code has time to run, as well as to keep the animation constrained to a certain speed
        await asyncio.sleep(0)

async def idle(): # Displays a single still frame, specifically the first frame in the animation, while panel isn't being held.
    i = 0
    for dot in frames[0]: # Only needs one loop because only the first frame is being accessed
        matrix[i] = dot   # Otherwise works identically to the animate() routine
        i = 0 if (i+1) > 24 else i+1 # Same deal as before
    matrix.brightness = idle_brightness
    matrix.show()

async def ctrl_detect():  # Constantly reads the state of the sensor pin to check if the panel should be animating.
    global animation_task # The signal is active high, so the 12V line that normally powers the panel's original LEDs
    while True:           # is going through a voltage divider to bring it down to a 3V "high" signal.
        if sensor.value:
            ctrl.set() # Set the "ctrl" event to "True" to tell the other subroutines that the animation should be playing
        else:
            ctrl.clear() # Clear the "ctrl" event to tell the other subroutines that the animation should stop, and the idle task should start
            if animation_task is not None: # Immediately stop the animation task if it's still playing.
                animation_task.cancel()    # Otherwise, the animation task and the idle task with clash,
                animation_task = None      # resulting in an unpleasant blinking effect.
                idle_task = asyncio.create_task(idle()) # Create and run the idle task.
                await idle_task
        await asyncio.sleep(0) # Allow other tasks time to execute

async def main(): # Main loop. Should be pretty self explanatory. Probably lots of redundant code here - might refactor later
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
