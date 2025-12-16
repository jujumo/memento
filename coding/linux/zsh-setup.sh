#!/bin/sh

# Install required packages
sudo apt-get update
sudo apt-get install -y zsh curl git nano htop 

# Install oh-my-zsh (official script)
RUNZSH=no ; 
OVERWRITE_CONFIRMATION=no ;
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"


# download custom theme
wget https://raw.githubusercontent.com/jujumo/memento/main/coding/linux/jumo.zsh-theme -O ~/.oh-my-zsh/themes/jumo.zsh-theme

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
rm -f profile.patch

echo "Now run 'source ~/.zshrc' or restart zsh to apply changes."