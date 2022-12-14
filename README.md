# My ANSI Art
Current ANSI Art image implementations use just one char "▀" (half block) to display low resolution image in a terminal.

This PoC aims to verify that using full range of ANSI block chars we can achive better resolution using the same number of chars.

## siv4 vs my-poc

#### original image 

<img src="doc/imgs/big_buck_bunny_bird.jpg" width=50%>

| siv4  | my-poc  |
| --- | --- |
|  $ ./siv4 doc/imgs/big_buck_bunny_bird.jpg  | $ ./my-poc doc/imgs/big_buck_bunny_bird.jpg |
| ![Original image](doc/imgs/siv4-ANSI-Art_6864-chars.png) | ![Original image](doc/imgs/my-PoC-ANSI-Art_6864-chars.png) |

More exemples [here](examples.md)

## Video player integration
I've integrated this algorithm in MPV opensource video player. See my fork with [new TCT algorithm](https://github.com/fsantagostinobietti/mpv/tree/tct-extended).
You can see video comparison:

### 'half-blocks' original algo 
https://user-images.githubusercontent.com/6057026/191210663-6cb56148-c3da-4792-a115-75cf79b20660.mp4 

###  'multi-blocks' new algo
https://user-images.githubusercontent.com/6057026/191210823-c5482fd3-2bb3-4200-b34e-8c1583a9c340.mp4


### References (aka "Standing on the shoulders of giants")
* Shell Image Viewer v4 - https://www.uninformativ.de/git/bin-pub/file/siv4.html
* (Almost) square pixels in the terminal - http://www.uninformativ.de/blog/postings/2016-12-17/0/POSTING-en.html
* ANSI Block Elements - https://en.wikipedia.org/wiki/Block_Elements
* https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit

### Similar projects
* https://github.com/stefanhaustein/TerminalImageViewer
