import pygame
from helper.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from helper.levels import LEVEL_DATA

def draw_level_select_page(screen, fonts, level_data, current_page=0):
    """
    Menggambar halaman pemilihan level.
    Menampilkan level sesuai tema (misal 1-10 Forest).
    """
    # 1. Background
    BG_COLOR = (242, 169, 59)
    screen.fill(BG_COLOR)
    
    # 2. Judul
    font_title = fonts.get('title')
    title_surf = font_title.render("PILIH LEVEL", True, (255, 255, 255))
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 60))
    screen.blit(title_surf, title_rect)

    # 3. Setup Grid Layout
    cols = 5
    rows = 2 # 10 levels per page seems reasonable
    
    start_x = 100
    start_y = 150
    btn_w = 100
    btn_h = 100
    gap = 40
    
    # Pagination Logic
    levels_per_page = 10
    total_levels = len(level_data)
    total_pages = (total_levels - 1) // levels_per_page + 1
    
    start_index = current_page * levels_per_page
    end_index = min(start_index + levels_per_page, total_levels)
    
    # Determine Theme Info based on page
    # Page 0 (Lv 1-10) -> Karakter
    # Page 1 (Lv 11-20) -> Sosial 
    # Page 2 (Lv 21+) -> Kehidupan
    theme_name = "KARAKTER"
    if current_page == 1: theme_name = "SOSIAL"
    elif current_page >= 2: theme_name = "KEHIDUPAN"
    
    # Draw Theme Header
    font_theme = fonts.get('menu')
    theme_surf = font_theme.render(f"THEME: {theme_name}", True, (92, 58, 33)) # Brownish
    screen.blit(theme_surf, (50, 100))

    level_buttons = [] # Store rects and level indices to return

    mouse_pos = pygame.mouse.get_pos()
    
    for i in range(start_index, end_index):
        rel_i = i - start_index
        r = rel_i // cols
        c = rel_i % cols
        
        x = start_x + c * (btn_w + gap)
        y = start_y + r * (btn_h + gap)
        
        rect = pygame.Rect(x, y, btn_w, btn_h)
        
        # Draw Button
        is_hover = rect.collidepoint(mouse_pos)
        color = (255, 248, 220) if not is_hover else (255, 255, 200)
        
        # Shadow
        pygame.draw.rect(screen, (70, 40, 10), (x, y+5, btn_w, btn_h), border_radius=15)
        # Main Body
        pygame.draw.rect(screen, color, rect, border_radius=15)
        # Outline
        pygame.draw.rect(screen, (70, 40, 10), rect, 3, border_radius=15)
        
        # Number Text
        font_num = fonts.get('title')
        num_surf = font_num.render(str(i + 1), True, (70, 40, 10))
        num_rect = num_surf.get_rect(center=rect.center)
        screen.blit(num_surf, num_rect)
        
        level_buttons.append((rect, i))

    # 4. Navigation Buttons (Back, Prev, Next)
    # Styles
    font_btn = fonts.get('menu')
    
    def draw_nav_btn(rect, text):
        is_hover = rect.collidepoint(mouse_pos)
        bg_col = (255, 100, 100) if "KEMBALI" in text else (255, 248, 220)
        if is_hover:
             bg_col = (255, 150, 150) if "KEMBALI" in text else (255, 255, 200)
        
        text_col = (255, 255, 255) if "KEMBALI" in text else (0,0,0)

        pygame.draw.rect(screen, (0,0,0), (rect.x, rect.y+4, rect.w, rect.h), border_radius=10)
        pygame.draw.rect(screen, bg_col, rect, border_radius=10)
        pygame.draw.rect(screen, (0,0,0), rect, 2, border_radius=10)
        
        txt_surf = font_btn.render(text, True, text_col)
        txt_rect = txt_surf.get_rect(center=rect.center)
        screen.blit(txt_surf, txt_rect)

    # Back Button
    btn_back = pygame.Rect(30, SCREEN_HEIGHT - 80, 150, 50)
    draw_nav_btn(btn_back, "KEMBALI")

    # Prev Button
    btn_prev = None
    if current_page > 0:
        btn_prev = pygame.Rect(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 80, 120, 50)
        draw_nav_btn(btn_prev, "< PREV")

    # Next Button
    btn_next = None
    if current_page < total_pages - 1:
        btn_next = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 80, 120, 50)
        draw_nav_btn(btn_next, "NEXT >")

    return level_buttons, btn_back, btn_prev, btn_next
