Name: server-web-app
Version: %{version}
Release: %{release}
Summary: %{name} rpm
Source0: %{name}-%{version}.tar.gz
Source1: %{name}-initd
Source2: logrotate
Group: Applications/Internet
License: Various
Vendor: blinkbox books
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires: nodejs >= 0.10.21

%description
Server Web App based on express and NodeJS

%prep

%setup -q

%build

%install

%{__mkdir} -p %{buildroot}%{_sysconfdir}/init.d
%{__install} -p %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/%{name}

%{__install} -d %{buildroot}%{_localstatedir}/www/server
%{__install} {app.js,package.json,newrelic.js} %{buildroot}%{_localstatedir}/www/server
%{__cp} -r {app,node_modules} %{buildroot}%{_localstatedir}/www/server

%{__mkdir} -p %{buildroot}%{_localstatedir}/log/%{name}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -p %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr( 0644, bbb_nodejs, bbb_nodejs, 0755 )
%attr(0755,root,root) %{_sysconfdir}/init.d/%{name}
%config(noreplace) %{_localstatedir}/www/server/app/config/config.json
%{_localstatedir}/www/server/*
%{_localstatedir}/log/%{name}
%attr(0644,root,root) %{_sysconfdir}/logrotate.d/%{name}

%pre
# Create the nodejs user and group (bbb UID/GID) but do not use useradd for nodejs
/usr/bin/getent group bbb_nodejs >/dev/null || /usr/sbin/groupadd -g 2003 bbb_nodejs
/usr/bin/getent passwd bbb_nodejs >/dev/null || /usr/sbin/useradd  -M -c "NodeJS on $(hostname -s)" -d /var/www/server -g bbb_nodejs -u 2003 -s /bin/nologin bbb_nodejs
exit 0

%post
if [ $1 -gt 1 ] ; then
/etc/init.d/server-web-app stop
/etc/init.d/server-web-app start
fi
if [ $1 -eq 1 ] ; then
chkconfig --level 2345 server-web-app on
/etc/init.d/server-web-app start
fi
exit 0

%postun
if [ $1 -eq 0 ] ; then
chkconfig --del server-web-app
fi
exit 0




%changelog
* Thu Aug 07 2014 Timothy Clarke <timothyc@blinkbox.com>
- Updated post commands to restart service on upgrade and ensure service in on boot.
* Wed Jul 30 2014 Timothy Clarke <timothyc@blinkbox.com>
- Tweaked spec so server/app/config/config.json is a config/noreplace file
