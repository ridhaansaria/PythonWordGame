# ui_menu.py
import pygame
from helper.settings import *
from pages.common import draw_button 

def draw_suit_decoration(screen, center_x, center_y, suit_type):
    """Fungsi menggambar hiasan simbol kartu (Diamond/Heart)"""
    color = (200, 50, 50) # Merah redup
    if suit_type == "diamond":
        # Gambar Wajik (Diamond)
        pts = [
            (center_x, center_y - 15),
            (center_x + 12, center_y),
            (center_x, center_y + 15),
            (center_x - 12, center_y)
        ]
        pygame.draw.polygon(screen, color, pts)
    elif suit_type == "circle":
        # Gambar Lingkaran dekoratif
        pygame.draw.circle(screen, color, (center_x, center_y), 8)

def draw_menu_page(screen, bg_image, font_title, font_btn, buttons):
    """Menggambar Halaman Menu Utama dengan Gaya Royal"""
    
    # 1. Background & Overlay Gelap
    if bg_image: screen.blit(bg_image, (0, 0))
    else: screen.fill(COLOR_BG)
    
    # Overlay gelap agar background tidak terlalu nabrak teks
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(overlay, (0,0))

    # 2. Panel Menu Utama (Kotak Kaca di Tengah)
    panel_w, panel_h = 450, 550
    panel_x = (SCREEN_WIDTH - panel_w) // 2
    panel_y = (SCREEN_HEIGHT - panel_h) // 2
    
    # Surface transparan untuk panel
    panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel_surf.fill(COLOR_PANEL_BG)
    
    # Border Emas/Ungu terang
    pygame.draw.rect(panel_surf, COLOR_PANEL_BORDER, (0,0, panel_w, panel_h), 4, border_radius=25)
    
    # Garis dalam
    pygame.draw.rect(panel_surf, (100, 80, 120), (10, 10, panel_w-20, panel_h-20), 2, border_radius=18)
    
    screen.blit(panel_surf, (panel_x, panel_y))

    # 3. Dekorasi Sudut Panel
    draw_suit_decoration(screen, panel_x + 35, panel_y + 35, "diamond")
    draw_suit_decoration(screen, panel_x + panel_w - 35, panel_y + 35, "diamond")
    draw_suit_decoration(screen, panel_x + 35, panel_y + panel_h - 35, "circle")
    draw_suit_decoration(screen, panel_x + panel_w - 35, panel_y + panel_h - 35, "circle")

    # 4. Judul Game (Dengan Efek Glow/Shadow)
    title_text = "ALICE'S"
    subtitle_text = "WORD SEARCH"
    
    # Render Judul Utama (ALICE'S) - Besar
    base_title = font_title.render(title_text, True, COLOR_HINT) # Warna Emas
    scaled_title = pygame.transform.scale(base_title, (int(base_title.get_width() * 1.5), int(base_title.get_height() * 1.5)))
    title_rect = scaled_title.get_rect(center=(SCREEN_WIDTH//2, panel_y + 100))
    
    # Shadow Judul
    shadow_surf = font_title.render(title_text, True, (0, 0, 0))
    scaled_shadow = pygame.transform.scale(shadow_surf, (int(shadow_surf.get_width() * 1.5), int(shadow_surf.get_height() * 1.5)))
    screen.blit(scaled_shadow, (title_rect.x + 4, title_rect.y + 4))
    
    screen.blit(scaled_title, title_rect)

    # Render Sub-Judul (WORD SEARCH) - Putih
    sub_surf = font_btn.render(subtitle_text, True, (220, 220, 255))
    sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH//2, panel_y + 160))
    screen.blit(sub_surf, sub_rect)
    
    # Garis pemisah di bawah judul
    pygame.draw.line(screen, COLOR_PANEL_BORDER, (panel_x + 80, panel_y + 190), (panel_x + panel_w - 80, panel_y + 190), 2)

    # 5. Tombol-tombol Menu
    mouse_pos = pygame.mouse.get_pos()
    
    # Kita gambar loop semua tombol
    labels = ["MULAI PETUALANGAN", "PETUNJUK", "KELUAR"]

    GOLD_BUTTON_COLOR = (255, 200, 50) 
    TEXT_COLOR = (50, 30, 0)
    
    for i, btn_rect in enumerate(buttons):
        label = labels[i] if i < len(labels) else "TOMBOL"
        draw_button(
            screen, 
            btn_rect, 
            label, 
            font_btn, 
            mouse_pos, 
            bg_color=GOLD_BUTTON_COLOR,
            text_color=TEXT_COLOR      
        )

    # 6. Footer / Version Text
    ver_surf = pygame.font.SysFont("Arial", 12).render("v1.0 - Made with Python & Pygame", True, (100, 100, 150))
    ver_rect = ver_surf.get_rect(center=(SCREEN_WIDTH//2, panel_y + panel_h - 20))
    screen.blit(ver_surf, ver_rect)

def draw_instructions_page(screen, bg_image, fonts, btn_back, mouse_pos):
    """Menggambar Halaman Petunjuk dengan gaya Card Modern"""
    
    # 1. Background Utama
    if bg_image: screen.blit(bg_image, (0, 0))
    else: screen.fill(COLOR_BG)
    
    # Overlay Gelap (Supaya fokus ke tengah)
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0,0))
    
    # 2. Panel Kartu (Di Tengah Layar)
    card_w, card_h = 600, 500
    card_x = (SCREEN_WIDTH - card_w) // 2
    card_y = (SCREEN_HEIGHT - card_h) // 2
    
    # Gambar Panel
    card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
    card_surf.fill(COLOR_PANEL_BG) # Pakai warna tema Alice
    pygame.draw.rect(card_surf, COLOR_PANEL_BORDER, (0,0, card_w, card_h), 3, border_radius=20)
    screen.blit(card_surf, (card_x, card_y))

    # 3. Judul Halaman
    title_text = "CARA BERMAIN"
    title_surf = fonts['title'].render(title_text, True, COLOR_HINT) # Warna Emas
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, card_y + 50))
    
    # Garis bawah judul
    pygame.draw.line(screen, COLOR_HINT, (title_rect.left, title_rect.bottom + 5), (title_rect.right, title_rect.bottom + 5), 2)
    screen.blit(title_surf, title_rect)

    # 4. Daftar Instruksi dengan Ikon
    instructions = [
        ("Tujuan:", "Temukan semua kata tersembunyi."),
        ("Kontrol:", "Klik & Tahan (Drag) mouse pada grid."),
        ("Arah:", "Kata bisa Horizontal (Mendatar) atau Vertikal."),
        ("Bantuan:", "Gunakan tombol HINT jika buntu."),
        ("Menang:", "Selesaikan level sebelum waktu habis!")
    ]
    
    start_y = card_y + 110
    gap_y = 60
    
    for i, (label, desc) in enumerate(instructions):
        item_y = start_y + (i * gap_y)
        icon_x = card_x + 50
        text_x = card_x + 100
        
        # A. Gambar Ikon Simpel (Visual Cue)
        center_icon = (icon_x, item_y + 10)
        pygame.draw.circle(screen, (80, 60, 100), center_icon, 20) # Background ikon bulat
        pygame.draw.circle(screen, COLOR_PANEL_BORDER, center_icon, 20, 2) # Border ikon
        
        # Logika gambar ikon spesifik per baris
        if i == 0: # Tujuan (Kaca Pembesar)
            pygame.draw.circle(screen, COLOR_Q_ACTIVE, (icon_x-2, item_y+8), 6, 2)
            pygame.draw.line(screen, COLOR_Q_ACTIVE, (icon_x+2, item_y+12), (icon_x+6, item_y+16), 2)
        elif i == 1: # Kontrol (Mouse)
            pygame.draw.rect(screen, COLOR_Q_ACTIVE, (icon_x-6, item_y+2, 12, 16), 2, border_radius=4)
            pygame.draw.line(screen, COLOR_Q_ACTIVE, (icon_x, item_y+2), (icon_x, item_y+8), 2)
        elif i == 2: # Arah (Panah)
            pygame.draw.line(screen, COLOR_Q_ACTIVE, (icon_x-5, item_y+10), (icon_x+5, item_y+10), 2) # Hor
            pygame.draw.line(screen, COLOR_Q_ACTIVE, (icon_x, item_y+5), (icon_x, item_y+15), 2) # Ver
        elif i == 3: # Hint (Lampu)
            pygame.draw.circle(screen, (255, 255, 0), (icon_x, item_y+8), 6) # Bohlam
            pygame.draw.rect(screen, (200, 200, 200), (icon_x-3, item_y+14, 6, 4)) # Ulir
        elif i == 4: # Menang (Piala/Bintang)
             pygame.draw.polygon(screen, COLOR_HINT, [(icon_x, item_y+2), (icon_x-5, item_y+15), (icon_x+5, item_y+15)])

        # B. Teks Label (Warna Terang)
        lbl_surf = fonts['menu'].render(label, True, COLOR_SELECT)
        screen.blit(lbl_surf, (text_x, item_y - 5))
        
        # C. Teks Deskripsi (Warna Putih)
        desc_surf = fonts['ui'].render(desc, True, (220, 220, 220))
        screen.blit(desc_surf, (text_x, item_y + 25))

    # 5. Tombol KEMBALI (Gaya Button Mewah)
    # Update posisi rect tombol agar ada di bawah panel
    btn_back.centerx = SCREEN_WIDTH // 2
    btn_back.y = card_y + card_h + 20
    btn_back.width = 200
    btn_back.height = 50
    
    color = COLOR_BTN_HOVER if btn_back.collidepoint(mouse_pos) else COLOR_BTN_NORMAL
    
    # Shadow
    pygame.draw.rect(screen, (100, 70, 0), (btn_back.x, btn_back.y + 4, btn_back.w, btn_back.h), border_radius=10)
    # Body
    pygame.draw.rect(screen, color, btn_back, border_radius=10)
    
    text_surf = fonts['menu'].render("KEMBALI", True, (50, 30, 0))
    text_rect = text_surf.get_rect(center=btn_back.center)
    screen.blit(text_surf, text_rect)