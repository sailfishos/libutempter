%define utempter_compat_ver 0.5.2

Name:       libutempter
Summary:    A privileged helper for utmp/wtmp updates
Version:    1.2.3
Release:    2
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
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains development files required to build
utempter-based software.


%prep
%setup -q -n %{name}-%{version}/%{name}

%build
cd %{name}

cat > %{name}.sysusers.conf <<_EOF
g utmp 22
g utempter 35
_EOF

make CFLAGS="$RPM_OPT_FLAGS" libdir="%{_libdir}" libexecdir="%{_libexecdir}"

%install
cd %{name}
%make_install libdir="%{_libdir}" libexecdir="%{_libexecdir}"
# NOTE: Static lib intentionally disabled.
rm -f %{buildroot}%{_libdir}/*.a

# Remove documentation
rm -Rf %{buildroot}%{_mandir}

install -D -m0644 %{name}.sysusers.conf %{buildroot}%{_sysusersdir}/%{name}.conf

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license %{name}/COPYING 
%{_libdir}/libutempter.so.0
%{_libdir}/libutempter.so.1.*
%dir %attr(755,root,utempter) %{_libexecdir}/utempter
%attr(2711,root,utmp) %{_libexecdir}/utempter/utempter
%{_sysusersdir}/%{name}.conf

%files devel
%doc %{name}/README
%{_includedir}/utempter.h
%{_libdir}/libutempter.so

