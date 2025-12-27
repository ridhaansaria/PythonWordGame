import pygame
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

def draw_decorative_circles(screen):
    """Dekorasi background"""
    pygame.draw.circle(screen, (255, 200, 80), (100, SCREEN_HEIGHT - 50), 120)
    s = pygame.Surface((200, 200), pygame.SRCALPHA)
    pygame.draw.circle(s, (255, 255, 255, 50), (100, 100), 80)
    screen.blit(s, (SCREEN_WIDTH - 150, 50))

# --- FUNGSI UTAMA YANG DIPERBAIKI ---
def draw_menu_page(screen, bg_image, fonts, buttons, char_image=None):
    """
    Pastikan argumen ke-3 adalah 'fonts' (Dictionary),
    dan argumen terakhir adalah 'char_image'.
    """
    
    # 1. Background
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        BG_COLOR = (242, 169, 59)
        screen.fill(BG_COLOR)
        draw_decorative_circles(screen)

    # 2. Judul Kecil "Let's Play"
    font_balsamiq = fonts.get('balsamiq', fonts.get('menu')) 
    
    draw_text_with_outline(screen, "Let's Play,", font_balsamiq, (SCREEN_WIDTH//2, 80), (255, 255, 255), (0,0,0), 0)

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
    labels = ["MULAI", "PETUNJUK", "KELUAR"]
    BTN_BG = (255, 255, 255) 
    BTN_TEXT = (0, 0, 0)
    
    font_btn = fonts.get('menu')

    for i, btn_rect in enumerate(buttons):
        label = labels[i] if i < len(labels) else "..."
        draw_button(screen, btn_rect, label, font_btn, mouse_pos, bg_color=BTN_BG, text_color=BTN_TEXT)

def draw_instructions_page(screen, bg_image, fonts, btn_back, mouse_pos):
    # Background
    if bg_image: screen.blit(bg_image, (0,0))
    else: screen.fill((242, 169, 59))

    # Panel
    card_rect = pygame.Rect(0, 0, 600, 500)
    card_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    pygame.draw.rect(screen, (255,255,255), card_rect, border_radius=20)
    pygame.draw.rect(screen, (0,0,0), card_rect, 3, border_radius=20)

    # Judul
    title = fonts['title'].render("CARA BERMAIN", True, (0,0,0))
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, card_rect.y + 50)))

    # Konten
    lines = ["1. Cari kata tersembunyi", "2. Drag mouse untuk memilih", "3. Gunakan Hint jika buntu", "4. Selesaikan sebelum waktu habis"]
    font_ui = fonts['ui']
    start_y = card_rect.y + 120
    for i, line in enumerate(lines):
        txt = font_ui.render(line, True, (0,0,0))
        screen.blit(txt, (card_rect.x + 50, start_y + i*60))

    # Tombol Kembali
    draw_button(screen, btn_back, "KEMBALI", fonts['menu'], mouse_pos, (0,0,0), (255,255,255))