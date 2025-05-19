import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

window_wdth = TILE_SIZE * ROWS
window_height = TILE_SIZE * COLS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = "black"
        self.rect = canvas.create_rectangle(x * TILE_SIZE, y * TILE_SIZE, (x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE, fill=self.color)

    def change_color(self, color):
        self.color = color
        canvas.itemconfig(self.rect, fill=self.color)

#game window 

window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window,bg="black", width=window_wdth, height=window_height, borderwidth= 0, highlightthickness=0)
canvas.pack()
window.update()

#centre the window
window_wdth = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_wdth / 2))
window_y = int((screen_height / 2) - (window_height / 2))
#format "(W)x(H)+(X)+(Y)"
window.geometry(f"{window_wdth}x{window_height}+{window_x}+{window_y}")

#initialize game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) #single tile snake's head 
food = Tile(10*TILE_SIZE, 10*TILE_SIZE) 
snake_body = [] #multiple snake tiles 
velocityX = 0
velocityY = 0
game_over = False
score = 0

def change_direction(e): #e = event
    #print(e)
    #print(e.keysym)
    global velocityX, velocityY, game_over
    if (game_over):
        return

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score

    if game_over:
        return

    # Check for collision with walls
    if snake.x < 0 or snake.x >= window_wdth or snake.y < 0 or snake.y >= window_height:
        game_over = True
        return

    # Check for collision with itself
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    # Check for collision with food
    if snake.x == food.x and snake.y == food.y:
        # Add a new tile to the snake's body at the last position
        if snake_body:
            last_tile = snake_body[-1]
            snake_body.append(Tile(last_tile.x, last_tile.y))
        else:
            snake_body.append(Tile(snake.x, snake.y))
        # Move the food to a new random position
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    # Update the snake's body positions
    if snake_body:
        # Move the body tiles to follow the head
        for i in range(len(snake_body) - 1, 0, -1):
            snake_body[i].x = snake_body[i - 1].x
            snake_body[i].y = snake_body[i - 1].y
        # Move the first body tile to the current position of the head
        snake_body[0].x = snake.x
        snake_body[0].y = snake.y

    # Move the snake's head
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def  draw():
    global snake, food, snake_body, game_over, score
    move() 

    canvas.delete("all") #clear the canvas7

    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill= "red")  

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill= "lime green")
    
    for tile in snake_body:
      canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill= "lime green")

    if (game_over):
        canvas.create_text(window_wdth /2 , window_height / 2, font="Arial 20", text=f"Game Over:{score}", fill="red")

    window.after(100, draw) #100ms = 1/10 second, 10 frames/second

draw()

window.bind("<KeyRelease>" , change_direction)
window.mainloop()

