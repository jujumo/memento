![icon_markdown](icon_rsync.svg "icon_rsync") [MÉMENTO](../README.md)::rsync
=====

[use Rsync as a time machine](https://blog.interlinked.org/tutorials/rsync_time_machine.html)

http://zarino.co.uk/post/synology-rsync-backup

```bash
rsync -avRCxn --out-format="FILE: %n" --progress --compare-dest=../save1 orig save2/
```


most usefull options
---------------------

| short	| long			| description 	|
|-------|---------------|---------------|
| `-a`	| `--archive` 	| Archive and includes a bunch of parameters to recurse directories, copy symlinks as symlinks, preserve permissions, preserve modification times, preserve group, preserve owner, and preserve device files. You usually want that option for all your backups. |
| `-b`	| `--backup`	| Make backups (see --suffix & --backup-dir) |
| `-C`	| `--cvs-exclude`| Auto ignore files in the same way CVS does. |
|		| `--exclude=PATTERN` | Excludes files matching PATTERN. |
| `-i`	| `--itemize-changes` | Print infos about each change. |
| 		| `--no-owner` | It does not try to set the owner to match.  |
| 		| `--no-group` | It does not try to set the group to match.  |
| `-x`	| `--one-file-system` 	| avoid crossing a filesystem boundary when recursing. |
| `-P`  | `--partial --progress` | Continues interrupted transfers and show a progress status for each file. This isn’t really necessary but I like it. |
|		| `--progress` 	| Show progress during transfert |
|| `--rsync-path=PATH`	| Specify path to rsync on the remote machine |
| `-t`	| `--times`		| Preserves file timestamps. |
| `-x` 	|				|  this one is important because it prohibits rsync to go beyond the local filesystem. For example if you backup you Linux-root partition, you should not include the /proc directory because rsync will get stuck in it. -x excludes all mounted filesystems from the backup which is probably what you want in most cases. |
| 		| `--link-dest` | this is a neat way to make full backups of your computers without losing much space. rsync links unchanged files to the previous backup (using hard-links, see below if you don’t know hard-links) and only claims space for changed files. This only works if you have a backup at hand, otherwise you have to make at least one backup beforehand. |
| `-z` 	| `--compress`	| Compress file data during the transfer. |

### Destination

| short	| long			| description 	|
|-------|---------------|---------------|
| `-a`	| `--archive` 	| Archive mode: includes a bunch of parameters to recurse directories, copy symlinks as symlinks, preserve permissions, preserve modification times, preserve group, preserve owner, and preserve device files. You usually want that option for all your backups. |
| `-b`	| `--backup`	| Make backups (see --suffix & --backup-dir) |
|		| `--backup-dir=DIR` 	|  Make backups into this directory |
|		| `--suffix=SUFFIX` 	| Override backup suffix |
| `-C`	| `--cvs-exclude`| Auto ignore files in the same way CVS does. |
| `-z` 	| `--compress`	| Compress file data during the transfer. |