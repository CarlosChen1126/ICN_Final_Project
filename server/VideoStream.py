import cv2


class VideoStream:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.file = cv2.VideoCapture(filename)
            self.frametime = 1/self.file.get(cv2.CAP_PROP_FPS)
        except:
            raise IOError
        self.frameNum = 0

    def nextFrame(self):
        """Get next frame."""
        retval, image = self.file.read()
        data = None
        if retval:
            data = cv2.imencode('.jpg', image)[1].tostring()
            self.frameNum += 1
        return data

    def frameNbr(self):
        """Get frame number."""
        return self.frameNum
