%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed 1

%define	cname	OpenCity

Summary:	City simulator game
Name:		opencity
Version:	0.0.6.4
Release:	2
License:	GPL
Group:		Games/Strategy
URL:		https://www.opencity.info/
Source0:	http://downloads.sourceforge.net/project/opencity/Stable/0.0.6/%{name}-%{version}stable.tar.bz2
Patch0:		opencity-0.0.6.4-gcc4.7.patch
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	pkgconfig(SDL_net)
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils


%description
OpenCity is a city simulator game project written in standard C++ with OpenGL
and SDL from scratch. It is not intended to be a clone of any famous city
simulator from Max*s. So, if you are looking to download a free SimCity 4 like,
please forget OpenCity. I work on it at my spare time, I really meant it
"my spare time" !

%prep
%setup -q -n %{name}-%{version}stable
%patch0 -p1

%build
%configure2_5x --bindir=%{_gamesbindir}
%make

%install
%makeinstall_std

# prepare icon
mkdir -p %{buildroot}{%{_miconsdir},%{_iconsdir},%{_liconsdir},%{_menudir}}
convert -geometry 16x16 %{name}.png %{buildroot}%{_miconsdir}/%{cname}.png
convert -geometry 32x32 %{name}.png %{buildroot}%{_iconsdir}/%{cname}.png
convert -geometry 48x48 %{name}.png %{buildroot}%{_liconsdir}/%{cname}.png

# copy file from /usr/share to /usr/share/games
mkdir -p %{buildroot}%{_gamesdatadir}/%{name}
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
mv %{buildroot}%{_gamesbindir}/%{name} %{buildroot}%{_gamesbindir}/%{name}-bin
cat > %{buildroot}%{_gamesbindir}/%{name} << EOF
#!/bin/sh
%{_gamesbindir}/%{name}-bin --data-dir %{_gamesdatadir}/%{name} --conf-dir %{_sysconfdir}/%{name}
EOF
chmod +x %{buildroot}%{_gamesbindir}/%{name}

%files
%doc AUTHORS COPYING INSTALL README
%doc docs/FAQ_it.txt docs/INSTALL_it.txt docs/README_it.txt
%doc docs/README_es.txt
%{_gamesbindir}/%{name}
%{_gamesbindir}/%{name}-bin
%{_sysconfdir}/%{name}
%{_gamesdatadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man6/*
%{_miconsdir}/%{cname}.png
%{_iconsdir}/%{cname}.png
%{_liconsdir}/%{cname}.png

