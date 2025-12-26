import pygame
from helper.settings import *

def draw_button(screen, rect, text, font, mouse_pos, bg_color=None, text_color=(0,0,0)):
    """Fungsi helper tombol yang fleksibel"""
    
    # 1. Tentukan Warna Background
    if bg_color is None:
        base_color = COLOR_SELECT if rect.collidepoint(mouse_pos) else COLOR_TILE
    else:
        # Jika ada request warna (misal Emas), gunakan itu
        if rect.collidepoint(mouse_pos):
            # Trik bikin warna lebih terang: batasi max 255
            r, g, b = bg_color
            base_color = (min(255, r+30), min(255, g+30), min(255, b+30))
        else:
            base_color = bg_color

    # 2. Gambar Shadow (Efek 3D)
    pygame.draw.rect(screen, (50, 30, 0), (rect.x, rect.y + 4, rect.w, rect.h), border_radius=10)

    # 3. Gambar Body Tombol
    pygame.draw.rect(screen, base_color, rect, border_radius=10)
    pygame.draw.rect(screen, (50, 30, 0), rect, 2, border_radius=10) # Border tipis

    # 4. Gambar Teks
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)