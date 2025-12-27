import pygame
from helper.settings import *

def draw_timer(screen, remaining_seconds, font):
    """Menggambar Timer di pojok kanan atas atau di panel"""
    # Konversi detik ke format Menit:Detik (MM:SS)
    minutes = int(remaining_seconds // 60)
    seconds = int(remaining_seconds % 60)
    time_text = f"{minutes:02}:{seconds:02}" # Format 03:05
    
    # Render teks
    timer_surf = font.render(f"WAKTU: {time_text}", True, COLOR_TIMER)
    
    # Posisi: Di atas panel soal (Kanan Atas)
    panel_x = START_X + (COLS * (GRID_SIZE + GRID_MARGIN)) + 30
    screen.blit(timer_surf, (panel_x, 20))

def draw_game_panel(screen, fonts, game_data, mouse_pos):
    """
    Menggambar Panel Game Sebelah Kanan
    Style: Paper Card (Krem & Coklat) - High Contrast
    """
    # Unpack data
    level_name = game_data['level_name']
    answers = game_data['answers']
    found_words = game_data['found_words']
    current_dict = game_data['current_dict']
    hints_left = game_data['hints_left']
    time_left = game_data['time_left']
    btn_hint_rect = game_data['btn_hint_rect']

    # --- 1. SETUP AREA PANEL ---
    # Posisi panel di sebelah kanan grid
    panel_x = START_X + (COLS * (GRID_SIZE + GRID_MARGIN)) + 40
    panel_width = 340 # Lebarkan sedikit biar lega
    panel_height = SCREEN_HEIGHT - 60
    panel_y_start = 30 

    # --- BACKGROUND PANEL (PAPER STYLE) ---
    # Warna Krem Terang (Solid) agar kontras dengan teks
    PANEL_BG_COLOR = (255, 248, 220) 
    PANEL_BORDER_COLOR = (255, 255, 255) # Outline putih
    TEXT_COLOR = (80, 50, 20) # Coklat Tua (Enak dibaca)

    # Gambar Kotak Panel
    panel_rect = pygame.Rect(panel_x, panel_y_start, panel_width, panel_height)
    pygame.draw.rect(screen, PANEL_BG_COLOR, panel_rect, border_radius=20)
    pygame.draw.rect(screen, PANEL_BORDER_COLOR, panel_rect, 4, border_radius=20) # Outline tebal

    # Setup Kursor Menggambar (Jarak dari atas panel)
    content_x = panel_x + 25
    current_y = panel_y_start + 30

    # --- 2. TIMER & TIME BAR (PENGGANTI PROGRESS BAR) ---
    # Teks Waktu
    minutes = int(time_left // 60)
    seconds = int(time_left % 60)
    timer_str = f"WAKTU: {minutes:02}:{seconds:02}"
    
    # Warna Timer: Merah jika < 30 detik, selain itu Coklat
    timer_col = (220, 50, 50) if time_left < 30 else TEXT_COLOR
    timer_surf = fonts['ui'].render(timer_str, True, timer_col)
    screen.blit(timer_surf, (content_x, current_y))
    current_y += 30

    # GAMBAR TIME BAR
    bar_width_total = panel_width - 50
    ratio = max(0, time_left / LEVEL_DURATION)
    bar_width_current = int(bar_width_total * ratio)

    # Background Bar (Abu-abu tipis)
    pygame.draw.rect(screen, (220, 220, 210), (content_x, current_y, bar_width_total, 12), border_radius=6)
    
    # Isi Bar (Warna Oranye/Kuning bergradasi ke Merah)
    bar_color = (255, 165, 0) # Oranye default
    if ratio < 0.3: bar_color = (255, 70, 70) # Merah jika kritis
    
    if bar_width_current > 0:
        pygame.draw.rect(screen, bar_color, (content_x, current_y, bar_width_current, 12), border_radius=6)
    
    current_y += 30 # Jarak ke Judul

    # --- 3. JUDUL LEVEL ---
    # Garis pemisah tipis
    pygame.draw.line(screen, (200, 180, 150), (content_x, current_y), (content_x + bar_width_total, current_y), 2)
    current_y += 20

    title_surf = fonts['title'].render(level_name, True, TEXT_COLOR)
    # Scale jika kepanjangan
    if title_surf.get_width() > panel_width - 50:
        scale = (panel_width - 50) / title_surf.get_width()
        title_surf = pygame.transform.scale(title_surf, (int(title_surf.get_width()*scale), int(title_surf.get_height()*scale)))
    
    screen.blit(title_surf, (content_x, current_y))
    current_y += 60

    # --- 4. DAFTAR KATA (CHECKLIST) ---
    # Kita gambar daftar kata
    font_list = fonts['ui']
    
    for q, ans in current_dict.items():
        is_found = ans in found_words
        
        # Warna Teks
        if is_found:
            row_color = (180, 180, 180) # Abu-abu jika sudah ketemu
            icon_color = (100, 200, 100) # Ikon Hijau
        else:
            row_color = TEXT_COLOR # Coklat Tua jika belum
            icon_color = (200, 200, 200) # Ikon Abu
            
        # Gambar Ikon Bulat / Centang
        icon_pos = (content_x + 10, current_y + 10)
        pygame.draw.circle(screen, icon_color, icon_pos, 8)
        if is_found:
            # Gambar centang kecil putih
            pygame.draw.line(screen, (255,255,255), (icon_pos[0]-3, icon_pos[1]), (icon_pos[0], icon_pos[1]+3), 2)
            pygame.draw.line(screen, (255,255,255), (icon_pos[0], icon_pos[1]+3), (icon_pos[0]+4, icon_pos[1]-4), 2)

        # Teks Soal/Kata
        # Jika teks terlalu panjang, potong
        display_text = q
        if len(display_text) > 25: display_text = display_text[:22] + "..."
        
        txt_surf = font_list.render(display_text, True, row_color)
        
        # Efek Coret (Strikethrough) jika sudah ketemu
        if is_found:
            strike_w = txt_surf.get_width()
            pygame.draw.line(screen, row_color, (content_x + 25, current_y + 10), (content_x + 25 + strike_w, current_y + 10), 2)

        screen.blit(txt_surf, (content_x + 25, current_y))

            
        current_y += 35 # Jarak antar baris

    # --- 5. TOMBOL HINT (STYLE BARU) ---
    # Posisikan tombol hint di bagian bawah panel
    btn_y = panel_y_start + panel_height - 70 
    btn_hint_rect.x = content_x
    btn_hint_rect.y = btn_y
    btn_hint_rect.width = panel_width - 50
    btn_hint_rect.height = 50

    # Warna Tombol Hint (Kuning Emas)
    BTN_COLOR = (255, 200, 0)
    SHADOW_COLOR = (180, 140, 0)
    
    # Efek Tombol (Shadow + Body)
    if hints_left > 0:
        if btn_hint_rect.collidepoint(mouse_pos):
            # Hover effect
            current_btn_color = (255, 220, 50)
            offset_y = 2
            shadow_h = 4
        else:
            current_btn_color = BTN_COLOR
            offset_y = 0
            shadow_h = 6
            
        # Gambar Bayangan
        pygame.draw.rect(screen, SHADOW_COLOR, (btn_hint_rect.x, btn_hint_rect.y + offset_y + shadow_h, btn_hint_rect.w, btn_hint_rect.h), border_radius=12)
        # Gambar Body
        btn_draw_rect = pygame.Rect(btn_hint_rect.x, btn_hint_rect.y + offset_y, btn_hint_rect.w, btn_hint_rect.h)
        pygame.draw.rect(screen, current_btn_color, btn_draw_rect, border_radius=12)
        pygame.draw.rect(screen, (0,0,0), btn_draw_rect, 2, border_radius=12)
        
        # Teks Hint
        hint_text = f"HINT ({hints_left})"
        txt_surf = fonts['menu'].render(hint_text, True, (0,0,0))
        txt_rect = txt_surf.get_rect(center=btn_draw_rect.center)
        screen.blit(txt_surf, txt_rect)
        
    else:
        # Tombol Mati (Abu-abu)
        pygame.draw.rect(screen, (200, 200, 200), btn_hint_rect, border_radius=12)
        txt_surf = fonts['menu'].render("HINT HABIS", True, (150, 150, 150))
        txt_rect = txt_surf.get_rect(center=btn_hint_rect.center)
        screen.blit(txt_surf, txt_rect)