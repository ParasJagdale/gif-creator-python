# Create a GIF with Python 🎞️


import imageio.v3 as iio

filenames = ['img1.jpg', 'img2.jpg']
images = [ ]

for filename in filenames:
  images.append(iio.imread(filename))

iio.imwrite('horse.gif', images, duration = 1000, loop = 0)