# My ANSI Art
Current ANSI Art image implementations use just one char "▀" (half block) to display low resolution image in a terminal.

This PoC aims to verify that using full range of ANSI block chars we can achive better resolution using the same number of chars.

Original image

![Original image](doc/imgs/big_buck_bunny_bird.jpg)

siv4 vs my-poc

|  siv4 algo  | my-poc algo |
| --- | --- |
| ![Original image](doc/imgs/siv4-ANSI-Art_6864-chars.png) | ![Original image](doc/imgs/my-PoC-ANSI-Art_6864-chars.png) |

### References (aka "Standing on the shoulders of giants")
* Shell Image Viewer v4 - https://www.uninformativ.de/git/bin-pub/file/siv4.html
* (Almost) square pixels in the terminal - http://www.uninformativ.de/blog/postings/2016-12-17/0/POSTING-en.html
* ANSI Block Elements - https://en.wikipedia.org/wiki/Block_Elements
* https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit
