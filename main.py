import pygame
import os

pygame.font.init()
pygame.mixer.init()


width, height = 900, 500   
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Battel Ship!")

white = (255, 255 , 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

border = pygame.Rect(width//2 - 5, 0, 10, height)

bullet_hit_sound = pygame.mixer.Sound('Assets/Spaceship Battle_Assets_Grenade+1.wav')
bullet_fire_sound = pygame.mixer.Sound('Assets/Spaceship Battle_Assets_Shot.wav')

health_font = pygame.font.SysFont('comicsans', 35)
winner_font = pygame.font.SysFont('comicsans', 100)

#Fotogramas por segundo
fps = 60
vel = 5
bullet_vel = 7
max_bullets = 4

spaceship_width, spaceship_height = 90, 70   

yellow_hip = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

yellow_spaceship_image = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(
    yellow_spaceship_image, (spaceship_width, spaceship_height)), 90)

red_spaceship_image = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
red_spaceship = pygame.transform.rotate(pygame.transform.scale(
    red_spaceship_image, (spaceship_width, spaceship_height)), 270)

space = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (width, height))


# Dibujamos lo que necesitamos en la pantalla
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    #El orden en el que dibujamos las cosas importa
    #Si dibujas la spaceship antes que el fondo, la spaceship no se verá

    win.blit(space, (0, 0))
    pygame.draw.rect(win, black, border)

    red_health_text = health_font.render("Health: " + str(red_health), 1, white)
    yellow_health_text = health_font.render("Health: " + str(yellow_health), 1, white)
    win.blit(red_health_text, (width - red_health_text.get_width() - 10, 10))
    win.blit(yellow_health_text, (10, 10))

    win.blit(yellow_spaceship, (yellow.x, yellow.y))
    win.blit(red_spaceship, (red.x, red.y))


    for bullet in red_bullets:
        pygame.draw.rect(win, red, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(win, yellow, bullet)

    #Actualiza la pantalla
    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - vel > 0: #LEFT
        yellow.x -= vel    
    if keys_pressed[pygame.K_d] and yellow.x + vel + yellow.width < border.x: #RIGHT
        yellow.x += vel
    if keys_pressed[pygame.K_w] and yellow.y - vel > 0: #UP
        yellow.y -= vel
    if keys_pressed[pygame.K_s] and yellow.y + vel + yellow.height < height- 15: #DOWN
        yellow.y += vel

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - vel > border.x + border.width: #LEFT
        red.x -= vel    
    if keys_pressed[pygame.K_RIGHT] and red.x + vel + red.width < width: #RIGHT
        red.x += vel
    if keys_pressed[pygame.K_UP] and red.y - vel > 0: #UP
        red.y -= vel
    if keys_pressed[pygame.K_DOWN] and red.y + vel + red.height < height - 15: #DOWN
        red.y += vel

#Esta función se encarga del movimiento de las balas, de la colisión de éstas
#y de eliminarlas cuando se salen de la pantalla
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)

        elif bullet.x > width:
            yellow_bullets.remove(bullet)
        
    
    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hip))
            red_bullets.remove(bullet)
        
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = winner_font.render(text, 1, white)
    win.blit(draw_text, (width/2 - draw_text.get_width() / 
                        2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

#Función principal
def main():
    #Estos rectángulos representan las spaceship
    red = pygame.Rect(700, 300, spaceship_width, spaceship_height)
    yellow = pygame.Rect(100, 300, spaceship_width, spaceship_height)

    red_bullets = []
    yellow_bullets = []

    red_health = 20
    yellow_health = 20

    clock = pygame.time.Clock()
    run = True

    while run:
        #Se encarga de que este bucle se repita 60 veces por segundo
        clock.tick(fps)

        #pygame.event.get() es una lista con todos los eventos
        #de pygame. Con el bucle for la recorremos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 + 5, 10, 5)
                    yellow_bullets.append(bullet)
                    bullet_fire_sound.play()
                
                #Se utilizan dos // en la división para que el resultado sea un número entero
                if event.key == pygame.K_RCTRL and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 + 5, 10, 5)
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()
                
            if event.type == red_hit:
                red_health -= 1
                bullet_hit_sound.play()

            if event.type ==yellow_hip:
                yellow_health -= 1
                bullet_hit_sound.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
  
        
        #Devuelve una lista con las teclas presionadas
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)


    main()          

#Este if comprueba si el fichero se llama main
if __name__ == "__main__":
    main()