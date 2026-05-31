import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game Layout and Display Constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 720
BOARD_SIZE = 600  # 600x600 grid pixels
GRID_COUNT = 10   
TILE_SIZE = BOARD_SIZE // GRID_COUNT

# High-Vibrancy UI Color Palette
COLOR_BG = (24, 24, 34)
COLOR_GRID_LIGHT = (245, 246, 250)
COLOR_GRID_DARK = (220, 224, 230)
COLOR_TEXT_DARK = (47, 53, 66)
COLOR_TEXT_LIGHT = (241, 242, 246)
COLOR_HUMAN = (9, 132, 227)     # Deep Electric Blue
COLOR_BOT = (214, 48, 49)       # Crimson Red
COLOR_LADDER = (38, 194, 129)   # Mint Green
COLOR_SNAKE = (225, 112, 85)    # Coral Orange
COLOR_GOLD = (253, 203, 110)    # Amber Gold

# Setup Window Screen Display Frame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snakes & Ladders King (Human vs Bot)")
clock = pygame.time.Clock()

# Fonts Setup
font_small = pygame.font.SysFont("arial", 16, bold=True)
font_medium = pygame.font.SysFont("arial", 22, bold=True)
font_large = pygame.font.SysFont("arial", 32, bold=True)

# Define Gameplay Board Core Paths Mapping (Start: End Location)
SNAKES_AND_LADDERS = {
    # Ladders (Climb Upwards)
    4: 25, 12: 44, 29: 71, 38: 59, 50: 70, 62: 83, 74: 93,
    # Snakes (Slide Downwards)
    21: 3, 34: 14, 49: 17, 64: 39, 88: 52, 95: 66, 98: 60
}

def get_tile_coordinates(tile_num):
    """
    Transforms numerical position ranges (1-100) into precise pixel vector space coordinates (X, Y).
    Generates a Boustrophedon (zigzag) snake pattern track layout.
    """
    if tile_num < 1:
        return -50, -50 # Hide structural markers offscreen before startup
        
    row = (tile_num - 1) // GRID_COUNT
    col = (tile_num - 1) % GRID_COUNT

    # Zigzag track calculation inversion based on odd matrix rows
    if row % 2 == 1:
        col = (GRID_COUNT - 1) - col

    # Convert mapping matrix data to absolute engine resolution coordinates
    x = col * TILE_SIZE + (TILE_SIZE // 2)
    y = BOARD_SIZE - (row * TILE_SIZE) - (TILE_SIZE // 2)
    return x, y

class PlayerToken:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.current_tile = 0       # Where the token physically is during execution frame
        self.logical_target = 0     # The endpoint target tile after a dice roll
        self.move_queue = []        # Path tracking for multi-step stepping hopping
        self.animation_delay = 0    # Delay timer to control walking pace speed
        self.is_sliding = False     # Flag for sliding down snakes or climbing ladders

    def setup_move_path(self, steps):
        """Calculates step-by-step path array blocks for human visual feedback tracking."""
        if self.logical_target + steps <= 100:
            start = self.logical_target
            self.logical_target += steps
            
            # Append every individual tile in the path sequence to the execution queue
            for i in range(1, steps + 1):
                self.move_queue.append(start + i)
            return True
        return False

    def process_movement_animation(self):
        """Updates animation tracking frames. Executes steps sequentially over time."""
        if self.animation_delay > 0:
            self.animation_delay -= 1
            return True # Unit busy moving inside timeline frame

        if self.move_queue:
            self.current_tile = self.move_queue.pop(0)
            self.animation_delay = 6  # Adjust frame delay count to increase/decrease speed
            
            # Check if token reached the intermediate dice target destination
            if not self.move_queue and self.current_tile == self.logical_target:
                # Evaluate if player landed directly on a Snake or a Ladder node shortcut
                if self.current_tile in SNAKES_AND_LADDERS:
                    self.logical_target = SNAKES_AND_LADDERS[self.current_tile]
                    self.move_queue.append(self.logical_target)
                    self.is_sliding = True
                    self.animation_delay = 15 # Give an extra pause for the slide transition
            return True
            
        self.is_sliding = False
        return False # Unit is resting idle

def draw_game_engine(human, bot, active_turn, display_message, dice_state):
    screen.fill(COLOR_BG)

    # 1. Render the Grid Squares Canvas Background
    for row in range(GRID_COUNT):
        for col in range(GRID_COUNT):
            tile_color = COLOR_GRID_LIGHT if (row + col) % 2 == 0 else COLOR_GRID_DARK
            rect = pygame.Rect(col * TILE_SIZE, BOARD_SIZE - (row + 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, tile_color, rect)
            pygame.draw.rect(screen, (189, 195, 199), rect, 1) # Thin Grid borders

            # Numerical assignment mapping computations
            disp_col = (GRID_COUNT - 1) - col if row % 2 == 1 else col
            tile_id = row * GRID_COUNT + disp_col + 1
            
            lbl = font_small.render(str(tile_id), True, COLOR_TEXT_DARK)
            screen.blit(lbl, (rect.x + 6, rect.y + 6))

    # 2. Render Board Shortcuts (Snakes and Ladders Connectors)
    for entry, exit_node in SNAKES_AND_LADDERS.items():
        ex, ey = get_tile_coordinates(entry)
        target_x, target_y = get_tile_coordinates(exit_node)
        
        if entry < exit_node:  # Render Climbing Ladder Graphics
            pygame.draw.line(screen, COLOR_LADDER, (ex - 4, ey), (target_x - 4, target_y), 5)
            pygame.draw.line(screen, COLOR_LADDER, (ex + 4, ey), (target_x + 4, target_y), 5)
            # Rungs on the ladder
            for step in range(1, 5):
                ratio = step / 5.0
                rx = ex + ratio * (target_x - ex)
                ry = ey + ratio * (target_y - ey)
                pygame.draw.line(screen, COLOR_LADDER, (rx - 6, ry), (rx + 6, ry), 3)
        else:  # Render Falling Snake Graphics
            pygame.draw.line(screen, COLOR_SNAKE, (ex, ey), (target_x, target_y), 7)
            pygame.draw.circle(screen, COLOR_SNAKE, (ex, ey), 10)  # Snake Head
            pygame.draw.circle(screen, (255, 255, 255), (ex - 3, ey - 2), 2) # Eye Indicator
            pygame.draw.circle(screen, (255, 255, 255), (ex + 3, ey - 2), 2)

    # 3. Render Player Movement Tokens (With overlap checks)
    hx, hy = get_tile_coordinates(human.current_tile)
    bx, by = get_tile_coordinates(bot.current_tile)

    if human.current_tile == bot.current_tile and human.current_tile > 0:
        pygame.draw.circle(screen, COLOR_HUMAN, (hx - 10, hy), 13)
        pygame.draw.circle(screen, (255, 255, 255), (hx - 10, hy), 13, 2)
        pygame.draw.circle(screen, COLOR_BOT, (bx + 10, by), 13)
        pygame.draw.circle(screen, (255, 255, 255), (bx + 10, by), 13, 2)
    else:
        if human.current_tile > 0:
            pygame.draw.circle(screen, COLOR_HUMAN, (hx, hy), 15)
            pygame.draw.circle(screen, (255, 255, 255), (hx, hy), 15, 2)
        if bot.current_tile > 0:
            pygame.draw.circle(screen, COLOR_BOT, (bx, by), 15)
            pygame.draw.circle(screen, (255, 255, 255), (bx, by), 15, 2)

    # 4. Control Interface Dashboard Panel Block Footer
    panel_y = BOARD_SIZE + 15
    txt_status = font_large.render(display_message, True, COLOR_GOLD if "Victory" in display_message or "Bot wins" in display_message else COLOR_TEXT_LIGHT)
    screen.blit(txt_status, (25, panel_y))
    
    # Render Dice UI Widget
    dice_rect = pygame.Rect(540, panel_y, 80, 80)
    pygame.draw.rect(screen, COLOR_TEXT_LIGHT, dice_rect, border_radius=12)
    pygame.draw.rect(screen, COLOR_GOLD, dice_rect, 4, border_radius=12)
    
    # Output Numerical Values Inside Dice Widget Canvas
    dice_val_str = str(dice_state["current_val"]) if dice_state["current_val"] else "?"
    txt_dice = font_large.render(dice_val_str, True, COLOR_TEXT_DARK)
    screen.blit(txt_dice, (dice_rect.x + 28, dice_rect.y + 22))

    # Input Call-To-Action Prompts Rendering
    if active_turn == "Human" and not dice_state["rolling"] and not human.move_queue and not bot.move_queue:
        lbl_action = font_small.render("CLICK DICE TO ROLL", True, COLOR_HUMAN)
        screen.blit(lbl_action, (515, panel_y + 85))
    elif active_turn == "Bot":
        lbl_action = font_small.render("BOT THINKING...", True, COLOR_BOT)
        screen.blit(lbl_action, (530, panel_y + 85))

    pygame.display.flip()

def main():
    player_human = PlayerToken("Player (Blue)", COLOR_HUMAN)
    player_bot = PlayerToken("Computer (Red)", COLOR_BOT)
    
    active_turn = "Human"
    display_message = "Your Turn! Click the white die to start."
    match_ended = False

    # Dice Global Simulation Parameters Configuration Dictionary
    dice_state = {
        "rolling": False,
        "frames_left": 0,
        "final_result": 0,
        "current_val": None
    }
    
    bot_decision_cooldown = 0 # Prevents the bot from instantly rolling before visual transitions complete

    while True:
        clock.tick(60) # Lock processing pipeline at smooth 60 Frames Per Second frame updates
        
        # Check active movement queue transitions status flag loops
        human_moving = player_human.process_movement_animation()
        bot_moving = player_bot.process_movement_animation()
        tokens_animating = human_moving or bot_moving

        # 1. Processing System Dice Rolling State Timelines
        if dice_state["rolling"]:
            dice_state["frames_left"] -= 1
            dice_state["current_val"] = random.randint(1, 6) # Generate rolling face flash chaos value
            
            if dice_state["frames_left"] <= 0:
                # Finished spinning execution. Freeze on calculated engine result output data.
                dice_state["rolling"] = False
                roll_outcome = dice_state["final_result"]
                dice_state["current_val"] = roll_outcome
                
                if active_turn == "Human":
                    valid_move = player_human.setup_move_path(roll_outcome)
                    if valid_move:
                        display_message = f"You rolled a {roll_outcome}! Advancing..."
                    else:
                        display_message = f"Rolled a {roll_outcome}! Too high to enter 100. Turn skipped."
                        active_turn = "Bot"
                        bot_decision_cooldown = 40
                else: # Engine logic for running bot movements execution paths
                    valid_move = player_bot.setup_move_path(roll_outcome)
                    if valid_move:
                        display_message = f"Bot rolled a {roll_outcome}! Traveling..."
                    else:
                        display_message = f"Bot rolled a {roll_outcome} and overshot 100. Turn skipped!"
                        active_turn = "Human"

        # 2. Monitor Game Over Trigger Milestones After Movement Completes
        if not tokens_animating and not dice_state["rolling"] and not match_ended:
            if player_human.logical_target == 100 and player_human.current_tile == 100:
                display_message = "Victory! You reached square 100!"
                match_ended = True
            elif player_bot.logical_target == 100 and player_bot.current_tile == 100:
                display_message = "Game Over! The Bot reached 100 first."
                match_ended = True

        # 3. System Environment Event Handling Infrastructure
        # To this:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN and not match_ended:
                # Execute rolling commands inside Human control windows frame context profiles
                if active_turn == "Human" and not tokens_animating and not dice_state["rolling"]:
                    mouse_pos = event.pos
                    dice_rect = pygame.Rect(540, BOARD_SIZE + 15, 80, 80)
                    
                    if dice_rect.collidepoint(mouse_pos):
                        dice_state["rolling"] = True
                        dice_state["frames_left"] = 20 # Keep spinning animation active for 20 frames
                        dice_state["final_result"] = random.randint(1, 6)
                        display_message = "Rolling the dice..."

        # 4. Handle Computer AI Turn Decision Engine Core Loops
        if active_turn == "Bot" and not tokens_animating and not dice_state["rolling"] and not match_ended:
            if bot_decision_cooldown > 0:
                bot_decision_cooldown -= 1
            else:
                dice_state["rolling"] = True
                dice_state["frames_left"] = 20
                dice_state["final_result"] = random.randint(1, 6)
                display_message = "Bot is rolling..."

        # 5. Hand over turn cycles when tokens come to rest
        if not tokens_animating and not dice_state["rolling"] and not match_ended:
            if active_turn == "Human" and player_human.current_tile == player_human.logical_target and display_message.startswith("You rolled"):
                active_turn = "Bot"
                bot_decision_cooldown = 40  # Add structural frame delay so Bot layout step feels organic
                display_message = "Bot's Turn..."
            elif active_turn == "Bot" and player_bot.current_tile == player_bot.logical_target and display_message.startswith("Bot rolled"):
                active_turn = "Human"
                display_message = "Your Turn! Click the die."

        # Pass frame canvas context data profiles down into visual graphics compiler layout
        draw_game_engine(player_human, player_bot, active_turn, display_message, dice_state)

if __name__ == "__main__":
    main()