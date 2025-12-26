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
    Menggambar seluruh UI sebelah kanan:
    - Panel Background
    - Timer (Dimasukkan ke sini biar rapi)
    - Progress Bar
    - List Soal
    - Tombol Hint
    """
    # Unpack data game biar kodenya pendek
    level_name = game_data['level_name']
    answers = game_data['answers']
    found_words = game_data['found_words']
    current_dict = game_data['current_dict']
    hints_left = game_data['hints_left']
    time_left = game_data['time_left']
    btn_hint_rect = game_data['btn_hint_rect']

    # 1. SETUP AREA PANEL
    panel_x = START_X + (COLS * (GRID_SIZE + GRID_MARGIN)) + 40
    panel_width = 320 
    panel_height = SCREEN_HEIGHT - 60 
    
    # Background Panel (Ungu Gelap Magic)
    panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel_surf.fill(COLOR_PANEL_BG) 
    pygame.draw.rect(panel_surf, COLOR_PANEL_BORDER, (0,0, panel_width, panel_height), 3, border_radius=20)
    screen.blit(panel_surf, (panel_x, 30))

    content_x = panel_x + 25
    current_y = 60 

    # 2. GAMBAR TIMER (DI DALAM PANEL - PALING ATAS)
    # Konversi detik ke MM:SS
    minutes = int(time_left // 60)
    seconds = int(time_left % 60)
    timer_str = f"WAKTU: {minutes:02}:{seconds:02}"
    
    # Warna timer berubah merah jika < 30 detik
    timer_col = (255, 100, 100) if time_left < 30 else (255, 255, 255)
    
    timer_surf = fonts['ui'].render(timer_str, True, timer_col)
    screen.blit(timer_surf, (content_x, current_y - 15)) # Posisi paling atas
    
    current_y += 30 # Geser ke bawah

    # 3. JUDUL LEVEL
    title_surf = fonts['title'].render(level_name, True, (255, 255, 255))
    if title_surf.get_width() > panel_width - 50:
        scale = (panel_width - 50) / title_surf.get_width()
        title_surf = pygame.transform.scale(title_surf, (int(title_surf.get_width()*scale), int(title_surf.get_height()*scale)))
    
    screen.blit(title_surf, (content_x, current_y))
    current_y += 65
    
    # 4. PROGRESS BAR
    total_q = len(answers)
    found_q = len(found_words)
    progress_pct = found_q / total_q if total_q > 0 else 0
    
    bar_w = panel_width - 50
    bar_h = 10
    pygame.draw.rect(screen, (50, 40, 70), (content_x, current_y, bar_w, bar_h), border_radius=5)
    if progress_pct > 0:
        pygame.draw.rect(screen, COLOR_Q_DONE, (content_x, current_y, bar_w * progress_pct, bar_h), border_radius=5)
    
    # Teks progress angka
    prog_txt = fonts['ui'].render(f"{found_q}/{total_q}", True, (200, 200, 200))
    screen.blit(prog_txt, (content_x + bar_w - prog_txt.get_width(), current_y - 20))
    
    current_y += 25
    pygame.draw.line(screen, COLOR_PANEL_BORDER, (content_x, current_y), (content_x + bar_w, current_y), 1)
    current_y += 20

    # 5. DAFTAR SOAL
    for q, ans in current_dict.items():
        is_found = ans in found_words
        
        # Warna & Style
        text_col = COLOR_Q_DIM if is_found else COLOR_Q_ACTIVE
        ans_col = COLOR_Q_DONE if is_found else COLOR_SELECT
        
        # Ikon
        icon_center = (content_x + 8, current_y + 10)
        if is_found:
            pygame.draw.circle(screen, COLOR_Q_DONE, icon_center, 8)
            # Centang simpel
            pygame.draw.line(screen, (0,0,0), (icon_center[0]-3, icon_center[1]), (icon_center[0], icon_center[1]+3), 2)
            pygame.draw.line(screen, (0,0,0), (icon_center[0], icon_center[1]+3), (icon_center[0]+4, icon_center[1]-4), 2)
        else:
            pygame.draw.circle(screen, (150, 150, 200), icon_center, 8, 2)

        # Teks Soal
        display_q = (q[:22] + '..') if len(q) > 22 else q
        q_surf = fonts['ui'].render(display_q, True, text_col)
        screen.blit(q_surf, (content_x + 25, current_y))
        
        current_y += 22
        
        # Teks Jawaban (Placeholder / Asli)
        ans_display = ans if is_found else " ".join(["_" for _ in ans])
        a_surf = fonts['ui'].render(ans_display, True, ans_col)
        screen.blit(a_surf, (content_x + 25, current_y))
        
        current_y += 35 

    # 6. TOMBOL HINT
    btn_y = 30 + panel_height - 60
    btn_hint_rect.x = content_x
    btn_hint_rect.y = btn_y
    btn_hint_rect.width = panel_width - 50
    btn_hint_rect.height = 45

    if hints_left > 0:
        color = COLOR_BTN_HOVER if btn_hint_rect.collidepoint(mouse_pos) else COLOR_BTN_NORMAL
        shadow_offset = 4
        # Shadow
        pygame.draw.rect(screen, (100, 70, 0), (btn_hint_rect.x, btn_hint_rect.y + shadow_offset, btn_hint_rect.w, btn_hint_rect.h), border_radius=10)
    else:
        color = COLOR_BTN_DISABLED
        shadow_offset = 0

    # Body Tombol
    pygame.draw.rect(screen, color, btn_hint_rect, border_radius=10)
    
    # Teks Tombol
    hint_str = f"HINT ({hints_left})" if hints_left > 0 else "HINT HABIS"
    hint_surf = fonts['menu'].render(hint_str, True, (50, 30, 0) if hints_left > 0 else (200,200,200))
    hint_rect = hint_surf.get_rect(center=btn_hint_rect.center)
    screen.blit(hint_surf, hint_rect)   
    