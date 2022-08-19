#!/usr/bin/python3

# 4x2 (rows x cols) size window of original scaled image that will be replaced 
# with a single unicode block char. We'll call it "char collapse window"

# Unicode block chars (https://en.wikipedia.org/wiki/Block_Elements) have a resolution of 
# 8x8 (rows x cols)

# In order to match with block chars resolution, we have to upscale image window to 8x8 size


from email.policy import default
from random import random
import sys, random, math

# ANSI utilities

def fg_rgb(r: int , g: int , b: int) -> str:
    return f"\u001b[38;2;{r};{g};{b}m"

def bg_rgb(r: int , g: int , b: int) -> str:
    return f"\u001b[48;2;{r};{g};{b}m"

def color_reset() -> str:
    return "\u001b[0m"

def ansi_char_sequence(char: str, fg: tuple[int,int,int], bg: tuple[int,int,int]) -> str:
    return fg_rgb(*fg) + bg_rgb(*bg) + char + color_reset()

# block chars map
BLOCK_CHAR = {
    '▀' : [ 1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,],
    '▐' : [ 0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,],
    '▟' : [ 0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,],
    '▜' : [ 1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,],
    '▛' : [ 1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,0,0,0,0,
            1,1,1,1,0,0,0,0,
            1,1,1,1,0,0,0,0,
            1,1,1,1,0,0,0,0,],
    '▙' : [ 1,1,1,1,0,0,0,0,
            1,1,1,1,0,0,0,0,
            1,1,1,1,0,0,0,0,
            1,1,1,1,0,0,0,0,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,],
    '▚' : [ 1,1,1,1,0,0,0,0,
            1,1,1,1,0,0,0,0,
            1,1,1,1,0,0,0,0,
            1,1,1,1,0,0,0,0,
            0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,
            0,0,0,0,1,1,1,1,],
    '▂' : [ 0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,],
    '▆' : [ 0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,],
    '▎' : [ 1,1,0,0,0,0,0,0,
            1,1,0,0,0,0,0,0,
            1,1,0,0,0,0,0,0,
            1,1,0,0,0,0,0,0,
            1,1,0,0,0,0,0,0,
            1,1,0,0,0,0,0,0,
            1,1,0,0,0,0,0,0,
            1,1,0,0,0,0,0,0,],
    '▊' : [ 1,1,1,1,1,1,0,0,
            1,1,1,1,1,1,0,0,
            1,1,1,1,1,1,0,0,
            1,1,1,1,1,1,0,0,
            1,1,1,1,1,1,0,0,
            1,1,1,1,1,1,0,0,
            1,1,1,1,1,1,0,0,
            1,1,1,1,1,1,0,0,],
    '▁' : [ 0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            1,1,1,1,1,1,1,1,],
    '▃' : [ 0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,],
    '▅' : [ 0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,],
    '▇' : [ 0,0,0,0,0,0,0,0,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,],
    '▏' : [ 1,0,0,0,0,0,0,0,
            1,0,0,0,0,0,0,0,
            1,0,0,0,0,0,0,0,
            1,0,0,0,0,0,0,0,
            1,0,0,0,0,0,0,0,
            1,0,0,0,0,0,0,0,
            1,0,0,0,0,0,0,0,
            1,0,0,0,0,0,0,0,],
    '▍' : [ 1,1,1,0,0,0,0,0,
            1,1,1,0,0,0,0,0,
            1,1,1,0,0,0,0,0,
            1,1,1,0,0,0,0,0,
            1,1,1,0,0,0,0,0,
            1,1,1,0,0,0,0,0,
            1,1,1,0,0,0,0,0,
            1,1,1,0,0,0,0,0,],
    '▋' : [ 1,1,1,1,1,0,0,0,
            1,1,1,1,1,0,0,0,
            1,1,1,1,1,0,0,0,
            1,1,1,1,1,0,0,0,
            1,1,1,1,1,0,0,0,
            1,1,1,1,1,0,0,0,
            1,1,1,1,1,0,0,0,
            1,1,1,1,1,0,0,0,],
    '▉' : [ 1,1,1,1,1,1,1,0,
            1,1,1,1,1,1,1,0,
            1,1,1,1,1,1,1,0,
            1,1,1,1,1,1,1,0,
            1,1,1,1,1,1,1,0,
            1,1,1,1,1,1,1,0,
            1,1,1,1,1,1,1,0,
            1,1,1,1,1,1,1,0,],
}

# char usage stats {char: int}
STATS = {}

class CharWindow:
    """Char collapse window: 4x2 (rows x cols) sized pixel"""
    
    def __init__(self) -> None:
        self.char_window_rgb = [] # list of rgb tuple

    def reset(self):
        self.char_window_rgb = []

    def add_row_rgb(self, row_rgb: list[tuple[int,int,int]]) -> None:
        self.char_window_rgb.extend( row_rgb )

    def print(self) -> None:
        for r in range(0, 8, 4):
            for c in range(2):
                fg = self.char_window_rgb[r+c+0]
                bg = self.char_window_rgb[r+c+2]
                print( fg_rgb(*fg) + bg_rgb(*bg) + "▀" + color_reset(), end="" )
            print()


    def get_upscaled_rgb(self, r: int, c: int) -> tuple[int, int, int]:
        """Upscaled window is 8x8 pixel. So 'r' and 'c' range in [0, 7]."""
        return self.char_window_rgb[ (r//2) * 2 + (c//4) ]

    def best_ansi_char(self) -> str:
        best_char, best_fg, best_bg, best_score = None, None, None, math.inf
        for char in BLOCK_CHAR:
            fg,bg = compute_fg_bg(char, self)
            score = compute_score(self, char, fg, bg)
            if score < best_score:
                best_char, best_fg, best_bg, best_score = char, fg, bg, score
        STATS[best_char] = STATS.get(best_char, 0) + 1
        return fg_rgb(*best_fg) + bg_rgb(*best_bg) + best_char + color_reset()


def compute_score(window: CharWindow, char: str, fg: tuple[int,int,int], bg: tuple[int,int,int]) -> int:
    """Compute fitness score for given char/fg/bg"""
    score = 0
    for r in range(8):
        for c in range(8):
            r0,g0,b0 = window.get_upscaled_rgb(r,c)
            is_fg = BLOCK_CHAR[char][r*8+c]==1
            r1,g1,b1 = fg if is_fg else bg
            score += math.sqrt((r1-r0)**2 + (g1-g0)**2 + (b1-b0)**2)
    return score

def compute_fg_bg(char: str, window: CharWindow) -> tuple[tuple[int,int,int], tuple[int,int,int]]:
    """Compute best fg/bg colors for given block char"""
    fg_r, fg_g, fg_b = 0, 0, 0
    bg_r, bg_g, bg_b = 0, 0, 0
    fg_count, bg_count = 0, 0
    for i in range(64):
        r,g,b = window.get_upscaled_rgb(i//8, i%8)
        is_fg = BLOCK_CHAR[char][i]>0
        if is_fg:
            fg_r += r
            fg_g += g
            fg_b += b
            fg_count += 1
        else:
            bg_r += r
            bg_g += g
            bg_b += b
            bg_count += 1
    return (fg_r//fg_count, fg_g//fg_count, fg_b//fg_count), (bg_r//bg_count, bg_g//bg_count, bg_b//bg_count)

def to_grayscale(r: int, g: int ,b: int) -> int:
    return int(0.3*r + 0.59*g + 0.11*b)

version = next(sys.stdin).rstrip()
if version != "P3":
    sys.stderr.write("ERR: wrong input format\n")
    quit()

cols, rows = ( int(v) for v in next(sys.stdin).rstrip().split() )

color_depth = next(sys.stdin).rstrip()
if color_depth != "255":
    sys.stderr.write("ERR: wrong input format\n")
    quit()

print("rows:", rows, "cols:", cols)


# load full image 
img_rgb = []
for line in sys.stdin:
    img_rgb.extend( [int(v) for v in line.rstrip().split()] )
# convert as list of pixels, i.e. tuples (r,g,b)
img_rgb = list( zip( *[iter(img_rgb)]*3 ) )

def build_window(r: int, c: int) -> CharWindow:
    win = CharWindow()
    for dr in range(4):
        idx = (4*r+dr) * cols
        win.add_row_rgb( [img_rgb[idx + c*2+0], img_rgb[idx + c*2+1]] )
    return win

# TEST
def test():
    tst =  build_window( random.randint(0, rows//4-1), random.randint(0, cols//2-1) )
    tst.print()
    for char in BLOCK_CHAR:
        fg,bg = compute_fg_bg(char,tst)
        score = compute_score(tst, char, fg, bg)
        print("score of", ansi_char_sequence(char, fg, bg), "is:", int(score))
    print("best ansi char is:",tst.best_ansi_char())

#test()
#quit()


for r in range(rows//4):
    for c in range(cols//2):
        win = build_window(r, c)
        print(win.best_ansi_char(), end='')
    print() # new line and flush
        
print(STATS)        

