import pygame
from player import Player
from client import Client
pygame.init()

with open("main.ini", "r") as f:
    config_data = f.readlines()
    host = config_data[1].split("=")[1].strip()
    port = int(config_data[2].split("=")[1].strip())
HOST, PORT = host, port

try:
    client = Client((HOST, PORT))
except ConnectionRefusedError:
    # Создаем всплывающее окно с сообщением об ошибке
    error_window = pygame.display.set_mode((300, 200))
    error_font = pygame.font.SysFont("Arial", 24)
    error_text = error_font.render("Сервер не найден или вы\nбыли им заблокированы!", True, (255, 0, 0))
    error_text_rect = error_text.get_rect(center=(150, 100))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        error_window.fill((0, 0, 0))
        error_window.blit(error_text, error_text_rect)
        pygame.display.update()
    exit(0)

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == ord('a'):
                client.move("left")
            if event.key == ord('d'):
                client.move("right")
            if event.key == ord('w'):
                client.move("up")
            if event.key == ord('s'):
                client.move("down")
        if event.type == pygame.QUIT:
            client.sock.close()
            exit()
    screen.fill((0, 0, 0))
    for i in client.players:
        player = Player((i["x"], i["y"]))
        screen.blit(player.image, player.rect)
    pygame.display.update()
    clock.tick(45)
