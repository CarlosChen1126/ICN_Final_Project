import pygame

pygame.init()
WIDTH, HEIGHT = 16*50, 10*50
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

YELLOW_BACKGROUND = (232, 221, 203)
BUTTON_COLOR = (3, 101, 110)
BUTTON_PRESSED_COLOR = (3, 54, 73)
WORD_COLOR = (205, 179 ,128)
FONT = pygame.font.SysFont('Segoe UI Black', 25, False, False)

pygame.display.set_caption("ICN final project")

# button
set_up = FONT.render('SET UP', True, WORD_COLOR) 
play = FONT.render('PLAY', True, WORD_COLOR)
pause = FONT.render('PAUSE', True, WORD_COLOR)
teardown = FONT.render('TEARDOWN', True, WORD_COLOR)

def update_window():
    WIN.fill(YELLOW_BACKGROUND)
    
    mouse = pygame.mouse.get_pos()      
    if 5 <= mouse[0] <= WIDTH/4*1-50 and HEIGHT*9/10 <= mouse[1] <= HEIGHT-10:
        pygame.draw.rect(WIN, BUTTON_PRESSED_COLOR, [5,HEIGHT*9/10,WIDTH/4-50,40]) 
    else:
        pygame.draw.rect(WIN, BUTTON_COLOR, [5,HEIGHT*9/10,WIDTH/4-50,40])
    
    if WIDTH/4*1 <= mouse[0] <= WIDTH/4*2-50 and HEIGHT*9/10 <= mouse[1] <= HEIGHT-10:
        pygame.draw.rect(WIN, BUTTON_PRESSED_COLOR, [WIDTH/4,HEIGHT*9/10,WIDTH/4-50,40]) 
    else:
        pygame.draw.rect(WIN, BUTTON_COLOR, [WIDTH/4,HEIGHT*9/10,WIDTH/4-50,40])
    
    if WIDTH/4*2 <= mouse[0] <= WIDTH/4*3-50 and HEIGHT*9/10 <= mouse[1] <= HEIGHT-10:
        pygame.draw.rect(WIN, BUTTON_PRESSED_COLOR, [WIDTH/4*2,HEIGHT*9/10,WIDTH/4-50,40]) 
    else:
        pygame.draw.rect(WIN, BUTTON_COLOR, [WIDTH/4*2,HEIGHT*9/10,WIDTH/4-50,40])
    
    if WIDTH/4*3 <= mouse[0] <= WIDTH/4*4-20 and HEIGHT*9/10 <= mouse[1] <= HEIGHT-10:
        pygame.draw.rect(WIN, BUTTON_PRESSED_COLOR, [WIDTH/4*3,HEIGHT*9/10,WIDTH/4-20,40]) 
    else:
        pygame.draw.rect(WIN, BUTTON_COLOR, [WIDTH/4*3,HEIGHT*9/10,WIDTH/4-20,40])

    
    OFFSET = 35
    WIN.blit(set_up, (OFFSET, HEIGHT*9/10))
    WIN.blit(play, (WIDTH/4*1+OFFSET, HEIGHT*9/10))
    WIN.blit(pause, (WIDTH/4*2+OFFSET, HEIGHT*9/10))
    WIN.blit(teardown, (WIDTH/4*3+OFFSET/2, HEIGHT*9/10))
    pygame.display.update()
    
def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 5 <= mouse[0] <= WIDTH/4*1-50 and HEIGHT*9/10 <= mouse[1] <= HEIGHT-10:
                    print('set up')
                    # set up
                elif WIDTH/4*1 <= mouse[0] <= WIDTH/4*2-50 and HEIGHT*9/10 <= mouse[1] <= HEIGHT-10:
                    print('play')
                    # play
                elif WIDTH/4*2 <= mouse[0] <= WIDTH/4*3-50 and HEIGHT*9/10 <= mouse[1] <= HEIGHT-10:
                    print('pause')
                    # pause
                elif WIDTH/4*3 <= mouse[0] <= WIDTH/4*4-20 and HEIGHT*9/10 <= mouse[1] <= HEIGHT-10:
                    # teardown
                    run = False
        update_window()
    pygame.quit()
    

if __name__ == "__main__":
    main()