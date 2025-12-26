# main.py
import pygame
import sys
import os

# --- IMPORT MODUL ---
from settings import *
from levels import LEVEL_DATA
from utils import create_grid
# Import file UI baru kita
from pages import draw_menu_page, draw_instructions_page 

class WordSearchGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Modular Word Search Game")
        self.clock = pygame.time.Clock()
        
        # --- SETUP FONT ---
        try:
            font_path = os.path.join("assets", "alice_font.ttf")
            self.font_tile = pygame.font.Font(font_path, 28)
            self.font_title = pygame.font.Font(font_path, 50)
        except:
            self.font_tile = pygame.font.SysFont('Arial', 24, bold=True)
            self.font_title = pygame.font.SysFont('Arial', 50, bold=True)
            
        self.font_ui = pygame.font.SysFont('Arial', 18)
        self.font_menu = pygame.font.SysFont('Arial', 30, bold=True)

        # --- SETUP UI RECTS (POSISI TOMBOL) ---
        center_x = SCREEN_WIDTH // 2
        self.btn_start = pygame.Rect(0, 0, 200, 50); self.btn_start.center = (center_x, 300)
        self.btn_help = pygame.Rect(0, 0, 200, 50); self.btn_help.center = (center_x, 370)
        self.btn_quit = pygame.Rect(0, 0, 200, 50); self.btn_quit.center = (center_x, 440)
        self.btn_back = pygame.Rect(0, 0, 150, 40); self.btn_back.bottomright = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20)

        # --- LOAD ASSETS & STATE ---
        self.images = {}
        self.load_images()
        self.game_state = "MENU"
        self.current_level_index = 0
        self.load_level(self.current_level_index)

    def load_level(self, index):
        level_info = LEVEL_DATA[index]
        self.level_name = level_info["name"]
        self.current_dict = level_info["data"]
        self.answers = list(self.current_dict.values())
        
        bg_name = level_info.get("bg_file", "bg.jpg")
        self.load_bg(bg_name)

        self.grid = create_grid(ROWS, COLS, self.answers)
        self.found_words = [] 
        self.grid_solved = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.selecting = False
        self.start_pos = None 
        self.current_pos = None

    def load_bg(self, bg_name):
        path = os.path.join("assets", bg_name)
        try:
            img = pygame.image.load(path)
            self.images['bg'] = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            # Fallback ke default bg
            try:
                img = pygame.image.load(os.path.join("assets", "bg.jpg"))
                self.images['bg'] = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except: self.images['bg'] = None

    def load_images(self):
        def load_asset(name, w, h):
            path = os.path.join("assets", name)
            try:
                img = pygame.image.load(path)
                return pygame.transform.scale(img, (w, h))
            except: return None

        self.load_bg('bg.jpg')
        self.images['tile'] = load_asset('tile.png', GRID_SIZE, GRID_SIZE)
        self.images['select'] = load_asset('tile_select.png', GRID_SIZE, GRID_SIZE)
        self.images['correct'] = load_asset('tile_correct.png', GRID_SIZE, GRID_SIZE)

    # --- LOGIKA GAMEPLAY (Grid, Drag, Cek Jawaban) ---
    def get_grid_pos(self, mouse_x, mouse_y):
        if mouse_x < START_X or mouse_y < START_Y: return None
        col = (mouse_x - START_X) // (GRID_SIZE + GRID_MARGIN)
        row = (mouse_y - START_Y) // (GRID_SIZE + GRID_MARGIN)
        if 0 <= row < ROWS and 0 <= col < COLS: return (row, col)
        return None

    def get_selected_cells(self):
        if not self.start_pos or not self.current_pos: return []
        r1, c1 = self.start_pos; r2, c2 = self.current_pos
        cells = []
        if r1 == r2: 
            start, end = min(c1, c2), max(c1, c2)
            for c in range(start, end + 1): cells.append((r1, c))
        elif c1 == c2: 
            start, end = min(r1, r2), max(r1, r2)
            for r in range(start, end + 1): cells.append((r, c1))
        return cells

    def check_answer(self):
        cells = self.get_selected_cells()
        if not cells: return
        word = ""
        for r, c in cells: word += self.grid[r][c]
            
        found_new = False
        if word in self.answers and word not in self.found_words:
            self.found_words.append(word); found_new = True
        elif word[::-1] in self.answers and word[::-1] not in self.found_words:
            self.found_words.append(word[::-1]); found_new = True

        if found_new:
            for r, c in cells: self.grid_solved[r][c] = True
            if len(self.found_words) == len(self.answers):
                if self.current_level_index < len(LEVEL_DATA) - 1:
                    self.game_state = "LEVEL_COMPLETE"
                else: self.game_state = "GAME_OVER"

    def draw_game(self):
        # Background
        if self.images['bg']: self.screen.blit(self.images['bg'], (0, 0))
        else: self.screen.fill(COLOR_BG)

        # Grid
        selected_cells = self.get_selected_cells() if self.selecting else []
        for r in range(ROWS):
            for c in range(COLS):
                x = START_X + c * (GRID_SIZE + GRID_MARGIN)
                y = START_Y + r * (GRID_SIZE + GRID_MARGIN)
                
                is_solved = self.grid_solved[r][c]
                is_selected = (r, c) in selected_cells
                
                if is_solved: img, color = self.images['correct'], COLOR_CORRECT
                elif is_selected: img, color = self.images['select'], COLOR_SELECT
                else: img, color = self.images['tile'], COLOR_TILE

                if img: self.screen.blit(img, (x, y))
                else: pygame.draw.rect(self.screen, color, (x, y, GRID_SIZE, GRID_SIZE))

                text = self.font_tile.render(self.grid[r][c], True, COLOR_TEXT)
                rect = text.get_rect(center=(x + GRID_SIZE//2, y + GRID_SIZE//2))
                self.screen.blit(text, rect)

        # Panel UI
        panel_x = START_X + (COLS * (GRID_SIZE + GRID_MARGIN)) + 30
        title = self.font_title.render(f"{self.level_name}", True, COLOR_UI_TEXT)
        title = pygame.transform.scale(title, (int(title.get_width()*0.6), int(title.get_height()*0.6)))
        self.screen.blit(title, (panel_x, START_Y))
        
        y_off = START_Y + 50
        for q, ans in self.current_dict.items():
            col = (255, 255, 0) if ans in self.found_words else COLOR_UI_TEXT
            self.screen.blit(self.font_ui.render(f"- {q}", True, col), (panel_x, y_off))
            disp = ans if ans in self.found_words else "_ " * len(ans)
            self.screen.blit(self.font_ui.render(f"  [{disp}]", True, col), (panel_x, y_off + 20))
            y_off += 50

    def draw_overlays(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0,0))
        
        txt1 = "LEVEL SELESAI!" if self.game_state == "LEVEL_COMPLETE" else "KAMU MENANG!"
        txt2 = "Tekan [SPASI] Lanjut" if self.game_state == "LEVEL_COMPLETE" else "Tekan [ESC] ke Menu"
        
        t1 = self.font_title.render(txt1, True, (255,255,255))
        t2 = self.font_menu.render(txt2, True, (200,200,200))
        self.screen.blit(t1, t1.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30)))
        self.screen.blit(t2, t2.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)))

    # --- MAIN LOOP ---
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                
                # --- INPUT LOGIC ---
                if self.game_state == "MENU":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.btn_start.collidepoint(event.pos):
                            self.current_level_index = 0; self.load_level(0); self.game_state = "PLAYING"
                        elif self.btn_help.collidepoint(event.pos): self.game_state = "INSTRUCTIONS"
                        elif self.btn_quit.collidepoint(event.pos): pygame.quit(); sys.exit()

                elif self.game_state == "INSTRUCTIONS":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.btn_back.collidepoint(event.pos): self.game_state = "MENU"

                elif self.game_state == "PLAYING":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = self.get_grid_pos(*event.pos)
                        if pos: self.selecting = True; self.start_pos = pos; self.current_pos = pos
                    elif event.type == pygame.MOUSEMOTION and self.selecting:
                        pos = self.get_grid_pos(*event.pos)
                        if pos: self.current_pos = pos
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.selecting:
                        self.selecting = False; self.check_answer(); self.start_pos = None
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.game_state = "MENU"

                elif self.game_state == "LEVEL_COMPLETE":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.current_level_index += 1; self.load_level(self.current_level_index); self.game_state = "PLAYING"

                elif self.game_state == "GAME_OVER":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.game_state = "MENU"

            # --- DRAW LOGIC (Panggil dari ui.py) ---
            if self.game_state == "MENU":
                # Panggil fungsi dari ui.py
                buttons_list = [self.btn_start, self.btn_help, self.btn_quit]
                draw_menu_page(self.screen, self.images['bg'], self.font_title, self.font_menu, buttons_list)
            
            elif self.game_state == "INSTRUCTIONS":
                # Panggil fungsi dari ui.py
                draw_instructions_page(self.screen, self.images['bg'], self.font_title, self.font_menu, self.font_menu, self.btn_back)
            
            elif self.game_state == "PLAYING":
                self.draw_game()
            
            elif self.game_state in ["LEVEL_COMPLETE", "GAME_OVER"]:
                self.draw_game()
                self.draw_overlays()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = WordSearchGame()
    game.run()