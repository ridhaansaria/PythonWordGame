import random
import string

def create_grid(rows, cols, words):
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    locations = {} # (BARU) Kamus untuk menyimpan koordinat jawaban
    
    for i, word in enumerate(words):
        placed = False
        attempts = 0
        
        # Logika Zig-Zag
        if i % 2 == 0: priority_dirs = ['H', 'V']
        else: priority_dirs = ['V', 'H']
            
        while not placed and attempts < 200:
            direction = priority_dirs[0] if attempts < 100 else random.choice(['H', 'V'])

            if direction == 'H': 
                if cols - len(word) < 0: continue 
                r = random.randint(0, rows - 1)
                c = random.randint(0, cols - len(word))
                
                collision = False
                for k in range(len(word)):
                    if grid[r][c + k] != '' and grid[r][c + k] != word[k]:
                        collision = True
                        break
                
                if not collision:
                    word_coords = [] # Simpan koordinat kata ini
                    for k in range(len(word)): 
                        grid[r][c + k] = word[k]
                        word_coords.append((r, c + k))
                    
                    locations[word] = word_coords # Masukkan ke kamus
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
                    word_coords = []
                    for k in range(len(word)): 
                        grid[r + k][c] = word[k]
                        word_coords.append((r + k, c))
                        
                    locations[word] = word_coords
                    placed = True     
            attempts += 1
            
    # Isi sisa kotak
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '': grid[r][c] = random.choice(string.ascii_uppercase)
            
    return grid, locations # (BARU) Return 2 nilai