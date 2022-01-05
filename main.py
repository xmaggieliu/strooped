import pygame

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Strooped!")

WHITE = (255, 255, 255)

def draw_win():
    WIN.fill(WHITE)
    pygame.display.update()


def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_win()
        

    pygame.quit()

if __name__ == "__main__":
    main()

