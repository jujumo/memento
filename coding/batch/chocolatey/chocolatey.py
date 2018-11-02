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
        formated = formated.replace("'", '"')
        return formated

    def help(self):
        return "--{name}='{value}'".format(name=self.name,
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


IA_ARG_D                    = ChocoArgInstall('/D="${installpath}"')
ARG_DIR                  = ChocoArgInstall('/DIR="${installpath}"')
ARG_INSTALLDIR           = ChocoArgInstall('INSTALLDIR="${installpath}"')
ARG_TARGETDIR            = ChocoArgInstall('TARGETDIR="${installpath}"')
ARG_APPLICATIONFOLDER    = ChocoArgInstall('APPLICATIONFOLDER="${installpath}"')
ARG_INSTALL_ROOT         = ChocoArgInstall('INSTALL_ROOT="${installpath}"')
ARG_INSTALLDIR_DEMI      = ChocoArgPackage('/InstallDir:"${installpath}"')
ARG_D_SEMI               = ChocoArgPackage('/D:"${installpath}"')
ARG_INSTALLPATH          = ChocoArgPackage('--installPath "${installpath}"')


packages = [
    ChocoPackage('firefox', tags=['admin'], installdir=IA_ARG_D),
    ChocoPackage('7zip', tags=['admin'], installdir=ChocoArgInstall('/D="${installpath}_"')),
    ChocoPackage('pycharm-community', tags=['dev'], installdir=IA_ARG_D),
    ChocoPackage('mpc-hc', installdir=ARG_DIR),
    ChocoPackage('notepadplusplus', tags=['admin'], installdir=IA_ARG_D),
    ChocoPackage('foobar2000', installdir=IA_ARG_D),
    ChocoPackage('filezilla', tags=['admin'], installdir=IA_ARG_D),
    ChocoPackage('git', tags=['dev'], installdir=ARG_DIR),
    ChocoPackage('pandoc', tags=['admin'], installdir=ARG_APPLICATIONFOLDER),
    ChocoPackage('teracopy', tags=['admin'], installdir=ARG_DIR),
    ChocoPackage('python3', tags=['dev'], installdir=ARG_INSTALLDIR_DEMI),
    ChocoPackage('miniconda3', tags=['dev'], installdir=ARG_D_SEMI),
    ChocoPackage('handbrake', installdir=IA_ARG_D),
    ChocoPackage('avidemux', installdir=IA_ARG_D),
    ChocoPackage('inkscape', installdir=ARG_INSTALLDIR),
    ChocoPackage('virtualbox', installdir=ARG_INSTALLDIR),
    ChocoPackage('cmake', tags=['dev'], installdir=ARG_INSTALL_ROOT),
    ChocoPackage('gitextensions', tags=['dev'], installdir=ARG_INSTALL_ROOT),
    ChocoPackage('imagemagick', tags=['admin', 'dev'], installdir=ARG_DIR),
    ChocoPackage('mobaxterm', tags=['admin'], installdir=ARG_INSTALLDIR),
    ChocoPackage('windirstat', tags=['admin'], installdir=IA_ARG_D),
    ChocoPackage('meld', tags=['admin', 'dev'], installdir=ARG_TARGETDIR),
    ChocoPackage('putty', tags=['admin'], installdir=ARG_INSTALLDIR),
    ChocoPackage('atom', tags=['admin'], installdir=IA_ARG_D),
    ChocoPackage('gimp', tags=['dev'], installdir=ARG_DIR),
    ChocoPackage('visualstudio2017community', tags=['dev'], installdir=ARG_INSTALLPATH),
    ChocoPackage('kodi', installdir=IA_ARG_D),

    ChocoPackage('virtualclonedrive', tags=['admin']),
    ChocoPackage('ffmpeg')
]

doc_src = list()

""" INSTALL TABLE """
doc_src.clear()
doc_src.append('.packages install path')
doc_src.append('[options="header"]')
doc_src.append('|=============================================================')
name_format = '| {:20}'
args_format = '| {:45}'
header = name_format.format('name') + args_format.format('install path argument')
doc_src.append(header + '\n')
for name, args in ((p.name, p.installdir_args) for p in packages if p.installdir_args):
    line = name_format.format(name)
    cell_str = ', '.join('`' + c.help() + '`' for c in args)
    line += args_format.format(cell_str)
    doc_src.append(line)
doc_src.append('|=============================================================')

PANDOC_PATH = path.splitext(path.realpath(__file__))[0] + '_table.adoc'
with open(PANDOC_PATH, 'w') as f:
    f.write('\n'.join(doc_src))

""" INSTALL BATCH """
doc_src.clear()
install_dirpath = r'C:\bin'
for p in packages:
    cmd = p.install_cmd(install_dirpath)
    doc_src.append(' '.join(cmd))
doc_src.append('----')

PANDOC_PATH = path.splitext(path.realpath(__file__))[0] + '_install.bat'
with open(PANDOC_PATH, 'w') as f:
    f.write('\n'.join(doc_src))
