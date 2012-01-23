Name:           cryptominisat
Version:        2.9.2
Release:        1%{?dist}
Summary:        SAT solver

# Some source files were borrowed from minisat2, which is MIT-licensed.
# The Mersenne Twister implementation is BSD-licensed.
# Original sources for this project are licensed GPL v3 or later.
License:        GPLv3+
URL:            http://www.msoos.org/cryptominisat2
Source0:        https://gforge.inria.fr/frs/download.php/30138/%{name}-%{version}.tar.gz

BuildRequires:  zlib-devel
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
CryptoMiniSat is a SAT solver that aims to become a premiere SAT solver
with all the features and speed of successful SAT solvers, such as
MiniSat and PrecoSat.  The long-term goals of CryptoMiniSat are to be an
efficient sequential, parallel and distributed solver.  There are
solvers that are good at one or the other, e.g. ManySat (parallel) or
PSolver (distributed), but we wish to excel at all.

CryptoMiniSat 2.5 won the SAT Race 2010 among 20 solvers submitted by
researchers and industry.

%package devel
Summary:        Header files for developing with %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Header files for developing applications that use %{name}.

%package libs
Summary:        Cryptominisat library

%description libs
The %{name} library.

%prep
%setup -q

%build
%configure --disable-static
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -i libtool
sed -i 's|^LIBS =.*|LIBS = -lz -lgomp|' Solver/Makefile
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# %%check
# cd tests
# set +e
# LD_LIBRARY_PATH=../Solver/.libs ../cryptominisat --nosolprint --verbosity=1 AProVE09-12.cnf.gz
# [ $? = 10 ]

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so

%files libs
%doc AUTHORS LICENSE-GPL LICENSE-MIT NEWS README TODO
%{_libdir}/lib%{name}-%{version}.so

%changelog
* Mon Jan 23 2012 Jerry James <loganjerry@gmail.com> - 2.9.2-1
- New upstream version
- Man page is now upstream
- All patches have been applied upstream
- Tests have been removed from the source distribution

* Mon Jan  9 2012 Jerry James <loganjerry@gmail.com> - 2.9.1-3
- Rebuild for GCC 4.7

* Mon Dec 19 2011 Dan Horák <dan[at]danny.cz> - 2.9.1-2
- FPU handling is x86 specific
- set library path so the test is run

* Wed Dec  7 2011 Jerry James <loganjerry@gmail.com> - 2.9.1-1
- Initial RPM
