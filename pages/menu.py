import pygame
import math
from helper.settings import *

def draw_button(screen, rect, text, font, mouse_pos, bg_color=(255,255,255), text_color=(0,0,0)):
    """Fungsi helper tombol sederhana"""
    # Warna berubah dikit saat hover
    if rect.collidepoint(mouse_pos):
        # Versi agak gelap dikit untuk efek hover
        r, g, b = bg_color
        current_bg = (max(0, r-30), max(0, g-30), max(0, b-30))
    else:
        current_bg = bg_color

    pygame.draw.rect(screen, (0,0,0), (rect.x, rect.y+4, rect.w, rect.h), border_radius=10)
    pygame.draw.rect(screen, current_bg, rect, border_radius=10)
    pygame.draw.rect(screen, (0,0,0), rect, 2, border_radius=10)
    
    txt_surf = font.render(text, True, text_color)
    txt_rect = txt_surf.get_rect(center=rect.center)
    screen.blit(txt_surf, txt_rect)

def draw_text_with_outline(screen, text, font, center_pos, text_col, outline_col, outline_width=2):
    """Helper membuat teks dengan garis tepi"""
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                surf = font.render(text, True, outline_col)
                rect = surf.get_rect(center=(center_pos[0] + dx, center_pos[1] + dy))
                screen.blit(surf, rect)
    surf = font.render(text, True, text_col)
    rect = surf.get_rect(center=center_pos)
    screen.blit(surf, rect)

def draw_decorative_shapes(screen):
    """Menggambar Bentuk Abstrak & Garis Merah"""
    
    # --- 1. LINGKARAN ABSTRAK (Kuning Muda) ---
    
    # Lingkaran Besar di Kiri Bawah
    pygame.draw.circle(screen, (255, 204, 100), (0, SCREEN_HEIGHT), 250)
    
    # Lingkaran Kecil di Kanan Atas
    pygame.draw.circle(screen, (255, 204, 100), (SCREEN_WIDTH, 0), 180)

# 2. FUNGSI UNTUK MENGGAMBAR SATU GELOMBANG PENDEK
    def draw_squiggle(start_x, start_y, length=80, color=(255, 77, 77)):
        points = []
        # Loop pendek sepanjang 'length' pixel
        for x in range(0, length, 3): 
            y = start_y + 10 * math.sin(0.1 * x)
            points.append((start_x + x, y))
        
        if len(points) > 1:
            pygame.draw.lines(screen, color, False, points, 6) # Tebal garis 6

    # 3. GAMBAR 3 GELOMBANG DI POSISI BERBEDA
    draw_squiggle(start_x=80, start_y=120)
    draw_squiggle(start_x=SCREEN_WIDTH - 180, start_y=300)
    draw_squiggle(start_x=120, start_y=550)

def draw_char_simple(screen, img, center_pos):
    """Helper menggambar karakter langsung (tanpa background putih)"""
    if img:
        img_rect = img.get_rect(center=center_pos)
        screen.blit(img, img_rect)


def draw_menu_page(screen,fonts, buttons, char_image=None):
    """
    Pastikan argumen ke-3 adalah 'fonts' (Dictionary),
    dan argumen terakhir adalah 'char_image'.
    """
    
    # 1. Background
    BG_COLOR = (242, 169, 59)
    screen.fill(BG_COLOR)
    draw_decorative_shapes(screen)

    # 2. Judul Kecil "Let's Play"
    font_balsamiq = fonts.get('balsamiq', fonts.get('menu')) 
    
    draw_text_with_outline(screen, "Let's Play,", font_balsamiq, (SCREEN_WIDTH//2, 80), (70, 39, 24), (0,0,0), 0)

    # 3. Judul Besar "WORD GAMES"
    font_title = fonts.get('title')
    title_scale = 2.0
    
    # Render WORD
    base_word = font_title.render("WORD", True, (252, 249, 218))
    base_word = pygame.transform.scale(base_word, (int(base_word.get_width() * title_scale), int(base_word.get_height() * title_scale)))
    rect_word = base_word.get_rect(center=(SCREEN_WIDTH//2, 150))
    
    # Shadow
    shadow_word = base_word.copy()
    shadow_word.fill((0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(shadow_word, (rect_word.x+5, rect_word.y+5))
    screen.blit(base_word, rect_word)

    # Render GAMES
    base_game = font_title.render("GAMES", True, (252, 249, 218))
    base_game = pygame.transform.scale(base_game, (int(base_game.get_width() * title_scale), int(base_game.get_height() * title_scale)))
    rect_game = base_game.get_rect(center=(SCREEN_WIDTH//2, 230))
    
    shadow_game = base_game.copy()
    shadow_game.fill((0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(shadow_game, (rect_game.x+5, rect_game.y+5))
    screen.blit(base_game, rect_game)

    # 4. Gambar Karakter
    if char_image:
        char_x = SCREEN_WIDTH - 160
        char_y = SCREEN_HEIGHT - 155
        
        char_rect = char_image.get_rect(center=(char_x, char_y))
        screen.blit(char_image, char_rect)
    else:
        pygame.draw.circle(screen, (255, 255, 255), (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100), 60)

    # 5. Tombol
    mouse_pos = pygame.mouse.get_pos()
    labels = ["MULAI", "LEVEL", "PENGATURAN", "PETUNJUK", "KELUAR"]
    BTN_BG = (255, 255, 255) 
    BTN_TEXT = (0, 0, 0)
    
    font_btn = fonts.get('menu')

    for i, btn_rect in enumerate(buttons):
        label = labels[i] if i < len(labels) else "..."
        draw_button(screen, btn_rect, label, font_btn, mouse_pos, bg_color=BTN_BG, text_color=BTN_TEXT)

    # 6. Watermark (Credits)
    # "A Game From : Retma | Nessa | Sovia | Hanif"
    font_watermark = fonts.get('small', fonts.get('ui')) # Gunakan font kecil
    watermark_text = "A Game From : Retma | Nessa | Sovia | Hanif"
    
    # Render teks
    wm_surf = font_watermark.render(watermark_text, True, (100, 60, 20)) # Coklat gelap
    wm_surf.set_alpha(int(255 * 0.85)) # Opacity 85%
    wm_rect = wm_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)) # Paling bawah
    screen.blit(wm_surf, wm_rect)

def draw_instructions_page(screen, fonts, btn_back, mouse_pos, char1=None, char2=None, char3=None):
    """Menggambar Halaman Petunjuk dengan Style 'Paper Card' (Mirip PDF)"""
    
    # 1. Background
    BG_COLOR = (242, 169, 59) # Warna Oranye Utama
    screen.fill(BG_COLOR)
    draw_decorative_shapes(screen)

    # 2. PANEL KERTAS (Warna Krem Terang)
    panel_w, panel_h = SCREEN_WIDTH - 100, SCREEN_HEIGHT - 120
    panel_rect = pygame.Rect(0, 0, panel_w, panel_h)
    panel_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
    
    # Warna Krem (Sesuai tema PDF)
    PANEL_COLOR = (255, 248, 220) 
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect, border_radius=20)
    
    # Outline Putih pada panel
    pygame.draw.rect(screen, (255, 255, 255), panel_rect, 4, border_radius=20)

    # 3. Judul "CARA BERMAIN" (Di luar/atas panel atau di dalam paling atas)
    font_title = fonts.get('title')
    title_text = "CARA BERMAIN"
    title_scale = 1.0
    
    base_title = font_title.render(title_text, True, (255, 255, 255))
    base_title = pygame.transform.scale(base_title, (int(base_title.get_width() * title_scale), int(base_title.get_height() * title_scale)))
    rect_title = base_title.get_rect(center=(SCREEN_WIDTH // 2, panel_rect.top - 15)) # Sedikit di atas panel

    # Shadow & Render Judul
    shadow_title = base_title.copy()
    shadow_title.fill((0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(shadow_title, (rect_title.x + 3, rect_title.y + 3))
    screen.blit(base_title, rect_title)

    # 4. TEKS INSTRUKSI (Warna Gelap di atas Krem)
    # Tidak pakai outline tebal, pakai warna kontras
    font_instr = fonts.get('balsamiq', fonts.get('menu'))
    TEXT_COLOR = (80, 50, 20) 

    lines = [
        "1. Temukan kata tersembunyi di dalam grid.",
        "2. Tarik garis (Drag) mouse untuk memilih kata.",
        "3. Kata bisa mendatar, menurun, atau diagonal.",
        "4. Gunakan tombol HINT jika merasa buntu.",
        "5. Selesaikan level sebelum waktu habis!",
    ]

    start_y = panel_rect.top + 60
    line_spacing = 45

    for i, line in enumerate(lines):
        # Render teks biasa (tanpa outline tebal)
        txt_surf = font_instr.render(line, True, TEXT_COLOR)
        txt_rect = txt_surf.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * line_spacing))
        screen.blit(txt_surf, txt_rect)

    # 5. KARAKTER (Di bagian bawah panel)
    chars_y_pos = panel_rect.bottom - 70 # Posisi vertikal karakter
    
    # Jarak antar karakter
    spacing_x = 180 
    center_x = SCREEN_WIDTH // 2
    
    # Gambar Karakter
    draw_char_simple(screen, char1, (center_x - spacing_x, chars_y_pos))
    draw_char_simple(screen, char2, (center_x, chars_y_pos))
    draw_char_simple(screen, char3, (center_x + spacing_x, chars_y_pos))

    # 6. Tombol KEMBALI (Di tengah bawah)
    # Kita ubah posisinya jadi di tengah bawah layar (di luar panel)
    btn_back.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
    btn_back.width = 200 # Perlebar sedikit
    
    BTN_BG = (255, 255, 255)
    BTN_TEXT = (0, 0, 0)
    draw_button(screen, btn_back, "KEMBALI", fonts.get('menu'), mouse_pos, bg_color=BTN_BG, text_color=BTN_TEXT)