from collections import defaultdict

class Package:
    arg_set = set()

    def __init__(self, name, **kwargs):
        self.name = name
        self.args = kwargs
        for k in kwargs:
            Package.arg_set.add(k)


def format_some(string, **kwargs):

    return string.format_map(defaultdict(lambda x: 'XXXXX', **kwargs))


MSI_IA_FORMAT_D = '/D="{installpath}\{name}"'
MSI_IA_FORMAT_DIR = '/DIR="{installpath}\{name}"'
MSI_IA_FORMAT_INSTALLDIR = 'INSTALLDIR="{installpath}\{name}"'
MSI_IA_FORMAT_TARGETDIR = 'TARGETDIR="{installpath}\{name}"'
packages = [
    Package('7zip', installargs=format_some(MSI_IA_FORMAT_D, name='{name}_')),
    Package('firefox', installargs=MSI_IA_FORMAT_D),
    Package('virtualbox', params="/NoDesktopShortcut", installargs=MSI_IA_FORMAT_INSTALLDIR),
    Package('pycharm-community', installargs=MSI_IA_FORMAT_D),
    Package('mpc-hc', installargs=MSI_IA_FORMAT_DIR),
    Package('notepadplusplus', installargs=MSI_IA_FORMAT_D),
    Package('foobar2000', installargs=MSI_IA_FORMAT_D),
    Package('filezilla', installargs=MSI_IA_FORMAT_D),
    Package('git', installargs=MSI_IA_FORMAT_DIR),
    Package('pandoc', installargs='APPLICATIONFOLDER="{installpath}pandoc"'),
    Package('teracopy', installargs=MSI_IA_FORMAT_DIR),
    #Package('miniconda3', params=['/InstallationType:AllUsers', '/D:{installpath}miniconda3']),
    Package('handbrake', installargs=MSI_IA_FORMAT_D),
    Package('avidemux', installargs=MSI_IA_FORMAT_D),
    Package('inkscape', installargs=MSI_IA_FORMAT_INSTALLDIR),
    Package('virtualbox', params='/NoDesktopShortcut', installargs=MSI_IA_FORMAT_INSTALLDIR),
    Package('cmake', installargs='INSTALL_ROOT={installpath}cmake'),
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
cell_format = '| {:40}'
lab_format =  '| {:10}'
header = lab_format.format('name')
arg_names = sorted(Package.arg_set)
for arg_name in arg_names:
    header += cell_format.format('`' + arg_name + '`')
print(header + '\n')
for p in packages:
    line = lab_format.format(p.name)
    for arg_name in arg_names:
        line += cell_format.format('`' + p.args.get(arg_name) + '`' if arg_name in p.args else '--')
    print(line)
print('|=============================================================')

""" INSTALL BATCH """
install_dirpath = r'C:\bin'

print('\n\n.install.bat')
print('[source,bat]')
print('----')
for p in packages:
    cmd = ['choco', 'install']
    cmd += [f'--{n}=\'{v}\'' for n, v in p.args.items()]
    cmd = [a.format(installpath='PATH', name=p.name) for a in cmd]
    print(' '.join(cmd))
print('----')