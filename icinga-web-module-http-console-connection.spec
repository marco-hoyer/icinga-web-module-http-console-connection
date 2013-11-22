Name:		icinga-web-module-http-console-connection
Version:	0.2
Release:	2%{?dist}
Summary:	HTTP connector for icinga-web

License:	GPL
URL:		https://github.com/marco-hoyer/icinga-web-module-http-console-connection
Source0:	HttpConsoleConnection.class.php
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch
Requires:	icinga-web

%description
The class delivered by this package serves a http connector for icinga-web to communicate with icinga instances using http.
This is intended to work together with livestatus-service, a rest api interface for mk_livestatus.
See https://github.com/ImmobilienScout24/livestatus_service for details.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/icinga-web/app/modules/Api/lib/console/
install -Dp -m0644 %SOURCE0 %{buildroot}/usr/share/icinga-web/app/modules/Api/lib/console/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/usr/share/icinga-web/app/modules/Api/lib/console/*

%post
# register class in icinga-web
echo "Adding HttpConsoleConnection to icinga-web autoload.xml ..."
sed '24i\        <autoload name="HttpConsoleConnection">%core.module_dir%/Api/lib/console/HttpConsoleConnection.class.php</autoload>' /usr/share/icinga-web/app/modules/Api/config/autoload.xml > /usr/share/icinga-web/app/modules/Api/config/autoload_new.xml
mv /usr/share/icinga-web/app/modules/Api/config/autoload.xml /usr/share/icinga-web/app/modules/Api/config/autoload.xml.orig
mv /usr/share/icinga-web/app/modules/Api/config/autoload_new.xml /usr/share/icinga-web/app/modules/Api/config/autoload.xml

# modify xml scheme to verify changes
sed '116i\            <xs:enumeration value="http" />' /usr/share/icinga-web/app/modules/Api/lib/xml/xsd/parts/access.xsd > /usr/share/icinga-web/app/modules/Api/lib/xml/xsd/parts/access_new.xsd
mv /usr/share/icinga-web/app/modules/Api/lib/xml/xsd/parts/access.xsd /usr/share/icinga-web/app/modules/Api/lib/xml/xsd/parts/access.xsd.orig
mv /usr/share/icinga-web/app/modules/Api/lib/xml/xsd/parts/access_new.xsd /usr/share/icinga-web/app/modules/Api/lib/xml/xsd/parts/access.xsd
# clear icinga-web cache
/usr/bin/icinga-web-clearcache

%postun
echo "Removing HttpConsoleConnection to icinga-web autoload.xml ..."
# restore original files
rm /usr/share/icinga-web/app/modules/Api/config/autoload.xml
rm /usr/share/icinga-web/app/modules/Api/lib/xml/xsd/parts/access.xsd
mv /usr/share/icinga-web/app/modules/Api/config/autoload.xml.orig /usr/share/icinga-web/app/modules/Api/config/autoload.xml
mv /usr/share/icinga-web/app/modules/Api/lib/xml/xsd/parts/access.xsd.orig /usr/share/icinga-web/app/modules/Api/lib/xml/xsd/parts/access.xsd
# clear icinga-web cache
/usr/bin/icinga-web-clearcache
