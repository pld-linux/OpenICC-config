#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	OpenICC configuration database
Summary(pl.UTF-8):	Baza danych konfiguracji OpenICC
Name:		OpenICC-config
Version:	0.1.0
Release:	1
License:	MIT
Group:		Applications/Graphics
#Source0Download: https://github.com/OpenICC/config/releases
Source0:	https://github.com/OpenICC/config/archive/%{version}/config-%{version}.tar.gz
# Source0-md5:	be0a04225e60be7f1e8f0c6e8a83f26f
URL:		https://github.com/OpenICC/config
BuildRequires:	cmake >= 2.6.2
%{?with_apidocs:BuildRequires:	doxygen >= 1.5.8}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	yajl-devel
Requires:	OpenICC-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OpenICC configuration data base allows to store, share and
manipulate colour management informations.

%description -l pl.UTF-8
Baza danych konfiguracji OpenICC pozwala na przechowywanie,
współdzielenie i operowanie informacjami dotyczącymi zarządzania
kolorami.

%package -n OpenICC-libs
Summary:	OpenICC configuration database library
Summary(pl.UTF-8):	Biblioteka bazy danych konfiguracji OpenICC
Group:		Libraries

%description -n OpenICC-libs
OpenICC configuration database library.

%description -n OpenICC-libs -l pl.UTF-8
Biblioteka bazy danych konfiguracji OpenICC.

%package -n OpenICC-devel
Summary:	Header files for OpenICC library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenICC
Group:		Development/Libraries
Requires:	OpenICC-libs = %{version}-%{release}
Requires:	yajl-devel

%description -n OpenICC-devel
Header files for OpenICC library.

%description -n OpenICC-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenICC.

%package -n OpenICC-static
Summary:	Static OpenICC library
Summary(pl.UTF-8):	Statyczna biblioteka OpenICC
Group:		Development/Libraries
Requires:	OpenICC-devel = %{version}-%{release}

%description -n OpenICC-static
Static OpenICC library.

%description -n OpenICC-static -l pl.UTF-8
Statyczna biblioteka OpenICC.

%package -n OpenICC-apidocs
Summary:	API documentation for OpenICC library
Summary(pl.UTF-8):	Dokumentacja API biblioteki OpenICC
Group:		Documentation
BuildArch:	noarch

%description -n OpenICC-apidocs
API documentation for OpenICC library.

%description -n OpenICC-apidocs -l pl.UTF-8
Dokumentacja API biblioteki OpenICC.

%prep
%setup -q -n config-%{version}

%build
install -d build
cd build
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/openicc

%find_lang OpenICC

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n OpenICC-libs -p /sbin/ldconfig
%postun	-n OpenICC-libs -p /sbin/ldconfig

%files -f OpenICC.lang
%defattr(644,root,root,755)
%doc README.md docs/{AUTHORS.md,COPYING.md,ChangeLog.md}
%attr(755,root,root) %{_bindir}/openicc-device

%files -n OpenICC-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOpenICC.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenICC.so.0

%files -n OpenICC-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOpenICC.so
%{_includedir}/openicc
%{_pkgconfigdir}/openicc.pc
%{_libdir}/cmake/openicc

%files -n OpenICC-static
%defattr(644,root,root,755)
%{_libdir}/libopenicc-static.a

%if %{with apidocs}
%files -n OpenICC-apidocs
%defattr(644,root,root,755)
%doc build/docs/html/*.{css,html,js,png}
%endif
