import os
import setuptools
import sys

from distutils import log
from distutils.command.build_ext import build_ext
from setuptools import Extension

PACKAGE_NAME = "cipherforsqlite"
VERSION = '1.0.0'
LONG_DESCRIPTION = \
"""A simple python package that works straight from pip. Based on pysqlcipher3"""

sources = [os.path.join("src", source)
           for source in ["blob.c", "module.c", "connection.c", "cursor.c", "cache.c",
                          "microprotocols.c", "prepare_protocol.c",
                          "statement.c", "util.c", "row.c"]]

packages = [PACKAGE_NAME, PACKAGE_NAME + ".test"]
include_dirs = []
packages.append(PACKAGE_NAME + ".test.python3")
EXTENSION_MODULE_NAME = "._sqlite3"

def quote_argument(arg):
    quote = '"'
    return quote + arg + quote

define_macros = [('MODULE_NAME', quote_argument(PACKAGE_NAME + '.dbapi2'))]

class AmalgationLibSQLCipherBuilder(build_ext):
    amalgamation_root = "amalgamation"
    amalgamation_header = os.path.join(amalgamation_root, 'sqlite3.h')
    amalgamation_source = os.path.join(amalgamation_root, 'sqlite3.c')

    def build_extension(self, ext):
        ext.define_macros.append(("SQLITE_ENABLE_FTS3", "1"))
        ext.define_macros.append(("SQLITE_ENABLE_RTREE", "1"))
        ext.define_macros.append(("SQLITE_ENABLE_LOAD_EXTENSION", "1"))
        ext.define_macros.append(("SQLITE_HAS_CODEC", "1"))
        ext.define_macros.append(("SQLITE_TEMP_STORE", "2"))

        ext.include_dirs.append(self.amalgamation_root)
        ext.sources.append(os.path.join(self.amalgamation_root, "sqlite3.c"))

        build_ext.build_extension(self, ext)

    def __setattr__(self, k, v):
        if k == "libraries":
            v = None
        self.__dict__[k] = v


def get_setup_args():
    return dict(
        name=PACKAGE_NAME,
        version=VERSION,
        python_requires=">=3.3",
        author="Maja Roczek",
        description="A simple python package that works straight from pip. Based on pysqlcipher3",
        long_description=LONG_DESCRIPTION,
        license="zlib/libpng",
        platforms="ALL",
        package_dir={PACKAGE_NAME: "lib"},
        packages=packages,
        ext_modules=[Extension(
            name=PACKAGE_NAME + EXTENSION_MODULE_NAME,
            sources=sources,
            define_macros=define_macros,
        extra_compile_args=['-fvisibility=default', '-fno-strict-aliasing'],
        extra_link_args=['-fvisibility=default']),
        ],
        cmdclass={
            "build_amalgamation": AmalgationLibSQLCipherBuilder
        },
        install_requires=[]
    )

def main():
    try:
        setuptools.setup(**get_setup_args())
    except BaseException as ex:
        log.info(str(ex))

if __name__ == "__main__":
    main()