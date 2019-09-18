from PIL import Image
import tempfile

def readimg(content):
    f=tempfile.TemporaryFile()
    f.write(content)
    return Image.open(f)
