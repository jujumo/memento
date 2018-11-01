import string
import os.path as path


def format_partial(template, **kwargs):
    return string.Template(template).safe_substitute(kwargs)


class ChocoArg:
    def __init__(self, name, syntax):
        self.name = name
        self._syntax = syntax

    def formating(self, **kwargs):
        formated = format_partial(self._syntax, **kwargs)
        formated = formated.replace('"', "'")
        return formated

    def help(self):
        return '--{name}="{value}"'.format(name=self.name,
                                           value=self.formating(installpath='<PATH>'))


class ChocoArgInstall(ChocoArg):
    def __init__(self, syntax):
        super().__init__('installargs', syntax)

    def formating(self, installpath=None):
        return super().formating(installpath=installpath)


class ChocoArgPackage(ChocoArg):
    def __init__(self, syntax):
        super().__init__('params', syntax)

    def formating(self, installpath=None):
        return super().formating(installpath=installpath)


class ChocoArgGroup:
    def __init__(self, name):
        self.name = name
        self.args = list()

    def update(self, choco_args):
        self.args.extend(arg for arg in choco_args if arg.name == self.name)

    def formating(self, **kwargs):
        formated = ' '.join(arg.formating(**kwargs) for arg in self.args)
        if formated:
            formated = '--{name}="{content}"'.format(name=self.name, content=formated)
        return formated


class ChocoPackage:
    def __init__(self, name, tags=[], installdir=[]):
        self.name = name
        self.tags = tags
        self.installdir_args = installdir if isinstance(installdir, list) else [installdir]
        # self.ia = ChocoArgGroup('installargs')
        # self.pp = ChocoArgGroup('params')
        # self.ia.update(self.installdir_args)
        # self.pp.update(self.installdir_args)

    def install_cmd(self, installdir=None, silent=True):
        # get all args
        installargs = ChocoArgGroup('installargs')
        params = ChocoArgGroup('params')
        if installdir:
            installargs.update(self.installdir_args)
            params.update(self.installdir_args)

        cmd_line = ['choco', 'install']
        if silent:
            cmd_line += ['-y']

        cmd_line.append(self.name)
        cmd_line.append(installargs.formating(installpath='{installdir}\\{name}'.format(installdir=installdir, name=self.name)))
        cmd_line.append(params.formating(installpath='{installdir}\\{name}'.format(installdir=installdir, name=self.name)))
        return cmd_line


ARG_D                    = ChocoArgInstall('/D="${installpath}"')
ARG_DIR                  = ChocoArgInstall('/DIR="${installpath}"')
ARG_INSTALLDIR           = ChocoArgInstall('INSTALLDIR="${installpath}"')
ARG_TARGETDIR            = ChocoArgInstall('TARGETDIR="${installpath}"')
ARG_APPLICATIONFOLDER    = ChocoArgInstall('APPLICATIONFOLDER="${installpath}"')
ARG_INSTALL_ROOT         = ChocoArgInstall('INSTALL_ROOT="${installpath}"')
ARG_INSTALLDIR_DEMI      = ChocoArgPackage('/InstallDir:"${installpath}"')
ARG_D_SEMI               = ChocoArgPackage('/D:"${installpath}"')
ARG_INSTALLPATH          = ChocoArgPackage('--installPath "${installpath}"')


packages = [
    ChocoPackage('firefox', installdir=ARG_D),
    ChocoPackage('7zip', installdir=ChocoArgInstall('/D="${installpath}_"')),
    ChocoPackage('pycharm-community', installdir=ARG_D),
    ChocoPackage('mpc-hc', installdir=ARG_DIR),
    ChocoPackage('notepadplusplus', installdir=ARG_D),
    ChocoPackage('foobar2000', installdir=ARG_D),
    ChocoPackage('filezilla', installdir=ARG_D),
    ChocoPackage('git', installdir=ARG_DIR),
    ChocoPackage('pandoc', installdir=ARG_APPLICATIONFOLDER),
    ChocoPackage('teracopy', installdir=ARG_DIR),
    ChocoPackage('python3', installdir=ARG_INSTALLDIR_DEMI),
    ChocoPackage('miniconda3', installdir=ARG_D_SEMI),
    ChocoPackage('handbrake', installdir=ARG_D),
    ChocoPackage('avidemux', installdir=ARG_D),
    ChocoPackage('inkscape', installdir=ARG_INSTALLDIR),
    ChocoPackage('virtualbox', installdir=ARG_INSTALLDIR),
    ChocoPackage('cmake', installdir=ARG_INSTALL_ROOT),
    ChocoPackage('gitextensions', installdir=ARG_INSTALL_ROOT),
    ChocoPackage('imagemagick', installdir=ARG_DIR),
    ChocoPackage('mobaxterm', installdir=ARG_INSTALLDIR),
    ChocoPackage('windirstat', installdir=ARG_D),
    ChocoPackage('meld', installdir=ARG_TARGETDIR),
    ChocoPackage('putty', installdir=ARG_INSTALLDIR),
    ChocoPackage('atom', installdir=ARG_D),
    ChocoPackage('gimp', installdir=ARG_DIR),
    ChocoPackage('visualstudio2017community', installdir=ARG_INSTALLPATH),
    ChocoPackage('ffmpeg')
]

""" BUILD PANODC """
doc_src = list()
doc_src.append('# image:icon_dos.svg["Chocolatey", width=64px] Chocolatey')
doc_src.append(':toc:\n\n')

""" INSTALL TABLE """
doc_src.append('.packages install path')
doc_src.append('[options="header"]')
doc_src.append('|=============================================================')
name_format = '| {:20}'
args_format = '| {:45}'
header = name_format.format('name') + args_format.format('install path argument')
doc_src.append(header + '\n')
for p in packages:
    line = name_format.format(p.name)
    cell_str = ', '.join('`' + c.help() + '`' for c in p.installdir_args) if p.installdir_args else 'NA.'
    line += args_format.format(cell_str)
    doc_src.append(line)
doc_src.append('|=============================================================')

""" INSTALL BATCH """
install_dirpath = r'C:\bin'

doc_src.append('\n\n.install.bat')
doc_src.append('[source,bat]')
doc_src.append('----')
for p in packages:
    cmd = p.install_cmd(install_dirpath)
    doc_src.append(' '.join(cmd))
doc_src.append('----')


""" WRITE FILE """
PANDOC_PATH = path.splitext(path.realpath(__file__))[0] + '.adoc'
with open(PANDOC_PATH, 'w') as f:
    f.write('\n'.join(doc_src))
