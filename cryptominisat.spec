Name:           cryptominisat
Version:        2.9.10
Release:        1%{?dist}
Summary:        SAT solver

# The Mersenne Twister implementation is BSD-licensed.
# All other files are MIT-licensed.
License:        MIT
URL:            http://www.msoos.org/cryptominisat2/
Source0:        https://github.com/msoos/cryptominisat/archive/%{name}-%{version}.zip

BuildRequires:  libtool
BuildRequires:  mariadb-devel
BuildRequires:  perl
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
Requires:       mariadb-devel%{?_isa}
Requires:       zlib-devel%{?_isa}

%description devel
Header files for developing applications that use %{name}.

%package libs
Summary:        Cryptominisat library

%description libs
The %{name} library.

%prep
%setup -q -n %{name}-%{name}-%{version}

# Fix version number
sed -i 's/2\.9\.9/%{version}/' configure.in

# Fix version number and output directory in library documentation
sed -e 's/2\.6\.0/%{version}/' \
    -e 's,/home/soos.*cryptominisat,'$PWD, \
    -i Doxyfile

# Generate the configure script
autoreconf -fi

%build
export CPPFLAGS="-DHAVE_MYSQL -DCMSAT_HAVE_MYSQL"
export LDFLAGS="-L%{_libdir}/mysql"
export LIBS="-lmysqlclient"
%configure --disable-static

# Eliminate hardcoded rpaths
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -i libtool

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# We don't want the libtool files
rm -f %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*

%files devel
%{_includedir}/cmsat/
%{_libdir}/lib%{name}.so

%files libs
%doc AUTHORS NEWS README TODO
%license LICENSE-MIT
%{_libdir}/lib%{name}-%{version}.so

%changelog
* Fri Sep  4 2015 Jerry James <loganjerry@gmail.com> - 2.9.10-1
- New upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.9.9-5
- Rebuilt for GCC 5 C++11 ABI change

* Wed Feb 11 2015 Jerry James <loganjerry@gmail.com> - 2.9.9-4
- Use license macro

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 Jerry James <loganjerry@gmail.com> - 2.9.9-1
- New upstream release

* Mon Sep 23 2013 Jerry James <loganjerry@gmail.com> - 2.9.8-1
- New upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Jerry James <loganjerry@gmail.com> - 2.9.6-1
- New upstream release

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
