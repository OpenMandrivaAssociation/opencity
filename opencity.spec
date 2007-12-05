%define	name		opencity
%define cname		OpenCity
%define version		0.0.5
%define release		%mkrel 2

Summary: 		OpenCity is a city simulator game
Name: 			%{name}
Version: 		%{version}		
Release: 		%{release}
License: 		GPL
Group: 			Games/Strategy
URL: 			http://www.opencity.info/
Source0: 		%{name}-%{version}stable.tar.bz2
BuildRoot: 		%{_tmppath}/%{name}-%{version}-%{release}-root
Buildrequires:		libSDL_net-devel
Buildrequires:		libSDL_mixer-devel
Buildrequires:		libSDL_image-devel
Buildrequires:		libmesagl-devel
Buildrequires:		libmesaglu-devel
Buildrequires:		ImageMagick
Buildrequires:		libpng-devel
Requires(post): 	desktop-file-utils
Requires(postun): 	desktop-file-utils


%description
OpenCity is a city simulator game project written in standard C++ with OpenGL
and SDL from scratch. It is not intended to be a clone of any famous city 
simulator from Max*s. So, if you are looking to download a free SimCity 4 like, 
please forget OpenCity. I work on it at my spare time, I really meant it 
"my spare time" !

%prep
%setup -q -n %{name}-%{version}stable

%build
%configure2_5x  --bindir=%{_gamesbindir} --sysconfdir=%{_gamesdatadir}
%make


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

#prepare icon
mkdir -p $RPM_BUILD_ROOT{%{_miconsdir},%{_iconsdir},%{_liconsdir},%{_menudir}}
convert -geometry 16x16 %{name}.png $RPM_BUILD_ROOT%{_miconsdir}/%{cname}.png
convert -geometry 32x32 %{name}.png $RPM_BUILD_ROOT%{_iconsdir}/%{cname}.png
convert -geometry 48x48 %{name}.png $RPM_BUILD_ROOT%{_liconsdir}/%{cname}.png


# copy file from /usr/share to /usr/share/games
mv  %{buildroot}%{_datadir}/%{name}/*  %{buildroot}%{_gamesdatadir}/%{name}/

# fix the .desktop
# an Icon name don't have an extension, so we remove it
perl -i -pe 's/opencity.png/opencity/' %{name}.desktop

desktop-file-install --add-category="X-MandrivaLinux-MoreApplications-Games-Strategy" \
		--dir %{buildroot}%{_datadir}/applications %{name}.desktop


#===============================================================================
# add a little script that launch opencity with datat path
# 1) rename binary : opencity -> opencity-bin
# 2) add script
#===============================================================================
mv $RPM_BUILD_ROOT%{_gamesbindir}/%{name} $RPM_BUILD_ROOT%{_gamesbindir}/%{name}-bin
cat > $RPM_BUILD_ROOT%{_gamesbindir}/%{name} << EOF
#!/bin/sh
%{_gamesbindir}/%{name}-bin --datadir %{_gamesdatadir}/%{name} --confdir %{_gamesdatadir}/%{name}
EOF
chmod +x $RPM_BUILD_ROOT%{_gamesbindir}/%{name}


%post
%{update_desktop_database}
%{update_menus}

%postun
%{clean_desktop_database}
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL README
%{_gamesbindir}/%{name}
%{_gamesbindir}/%{name}-bin
%{_gamesdatadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man6/*
%{_miconsdir}/%{cname}.png
%{_iconsdir}/%{cname}.png
%{_liconsdir}/%{cname}.png

