import pygame

pygame.init() 
screen = pygame.display.set_mode((400,500))
clock = pygame.time.Clock()

test_surface = pygame.Surface((100, 200))
test_surface.fill((0,0,255))
#test_rect = pygame.Rect(100,200,100,100)
test_rect = test_surface.get_rect(topright = (200,255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #Dibuja todos los elementos
    screen.fill((175,215,70))
    #pygame.draw.ellipse(screen,pygame.Color('red'), test_rect)
    test_rect.left +=1
    screen.blit(test_surface, (200,250))
    #screen.blit(test_surface, test_rect)
    pygame.display.update()
    clock.tick(60) #no correra mas rapido que 60 por segundo
