# utils.py
import random
import string

def create_grid(rows, cols, words):
    # Membuat grid kosong
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    
    for i, word in enumerate(words):
        placed = False
        attempts = 0
        
        # Logika Zig-Zag (Genap Horizontal, Ganjil Vertikal)
        if i % 2 == 0: priority_dirs = ['H', 'V']
        else: priority_dirs = ['V', 'H']
            
        while not placed and attempts < 200:
            direction = priority_dirs[0] if attempts < 100 else random.choice(['H', 'V'])

            if direction == 'H': # Horizontal
                if cols - len(word) < 0: continue 
                r = random.randint(0, rows - 1)
                c = random.randint(0, cols - len(word))
                
                # Cek Tabrakan
                collision = False
                for k in range(len(word)):
                    if grid[r][c + k] != '' and grid[r][c + k] != word[k]:
                        collision = True
                        break
                
                if not collision:
                    for k in range(len(word)): grid[r][c + k] = word[k]
                    placed = True
            
            else: # Vertikal
                if rows - len(word) < 0: continue
                r = random.randint(0, rows - len(word))
                c = random.randint(0, cols - 1)
                
                collision = False
                for k in range(len(word)):
                    if grid[r + k][c] != '' and grid[r + k][c] != word[k]:
                        collision = True
                        break
                
                if not collision:
                    for k in range(len(word)): grid[r + k][c] = word[k]
                    placed = True     
            attempts += 1
            
    # Isi kotak sisa dengan huruf acak
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '': grid[r][c] = random.choice(string.ascii_uppercase)
            
    return grid