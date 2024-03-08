from display import *

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        display()
        # print(clock.get_fps())
    pygame.quit()


main()
