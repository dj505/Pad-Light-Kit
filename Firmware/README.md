# Making and Using Animations
To work properly, images must be formatted a specific way.  
You'll need:
* [GIMP](https://www.gimp.org/)
* Your spritesheet
    * Spritesheet must be 1 vertical column of 5x5 sprites
    * I like [Piskel](https://www.piskelapp.com) for making sprites but you can use whatever you'd like

# Instructions
1. Use your favourite pixel art animation editor thing to put together an animation. I like Piskel, since it makes this process easy. Make sure your canvas is 5x5 pixels!
2. Once your animation is ready, export it as a PNG image. **Make sure it's saved as 1 column, with as many rows as you have frames.**
3. Open up your image in GIMP, or your preferred image editing software. Re-export the image as a bitmap with **24 bit colour depth** and no special encoding stuff (make sure run length encoding is off!)
4. Drop your new bitmap spritesheet in the "Image" folder, with the filename `image.bmp`

Your animation should now display :) Example bitmaps will be provided once this project has been properly tested. If you don't see your animation, something probably went wrong with the settings chosen when exporting from GIMP. Double check that the colour depth is correct!
