from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
import io, os, subprocess, warnings, platform
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
    
    def build_extension(self, ext) -> None:
        if ext.extra_compile_args is None: ext.extra_compile_args = []
        if self.compiler.compiler_type == 'msvc':
            ext.extra_compile_args = [*ext.extra_compile_args, '/utf-8', '/w']
        elif self.compiler.compiler_type == 'mingw32':
            ext.extra_compile_args = [*ext.extra_compile_args, '-w']
        if isinstance(ext, PyScwsExtension):
            ext.prepare()
        return super().build_extension(ext)
        

class PyScwsExtension(Extension):
    def __init__(self, sources, *args, **kwargs):
        sources = [str(s) for s in sources]
        super().__init__('scws', sources, *args, **kwargs)

    def prepare(self):
        format_in(PROJECT_HOME / 'src' / 'scws' / 'libscws' / 'version.h.in', {
            'VERSION': 'git-%s' % get_git_repo_version(PROJECT_HOME / 'src' / 'scws'),
            'PACKAGE_BUGREPORT': 'Python: TsXor/pyscws, C: hightman/scws',
        })
        cy_me = cythonize([self])[0]
        self.sources = cy_me.sources


extensions = [
    PyScwsExtension([
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
    ])
]

setup(
    ext_modules=extensions,
    cmdclass={
        'build_ext': pyscws_build_ext,
    }
)