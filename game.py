import pygame
import random
import string
import sys

# --- 1. KONFIGURASI ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
GRID_SIZE = 45   
GRID_MARGIN = 5     
ROWS = 12          
COLS = 12           

START_X = 50
START_Y = 50

# Warna
COLOR_BG = (30, 30, 30)
COLOR_TILE = (255, 255, 255)
COLOR_SELECT = (100, 200, 255)   # Biru Alice
COLOR_CORRECT = (100, 255, 100)  # Hijau
COLOR_TEXT = (0, 0, 0)
COLOR_UI_TEXT = (255, 255, 255)

# --- 2. DATA KUIS ---
DATA_KUIS = {
    "Tokoh utama Alice in...": "WONDERLAND",
    "Kucing yang bisa senyum": "CHESHIRE",
    "Ratu pemarah (Kartu)": "HEARTS",
    "Pembuat topi gila": "HATTER",
    "Hewan pembawa jam": "RABBIT"
}

answers = list(DATA_KUIS.values())

# --- 3. LOGIKA GENERATOR GRID (Horizontal & Vertical) ---

def create_grid(rows, cols, words):
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    
    for word in words:
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            # Acak arah: 0 = Horizontal, 1 = Vertical
            direction = random.choice(['H', 'V']) 
            
            if direction == 'H': # Horizontal (Kiri ke Kanan)
                r = random.randint(0, rows - 1)
                c = random.randint(0, cols - len(word))
                
                # Cek tabrakan huruf
                collision = False
                for i in range(len(word)):
                    if grid[r][c + i] != '' and grid[r][c + i] != word[i]:
                        collision = True
                        break
                
                if not collision:
                    for i in range(len(word)):
                        grid[r][c + i] = word[i]
                    placed = True
            
            elif direction == 'V': # Vertical (Atas ke Bawah)
                r = random.randint(0, rows - len(word))
                c = random.randint(0, cols - 1)
                
                # Cek tabrakan huruf
                collision = False
                for i in range(len(word)):
                    if grid[r + i][c] != '' and grid[r + i][c] != word[i]:
                        collision = True
                        break
                
                if not collision:
                    for i in range(len(word)):
                        grid[r + i][c] = word[i]
                    placed = True
                    
            attempts += 1
            
    # Isi sisa kotak dengan huruf acak
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '':
                grid[r][c] = random.choice(string.ascii_uppercase)
                
    return grid

# --- 4. KELAS UTAMA GAME ---

class WordSearchGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Alice's Word Search (H & V)")
        self.clock = pygame.time.Clock()
        
        self.font_tile = pygame.font.SysFont('Arial', 28, bold=True)
        self.font_ui = pygame.font.SysFont('Arial', 18)
        self.font_title = pygame.font.SysFont('Arial', 24, bold=True)

        self.images = {}
        self.load_images()

        # Setup Logic
        self.grid = create_grid(ROWS, COLS, answers)
        self.found_words = [] 
        self.grid_solved = [[False for _ in range(COLS)] for _ in range(ROWS)]
        
        self.selecting = False
        self.start_pos = None 
        self.current_pos = None 

    def load_images(self):
        def load_safe(name, w, h):
            try:
                img = pygame.image.load(name)
                return pygame.transform.scale(img, (w, h))
            except:
                return None
        self.images['bg'] = load_safe('bg.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.images['tile'] = load_safe('tile.png', GRID_SIZE, GRID_SIZE)
        self.images['select'] = load_safe('tile_select.png', GRID_SIZE, GRID_SIZE)
        self.images['correct'] = load_safe('tile_correct.png', GRID_SIZE, GRID_SIZE)

    def get_grid_pos(self, mouse_x, mouse_y):
        if mouse_x < START_X or mouse_y < START_Y: return None
        col = (mouse_x - START_X) // (GRID_SIZE + GRID_MARGIN)
        row = (mouse_y - START_Y) // (GRID_SIZE + GRID_MARGIN)
        if 0 <= row < ROWS and 0 <= col < COLS:
            return (row, col)
        return None

    def get_selected_cells(self):
        # --- BAGIAN PENTING: LOGIKA DRAG MOUSE ---
        if not self.start_pos or not self.current_pos:
            return []
            
        r1, c1 = self.start_pos
        r2, c2 = self.current_pos
        
        cells = []
        
        # 1. Logika Horizontal (Baris sama, Kolom beda)
        if r1 == r2: 
            start, end = min(c1, c2), max(c1, c2)
            for c in range(start, end + 1):
                cells.append((r1, c))
                
        # 2. Logika Vertical (Kolom sama, Baris beda)
        elif c1 == c2: 
            start, end = min(r1, r2), max(r1, r2)
            for r in range(start, end + 1):
                cells.append((r, c1))
        
        # (Opsional: Diagonal bisa ditambahkan di sini dengan logika abs(r1-r2) == abs(c1-c2))
        
        return cells

    def check_answer(self):
        cells = self.get_selected_cells()
        if not cells: return
        
        # Susun huruf dari sel yang dipilih jadi kata
        word = ""
        for r, c in cells:
            word += self.grid[r][c]
            
        # Cek Jawaban (Normal & Terbalik)
        # Terbalik diperlukan jika user drag dari Bawah ke Atas atau Kanan ke Kiri
        if word in answers and word not in self.found_words:
            self.found_words.append(word)
            for r, c in cells:
                self.grid_solved[r][c] = True
            print(f"Ketemu: {word}")
            
        elif word[::-1] in answers and word[::-1] not in self.found_words:
            self.found_words.append(word[::-1])
            for r, c in cells:
                self.grid_solved[r][c] = True
            print(f"Ketemu: {word[::-1]}")

    def draw(self):
        # Gambar BG
        if self.images['bg']: self.screen.blit(self.images['bg'], (0, 0))
        else: self.screen.fill(COLOR_BG)

        # Gambar Grid
        selected_cells = self.get_selected_cells() if self.selecting else []
        
        for r in range(ROWS):
            for c in range(COLS):
                x = START_X + c * (GRID_SIZE + GRID_MARGIN)
                y = START_Y + r * (GRID_SIZE + GRID_MARGIN)
                
                is_solved = self.grid_solved[r][c]
                is_selected = (r, c) in selected_cells
                
                if is_solved:
                    img, color = self.images['correct'], COLOR_CORRECT
                elif is_selected:
                    img, color = self.images['select'], COLOR_SELECT
                else:
                    img, color = self.images['tile'], COLOR_TILE

                if img: self.screen.blit(img, (x, y))
                else: pygame.draw.rect(self.screen, color, (x, y, GRID_SIZE, GRID_SIZE))

                letter = self.grid[r][c]
                text_surf = self.font_tile.render(letter, True, COLOR_TEXT)
                text_rect = text_surf.get_rect(center=(x + GRID_SIZE//2, y + GRID_SIZE//2))
                self.screen.blit(text_surf, text_rect)

        # Gambar UI Soal
        panel_x = START_X + (COLS * (GRID_SIZE + GRID_MARGIN)) + 30
        title = self.font_title.render("DAFTAR PERTANYAAN:", True, COLOR_UI_TEXT)
        self.screen.blit(title, (panel_x, START_Y))
        
        y_offset = START_Y + 40
        for q, ans in DATA_KUIS.items():
            text_color = (255, 255, 0) if ans in self.found_words else COLOR_UI_TEXT
            q_surf = self.font_ui.render(f"- {q}", True, text_color)
            self.screen.blit(q_surf, (panel_x, y_offset))
            y_offset += 30
            display_ans = ans if ans in self.found_words else "_ " * len(ans)
            ans_surf = self.font_ui.render(f"  [{display_ans}]", True, text_color)
            self.screen.blit(ans_surf, (panel_x, y_offset))
            y_offset += 40

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = self.get_grid_pos(*event.pos)
                        if pos:
                            self.selecting = True
                            self.start_pos = pos
                            self.current_pos = pos
                elif event.type == pygame.MOUSEMOTION:
                    if self.selecting:
                        pos = self.get_grid_pos(*event.pos)
                        if pos: self.current_pos = pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.selecting:
                        self.selecting = False
                        self.check_answer()
                        self.start_pos = None
                        self.current_pos = None

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = WordSearchGame()
    game.run()