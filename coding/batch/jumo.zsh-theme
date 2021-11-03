# vim:ft=zsh ts=2 sw=2 sts=2
#
# agnoster's Theme - https://gist.github.com/3712874
# A Powerline-inspired theme for ZSH
#
# # README
#
# In order for this theme to render correctly, you will need a
# [Powerline-patched font](https://github.com/Lokaltog/powerline-fonts).
# Make sure you have a recent version: the code points that Powerline
# uses changed in 2012, and older versions will display incorrectly,
# in confusing ways.
#
# In addition, I recommend the
# [Solarized theme](https://github.com/altercation/solarized/) and, if you're
# using it on Mac OS X, [iTerm 2](https://iterm2.com/) over Terminal.app -
# it has significantly better color fidelity.
#
# If using with "light" variant of the Solarized color schema, set
# SOLARIZED_THEME variable to "light". If you don't specify, we'll assume
# you're using the "dark" variant.
#
# # Goals
#
# The aim of this theme is to only show you *relevant* information. Like most
# prompts, it will only show git information when in a git working directory.
# However, it goes a step further: everything from the current user and
# hostname to whether the last call exited with an error to whether background
# jobs are running in this shell will all be displayed automatically when
# appropriate.

### Segment drawing
# A few utility functions to make it easy and re-usable to draw segmented prompts

LAST_SEGMENT='NONE'

case ${SOLARIZED_THEME:-dark} in
    light) CURRENT_FG='white';;
    *)     CURRENT_FG='black';;
esac

# Special Powerline characters

() {
  local LC_ALL="" LC_CTYPE="en_US.UTF-8"
  # NOTE: This segment separator character is correct.  In 2012, Powerline changed
  # the code points they use for their special characters. This is the new code point.
  # If this is not working for you, you probably have an old version of the
  # Powerline-patched fonts installed. Download and install the new version.
  # Do not submit PRs to change this unless you have reviewed the Powerline code point
  # history and have new information.
  # This is defined using a Unicode escape sequence so it is unambiguously readable, regardless of
  # what font the user is viewing this source code in. Do not replace the
  # escape sequence with a single literal character.
  # Do not change this! Do not make it '\u2b80'; that is the old, wrong code point.
  SEGMENT_SEPARATOR=$'-'
  SEGMENT_START=$'['
  SEGMENT_STOP=$']'
}


# Takes arguments foreground.  can be omitted,
prompt_segment() {
  local fg
  [[ -n $1 ]] && fg="%F{$1}" || fg="%f"

  if [[ $LAST_SEGMENT != 'NONE' ]]; then
    echo -n "%{%f%}$SEGMENT_SEPARATOR"
  fi

  LAST_SEGMENT=$2
  echo -n "$SEGMENT_START%{$fg%}$2%{%f%}$SEGMENT_STOP"
}

prompt_start() {
    if [[ $RETVAL -ne 0 ]]; then
         echo -n "%{%F{red}%}"
    fi
    echo -n "┌"
}


# End the prompt, closing any open segments
prompt_return() {
    echo -n "\n"
}

### Prompt components
# Each component will draw itself, and hide itself if no information needs to be shown

# Context: user@hostname (who am I and where am I)
prompt_context() {
  if [[ "$USER" != "$DEFAULT_USER" || -n "$SSH_CLIENT" ]]; then
    prompt_segment green "%(!.%{%F{yellow}%}.)%n@%m"
  fi
}

# if conda env is activated
prompt_conda() {
  (( ${+CONDA_PREFIX} )) || return
  CONDA_PROMPT_MODIFIER="[$(basename $CONDA_PREFIX)]"
  prompt_segment magenta $CONDA_PROMPT_MODIFIER
}

# Dir: current working directory: only dirname
prompt_dirpath() {
    prompt_segment blue "%1~/"
}

prompt_root() {
  ROOT_DIR=$(pwd -P | cut -d "/" -f2)
  PROMPT_ROOT="/${ROOT_DIR}"
  prompt_segment cyan $PROMPT_ROOT
}

# Dir: current working directory name
prompt_mount() {
    # display /root/…/dirname
    # where root is the root directory (helps to know )
    CURRENT_MNT=`findmnt -T ${PWD} -n -o TARGET`
    ROOT_MNT=$(echo "$CURRENT_MNT" | cut -d "/" -f2)
    PROMPT_MNT="/${ROOT_MNT}"
    prompt_segment cyan $PROMPT_MNT
}

# Virtualenv: current working virtualenv
prompt_virtualenv() {
  local virtualenv_path="$VIRTUAL_ENV"
  if [[ -n $virtualenv_path && -n $VIRTUAL_ENV_DISABLE_PROMPT ]]; then
    prompt_segment blue "(`basename $virtualenv_path`)"
  fi
}

prompt_time() {
    prompt_segment '012' '%*'
}

prompt_exec() {
    if [[ $RETVAL -ne 0 ]]; then
         echo -n "%{%F{red}%}"
    fi
    echo -n "└> %f%k"
}

build_prompt() {
    RETVAL=$?
    prompt_start
    prompt_time
    prompt_context
    prompt_conda
    prompt_root
    prompt_dirpath
    prompt_return
    prompt_exec
}

PROMPT='%{%f%b%k%}$(build_prompt)'
