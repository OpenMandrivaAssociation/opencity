%define	name		opencity
%define cname		OpenCity
%define version		0.0.4
%define release		%mkrel 1

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

%description
OpenCity is a city simulator game project written in standard C++ with OpenGL
and SDL from scratch. It is not intended to be a clone of any famous city 
simulator from Max*s. So, if you are looking to download a free SimCity 4 like, 
please forget OpenCity. I work on it at my spare time, I really meant it 
"my spare time" !

%prep
%setup -q -n %{name}-%{version}stable

%build
%configure2_5x  --bindir=%{_gamesbindir}
%make


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

#move data to %%{_gamesdatadir}
mkdir -p $RPM_BUILD_ROOT%{_gamesdatadir}
mv $RPM_BUILD_ROOT%{_datadir}/%{name} $RPM_BUILD_ROOT%{_gamesdatadir}/

#prepare icon
mkdir -p $RPM_BUILD_ROOT{%{_miconsdir},%{_iconsdir},%{_liconsdir},%{_menudir}}
convert -geometry 16x16 %{cname}.png $RPM_BUILD_ROOT%{_miconsdir}/%{cname}.png
convert -geometry 32x32 %{cname}.png $RPM_BUILD_ROOT%{_iconsdir}/%{cname}.png
convert -geometry 48x48 %{cname}.png $RPM_BUILD_ROOT%{_liconsdir}/%{cname}.png

# prepare menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat > $RPM_BUILD_ROOT%{_menudir}/%{name} << EOF
?package(%name): needs="x11" \
        section="More Applications/Games/Strategy" \
        title="%{cname}" \
        longtitle="%{cname}" \
        command="%{_gamesbindir}/%{name}" \
        icon="%{cname}.png" \
	xdg="true"
EOF

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{cname}.desktop << EOF
[Desktop Entry]
Name=%{cname}
Comment=%{Summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{cname}
Terminal=false
Type=Application
Categories=Game;StrategyGame;X-MandrivaLinux-MoreApplications-Games-Strategy;
EOF

#===============================================================================
# add a little script that launch opencity with datat path
# 1) rename binary : opencity -> opencity-bin
# 2) add script
#===============================================================================
mv $RPM_BUILD_ROOT%{_gamesbindir}/%{name} $RPM_BUILD_ROOT%{_gamesbindir}/%{name}-bin
cat > $RPM_BUILD_ROOT%{_gamesbindir}/%{name} << EOF
#!/bin/sh
%{_gamesbindir}/%{name}-bin --homedir %{_gamesdatadir}/%{name}
EOF
chmod +x $RPM_BUILD_ROOT%{_gamesbindir}/%{name}


%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL README
%{_gamesbindir}/%{name}
%{_gamesbindir}/%{name}-bin
%{_menudir}/%{name}
%{_gamesdatadir}/%{name}
%{_datadir}/applications/OpenCity.desktop
%{_miconsdir}/%{cname}.png
%{_iconsdir}/%{cname}.png
%{_liconsdir}/%{cname}.png


