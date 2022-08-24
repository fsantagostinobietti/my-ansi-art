#!/usr/bin/env python3

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
    """Char collapse window: RxC (rows x cols) sized pixel"""
    R, C = 8, 4 #4, 2  # rows, cols
    
    def __init__(self) -> None:
        self.char_window_rgb = [] # list of rgb tuple

    def add_row_rgb(self, row_rgb: list[tuple[int,int,int]]) -> None:
        self.char_window_rgb.extend( row_rgb )

    def __to_grayscale(self) -> None:
        self.char_window_rgb = [grayscale(*rgb) for rgb in self.char_window_rgb]

    def __to_bw(self) -> None:
        """ TEST - use only on grayscale image"""
        #self.__to_grayscale()
        threashold = sum([gray for gray,_,_ in self.char_window_rgb]) / len(self.char_window_rgb)
        self.char_window_rgb = [ (255,255,255) if g > threashold else (0,0,0) for g,_,_ in self.char_window_rgb ]


    def print(self) -> None:
        """Test purposes"""
        for r in range(0, CharWindow.R*CharWindow.C, CharWindow.R):
            for c in range(CharWindow.C):
                fg = self.char_window_rgb[r+c+0]
                bg = self.char_window_rgb[r+c+CharWindow.C]
                print( fg_rgb(*fg) + bg_rgb(*bg) + "▀" + color_reset(), end="" )
            print()
        print()
        char, _, _, _ = self.best_char()
        print("rgb: best char:", char)
        # grayscale
        self.__to_grayscale()
        for r in range(0, CharWindow.R*CharWindow.C, CharWindow.R):
            for c in range(CharWindow.C):
                fg = self.char_window_rgb[r+c+0]
                bg = self.char_window_rgb[r+c+CharWindow.C]
                print( fg_rgb(*fg) + bg_rgb(*bg) + "▀" + color_reset(), end="" )
            print()
        print()
        char, _, _, _ = self.best_char()
        print("grayscale: best char:", char)
        # black/white
        self.__to_bw()
        for r in range(0, CharWindow.R*CharWindow.C, CharWindow.R):
            for c in range(CharWindow.C):
                fg = self.char_window_rgb[r+c+0]
                bg = self.char_window_rgb[r+c+CharWindow.C]
                print( fg_rgb(*fg) + bg_rgb(*bg) + "▀" + color_reset(), end="" )
            print()
        char, _, _, _ = self.best_char()
        print("b/w: best char:", char)

    def get_upscaled_rgb(self, r: int, c: int) -> tuple[int, int, int]:
        """Upscaled window is 8x8 pixel. So 'r' and 'c' range in [0, 7]."""
        if (CharWindow.R,CharWindow.C) == (4,2):
            return self.char_window_rgb[ (r//2) * 2 + (c//4) ]
        elif (CharWindow.R,CharWindow.C) == (8,4):
            return self.char_window_rgb[ r*4 + (c//2) ]
        else:
            raise Exception("Usupported (R,C) !")

    def best_char(self) -> tuple[str, tuple[int, int, int], tuple[int, int, int], int]:
        """ Return the best block char for this window """
        best_char, best_fg, best_bg, best_loss = None, None, None, math.inf
        for char in BLOCK_CHAR:
            fg,bg = compute_fg_bg(char, self)
            loss = compute_loss(self, char, fg, bg)
            if loss < best_loss:
                best_char, best_fg, best_bg, best_loss = char, fg, bg, loss
        return best_char, best_fg, best_bg, best_loss

    def best_char2(self) -> tuple[str, tuple[int, int, int], tuple[int, int, int], int]:
        """ Use black/white to detect best char """
        # backup rgb list
        rgb_orig = self.char_window_rgb.copy()
        self.__to_grayscale()
        self.__to_bw()
        char,_,_,_ = self.best_char()
        # restore orig list
        self.char_window_rgb = rgb_orig
        fg,bg = compute_fg_bg(char, self)
        loss = compute_loss(self, char, fg, bg)
        return char, fg, bg, loss

    def printable_ansi_char(self, char: str, fg: int, bg: int) -> str:
        #STATS[best_char] = STATS.get(best_char, 0) + 1
        return fg_rgb(*fg) + bg_rgb(*bg) + char + color_reset()


def compute_loss(window: CharWindow, char: str, fg: tuple[int,int,int], bg: tuple[int,int,int]) -> int:
    """Compute loss for given char/fg/bg"""
    loss = 0
    for r in range(8):
        for c in range(8):
            r0,g0,b0 = window.get_upscaled_rgb(r,c)
            is_fg = BLOCK_CHAR[char][r*8+c]==1
            r1,g1,b1 = fg if is_fg else bg
            loss += (r1-r0)**2 + (g1-g0)**2 + (b1-b0)**2
    return loss

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

def grayscale(r: int, g: int ,b: int) -> tuple[int,int,int]:
    """compute grayscale value from rgb tuple"""
    gray = int(0.3*r + 0.59*g + 0.11*b)
    return (gray, gray, gray)

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
    for dr in range(CharWindow.R):
        base = (CharWindow.R*r+dr) * cols
        win.add_row_rgb( [ img_rgb[base + c*CharWindow.C+dc]  for dc in range(CharWindow.C) ] )
    return win

# TEST
def test():
    tst =  build_window( random.randint(0, rows//CharWindow.R-1), random.randint(0, cols//CharWindow.C-1) )
    tst.print()
    #for char in BLOCK_CHAR:
    #    fg,bg = compute_fg_bg(char,tst)
    #    loss = compute_loss(tst, char, fg, bg)
    #    print("[", ansi_char_sequence(char, fg, bg), "loss:", int(loss),"]", end="")
    #print()
    #best_char, best_fg, best_bg, _ = tst.best_char()
    #print("best ansi char is:",tst.printable_ansi_char(best_char, best_fg, best_bg))

#test()
#quit()


for r in range(rows//CharWindow.R):
    for c in range(cols//CharWindow.C):
        win = build_window(r, c)
        char, fg, bg, _ = win.best_char()
        print(win.printable_ansi_char(char, fg, bg), end='')
    print() # new line and flush
        
print(STATS)        

