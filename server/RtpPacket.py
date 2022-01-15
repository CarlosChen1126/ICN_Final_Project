from time import time
HEADER_SIZE = 16 #12 + 4

class RtpPacket:
	def __init__(self):
		pass	
	def encode(self, Ver, P, X, CC, M, PT, SeqNum, SSI, CI, payload):
		#Time Stamps
		TS = int(time())
		#construct header
		self.header = bytearray(HEADER_SIZE)
		self.header[0] = self.header[0] | (Ver & 0x03) << 6		#2bit
		self.header[0] = self.header[0] | (P   & 0x01) << 5		#1bit
		self.header[0] = self.header[0] | (X   & 0x01) << 4		#1bit
		self.header[0] = self.header[0] | (CC  & 0x0F) 			#4bit
		self.header[1] = self.header[1] | (M   & 0x01) << 7		#1bit
		self.header[1] = self.header[1] | (PT  & 0x7F) 			#7bit
		self.header[2] = (SeqNum >> 8  & 0xFF)					#SeqNum first 8 bit
		self.header[3] = (SeqNum  	   & 0xFF) 					#SeqNum second 8 bit
		self.header[4] = (TS >> 24  & 0xFF) 					#TS 32 bit
		self.header[5] = (TS >> 16  & 0xFF)  
		self.header[6] = (TS >>  8  & 0xFF)	
		self.header[7] = (TS        & 0xFF)	
		self.header[8] = (SSI >> 24  & 0xFF) 					#SSI 32 bit
		self.header[9] = (SSI >> 16  & 0xFF)  
		self.header[10] = (SSI >>  8  & 0xFF)	
		self.header[11] = (SSI        & 0xFF)	
		self.header[12] = (CI >> 24  & 0xFF) 					#CI 32 bit
		self.header[13] = (CI >> 16  & 0xFF)  
		self.header[14] = (CI >>  8  & 0xFF)	
		self.header[15] = (CI        & 0xFF)	
		#construct payload
		self.payload = 	payload
	def decode(self, byteStream):
		#拿到byte stream之後拆成header跟payload
		self.header = bytearray(byteStream[:HEADER_SIZE])
		self.payload = byteStream[HEADER_SIZE:]
	def version(self):
		return int(self.header[0] >> 6)
	def payloadType(self):
		return self.header[1] & 0x7F
	def seqNum(self):
		return int(self.header[2] << 8  | self.header[3])
	def timestamp(self):
		timestamp = (self.header[4] << 24) | (self.header[5] << 16) | (self.header[6] << 8) | self.header[7]
		return int(timestamp)
	def getPayload(self):
		return self.payload
	def getPacket(self):
		return self.header + self.payload