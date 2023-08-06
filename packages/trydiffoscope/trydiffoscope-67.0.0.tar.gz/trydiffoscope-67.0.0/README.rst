-------------
trydiffoscope
-------------

Uploading
==========

Please also release a signed tarball:

::

    $ VERSION="$(dpkg-parsechangelog -SVersion)"

    $ git archive --format=tar --prefix=trydiffoscope-${VERSION}/ ${VERSION} | bzip2 -9 > trydiffoscope-${VERSION}.tar.bz2

    $ gpg --detach-sig --armor --output=trydiffoscope-${VERSION}.tar.bz2.asc < trydiffoscope-${VERSION}.tar.bz2

    $ scp trydiffoscope-${VERSION}* alioth.debian.org:/home/groups/reproducible/htdocs/releases/trydiffoscope
