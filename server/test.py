########Only for TEST########
import base64
with open("test.jpg", "rb") as imageFile:
    str = base64.encodebytes(imageFile.read())
    print(len(str))
with open("tex.jpg", 'wb') as writeFile:
    img = base64.decodebytes(str)
    writeFile.write(img)
