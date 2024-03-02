#
# Conditional build:
%bcond_with	tests		# build with tests
#
# TODO:
# - runtime Requires if any

%define		kdeframever	6.0
%define		qtver		5.15.2
%define		kfname		ksvg
Summary:	svg library
Name:		kf6-%{kfname}
Version:	6.0.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	9ffd741e4f57e6a619e113098cddcd87
URL:		http://www.kde.org/
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	Qt6Svg-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	catdoc
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf6-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SVG library.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

#%find_lang libkirigami6 --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKF6Svg.so.*.*
%ghost %{_libdir}/libKF6Svg.so.6
%dir %{_libdir}/qt6/qml/org/kde/ksvg
%{_libdir}/qt6/qml/org/kde/ksvg/corebindingsplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/ksvg/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/ksvg/libcorebindingsplugin.so
%{_libdir}/qt6/qml/org/kde/ksvg/qmldir
%{_datadir}/qlogging-categories6/ksvg.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KSvg
%{_libdir}/cmake/KF6Svg
%{_libdir}/libKF6Svg.so
