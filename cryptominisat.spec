Name:           cryptominisat
Version:        5.0.1
Release:        1%{?dist}
Summary:        SAT solver

# Most of the code is MIT, but a few files are LGPLv2, which subsumes MIT
License:        LGPLv2
URL:            http://www.msoos.org/
Source0:        https://github.com/msoos/%{name}/archive/%{version}.tar.gz
# Text is from the sources, therefore under the same copyright and license as
# the code.  Man page formatting contributed by Jerry James.
Source1:        cryptominisat5.1

BuildRequires:  boost-devel
BuildRequires:  chrpath
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gperftools-devel
BuildRequires:  m4ri-devel
BuildRequires:  python2-devel
BuildRequires:  swig
BuildRequires:  tbb-devel
BuildRequires:  vim-common
BuildRequires:  zlib-devel

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
CryptoMiniSat is a modern, multi-threaded, feature-rich, simplifying SAT
solver. Highlights:
- Instance simplification at every point of the search (inprocessing)
- Over 100 configurable parameters to tune to specific needs
- Collection of statistical data to MySQL database + javascript-based
  visualization of it
- Clean C++ and python interfaces

%package devel
Summary:        Header files for developing with %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       m4ri-devel%{?_isa}
Requires:       tbb-devel%{?_isa}

%description devel
Header files for developing applications that use %{name}.

%package libs
Summary:        Cryptominisat library

%description libs
The %{name} library.

%package -n python2-%{name}
Summary:        Python 2 interface to %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%{?python_provide:%python_provide python-%{name}}

%description -n python2-%{name}
Python 2 interface to %{name}.

%prep
%setup -q

# Don't override our compiler flags
sed -i 's/-O3 -mtune=native/-DNDEBUG/' CMakeLists.txt
if [ "%{_libdir}" = "%{_prefix}/lib64" ]; then
  sed -i 's,${dir}/lib,&64,g' cmake/FindPkgMacros.cmake
fi

# Fix the python install
sed -ri 's|install |&--root %{buildroot} |' python/CMakeLists.txt

%build
%cmake
%make_build

%install
%make_install

# Install the man page
mkdir -p %{buildroot}%{_mandir}/man1
sed 's/@VERSION@/%{version}/' %{SOURCE1} > \
    %{buildroot}%{_mandir}/man1/cryptominisat5.1
touch -r %{SOURCE1} %{buildroot}%{_mandir}/man1/cryptominisat5.1

# Move library files to where they should go
if [ "%{_libdir}" = "%{_prefix}/lib64" ]; then
  mkdir -p %{buildroot}%{_libdir}
  mv %{buildroot}%{_prefix}/lib/lib%{name}* %{buildroot}%{_libdir}
  mv %{buildroot}%{_prefix}/lib/cmake %{buildroot}%{_libdir}
  sed -i 's|%{_prefix}/lib/|%{_libdir}/|' \
      %{buildroot}%{_libdir}/cmake/cryptominisat5/*.cmake
fi

# Remove buildroot paths from cmake files
sed -i 's|%{buildroot}||' %{buildroot}%{_libdir}/cmake/cryptominisat5/*.cmake

# Remove rpaths
chrpath -d %{buildroot}%{_bindir}/cryptominisat5
chrpath -d %{buildroot}%{_bindir}/cryptominisat5_simple

# Fix permissions
chmod 0755 %{buildroot}%{python2_sitearch}/pycryptosat.so

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc README.markdown
%{_bindir}/cryptominisat5
%{_bindir}/cryptominisat5_simple
%{_mandir}/man1/cryptominisat5*

%files devel
%{_includedir}/cryptominisat5/
%{_libdir}/libcryptominisat5.so
%{_libdir}/cmake/

%files libs
%doc AUTHORS
%license LICENSE-SCALMC
%{_libdir}/libcryptominisat5.so.*

%files -n python2-%{name}
%doc python/README.rst
%license python/LICENSE
%{python2_sitearch}/pycryptosat*

%changelog
* Sat Nov 25 2017 Jerry James <loganjerry@gmail.com> - 5.0.1-1
- Update to major version 5

* Sat Sep 23 2017 Jerry James <loganjerry@gmail.com> - 2.9.11-6
- Update the mariadb BR (bz 1493618)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Mar 19 2016 Jerry James <loganjerry@gmail.com> - 2.9.11-1
- New upstream release

* Sat Mar  5 2016 Jerry James <loganjerry@gmail.com> - 2.9.10-3
- post/postun scripts are for libs, not the main package

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

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
