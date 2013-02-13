Name:           cryptominisat
Version:        2.9.5
Release:        2%{?dist}
Summary:        SAT solver

# The Mersenne Twister implementation is BSD-licensed.
# All other files are MIT-licensed.
License:        MIT
URL:            http://www.msoos.org/cryptominisat2/
Source0:        https://gforge.inria.fr/frs/download.php/31107/cmsat-%{version}.tar.gz

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
%setup -q -n cmsat-%{version}

%build
%configure --disable-static
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -i libtool
sed -i 's|^LIBS =.*|LIBS = -lz -lgomp|' cmsat/Makefile
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*

%files devel
%{_includedir}/cmsat/
%{_libdir}/lib%{name}.so

%files libs
%doc AUTHORS LICENSE-MIT NEWS README TODO
%{_libdir}/lib%{name}-%{version}.so

%changelog
* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug  6 2012 Jerry James <loganjerry@gmail.com> - 2.9.5-1
- New upstream release
- Project files now carry the MIT license

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 16 2012 Jerry James <loganjerry@gmail.com> - 2.9.3-1
- New upstream version

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.2-2
- Rebuilt for c++ ABI breakage

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
