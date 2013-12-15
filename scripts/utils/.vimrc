syntax enable
set tw=78
set sw=4
set ts=4
set sm
autocmd BufRead,BufNewFile *.py syntax on
autocmd BufRead,BufNewFile *.py set ai
set autoindent
set cindent
set expandtab
set showmatch
set paste
"para hacer lo mismo desde vim : zn 
set nofoldenable
"set number
"colores
"highlight Comment ctermfg=lightblue 
"colorscheme peachpuff
"colorscheme darkblue 
"set spell spellang=en

" Only do this part when compiled with support for autocommands
if has("autocmd")
  " In text files, always limit the width of text to 80 characters
  autocmd BufRead *.txt set tw=80
  " When editing a file, always jump to the last cursor position
  autocmd BufReadPost *
  \ if line("'\"") > 0 && line ("'\"") <= line("$") |
  \   exe "normal! g'\"" |
  \ endif
endif

" decimal in hex => echo printf('%x',123)
" hex to decimal => echo 0x123
" setlocal display=uhex
" set list
