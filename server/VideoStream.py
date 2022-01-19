import cv2


class VideoStream:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.file = cv2.VideoCapture(filename)
        except:
            raise IOError
        self.frameNum = 0

    def nextFrame(self):
        """Get next frame."""
        '''
		data = self.file.read(5) # Get the framelength from the first 5 bits
		if data: 
			framelength = int(data)
							
			# Read the current frame
			data = self.file.read(framelength)
			self.frameNum += 1
		return data
		'''
        retval, image = self.file.read()
        data = None
        if retval:
            data = cv2.imencode('.jpg', image)[1].tostring()
            self.frameNum += 1
        return data

    def frameNbr(self):
        """Get frame number."""
        return self.frameNum
