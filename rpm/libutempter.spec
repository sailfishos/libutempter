%define utempter_compat_ver 0.5.2

Name:       libutempter
Summary:    A privileged helper for utmp/wtmp updates
Version:    1.1.5
Release:    2
Group:      System/Libraries
License:    LGPLv2+
URL:        https://github.com/sailfishos/libutempter
Source0:    %{name}-%{version}.tar.bz2
Requires(pre): shadow-utils
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides:   utempter = %{utempter_compat_ver}
Obsoletes:   utempter

%description
This library provides interface for terminal emulators such as
screen and xterm to record user sessions to utmp and wtmp files.


%package devel
Summary:    Development environment for utempter
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains development files required to build
utempter-based software.


%prep
%setup -q -n %{name}-%{version}/%{name}

%build
cd %{name}
make CFLAGS="$RPM_OPT_FLAGS" libdir="%{_libdir}" libexecdir="%{_libexecdir}"

%install
cd %{name}
rm -rf %{buildroot}
make install DESTDIR="$RPM_BUILD_ROOT" libdir="%{_libdir}" libexecdir="%{_libexecdir}"
# NOTE: Static lib intentionally disabled.
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%pre
{
%{_sbindir}/groupadd -g 22 -r -f utmp || :
%{_sbindir}/groupadd -g 35 -r -f utempter || :
}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license %{name}/COPYING 
%{_libdir}/libutempter.so.0
%{_libdir}/libutempter.so.1.1.5
%dir %attr(755,root,utempter) %{_libexecdir}/utempter
%attr(2711,root,utmp) %{_libexecdir}/utempter/utempter

%files devel
%defattr(-,root,root,-)
%doc %{name}/README
%{_includedir}/utempter.h
%{_libdir}/libutempter.so

