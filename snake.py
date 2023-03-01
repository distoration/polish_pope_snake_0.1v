import pygame
import random
import sys
import tkinter as tk
from tkinter import messagebox
import os
# Initialize Pygame

def game():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("barka.mp3")
    # Set up the game window
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480
    CELL_SIZE = 20
    GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
    GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Papawonsz_v2137 BETA')

    # Set up colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    food_image = pygame.image.load(os.path.join('images', 'kremowka.jpg')).convert_alpha()
    food_image = pygame.transform.scale(food_image, (CELL_SIZE, CELL_SIZE))

    pygame.mixer.music.play(-1)




    # Set up the clock
    clock = pygame.time.Clock()

# Define the Snake class
    class Snake:
        def __init__(self):
            self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
            self.direction = 'RIGHT'
            self.score = 0
            self.font = pygame.font.SysFont(None, 32)
            self.game_over_flag = False
            self.image = pygame.image.load(os.path.join('images', 'wojtyla.png')).convert_alpha()
            self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))



        def move(self):
            head = self.body[0]
            if self.direction == 'RIGHT':
                new_head = (head[0] + 1, head[1])
            elif self.direction == 'LEFT':
                new_head = (head[0] - 1, head[1])
            elif self.direction == 'UP':
                new_head = (head[0], head[1] - 1)
            elif self.direction == 'DOWN':
                new_head = (head[0], head[1] + 1)
            self.body.insert(0, new_head)
            if len(self.body) > self.score + 1:
                self.body.pop()

        def draw(self):
            for cell in self.body:
                screen.blit(self.image, (cell[0]*CELL_SIZE, cell[1]*CELL_SIZE))

        def change_direction(self, direction):
            if direction == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'
            elif direction == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            elif direction == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            elif direction == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'

        def check_collision(self):
            head = self.body[0]
            if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
                return True
            for cell in self.body[1:]:
                if head == cell:
                    return True
            return False

        def check_eat(self, food_x, food_y):
            head = self.body[0]
            if head == (food_x, food_y):
                self.score += 1
                return True
            else:
                return False

        def show_score(self):
            draw_text(f"Twoje kremówki: {self.score}", (WINDOW_WIDTH - 100, 10), None, 32)


        def update(self):
            self.move()
            if self.check_collision():
                self.game_over()
            self.check_eat_food()
            self.update_ui()

        def grow(self):
            self.score += 1

        def game_over(self):
            if not self.game_over_flag:
                self.game_over_flag = True
                print(f"Papawonsz umarł! kremówki: {self.score}")
                draw_text(f"Papawonsz umarł! kremówki: {self.score} Grasz ponownie? (Y/N)", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), None, 32)
                pygame.display.update()




    def draw_cell(x, y, color):
        pygame.draw.rect(screen, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw_text(text, pos, font, size):
        font = pygame.font.SysFont(font, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)


    # Define the Food class
    # Define the Food class
    class Food:
        def __init__(self):
            self.generate()

        def generate(self):
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

        def draw(self):
                screen.blit(food_image, (self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE))





    


    while True:
        # Set up the initial game state
        snake = Snake()
        food = Food()
        speed_multiplier = 1

        # Game loop
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction('UP')
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction('DOWN')
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction('LEFT')
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction('RIGHT')

            # Move snake
            snake.move()

            # Check for collisions
            if snake.check_collision():
                    # Ask user whether they want to play again
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_y:
                                game()
                            elif event.key == pygame.K_n:
                                pygame.quit()
                                sys.exit()  # exit game
                        
                    snake.game_over()
                    #draw_text("Game Over! your score:  Play again? (Y/N)", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), None, 32)

                    

                    pygame.display.update()
                    clock.tick(10)
                continue  # start new game

            if snake.check_eat(food.position[0], food.position[1]):
                food = Food()
                snake.score += 1
                speed_multiplier += 0.05

            # Draw screen
            screen.fill(BLACK)
            snake.draw()
            food.draw()
            snake.show_score()
            pygame.display.update()



            # Calculate new game speed and set clock speed
            game_speed = 10 * speed_multiplier
            clock.tick(game_speed)


game()







