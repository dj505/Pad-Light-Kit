import asyncio
import board
import digitalio
import neopixel
from bmp_reader import BMPReader

img = BMPReader("bitmap/image.bmp")

matrix = neopixel.NeoPixel(board.GP0, 25, brightness=1, auto_write=False)
sheet = img.get_pixels()
frames = []

sensor = digitalio.DigitalInOut(board.GP4)
sensor.direction = digitalio.Direction.INPUT
sensor.pull = digitalio.Pull.UP # Active low for testing purposes. Will be updated later.

frame_delay = 0.05 # Animation timing; adjust to change playback speed

for i in range(0, img.height, 25): # Spritesheets should be vertical columns of 5x5 sprites for this project, or 25 "pixels" per sprite.
    frames.append(sheet[i:i + 25])

ctrl = asyncio.Event()
ctrl.clear()
animation_task = None

async def animate():
    while True:
        i = 0
        for frame in frames[i]:
            for dot in frame:
                matrix[i] = dot
                i = 0 if (i+1) > 24 else i+1
            matrix.brightness = 1
            matrix.show()
            await asyncio.sleep(frame_delay)
        await asyncio.sleep(0)
        
async def idle():
    i = 0
    for dot in frames[0][0]:
        matrix[i] = dot
        i += 1
    matrix.brightness = 0.1
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