# pyTrivialCache

[![PyPI](https://img.shields.io/pypi/v/pyTrivialCache.svg)](https://pypi.python.org/pypi/pyTrivialCache)

The poor man's API for manipulating a file system cache.

### Usage

As a standalone script:

        $ cd /tmp
        $ touch a b c

        $ pyTrivialCache --basedir $(mktemp -d)
        Welcome to the pyTrivialCache shell.  Type help or ? to list commands.

        (pyTrivialCache:ZILAYMHG) list

        (pyTrivialCache:ZILAYMHG) push a
        Pushing a unto ZILAYMHG.
        (pyTrivialCache:ZILAYMHG) push b
        Pushing b unto ZILAYMHG.
        (pyTrivialCache:ZILAYMHG) push c
        Pushing c unto ZILAYMHG.
        (pyTrivialCache:ZILAYMHG) list
        a
        b
        c

        (pyTrivialCache:ZILAYMHG) unpush c
        Unpushing c from ZILAYMHG.
        (pyTrivialCache:ZILAYMHG) list
        a
        b

        (pyTrivialCache:ZILAYMHG) purge
        Unpushing a from ZILAYMHG.
        Unpushing b from ZILAYMHG.
        (pyTrivialCache:ZILAYMHG) list

        (pyTrivialCache:ZILAYMHG) quit
        Disconnected from ZILAYMHG.

As a module:

        $ cd /tmp
        $ touch a b c

        from pyTrivialCache import pyTrivialCache
        import tempfile

        basedir = tempfile.mkdtemp()
        cache = pyTrivialCache(basedir)

        cache.traverse()
        > []

        cache.push('a')
        > Pushing a unto PVAK4UE0.
        cache.push('b')
        > Pushing b unto PVAK4UE0.
        cache.push('c')
        > Pushing c unto PVAK4UE0.
        cache.traverse()
        > ['a', 'b', 'c']

        cache.unpush('c')
        > Unpushing c from PVAK4UE0.
        cache.traverse()
        > ['a', 'b']

        cache.purge()
        > Unpushing a from PVAK4UE0.
        > Unpushing b from PVAK4UE0.
        cache.traverse()
        > []

### Tests

To run the test suite, the following environment variables should be defined; in addition, the `PYTRIVIALCACHE_WD` folder should contain at least three objects, namely, `a`, `b`, and `c`:

* `PYTRIVIALCACHE_BASEDIR`
* `PYTRIVIALCACHE_WD`

For example,

        $ export PYTRIVIALCACHE_BASEDIR=$(mktemp -d)
        $ export PYTRIVIALCACHE_WD=$(mktemp -d)
        $ touch $PYTRIVIALCACHE_WD/{a,b,c}
        $ python setup.py test
