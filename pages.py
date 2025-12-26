import pygame
from settings import *

def draw_button(screen, rect, text, font, mouse_pos):
    """Fungsi pembantu untuk menggambar tombol dengan efek hover"""
    # Cek apakah mouse ada di atas tombol (Hover)
    color = COLOR_SELECT if rect.collidepoint(mouse_pos) else COLOR_TILE
    
    # Gambar Kotak Tombol
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, (0,0,0), rect, 3, border_radius=10) # Border hitam
    
    # Gambar Teks di tengah tombol
    text_surf = font.render(text, True, (0,0,0))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_menu_page(screen, bg_image, font_title, font_btn, buttons):
    """Menggambar Halaman Menu Utama"""
    # 1. Background
    if bg_image: screen.blit(bg_image, (0, 0))
    else: screen.fill(COLOR_BG)
    
    # Overlay gelap transparan
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    screen.blit(overlay, (0,0))

    # 2. Judul Game
    title_text = "WORD SEARCH ADVENTURE"
    title_surf = font_title.render(title_text, True, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 150))
    
    # Efek Bayangan Judul
    shadow_surf = font_title.render(title_text, True, (0, 0, 0))
    screen.blit(shadow_surf, (title_rect.x + 3, title_rect.y + 3))
    screen.blit(title_surf, title_rect)

    # 3. Gambar Tombol (Start, Help, Quit)
    mouse_pos = pygame.mouse.get_pos()
    
    # Kita unpack list buttons: [btn_start, btn_help, btn_quit]
    draw_button(screen, buttons[0], "MULAI", font_btn, mouse_pos)
    draw_button(screen, buttons[1], "PETUNJUK", font_btn, mouse_pos)
    draw_button(screen, buttons[2], "KELUAR", font_btn, mouse_pos)

def draw_instructions_page(screen, bg_image, font_title, font_text, font_btn, btn_back):
    """Menggambar Halaman Petunjuk"""
    # 1. Background (sedikit lebih gelap biar teks terbaca)
    if bg_image: screen.blit(bg_image, (0, 0))
    else: screen.fill(COLOR_BG)
    
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) # Lebih gelap
    screen.blit(overlay, (0,0))
    
    # 2. Judul
    title = font_title.render("CARA BERMAIN", True, COLOR_SELECT)
    screen.blit(title, (50, 50))
    
    # 3. Daftar Instruksi
    instructions = [
        "1. Cari kata-kata tersembunyi di dalam kotak huruf.",
        "2. Kata bisa mendatar (Horizontal) atau menurun (Vertikal).",
        "3. Klik dan Tahan (Drag) mouse dari huruf awal ke akhir.",
        "4. Jika benar, kotak akan berubah warna hijau.",
        "5. Temukan semua kata untuk lanjut ke level berikutnya.",
        "",
        "Selamat Bermain!"
    ]
    
    y = 130
    for line in instructions:
        text = font_text.render(line, True, (255, 255, 255))
        screen.blit(text, (50, y))
        y += 40
        
    # 4. Tombol Kembali
    mouse_pos = pygame.mouse.get_pos()
    draw_button(screen, btn_back, "KEMBALI", font_btn, mouse_pos)