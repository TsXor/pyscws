from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
import io, os, subprocess, warnings, platform, yaml
from pathlib import Path


PROJECT_HOME = Path(__file__).parent
os.chdir(PROJECT_HOME)


def iter_fp_chars(fp: io.TextIOWrapper):
    char = fp.read(1)
    while char:
        yield char
        char = fp.read(1)

def format_in(path: Path, vars: dict[str, str]):
    with open(path, 'rt') as in_fp:
        with open(path.parent / path.name.removesuffix('.in'), 'wt') as out_fp:
            in_var: bool = False
            var_name: str = ''
            for in_char in iter_fp_chars(in_fp):
                if in_char == '@':
                    in_var = not in_var
                elif in_var:
                    var_name += in_char
                else:
                    if var_name:
                        out_fp.write(vars[var_name])
                        var_name = ''
                    out_fp.write(in_char)

def get_git_repo_version(path: Path):
    try:
        sp = subprocess.run(
            'git --help',
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    except subprocess.SubprocessError:
        return 'git-not-installed'

    orig_dir = Path('.').absolute()
    os.chdir(path)
    try:
        sp = subprocess.run(
            'git log -n 1 --pretty=format:%H',
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True
        )
        result = sp.stdout.decode()
    except subprocess.SubprocessError:
        result = 'unknown'
    os.chdir(orig_dir)
    return result

def format_classifiers(dic: dict):
    iter_stack = [iter(dic.items())]
    key_stack = [None]
    while iter_stack:
        try:
            k, this_data = next(iter_stack[-1])
            key_stack[-1] = k
            if len(key_stack) >= 2:
                yield ' :: '.join(key_stack)
            if type(this_data) is dict:
                iter_stack.append(iter(this_data.items()))
                key_stack.append(None)
            elif type(this_data) is list:
                for kwd in this_data:
                    yield ' :: '.join([*key_stack, kwd])
            else:
                yield ' :: '.join([*key_stack, str(this_data)])
        except StopIteration:
            iter_stack.pop()
            key_stack.pop()

def read_info(info_path: Path, readme_path: Path):
    with open(info_path, mode='rt', encoding='utf-8') as info_fp:
        data = yaml.load_all(info_fp, Loader=yaml.FullLoader)
        info = list(data)[0]
    info['classifiers'] = list(format_classifiers(info['classifiers']))
    info['keywords'] = ','.join(info['keywords'])
    with open(readme_path, mode='rt', encoding='utf-8') as readme_fp:
        info['long_description'] = readme_fp.read()
    version = info['version']
    version_reupload = info['version_reuploads'].get(version, 0)
    info['version'] = '%s.%d' % (version, version_reupload)
    return info

class pyscws_build_ext(build_ext):
    def run(self):
        bits, linkage = platform.architecture()
        #if self.compiler is None and 'windows' in linkage.lower():
        #    print('未指定编译器，选择mingw32')
        #    self.compiler = 'mingw32'
        if self.compiler == 'mingw32':
            if '64' in bits:
                if self.define is None: self.define = []
                self.define.append(('MS_WIN64', ''))
        super().run()
    
    def build_extension(self, ext):
        if ext.extra_compile_args is None: ext.extra_compile_args = []
        if self.compiler.compiler_type == 'msvc':
            ext.extra_compile_args = [*ext.extra_compile_args, '/utf-8', '/w']
        elif self.compiler.compiler_type == 'mingw32':
            ext.extra_compile_args = [*ext.extra_compile_args, '-w']
        if hasattr(ext, 'prepare') and callable(ext.prepare):
            ext.prepare()
        super().build_extension(ext)
        if hasattr(ext, 'dstdir'):
            ext_binpath = Path(self.get_ext_fullpath(ext.name))
            ext_dstpath = ext_binpath.parent
            for part in ext.dstdir.split('/'):
                ext_dstpath /= part
            ext_dstpath.mkdir(parents=True, exist_ok=True)
            ext_dstpath /= ext_binpath.name
            ext_binpath.replace(ext_dstpath)

class PyScwsExtension(Extension):
    def __init__(self):
        sources = [str(s) for s in (
            PROJECT_HOME / 'src' / 'scws.pyx',
            *(PROJECT_HOME / 'src' / 'scws' / 'libscws' / f for f in (
                'charset.c',
                'crc32.c',
                'pool.c',
                'scws.c',
                'xdict.c',
                'darray.c',
                'rule.c',
                'lock.c',
                'xdb.c',
                'xtree.c',
            ))
        )]
        self.dstdir = 'pyscws'
        super().__init__('scws', sources, include_dirs=[str(PROJECT_HOME / 'src')])

    def prepare(self):
        format_in(PROJECT_HOME / 'src' / 'scws' / 'libscws' / 'version.h.in', {
            'VERSION': 'git-%s' % get_git_repo_version(PROJECT_HOME / 'src' / 'scws'),
            'PACKAGE_BUGREPORT': 'Python: TsXor/pyscws, C: hightman/scws',
        })


extensions = [
    PyScwsExtension()
]

setup(
    ext_modules=extensions,
    cmdclass={
        'build_ext': pyscws_build_ext,
    },
    packages=['pyscws'],
    package_dir={'pyscws': 'src'},
    package_data={'pyscws': ['scws.pyi']},
    **read_info(
        PROJECT_HOME / 'info.yml',
        PROJECT_HOME / 'README.rst',
    )
)
