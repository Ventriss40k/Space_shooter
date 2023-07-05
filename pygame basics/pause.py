import pygame
from pygame.constants import QUIT
pygame.init()

# This code allows to stop action in game and draw a menu
# In menu there are 2 buttons - continue and exit
# To unpause and exit program respectively
# also ESC - toggles pause
# Buttons are highlighted, when hovered over

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
bg = pygame.Surface((screen_width, screen_height))
bg.fill("black")


#  Imitation of somethong happening ---------------------------------------------
class Ufo(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,20))
        self.image.fill("green")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.pos = [x,y]
        self.x_speed = 2
        self.y_speed = 1
        self.x_range = 200, 600
        self.y_range = 100, 500

    def update(self):
        self.pos[0] += self.x_speed
        self.pos[1] += self.y_speed
        self.rect.center = self.pos
        if self.rect.centerx <self.x_range[0]:
            self.x_speed *= -1
        if self.rect.centerx >self.x_range[1]:
            self.x_speed *= -1

        if self.rect.centery <self.y_range[0]:
            self.y_speed *= -1
        if self.rect.centery >self.y_range[1]:
            self.y_speed *= -1
ufo1 = Ufo(400,300)
ufo2 = Ufo(300,100)
ufo3 = Ufo(200,200)
ufo4 = Ufo(500,100)
sprites_to_add = [ufo1, ufo2, ufo3, ufo4]
object_group = pygame.sprite.Group()
object_group.add(sprites_to_add)
# ---------------------------------------------


class Button(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        pygame.sprite.Sprite.__init__(self)
        self.font_normal = pygame.font.SysFont(None, 80)
        self.font_hover = pygame.font.SysFont(None, 90)
        self.font = self.font_normal
        self.text = text
        self.pos = list(pos)
        self.image = self.font.render(text, True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        self.mouse_pointed = False



    def mouse_hover_on(self):
        self.font_update()
        self.font = self.font_hover
        self.mouse_pointed = True


    def mouse_hover_off(self):
        self.font_update()
        self.font = self.font_normal
        self.mouse_pointed = False

    def font_update(self):
        self.image = self.font.render(self.text, True, (pygame.color.Color("Green")))


resume_button = Button("Resume",  (screen_width//2, screen_height//2-2))
exit_button = Button("Quit", (screen_width//2, screen_height//2+100))


pause_menu_buttons = pygame.sprite.Group()
pause_menu_buttons.add(resume_button, exit_button)
# get optimal menu width
pause_menu_width = 0
for i in pause_menu_buttons:
    if i.rect.width > pause_menu_width:
        pause_menu_width = i.rect.width
pause_menu_width *= 1.5

# get optimal menu height
pause_menu_height = 30
for i in pause_menu_buttons: 
    pause_menu_height += i.rect.height * 1.2
pause_menu_height *= 1.3 




pause_menu_rect = pygame.Rect(0,0,pause_menu_width, pause_menu_height)
pause_menu_rect.center = (screen_width//2, screen_height//2)

button_space = pause_menu_height/len(pause_menu_buttons) # button height + top, down padding

#adjusting buttons position in menu
n_button = 0
for i in pause_menu_buttons: 
    n_button += 1
    i.rect.centerx = pause_menu_rect.centerx 
    i.pos[0] = pause_menu_rect.centerx 
    i.rect.centery = pause_menu_rect.top + (button_space * n_button - button_space//2 )
    i.pos[1]= pause_menu_rect.top + (button_space * n_button - button_space//2 )

paused = False


FPS = pygame.time.Clock()
is_working = True
font = pygame.font.SysFont(None, 24)



while is_working:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
        if event.type == pygame.MOUSEBUTTONDOWN and resume_button.mouse_pointed:
            paused = not paused
            print("Click on resume")
        if event.type == pygame.MOUSEBUTTONDOWN and exit_button.mouse_pointed:
            print("Click on exit")
            is_working = False          

    if paused:
        #menu background
        # pygame.draw.rect(screen, (255, 255, 255), (50, 50, 300, 300))
        pygame.draw.rect(screen, (255, 255, 255), pause_menu_rect)
        
        # check for mouse hover and update fonts of buttons
        if resume_button.rect.collidepoint(pygame.mouse.get_pos()):
            resume_button.mouse_hover_on()
        else:
            resume_button.mouse_hover_off()

        if exit_button.rect.collidepoint(pygame.mouse.get_pos()):
            exit_button.mouse_hover_on()
        else:
            exit_button.mouse_hover_off()

        pause_menu_buttons.draw(screen)

        

    else:
    #  Imitation of somethong happening ---------------------------------------------
        screen.blit(bg,(0,0))
        object_group.update()
        object_group.draw(screen)
    # ---------------------------------------------
    pygame.display.flip()