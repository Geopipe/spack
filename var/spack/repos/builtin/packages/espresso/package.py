import llnl.util.tty as tty

from spack import *


class Espresso(Package):
    """
    QE is an integrated suite of Open-Source computer codes for electronic-structure calculations and materials
    modeling at the nanoscale. It is based on density-functional theory, plane waves, and pseudopotentials.
    """
    homepage = 'http://quantum-espresso.org'
    url = 'http://www.qe-forge.org/gf/download/frsrelease/204/912/espresso-5.3.0.tar.gz'

    version('5.3.0', '6848fcfaeb118587d6be36bd10b7f2c3')

    variant('mpi', default=True, description='Build Quantum-ESPRESSO with mpi support')
    variant('openmp', default=False, description='Enables openMP support')
    variant('scalapack', default=False, description='Enables scalapack support')
    variant('elpa', default=True, description='Use elpa as an eigenvalue solver')

    depends_on('blas')
    depends_on('lapack')

    depends_on('mpi', when='+mpi')
    depends_on('elpa', when='+elpa')
    depends_on('scalapack', when='+scalapack')

    def check_variants(self, spec):
        error = 'you cannot ask for \'+{variant}\' when \'+mpi\' is not active'
        if '+scalapack' in spec and '~mpi' in spec:
            raise RuntimeError(error.format(variant='scalapack'))
        if '+elpa' in spec and '~mpi' in spec:
            raise RuntimeError(error.format(variant='elpa'))

    def install(self, spec, prefix):
        self.check_variants(spec)

        options = ['-prefix=%s' % prefix]

        if '+mpi' in spec:
            options.append('--enable-parallel')

        if '+openmp' in spec:
            options.append('--enable-openmp')

        if '+scalapack' in spec:
            options.append('--with-scalapack=yes')

        if '+elpa' in spec:
            options.append('--with-elpa=%s' % spec['elpa'].prefix)

        configure(*options)
        make('all')
        make('install')
