import sys, os
import pygame
from clientworker import Clientworker
import threading


class PlayerWindow:
    def __init__(self, HOST, PORT):
        # Init
        pygame.init()
        self.WIDTH, self.HEIGHT = 16*60, 9*60
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.YELLOW_BACKGROUND = (232, 221, 203)
        self.BUTTON_COLOR = (3, 101, 110)
        self.BUTTON_PRESSED_COLOR = (3, 54, 73)
        self.WORD_COLOR = (205, 179, 128)
        self.FONT = pygame.font.SysFont('Segoe UI Black', int(self.WIDTH/25), False, False)
        pygame.display.set_caption("ICN final project")
        self.clock = pygame.time.Clock()
        self.cache_name = 'test_res.jpg'

        # address# & port#  e.g.:'127.0.0.1', 8888
        self.send_and_receive = Clientworker()
        self.send_and_receive.connectToServer(HOST, PORT)
        response = self.send_and_receive.rtspclient.recv(1024).decode("utf-8")

        # Settings
        color_inactive = (205, 179, 128)
        color_active = (100, 100, 200)
        color = color_inactive
        text = ""
        active = False

        # Font
        font = pygame.font.Font(None, 32)

        # Input box
        input_box = pygame.Rect(100, 100, 140, 32)
        run = True
        while(run):
            self.WIN.fill(self.YELLOW_BACKGROUND)
            offset = self.WIDTH/50
            message = self.FONT.render(response, True, self.WORD_COLOR)
            input_message = self.FONT.render('Which video would you like to watch?', True, self.WORD_COLOR)
            self.WIN.blit(message, (self.WIDTH/4*1+offset, self.HEIGHT*2/10))
            self.WIN.blit(input_message, (self.WIDTH/10*1+offset, self.HEIGHT*4/10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    active = True if input_box.collidepoint(event.pos) else False

                    # Change the current color of the input box
                    color = color_active if active else color_inactive

                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            input_file = text
                            text = ""
                            self.send_and_receive.fileName = str("./video/"+input_file)
                            self.send_and_receive.sendRtspRequest('SETUP')
                            response = self.send_and_receive.rtspclient.recv(1024).decode("utf-8")
                            lines = response.split('\n')
                            seqNum = int(lines[1].split(' ')[1])
                            # only handle right sequence number
                            if(self.send_and_receive.rtspSeq == seqNum):

                                if(int(lines[0].split(' ')[1]) == 200):
                                    self.send_and_receive.state = "SETUP"
                                    format = int(lines[3].split(' ')[1])
                                    channel = int(lines[4].split(' ')[1])
                                    rate = int(lines[5].split(' ')[1])
                                    self.send_and_receive.stream = self.send_and_receive.p.open(
                                        format = format,
                                        channels = channel,
                                        rate = rate,
                                        output = True
                                    )
                                    self.send_and_receive.constructRTPclient()
                                    threading.Thread(target=self.send_and_receive.write_video).start()
                                    threading.Thread(target=self.send_and_receive.write_audio).start()
                                    threading.Thread(target=self.send_and_receive.play_audio).start()
                                    threading.Thread(target=self.send_and_receive.recvRtspResponse).start()
                                    run = False
                                else:
                                    #file not found
                                    response = 'File not found. Try again: '
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            # Input box
            text_surface = font.render(text, True, color)
            input_box_width = max(200, text_surface.get_width()+10)
            input_box.w = input_box_width
            input_box.center = (self.WIDTH/2, self.HEIGHT/1.8)

            # Updates
            self.WIN.blit(text_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(self.WIN, color, input_box, 3)
            pygame.display.flip()
            pygame.display.update()

    def update_window(self):
        self.WIN.fill(self.YELLOW_BACKGROUND)

        if (self.send_and_receive.state == "PLAY"):
            if(self.send_and_receive.videobuffer[self.send_and_receive.videoframe%200] != 0 and self.send_and_receive.videoframe <= self.send_and_receive.videorecordframe):
                #update frame
                bytedata = self.send_and_receive.videobuffer[self.send_and_receive.videoframe%200]
                self.send_and_receive.image_decode(self.cache_name, bytedata)
                self.send_and_receive.videoframe += 1
            try:
                picture = pygame.image.load(self.cache_name)
                image_rect = picture.get_rect(center=self.WIN.get_rect().center)
                width = image_rect.right - image_rect.left
                height = image_rect.bottom - image_rect.top
                if (width*self.HEIGHT <= height*self.WIDTH):
                    picture = pygame.transform.scale(picture, (int(self.HEIGHT*9/10*width/height), int(self.HEIGHT*9/10)))
                    self.WIN.blit(picture, ((self.WIDTH - self.HEIGHT*9/10*width/height)/2,0))
                else:
                    picture = pygame.transform.scale(picture, (int(self.WIDTH), int(self.WIDTH/width*height)))
                    self.WIN.blit(picture, (0,0))
            except:
                pass

        elif (self.send_and_receive.state == "PAUSE" or self.send_and_receive.state == "OFF"):
            picture = pygame.image.load(self.cache_name)
            image_rect = picture.get_rect(center=self.WIN.get_rect().center)
            width = image_rect.right - image_rect.left
            height = image_rect.bottom - image_rect.top
            if (width*self.HEIGHT <= height*self.WIDTH):
                picture = pygame.transform.scale(picture, (int(self.HEIGHT*9/10*width/height), int(self.HEIGHT*9/10)))
                self.WIN.blit(picture, ((self.WIDTH - self.HEIGHT*9/10*width/height)/2,0))
            else:
                picture = pygame.transform.scale(picture, (int(self.WIDTH), int(self.WIDTH/width*height)))
                self.WIN.blit(picture, (0,0))

        # button & press
        pygame.draw.rect(self.WIN, self.BUTTON_COLOR, [
                             0, self.HEIGHT*9/10, self.WIDTH, self.HEIGHT/10])
        mouse = pygame.mouse.get_pos()
        if 0 <= mouse[0] < self.WIDTH/4*1 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT:
            pygame.draw.rect(self.WIN, self.BUTTON_PRESSED_COLOR, [
                             0, self.HEIGHT*9/10, self.WIDTH/4, self.HEIGHT/10])

        if self.WIDTH/4*1 <= mouse[0] < self.WIDTH/4*2 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT:
            pygame.draw.rect(self.WIN, self.BUTTON_PRESSED_COLOR, [
                             self.WIDTH/4, self.HEIGHT*9/10, self.WIDTH/4, self.HEIGHT/10])

        if self.WIDTH/4*2 <= mouse[0] < self.WIDTH/4*3 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT:
            pygame.draw.rect(self.WIN, self.BUTTON_PRESSED_COLOR, [
                             self.WIDTH/4*2, self.HEIGHT*9/10, self.WIDTH/4, self.HEIGHT/10])

        if self.WIDTH/4*3 <= mouse[0] <= self.WIDTH/4*4 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT:
            pygame.draw.rect(self.WIN, self.BUTTON_PRESSED_COLOR, [
                             self.WIDTH/4*3, self.HEIGHT*9/10, self.WIDTH/4, self.HEIGHT/10])

        # word
        
        play = self.FONT.render('Play', True, self.WORD_COLOR)
        pause = self.FONT.render('Pause', True, self.WORD_COLOR)
        
        offset = self.WIDTH/50
        self.WIN.blit(play, (self.WIDTH/4*1+offset, self.HEIGHT*9/10))
        self.WIN.blit(pause, (self.WIDTH/4*2+offset, self.HEIGHT*9/10))

        pygame.display.update()

    def window_handler(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if 5 <= mouse[0] <= self.WIDTH/4*1-50 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT-10:
                        pass
                        # slower
                    elif self.WIDTH/4*1 <= mouse[0] <= self.WIDTH/4*2-50 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT-10:
                        print('play')
                        self.send_and_receive.sendRtspRequest('PLAY')
                    elif self.WIDTH/4*2 <= mouse[0] <= self.WIDTH/4*3-50 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT-10:
                        print('pause')
                        self.send_and_receive.sendRtspRequest('PAUSE')
                    elif self.WIDTH/4*3 <= mouse[0] <= self.WIDTH/4*4-20 and self.HEIGHT*9/10 <= mouse[1] <= self.HEIGHT-10:
                        pass
                        # faster
            self.update_window()
            self.clock.tick(30)
        self.send_and_receive.sendRtspRequest('TEARDOWN')
        try:
            os.remove(self.cache_name)
        except OSError as e:
            print(e)
        pygame.quit()


if __name__ == "__main__":
    HOST, PORT = sys.argv[1], int(sys.argv[2])
    player = PlayerWindow(HOST, PORT)
    player.window_handler()
