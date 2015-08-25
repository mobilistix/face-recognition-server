from PIL import Image
from io import BytesIO

# Image.DEBUG=1
# Image.init()

# works
im = Image.open('/tmp/test.jpg')
print(im.format, im.size, im.mode)
im.close()

file_ = open('/tmp/test.jpg','rb')
b  = file_.read()
file_.close()
print('read file with ',len(b), ' bytes')

im = Image.open(BytesIO(b))
print('format: ', im.format, ', mode: ', im.mode, ', size: ', im.size, ', width: ', im.width, ', height: ', im.height)



# image = Image.fromarray(b2)
# view = b2.getbuffer()
# image2 = Image.fromarray(view)


# failes
## decoder = "jpeg"
## mode = "RGB"
## im_size = 320, 240 
## image = Image.frombytes(mode, im_size, b, decoder, None)

print('done')
# OUTPUT
# JPEG (320, 240) RGB
# read file with  16143  bytes
# Traceback (most recent call last):
#   File "piltest.py", line 17, in <module>
#     image = Image.frombytes(mode, im_size, b, decoder, None)
#   File "/root/.virtualenvs/cv/lib/python3.4/site-packages/PIL/Image.py", line 2085, in frombytes
#     im.frombytes(data, decoder_name, args)
#   File "/root/.virtualenvs/cv/lib/python3.4/site-packages/PIL/Image.py", line 741, in frombytes
#     d = _getdecoder(self.mode, decoder_name, args)
#   File "/root/.virtualenvs/cv/lib/python3.4/site-packages/PIL/Image.py", line 418, in _getdecoder
#     return decoder(mode, *args + extra)
# TypeError: function takes at least 3 arguments (2 given)
# 
