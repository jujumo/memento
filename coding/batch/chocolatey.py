import string


class Package:
    arg_set = set()

    def __init__(self, name, **kwargs):
        self.name = name
        self.args = dict()
        for k, v in kwargs.items():
            self.args[k] = v if isinstance(v, list) else [v]
        for k in self.args:
            Package.arg_set.add(k)


def format_some(template, **kwargs):
    return string.Template(template).safe_substitute(kwargs)


MSI_IA_FORMAT_D = '/D="${installpath}\${name}"'
MSI_IA_FORMAT_DIR = '/DIR="${installpath}\${name}"'
MSI_IA_FORMAT_INSTALLDIR = 'INSTALLDIR="${installpath}\${name}"'
MSI_IA_FORMAT_TARGETDIR = 'TARGETDIR="${installpath}\${name}"'
MSI_IA_FORMAT_APPLICATIONFOLDER = 'APPLICATIONFOLDER="${installpath}\${name}"'
MSI_IA_FORMAT_INSTALL_ROOT = 'INSTALL_ROOT="${installpath}\${name}"'

packages = [
    Package('7zip', installargs=format_some(MSI_IA_FORMAT_D, name='${name}_')),
    Package('firefox', installargs=MSI_IA_FORMAT_D),
    Package('virtualbox', params="/NoDesktopShortcut", installargs=MSI_IA_FORMAT_INSTALLDIR),
    Package('pycharm-community', installargs=MSI_IA_FORMAT_D),
    Package('mpc-hc', installargs=MSI_IA_FORMAT_DIR),
    Package('notepadplusplus', installargs=MSI_IA_FORMAT_D),
    Package('foobar2000', installargs=MSI_IA_FORMAT_D),
    Package('filezilla', installargs=MSI_IA_FORMAT_D),
    Package('git', installargs=MSI_IA_FORMAT_DIR),
    Package('pandoc', installargs=[MSI_IA_FORMAT_APPLICATIONFOLDER, 'ALLUSERS=1']),
    Package('teracopy', installargs=MSI_IA_FORMAT_DIR),
    Package('python3', params='/InstallDir:"${installpath}\${name}"'),
    Package('miniconda3', params=['/InstallationType:AllUsers', '/D:${installpath}/${name}']),
    Package('handbrake', installargs=MSI_IA_FORMAT_D),
    Package('avidemux', installargs=MSI_IA_FORMAT_D),
    Package('inkscape', installargs=MSI_IA_FORMAT_INSTALLDIR),
    Package('virtualbox', params='/NoDesktopShortcut', installargs=MSI_IA_FORMAT_INSTALLDIR),
    Package('cmake', installargs='INSTALL_ROOT=${installpath}cmake'),
    Package('gitextensions', installargs=MSI_IA_FORMAT_INSTALLDIR),
    Package('imagemagick', installargs=MSI_IA_FORMAT_DIR),
    Package('mobaxterm', installargs=MSI_IA_FORMAT_INSTALLDIR),
    Package('windirstat ', installargs=MSI_IA_FORMAT_D),
    Package('meld', installargs=MSI_IA_FORMAT_TARGETDIR),
    Package('putty', installargs=MSI_IA_FORMAT_INSTALLDIR),
    Package('atom', installargs=MSI_IA_FORMAT_D),
    Package('ffmpeg')
]


""" INSTALL TABLE """
print('.install.bat')
print('[options="header"]')
print('|=============================================================')
cell_format = '| {:45}'
lab_format =  '| {:20}'
header = lab_format.format('name')
arg_names = sorted(Package.arg_set)
for arg_name in arg_names:
    header += cell_format.format('`' + arg_name + '`')
print(header + '\n')
for p in packages:
    line = lab_format.format(p.name)
    for arg_name in arg_names:
        cell_str = ', '.join('`' + c + '`' for c in p.args.get(arg_name)) if arg_name in p.args else '--'
        line += cell_format.format(cell_str)
    print(line)
print('|=============================================================')

""" INSTALL BATCH """
install_dirpath = r'C:\bin'

print('\n\n.install.bat')
print('[source,bat]')
print('----')
for p in packages:
    cmd = ['choco', 'install', p.name]
    cmd += [f'--{n}=\'{v}\'' for n, vs in p.args.items() for v in vs]
    cmd = [format_some(arg, installpath='%bin%', name=p.name) for arg in cmd]
    print(' '.join(cmd))
print('----')