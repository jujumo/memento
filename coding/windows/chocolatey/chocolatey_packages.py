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
        formated = formated.replace('"', '""')
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
            formated = '--{name}=\'{content}\''.format(name=self.name, content=formated)
        return formated


class ChocoPackage:
    def __init__(self, name, tags=[], installdir=[]):
        self.name = name
        self.tags = tags
        self.installdir_args = installdir if isinstance(installdir, list) else [installdir]

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


# installargs
IA_D_EQ                    = ChocoArgInstall('/D="${installpath}"')
IA_DIR_EQ                  = ChocoArgInstall('/DIR="${installpath}"')
IA_INSTALLDIR_EQ           = ChocoArgInstall('INSTALLDIR="${installpath}"')
IA_TARGETDIR_EQ            = ChocoArgInstall('TARGETDIR="${installpath}"')
IA_APPLICATIONFOLDER_EQ    = ChocoArgInstall('APPLICATIONFOLDER="${installpath}"')
IA_INSTALL_ROOT_EQ         = ChocoArgInstall('INSTALL_ROOT="${installpath}"')
# parameters
PARAMS_ARG_D_EQ             = ChocoArgPackage('/D="${installpath}"')
PARAMS_INSTALLDIR_DEMI      = ChocoArgPackage('/InstallDir:"${installpath}"')
PARAMS_D_SEMI               = ChocoArgPackage('/D:"${installpath}"')
PARAMS_INSTALLPATH          = ChocoArgPackage('--installPath "${installpath}"')


packages = [
    ChocoPackage('firefox', tags=['admin'], installdir=IA_D_EQ),
    ChocoPackage('7zip', tags=['admin'], installdir=ChocoArgInstall('/D="${installpath}_"')),
    ChocoPackage('pycharm-community', tags=['dev'], installdir=IA_D_EQ),
    ChocoPackage('mpc-hc', tags=['media'], installdir=IA_DIR_EQ),
    ChocoPackage('notepadplusplus', tags=['admin'], installdir=IA_D_EQ),
    ChocoPackage('foobar2000', tags=['media'], installdir=IA_D_EQ),
    ChocoPackage('filezilla', tags=['admin'], installdir=IA_D_EQ),
    ChocoPackage('git', tags=['dev'], installdir=IA_DIR_EQ),
    ChocoPackage('pandoc', tags=['admin'], installdir=IA_APPLICATIONFOLDER_EQ),
    ChocoPackage('teracopy', tags=['admin'], installdir=IA_DIR_EQ),
    ChocoPackage('python3', tags=['dev'], installdir=PARAMS_INSTALLDIR_DEMI),
    ChocoPackage('miniconda3', tags=['dev'], installdir=IA_D_EQ),
    ChocoPackage('handbrake', tags=['media'], installdir=IA_D_EQ),
    ChocoPackage('avidemux', tags=['media'], installdir=IA_D_EQ),
    ChocoPackage('inkscape', tags=['media'], installdir=IA_INSTALLDIR_EQ),
    ChocoPackage('virtualbox', installdir=IA_INSTALLDIR_EQ),
    ChocoPackage('cmake', tags=['dev'], installdir=IA_INSTALL_ROOT_EQ),
    ChocoPackage('gitextensions', tags=['dev'], installdir=IA_INSTALL_ROOT_EQ),
    ChocoPackage('imagemagick', tags=['admin', 'dev', 'media'], installdir=IA_DIR_EQ),
    ChocoPackage('mobaxterm', tags=['admin'], installdir=IA_INSTALLDIR_EQ),
    ChocoPackage('windirstat', tags=['admin'], installdir=IA_D_EQ),
    ChocoPackage('meld', tags=['admin', 'dev'], installdir=IA_TARGETDIR_EQ),
    ChocoPackage('putty', tags=['admin'], installdir=IA_INSTALLDIR_EQ),
    ChocoPackage('atom', tags=['admin'], installdir=IA_D_EQ),
    ChocoPackage('gimp', tags=['dev', 'media'], installdir=IA_DIR_EQ),
    ChocoPackage('visualstudio2017community', tags=['dev'], installdir=PARAMS_INSTALLPATH),
    ChocoPackage('kodi', tags=['media'], installdir=IA_D_EQ),
    ChocoPackage('virtualclonedrive', tags=['admin'], installdir=IA_D_EQ),
    ChocoPackage('deluge', tags=['admin'], installdir=IA_D_EQ),
    ChocoPackage('fsviewer', tags=['media'], installdir=IA_D_EQ),
    ChocoPackage('retroarch', tags=['media'], installdir=IA_D_EQ),
    ChocoPackage('openssl.light', tags=['dev', 'admin'], installdir=PARAMS_INSTALLDIR_DEMI),
    ChocoPackage('ffmpeg', tags=['media', 'dev']),
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

PANDOC_PATH = path.splitext(path.realpath(__file__))[0] + '_install.bat'
with open(PANDOC_PATH, 'w') as f:
    f.write('\n'.join(doc_src))
