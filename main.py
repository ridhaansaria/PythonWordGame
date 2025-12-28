import pygame
import sys
import os

from helper.settings import *
from helper.levels import LEVEL_DATA
from helper.utils import create_grid
from pages.menu import draw_menu_page, draw_instructions_page
from pages.game import draw_game_panel, draw_timer
from pages.levels import draw_level_select_page
from pages.settings import draw_settings_page

def resource_path(relative_path):
    """ Dapatkan path absolut ke resource, kompatibel dengan dev dan PyInstaller """
    try:
        # PyInstaller membuat temp folder di _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class WordSearchGame:
    def __init__(self):
        pygame.init()

        # Custom Config (Mutable)
        self.config_duration = LEVEL_DURATION # Default from settings.py (originally 180)
        self.config_max_hints = MAX_HINTS     # Default from settings.py (originally 3)

        # --- 1. SETUP AUDIO (MIXER) ---
        try:
            pygame.mixer.init()
        except:
            print("Audio device tidak ditemukan. Game berjalan tanpa suara.")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Word Games")
        
        # --- SETUP ICON ---
        try:
            # Gunakan resource_path agar icon terbaca di .exe juga
            icon_path = resource_path(os.path.join("assets", "images", "icon.ico"))
            if os.path.exists(icon_path):
                icon_img = pygame.image.load(icon_path)
                # Scale icon to typical size (e.g. 64x64)
                icon_img = pygame.transform.scale(icon_img, (64, 64))
                pygame.display.set_icon(icon_img)
        except:
            pass
            
        self.clock = pygame.time.Clock()
        
        # --- SETUP FONT ---
        self.fonts = {}
        try:
            # Gunakan resource_path
            font_path = resource_path(os.path.join("assets", "fonts", "LuckiestGuy.ttf"))
            balsamiq_path = resource_path(os.path.join("assets", "fonts", "BalsamiqSans-Bold.ttf"))
            
            # Font Utama
            self.fonts['tile'] = pygame.font.Font(font_path, 28)
            self.fonts['title'] = pygame.font.Font(font_path, 40)
            
            # Font Balsamiq (Untuk "Let's Play")
            if os.path.exists(balsamiq_path):
                self.fonts['balsamiq'] = pygame.font.Font(balsamiq_path, 30)
            else:
                self.fonts['balsamiq'] = pygame.font.SysFont('Arial', 30, bold=True)
                
        except:
            print("Font custom tidak ditemukan, menggunakan default.")
            self.fonts['tile'] = pygame.font.SysFont('Arial', 24, bold=True)
            self.fonts['title'] = pygame.font.SysFont('Arial', 40, bold=True)
            self.fonts['balsamiq'] = pygame.font.SysFont('Arial', 30, bold=True)
            
        self.fonts['ui'] = pygame.font.SysFont('Arial', 18)
        self.fonts['small'] = pygame.font.SysFont('Arial', 14) # Untuk watermark/detail kecil
        self.fonts['menu'] = pygame.font.SysFont('Arial', 24, bold=True)

        # --- SETUP TOMBOL ---
        cx = SCREEN_WIDTH // 2
        # Posisi tombol agak ke bawah karena judul besar
        self.btn_start = pygame.Rect(0, 0, 280, 50); self.btn_start.center = (cx, 350)
        self.btn_help = pygame.Rect(0, 0, 280, 50); self.btn_help.center = (cx, 420)
        self.btn_quit = pygame.Rect(0, 0, 280, 50); self.btn_quit.center = (cx, 490)

        # BUTTON BARU: LEVEL
        # Geser posisi tombol agar muat
        self.btn_start.center = (cx, 320)
        self.btn_levels = pygame.Rect(0, 0, 280, 50); self.btn_levels.center = (cx, 390)
        self.btn_settings = pygame.Rect(0, 0, 280, 50); self.btn_settings.center = (cx, 460)
        self.btn_help.center = (cx, 530)
        self.btn_quit.center = (cx, 600)
        
        self.btn_back = pygame.Rect(0, 0, 150, 40); self.btn_back.bottomright = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20)
        
        self.btn_hint = pygame.Rect(0, 0, 100, 40)

        # --- LOAD ASSETS ---
        self.images = {}
        self.load_images()

        self.sounds = {}
        self.load_sounds()
        
        self.game_state = "MENU"
        self.current_level_index = 0
        self.current_level_page_idx = 0 # Untuk pagination level
        self.load_level(self.current_level_index)

    def load_images(self):
        def load_asset(name, w, h):
            try:
                # Gunakan resource_path
                path = resource_path(os.path.join("assets", "images", name))
                if not os.path.exists(path):
                    print(f"Warning: {name} tidak ditemukan at {path}")
                    return None
                img = pygame.image.load(path)
                return pygame.transform.scale(img, (w, h))
            except: 
                return None

        # --- LOAD BACKGROUND THEMES ---
        self.bg_themes = {}
        self.bg_themes['forest'] = load_asset('bg_forest.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bg_themes['city']   = load_asset('bg_city.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bg_themes['ocean']  = load_asset('bg_ocean.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Default Background
        self.images['bg'] = self.bg_themes['forest']

        # --- Load Aset Lainnya ---
        self.images['tile'] = load_asset('tile.png', GRID_SIZE, GRID_SIZE)
        self.images['select'] = load_asset('tile_select.png', GRID_SIZE, GRID_SIZE)
        self.images['correct'] = load_asset('tile_correct.png', GRID_SIZE, GRID_SIZE)
        
        # Load Karakter Menu (Pastikan nama file benar)
        self.images['char_menu'] = load_asset('character_menu.png', 350, 350)

        instr_char_size = 150 
        self.images['char_i1'] = load_asset('char_instr_1.png', instr_char_size, instr_char_size)
        self.images['char_i2'] = load_asset('char_instr_2.png', instr_char_size, instr_char_size)
        self.images['char_i3'] = load_asset('char_instr_3.png', instr_char_size, instr_char_size)

    def load_level(self, index):
        level_info = LEVEL_DATA[index]
        self.level_name = level_info["name"]
        self.current_dict = level_info["data"]
        self.answers = list(self.current_dict.values())
        
        # --- LOGIKA BATCH BACKGROUND (1-10 Hutan, 11-20 Kota, dst) ---
        level_num = index + 1
        selected_bg = None
        
        if 1 <= level_num <= 10:
            selected_bg = self.bg_themes.get('forest')
        elif 11 <= level_num <= 20:
            selected_bg = self.bg_themes.get('city')
        else:
            selected_bg = self.bg_themes.get('ocean')

        # Fallback jika background tema tidak ditemukan
        if selected_bg:
            self.images['bg'] = selected_bg
        else:
             # Coba load dari data level, atau default forest
             bg_file = level_info.get("bg_file")
             if bg_file: self.load_bg(bg_file)
             else: self.images['bg'] = self.bg_themes.get('forest')

        self.grid, self.word_locations = create_grid(ROWS, COLS, self.answers)
        
        self.found_words = [] 
        self.grid_solved = [[False for _ in range(COLS)] for _ in range(ROWS)]
        self.selecting = False
        self.start_pos = None 
        self.current_pos = None
        
        self.hints_left = self.config_max_hints
        self.hint_cell = None 
        
        self.start_ticks = pygame.time.get_ticks()
        self.level_duration = self.config_duration

    def load_bg(self, bg_name):
        # Gunakan resource_path
        path = resource_path(os.path.join("assets","images", bg_name))
        try:
            img = pygame.image.load(path)
            self.images['bg'] = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            pass

    def load_sounds(self):
        def load_sfx(name):
            try:
                # Gunakan resource_path
                path = resource_path(os.path.join("assets", "audio", name))
                if os.path.exists(path):
                    return pygame.mixer.Sound(path)
                return None
            except:
                return None

        self.sounds['click'] = load_sfx('click.wav')
        self.sounds['correct'] = load_sfx('correct.wav')
        self.sounds['win'] = load_sfx('win.wav')

    def play_sfx(self, name):
        if name in self.sounds and self.sounds[name] is not None:
            self.sounds[name].play()

    def play_bgm(self, filename):
        try:
            # Gunakan resource_path
            path = resource_path(os.path.join("assets", "audio", filename))
            if os.path.exists(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
        except:
            print("BGM Error")
    
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

    def use_hint(self):
        if self.hints_left > 0:
            for word in self.answers:
                if word not in self.found_words:
                    coords = self.word_locations.get(word)
                    if coords:
                        self.hint_cell = coords[0] 
                        self.hints_left -= 1
                        break

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
            self.play_sfx('correct') # Mainkan suara
            for r, c in cells: self.grid_solved[r][c] = True
            if self.hint_cell in cells: self.hint_cell = None
            if len(self.found_words) == len(self.answers):
                self.play_sfx('win') # Mainkan suara
                if self.current_level_index < len(LEVEL_DATA) - 1:
                    self.game_state = "LEVEL_COMPLETE"
                else: self.game_state = "GAME_OVER"

    def draw_game(self):
        if self.images['bg']: self.screen.blit(self.images['bg'], (0, 0))
        else: self.screen.fill(COLOR_BG)

        mouse_pos = pygame.mouse.get_pos()
        hover_cell = self.get_grid_pos(*mouse_pos)

        selected_cells = self.get_selected_cells() if self.selecting else []
        
        if self.hint_cell:
            hr, hc = self.hint_cell
            if not self.grid_solved[hr][hc]:
                hx = START_X + hc * (GRID_SIZE + GRID_MARGIN)
                hy = START_Y + hr * (GRID_SIZE + GRID_MARGIN)
                pygame.draw.rect(self.screen, COLOR_HINT, (hx, hy, GRID_SIZE, GRID_SIZE))

        for r in range(ROWS):
            for c in range(COLS):
                x = START_X + c * (GRID_SIZE + GRID_MARGIN)
                y = START_Y + r * (GRID_SIZE + GRID_MARGIN)
                
                is_solved = self.grid_solved[r][c]
                is_selected = (r, c) in selected_cells
                is_hovered = (r, c) == hover_cell
                
                img = None
                base_color = COLOR_TILE
                if is_solved: 
                    img = self.images['correct'] 
                    base_color = COLOR_CORRECT
                elif is_selected: 
                    img = self.images['select']  
                    base_color = COLOR_SELECT
                elif is_hovered: 
                    base_color = COLOR_HOVER
                is_active_hint = ((r, c) == self.hint_cell and not is_solved and not is_selected and not is_hovered)

                if not is_active_hint:
                    pygame.draw.rect(self.screen, base_color, (x, y, GRID_SIZE, GRID_SIZE), border_radius=8)
                    if img: 
                        self.screen.blit(img, (x, y))

                text = self.fonts['tile'].render(self.grid[r][c], True, COLOR_TEXT)
                rect = text.get_rect(center=(x + GRID_SIZE//2, y + GRID_SIZE//2))
                self.screen.blit(text, rect)

        seconds_passed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        time_left = max(0, self.level_duration - seconds_passed)
        
        game_data = {
            'level_name': self.level_name,
            'answers': self.answers,
            'found_words': self.found_words,
            'current_dict': self.current_dict,
            'hints_left': self.hints_left,
            'time_left': time_left,
            'total_duration': self.level_duration, 
            'btn_hint_rect': self.btn_hint 
        }
        
        # Capture the returned back button rect
        self.btn_back_game_rect = draw_game_panel(self.screen, self.fonts, game_data, mouse_pos)

    def draw_overlays(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0,0))
        
        txt1 = txt2 = ""
        col_t1 = (255, 255, 255)

        if self.game_state == "LEVEL_COMPLETE":
            txt1, txt2 = "LEVEL SELESAI!", "Tekan [SPASI] Lanjut"
            col_t1 = COLOR_CORRECT
        elif self.game_state == "GAME_OVER":
            txt1, txt2 = "KAMU MENANG!", "Tekan [ESC] ke Menu"
            col_t1 = COLOR_HINT
        elif self.game_state == "TIME_UP":
            txt1, txt2 = "WAKTU HABIS!", "Tekan [R] Ulangi Level"
            col_t1 = (255, 50, 50)
        
        t1 = self.fonts['title'].render(txt1, True, col_t1)
        t2 = self.fonts['menu'].render(txt2, True, (200,200,200))
        self.screen.blit(t1, t1.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30)))
        self.screen.blit(t2, t2.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)))

    def run(self):
        while True:
            if self.game_state == "PLAYING":
                seconds_passed = (pygame.time.get_ticks() - self.start_ticks) / 1000
                if seconds_passed >= self.level_duration:
                    self.game_state = "TIME_UP"

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                
                if self.game_state == "MENU":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.btn_start.collidepoint(event.pos):
                            self.play_sfx('click')
                            self.current_level_index = 0; self.load_level(0); self.game_state = "PLAYING"
                        elif self.btn_levels.collidepoint(event.pos):
                            self.play_sfx('click')
                            self.game_state = "LEVEL_SELECT"
                        elif self.btn_settings.collidepoint(event.pos):
                            self.play_sfx('click')
                            self.game_state = "SETTINGS"
                        elif self.btn_help.collidepoint(event.pos): 
                            self.play_sfx('click')
                            self.game_state = "INSTRUCTIONS"
                        elif self.btn_quit.collidepoint(event.pos): 
                            self.play_sfx('click')
                            pygame.quit(); sys.exit()

                elif self.game_state == "LEVEL_SELECT":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # Cek tombol level
                         l_buttons, b_back, b_prev, b_next = draw_level_select_page(self.screen, self.fonts, LEVEL_DATA, self.current_level_page_idx)
                         
                         if b_back.collidepoint(event.pos):
                             self.play_sfx('click')
                             self.game_state = "MENU"
                         elif b_prev and b_prev.collidepoint(event.pos):
                             self.play_sfx('click')
                             self.current_level_page_idx = max(0, self.current_level_page_idx - 1)
                         elif b_next and b_next.collidepoint(event.pos):
                             self.play_sfx('click')
                             self.current_level_page_idx += 1 # Batas max dicek di draw_level_select_page logic render, tapi aman ditambah karena tombol next hanya muncul jika ada page
                         else:
                             for rect, idx in l_buttons:
                                 if rect.collidepoint(event.pos):
                                     self.play_sfx('click')
                                     self.current_level_index = idx
                                     self.load_level(idx)
                                     self.game_state = "PLAYING"
                                     break

                elif self.game_state == "INSTRUCTIONS":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.btn_back.collidepoint(event.pos): 
                            self.play_sfx('click')
                            self.game_state = "MENU"

                elif self.game_state == "PLAYING":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # Cek Back Button (Dynamic Rect from draw_game)
                        # Note: btn_back_game_rect might not be set on very first frame if loop runs first? 
                        # Usually draw runs once before input? No, typically input then draw.
                        # So let's handle attribute error just in case or init it.
                        # For safety, we check existence.
                        if hasattr(self, 'btn_back_game_rect') and self.btn_back_game_rect.collidepoint(event.pos):
                            self.play_sfx('click')
                            self.game_state = "MENU" # User requested Menu Utama
                        elif self.btn_hint.collidepoint(event.pos): 
                            self.play_sfx('click')
                            self.use_hint()
                        else:
                            pos = self.get_grid_pos(*event.pos)
                            if pos: self.selecting = True; self.start_pos = pos; self.current_pos = pos
                            
                    elif event.type == pygame.MOUSEMOTION and self.selecting:
                        pos = self.get_grid_pos(*event.pos)
                        if pos: self.current_pos = pos
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.selecting:
                        self.selecting = False; self.check_answer(); self.start_pos = None
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.game_state = "LEVEL_SELECT" # Balik ke level select aja enak

                elif self.game_state == "SETTINGS":
                    btns_cfg, b_back = draw_settings_page(self.screen, self.fonts, self.config_duration, self.config_max_hints)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if b_back.collidepoint(event.pos):
                            self.play_sfx('click')
                            self.game_state = "MENU"
                        
                        # Handle Config Buttons
                        if btns_cfg.get('time_minus') and btns_cfg['time_minus'].collidepoint(event.pos):
                            self.play_sfx('click')
                            self.config_duration = max(30, self.config_duration - 30)
                        elif btns_cfg.get('time_plus') and btns_cfg['time_plus'].collidepoint(event.pos):
                            self.play_sfx('click')
                            self.config_duration += 30
                            
                        if btns_cfg.get('hint_minus') and btns_cfg['hint_minus'].collidepoint(event.pos):
                            self.play_sfx('click')
                            self.config_max_hints = max(0, self.config_max_hints - 1)
                        elif btns_cfg.get('hint_plus') and btns_cfg['hint_plus'].collidepoint(event.pos):
                            self.play_sfx('click')
                            self.config_max_hints += 1

                elif self.game_state == "LEVEL_COMPLETE":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.current_level_index += 1; self.load_level(self.current_level_index); self.game_state = "PLAYING"



                elif self.game_state == "GAME_OVER":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.game_state = "MENU"

                elif self.game_state == "TIME_UP":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r: self.load_level(self.current_level_index); self.game_state = "PLAYING"
                        elif event.key == pygame.K_ESCAPE: self.game_state = "MENU"

            if self.game_state == "MENU":
                buttons_list = [self.btn_start, self.btn_levels, self.btn_settings, self.btn_help, self.btn_quit]
                # --- PERBAIKAN UTAMA DI SINI ---
                draw_menu_page(
                    self.screen, 
                    self.fonts, 
                    buttons_list, 
                    self.images.get('char_menu')
                )
            
            elif self.game_state == "INSTRUCTIONS":
                draw_instructions_page(
                    self.screen, 
                    self.fonts, 
                    self.btn_back, 
                    pygame.mouse.get_pos(),
                    self.images.get('char_i1'),
                    self.images.get('char_i2'),
                    self.images.get('char_i3')
                )
                
            elif self.game_state == "LEVEL_SELECT":
                 draw_level_select_page(self.screen, self.fonts, LEVEL_DATA, self.current_level_page_idx)

            elif self.game_state == "PLAYING":
                self.draw_game()
                # draw_back_button removed, now handled inside draw_game -> draw_game_panel

            
            elif self.game_state in ["LEVEL_COMPLETE", "GAME_OVER", "TIME_UP"]:
                self.draw_game()
                self.draw_overlays()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = WordSearchGame()
    game.run()