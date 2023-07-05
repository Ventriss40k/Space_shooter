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
    def __init__(self, text, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.font_normal = pygame.font.SysFont(None, 80)
        self.font_hover = pygame.font.SysFont(None, 90)
        self.font = self.font_normal
        self.text = text
        self.pos = [x, y]
        self.image = self.font.render(text, True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
        self.mouse_pointed = False

    def update(self):
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]
    
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.mouse_hover_on()
        else:
            self.mouse_hover_off()


    def mouse_hover_on(self):
        self.font_update()
        self.font = self.font_hover
        self.mouse_pointed = True


    def mouse_hover_off(self):
        self.font_update()
        self.font = self.font_normal
        self.mouse_pointed = False

    def font_update(self):
        self.image = self.font.render(self.text, True, (pygame.color.Color("Green3")))

class PauseMenu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.buttons_group = pygame.sprite.Group()   
        self.resume_button = Button("Resume", 0, 0)
        self.exit_button = Button("Quit", 0, 0)
        # self.settings_button = Button("Settings", 0, 0)
        # self.save_button = Button("Save", 0, 0)
        # self.load_button = Button("Load", 0, 0)
        self.buttons_list = [self.resume_button, self.exit_button]

        # self.buttons_list = [self.resume_button, self.settings_button, self.save_button, self.load_button, self.exit_button]
        self.button_height = self.resume_button.rect.height
        self.button_padding_multiplyer = 1.3
        self.per_button_height =  self.button_height * self.button_padding_multiplyer 
        self.menu_width = max(self.buttons_list, key=lambda button: button.rect.width).rect.width * 1.5 
        self.menu_height = len(self.buttons_list) * self.per_button_height
        self.rect = pygame.Rect(0,0,self.menu_width, self.menu_height)
        self.rect.center = (screen_width//2, screen_height//2)
        n_button = 0
        for i in self.buttons_list: 
            n_button += 1  
            i.pos = [self.rect.centerx,self.rect.top + self.per_button_height*n_button - self.per_button_height//2 ]
            self.buttons_group.add(i)
    def update(self):
        pygame.draw.rect(screen, pygame.color.Color("ivory3"), self.rect)
        self.buttons_group.update()
        self.buttons_group.draw(screen)




paused = False


FPS = pygame.time.Clock()
is_working = True
font = pygame.font.SysFont(None, 24)
pause_menu = PauseMenu()


while is_working:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
        if event.type == pygame.MOUSEBUTTONDOWN and pause_menu.resume_button.mouse_pointed:
            paused = not paused
            print("Click on resume")
        if event.type == pygame.MOUSEBUTTONDOWN and pause_menu.exit_button.mouse_pointed:
            print("Click on exit")
            is_working = False          

    if paused:
        pause_menu.update()
    else:
    #  Imitation of somethong happening ---------------------------------------------
        screen.blit(bg,(0,0))
        object_group.update()
        object_group.draw(screen)
    # ---------------------------------------------
    pygame.display.flip()