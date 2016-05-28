" pathogen
execute pathogen#infect()
call pathogen#helptags()

"set lines=30 columns=95 " start size
set nocp " non-compatible
set bs=2 " backspace through leading spaces & linebreak
set fo=cqrt " format for comments etc.
set ls=2 " always show status line
set ww=<,>,h,l,[,] " move cursor through linebreaks
set tabstop=8 " width of \t
set autochdir " cd to current file
set autoindent " pass indentation of the current line to the new line
set smartindent " indent after { and noindent before #
set expandtab " convert tab input to spaces
set softtabstop=4
set shiftwidth=4 " control the reindentation with < and >
set incsearch " search while typing
set pastetoggle=<F10> " Toggle paste/insert mode
set wildmode=longest:full " autocomplete filenames to the longest possible
set wildmenu " show autocomplete multiple matches
set title " set teminal title
set nojoinspaces " single space after '.' when joining lines
set foldlevel=99 " unfold all by default
set spellcapcheck= " skip capitalization check

set display+=lastline " partially display lastline even if it doesn't fit

syntax on " syntax highlight
filetype plugin indent on " enable type-specific plugins
"let loaded_matchparen = 1 " disable bracket matching

" disable help
nnoremap <F1> <nop>

" disable Ex mode
nnoremap Q <nop>

" disable man page lookup
nnoremap K <nop>
vnoremap K <nop>

" line numbers
set number
nnoremap <F2> :set nonumber!<CR>:set foldcolumn=0<CR>

" highlight the search query word, disable highlight when entering insert mode
set hlsearch
autocmd InsertEnter * :let @/=""
autocmd InsertLeave * :let @/=""

" Navigate over windows
"noremap <C-J> <C-W>j
"noremap <C-K> <C-W>k
"noremap <C-H> <C-W>h
"noremap <C-L> <C-W>l

" tex filetype -- the attempt to judge by content will fail for those files without headers
au BufRead,BufNewFile *.tex setlocal spell filetype=tex
au BufRead,BufNewFile *.cls setlocal spell filetype=tex
au BufRead,BufNewFile *.sty setlocal spell filetype=tex

" buftabs  -- use :bd to close current buffer!
set hidden " change buffer without saving
let g:buftabs_only_basename=1
let g:buftabs_in_statusline=1
noremap <C-J> :bprev<CR>
noremap <C-K> :bnext<CR>
noremap <C-Q> :bd<CR>
"noremap <C-j> :call Buftabs_show(expand('<abuf>'))<CR>

"" ctags for c++
"map <F8> :!~/.bin/generate-diagham-tags<CR>
"set tags+=~/.bin/diagham-tags

" asymptote
augroup filetypedetect
au BufNewFile,BufRead *.asy     setf asy
augroup END
filetype plugin on

" python
let python_highlight_all = 1
let python_version_2 = 1
au! FileType python setl nosmartindent " http://stackoverflow.com/a/2064318

" release Ctrl-C from SQL plugin
let g:ftplugin_sql_omni_key = '<C-j>'

"set term=rxvt-unicode # enables italics, but screen bleeds after exit vim
set background=dark
set t_Co=256
set t_AB=[48;5;%dm
set t_AF=[38;5;%dm
colorscheme mycolors
