#!/bin/sh

# Create patch file
cat <<'EOT' > profile.patch
11c11
< ZSH_THEME="robbyrussell"
---
> ZSH_THEME="jumo"
73c73,82
< plugins=(git)
---
> plugins=(
>         cp
>         gitfast
>         common-aliases
>         rsync
>         debian
>         sudo
>         screen
>         docker
> )
EOT

# Apply patch
patch ~/.zshrc -i profile.patch

# Source updated .zshrc
. ~/.zshrc