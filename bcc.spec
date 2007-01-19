Summary:	Bruce's C compiler
Summary(pl):	Kompilator C Bruce'a
Name:		bcc
Version:	0.16.17
Release:	2
License:	GPL
Group:		Development/Languages
#Source0Download: http://www.cix.co.uk/~mayday/
Source0:	http://www.cix.co.uk/~mayday/dev86/Dev86src-%{version}.tar.gz
# Source0-md5:	e7bbfdbe61c2fb964994a087e29b0087
Patch0:		Dev86src-noroot.patch
Patch1:		Dev86src-opt.patch
URL:		http://www.cix.co.uk/~mayday/
Requires:	bin86
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# don't try to strip Linux-8086 objects
%define		no_install_post_strip	1

%description
Bcc is a simple C compiler that produces 8086 assembler, in addition
compiler compile time options allow 80386 or 6809 versions. The
compiler understands traditional K&R C with just the restriction that
bit fields are mapped to one of the other integer types.

%description -l pl
Bcc jest prostym kompilatorem C tworz±cym pliki asemblerowe 8086,
a dodatkowo pozwala na wybranie wersji 80386 lub 6809. Kompilator
rozumie tradycyjne C K&R z takim ograniczeniem, ¿e pola bitowe
s± odwzorowywane do jednego z innych typów ca³kowitych.

%prep
%setup -q -n dev86-%{version}
%patch0 -p1
%patch1 -p1

%build
CC="%{__cc}" \
%{__make} all other \
	OPT="%{rpmcflags}" <<!FooBar!
5
quit
!FooBar!

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-all \
	DIST=$RPM_BUILD_ROOT

# FFU (dis88/Makefile is not ready)
#	MANDIR=%{_mandir}

cp -R libc/kinclude $RPM_BUILD_ROOT%{_libdir}/bcc

ln -sf objdump86 $RPM_BUILD_ROOT%{_bindir}/nm86
ln -sf objdump86 $RPM_BUILD_ROOT%{_bindir}/size86

# these are separated in bin86 package
rm -f $RPM_BUILD_ROOT%{_bindir}/{as86,ld86}
rm -f $RPM_BUILD_ROOT/usr/man/man1/{as,ld}86.1*
# move man pages where they belong
install -d $RPM_BUILD_ROOT%{_mandir}
mv -f $RPM_BUILD_ROOT/usr/man/* $RPM_BUILD_ROOT%{_mandir}

%{!?debug:strip -R .comment -R .note $RPM_BUILD_ROOT%{_bindir}/{ar86,bcc,elksemu,objdump86}}
%{!?debug:strip -R .comment -R .note $RPM_BUILD_ROOT%{_libdir}/bcc/{bcc*,copt,unproto}}

mv -f bootblocks/README README.bootblocks
mv -f copt/README README.copt
mv -f dis88/README README.dis88
mv -f elksemu/README README.elksemu
mv -f unproto/README README.unproto

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes Contributors README*
%attr(755,root,root) %{_bindir}/ar86
%attr(755,root,root) %{_bindir}/bcc
%attr(755,root,root) %{_bindir}/dis86
%attr(755,root,root) %{_bindir}/elksemu
%attr(755,root,root) %{_bindir}/makeboot
%attr(755,root,root) %{_bindir}/nm86
%attr(755,root,root) %{_bindir}/objdump86
%attr(755,root,root) %{_bindir}/size86
%dir %{_libdir}/bcc
%attr(755,root,root) %{_libdir}/bcc/as86_encap
%attr(755,root,root) %{_libdir}/bcc/bcc-cc1
%attr(755,root,root) %{_libdir}/bcc/bcc-cpp
%attr(755,root,root) %{_libdir}/bcc/copt
%attr(755,root,root) %{_libdir}/bcc/unproto
%{_libdir}/bcc/i386
%{_libdir}/bcc/include
%{_libdir}/bcc/kinclude
%{_libdir}/bcc/crt*.o
%{_libdir}/bcc/lib*.a
%{_libdir}/bcc/rules.*
%{_mandir}/man1/*
