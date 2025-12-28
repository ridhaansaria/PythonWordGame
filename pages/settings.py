import pygame
from helper.settings import SCREEN_WIDTH, SCREEN_HEIGHT

def draw_settings_page(screen, fonts, current_duration, current_hints):
    """
    Menggambar halaman pengaturan.
    Returns:
       dict of rects: {'time_minus': rect, 'time_plus': Rect, ...}
       btn_back: Rect
    """
    # 1. Background
    BG_COLOR = (242, 169, 59)
    screen.fill(BG_COLOR)
    
    # 2. Judul
    font_title = fonts.get('title')
    title_surf = font_title.render("PENGATURAN", True, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
    screen.blit(title_surf, title_rect)

    # 3. Setup Layout
    cx = SCREEN_WIDTH // 2
    start_y = 200
    gap_y = 120
    
    font_label = fonts.get('menu')
    font_val = fonts.get('title')
    
    buttons = {}
    
    # --- HELPER DRAW ROW ---
    def draw_config_row(y_pos, label_text, value_text, key_prefix):
        # Label
        lbl_surf = font_label.render(label_text, True, (70, 40, 10))
        lbl_rect = lbl_surf.get_rect(center=(cx, y_pos - 40))
        screen.blit(lbl_surf, lbl_rect)
        
        # Value Box
        val_surf = font_val.render(value_text, True, (0, 0, 0))
        val_rect = val_surf.get_rect(center=(cx, y_pos + 10))
        
        # Buttons (-) [ Value ] (+)
        btn_size = 50
        spacing = 80
        
        # Minus Button
        rect_minus = pygame.Rect(0, 0, btn_size, btn_size)
        rect_minus.center = (cx - spacing - 40, y_pos + 10)
        
        # Plus Button
        rect_plus = pygame.Rect(0, 0, btn_size, btn_size)
        rect_plus.center = (cx + spacing + 40, y_pos + 10)
        
        # Draw Buttons
        mouse_pos = pygame.mouse.get_pos()
        
        for r, symb, k in [(rect_minus, "-", f"{key_prefix}_minus"), (rect_plus, "+", f"{key_prefix}_plus")]:
            is_hover = r.collidepoint(mouse_pos)
            col = (255, 200, 50) if not is_hover else (255, 230, 100)
            
            pygame.draw.rect(screen, (0,0,0), (r.x, r.y+4, r.w, r.h), border_radius=10)
            pygame.draw.rect(screen, col, r, border_radius=10)
            pygame.draw.rect(screen, (0,0,0), r, 2, border_radius=10)
            
            txt = font_label.render(symb, True, (0,0,0))
            tr = txt.get_rect(center=r.center)
            screen.blit(txt, tr)
            
            buttons[k] = r

        # Draw Value
        screen.blit(val_surf, val_rect)

    # --- ROW 1: WAKTU ---
    draw_config_row(start_y, "WAKTU (Detik)", str(current_duration), "time")
    
    # --- ROW 2: HINT ---
    draw_config_row(start_y + gap_y, "JUMLAH HINT", str(current_hints), "hint")

    # 4. Back Button (Simpan)
    btn_back = pygame.Rect(0, 0, 200, 60)
    btn_back.center = (cx, SCREEN_HEIGHT - 100)
    
    is_hover_back = btn_back.collidepoint(pygame.mouse.get_pos())
    back_col = (100, 255, 100) if not is_hover_back else (150, 255, 150)
    
    pygame.draw.rect(screen, (0,0,0), (btn_back.x, btn_back.y+4, btn_back.w, btn_back.h), border_radius=15)
    pygame.draw.rect(screen, back_col, btn_back, border_radius=15)
    pygame.draw.rect(screen, (0,0,0), btn_back, 2, border_radius=15)
    
    txt_surf = font_label.render("SIMPAN", True, (0,0,0))
    txt_rect = txt_surf.get_rect(center=btn_back.center)
    screen.blit(txt_surf, txt_rect)

    return buttons, btn_back
