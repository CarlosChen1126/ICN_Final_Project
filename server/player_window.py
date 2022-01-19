import sys
import pygame
from clientworker import Clientworker
import threading
from RtpPacket import RtpPacket


class PlayerWindow:
    def __init__(self, HOST, PORT):
        pygame.init()
        self.WIDTH, self.HEIGHT = 16*60, 10*60
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.YELLOW_BACKGROUND = (232, 221, 203)
        self.BUTTON_COLOR = (3, 101, 110)
        self.BUTTON_PRESSED_COLOR = (3, 54, 73)
        self.WORD_COLOR = (205, 179, 128)
        self.FONT = pygame.font.SysFont(
            'Segoe UI Black', int(self.WIDTH/30), False, False)

        pygame.display.set_caption("ICN final project")

        self.send_and_receive = Clientworker()
        # address# & port#  e.g.:'127.0.0.1', 8888
        self.send_and_receive.connectToServer(HOST, PORT)
        self.send_and_receive.sendRtspRequest('SETUP')

    def update_window(self):
        self.WIN.fill(self.YELLOW_BACKGROUND)

        if (self.send_and_receive.state == "PLAY"):
            response = self.send_and_receive.rtpclient.recv(65535)
            if response:
                rtp = RtpPacket()
                rtp.decode(response)
                print('payload: ', len(rtp.getPayload()))
                bytedata = rtp.getPayload()
                cache_name = "test_res.jpg"
                self.send_and_receive.image_decode(cache_name, bytedata)
            else:
                # movie end
                self.send_and_receive.state = "PAUSE"
            picture = pygame.image.load('test_res.jpg')
            #picture = pygame.transform.scale(picture, (self.WIDTH, self.HEIGHT*9/10))
            self.WIN.blit(picture, (0, 0))
        elif (self.send_and_receive.state == "PAUSE"):
            picture = pygame.image.load('test_res.jpg')
            #picture = pygame.transform.scale(picture, (self.WIDTH, self.HEIGHT*9/10))
            self.WIN.blit(picture, (0, 0))

        # button & press
        mouse = pygame.mouse.get_pos()
        if 5 <= mouse[0] <= self.WIDTH/4*1-50 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT-10:
            pygame.draw.rect(self.WIN, self.BUTTON_PRESSED_COLOR, [
                             5, self.HEIGHT*9/10, self.WIDTH/4-50, self.HEIGHT/10])
        else:
            pygame.draw.rect(self.WIN, self.BUTTON_COLOR, [
                             5, self.HEIGHT*9/10, self.WIDTH/4-50, self.HEIGHT/10])

        if self.WIDTH/4*1 <= mouse[0] <= self.WIDTH/4*2-50 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT-10:
            pygame.draw.rect(self.WIN, self.BUTTON_PRESSED_COLOR, [
                             self.WIDTH/4, self.HEIGHT*9/10, self.WIDTH/4-50, self.HEIGHT/10])
        else:
            pygame.draw.rect(self.WIN, self.BUTTON_COLOR, [
                             self.WIDTH/4, self.HEIGHT*9/10, self.WIDTH/4-50, self.HEIGHT/10])

        if self.WIDTH/4*2 <= mouse[0] <= self.WIDTH/4*3-50 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT-10:
            pygame.draw.rect(self.WIN, self.BUTTON_PRESSED_COLOR, [
                             self.WIDTH/4*2, self.HEIGHT*9/10, self.WIDTH/4-50, self.HEIGHT/10])
        else:
            pygame.draw.rect(self.WIN, self.BUTTON_COLOR, [
                             self.WIDTH/4*2, self.HEIGHT*9/10, self.WIDTH/4-50, self.HEIGHT/10])

        if self.WIDTH/4*3 <= mouse[0] <= self.WIDTH/4*4-20 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT-10:
            pygame.draw.rect(self.WIN, self.BUTTON_PRESSED_COLOR, [
                             self.WIDTH/4*3, self.HEIGHT*9/10, self.WIDTH/4-20, self.HEIGHT/10])
        else:
            pygame.draw.rect(self.WIN, self.BUTTON_COLOR, [
                             self.WIDTH/4*3, self.HEIGHT*9/10, self.WIDTH/4-20, self.HEIGHT/10])

        # word
        slower = self.FONT.render('Slower', True, self.WORD_COLOR)
        play = self.FONT.render('Play', True, self.WORD_COLOR)
        pause = self.FONT.render('Pause', True, self.WORD_COLOR)
        faster = self.FONT.render('Faster', True, self.WORD_COLOR)
        offset = self.WIDTH/50
        self.WIN.blit(slower, (offset, self.HEIGHT*9/10))
        self.WIN.blit(play, (self.WIDTH/4*1+offset, self.HEIGHT*9/10))
        self.WIN.blit(pause, (self.WIDTH/4*2+offset, self.HEIGHT*9/10))
        self.WIN.blit(faster, (self.WIDTH/4*3+offset/2, self.HEIGHT*9/10))

        pygame.display.update()

    def window_handler(self):
        run = True
        threading.Thread(target=self.send_and_receive.recvRtspResponse).start()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if 5 <= mouse[0] <= self.WIDTH/4*1-50 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT-10:
                        print('slower')
                        # slower
                    elif self.WIDTH/4*1 <= mouse[0] <= self.WIDTH/4*2-50 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT-10:
                        print('play')
                        self.send_and_receive.sendRtspRequest('PLAY')
                    elif self.WIDTH/4*2 <= mouse[0] <= self.WIDTH/4*3-50 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT-10:
                        print('pause')
                        self.send_and_receive.sendRtspRequest('PAUSE')
                    elif self.WIDTH/4*3 <= mouse[0] <= self.WIDTH/4*4-20 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT-10:
                        print('faster')
                        # faster
            self.update_window()
        self.send_and_receive.sendRtspRequest('TEARDOWN')
        pygame.quit()


if __name__ == "__main__":
    test1 = PlayerWindow(sys.argv[1], int(sys.argv[2]))
    test1.window_handler()

    '''
    t_list = []

    test1 = PlayerWindow()
    t1 = threading.Thread(target = test1.window_handler)
    t_list.append(t1)
    test2 = PlayerWindow()
    t2 = threading.Thread(target = test2.window_handler)
    t_list.append(t2)

    for t in t_list:
        t.start()
    for t in t_list:
        t.join()
    '''
