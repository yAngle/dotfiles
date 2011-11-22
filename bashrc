export PATH=$HOME/bin:$PATH
export TEXINPUTS=".:$HOME/Documents/Repository/:"
[ -e /opt/intel/composerxe/bin/compilervars.sh ] && source /opt/intel/composerxe/bin/compilervars.sh intel64

# git
__git_ps1 ()
{
    local foo="bar"
}
[ -e $HOME/bin/git-completion.sh ] && source $HOME/bin/git-completion.sh

# Check for an interactive session
[ -z "$PS1" ] && return

alias ls="ls --color=auto"

# disable XON/XOFF, to use CTRL-S/Q
stty -ixon

# color grep
if echo hello|grep --color=auto l >/dev/null 2>&1; then
  export GREP_OPTIONS="--color=auto"
  export GREP_COLORS="ms=01;37;41:mc=01;31:sl=:cx=:fn=4;34:ln=32:bn=32:se=1;31"
fi

# PS1
PS1_NAME="home"
[ -e $HOME/.ps1-name ] && source $HOME/.ps1-name

case "$PS1_NAME" in
    "home")
        PS1='\[\e[0;33m\]\u \[\e[0;34m\]\w\[\e[1;36m\]$(__git_ps1 " [%s]") \[\e[0;33m\]\$ \[\e[0m\]';;
    "home-git")
        PS1='\[\e[1;30m\]\u\[\e[m\] \[\e[0;34m\]\w\[\e[m\]$(__git_ps1 " [%s]") \[\e[1;30m\]\$\[\e[m\] \[\e[0m\]';;
    "home-root")
        PS1='\[\e[0;32m\]\u\[\e[m\] \[\e[0;34m\]\w\[\e[m\]$(__git_ps1 " [%s]") \[\e[0;32m\]\$\[\e[m\] \[\e[0m\]';;
    "thinkpad")
        PS1='\[\e[1;35m\]\u \[\e[0;34m\]\w\[\e[1;36m\]$(__git_ps1 " [%s]") \[\e[1;35m\]\$ \[\e[0m\]';;
    "office")
        PS1='\[\e[0;36m\]\u \[\e[1;35m\]\w\[\e[1;36m\]$(__git_ps1 " [%s]") \[\e[0;33m\]\$ \[\e[0m\]';;
    "office-root")
        PS1='\[\e[1;35m\]\u \[\e[0;36m\]\w\[\e[1;36m\]$(__git_ps1 " [%s]") \[\e[0;33m\]\$ \[\e[0m\]';;
esac

if test "$TERM" = "xterm" -o \
        "$TERM" = "xterm-color" -o \
        "$TERM" = "xterm-256color" -o \
        "$TERM" = "rxvt" -o \
        "$TERM" = "rxvt-unicode" -o \
        "$TERM" = "xterm-xfree86"; then
    PROMPT_COMMAND='echo -ne "\033]0;${PWD/$HOME/~}\007"'
    export PROMPT_COMMAND
fi

