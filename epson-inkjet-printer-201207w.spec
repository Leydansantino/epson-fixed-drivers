# Copyright (C) Seiko Epson Corporation 2012.

# --- Añadir definición para compatibilidad con CUPS en F43 ---
%define _cupsserverbin /usr/lib/cups
# --- Fin de la definición ---

%define pkgtarname epson-inkjet-printer-201207w
%define drivername epson-driver
%define filtername epson-inkjet-printer-filter
%define supplier %{pkgtarname}
%define filterver 1.0.2

%define driverstr epson-inkjet-printer
%define extraversion -1
%define supplierstr Seiko Epson Corporation
%define debug_package %{nil}
%define __debug_install_post %{nil}

AutoReqProv: no

Name: %{pkgtarname}
Summary: Epson Inkjet Printer Driver (ESC/P-R) for L110/L210/L300/L350/L355/L550/L555 models
Version: 1.0.1
Release: 1
Source0: %{filtername}-%{filterver}.tar.gz
Source1: %{pkgtarname}-%{version}.tar.gz
License: LGPL and SEIKO EPSON CORPORATION SOFTWARE LICENSE AGREEMENT
Vendor: Seiko Epson Corporation
URL: http://download.ebz.epson.net/dsc/search/01/search/?OSC=LX

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
This rpm package contains Epson Inkjet Printer Driver (ESC/P-R) for
Linux. It supports the following printers:
    EPSON L110/L210/L300/L350/L355/L550/L555

%prep
%setup -c -n %{pkgtarname}-%{version}-build -a 0 -a 1

%build
# Estas correcciones ya estaban en el SPEC original, son importantes.
export CFLAGS="%{optflags} -fcommon -fno-PIE -fno-PIC -no-pie"
export CXXFLAGS="%{optflags} -fcommon -fno-PIE -fno-PIC -no-pie"
export LDFLAGS="-Wl,-z,relro,-z,now -no-pie"

cd epson-inkjet-printer-filter-1.0.2

%configure
make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_cupsserverbin}/filter
install -d %{buildroot}%{_docdir}
# Instalar el filtro (Source0)
cd epson-inkjet-printer-filter-1.0.2
install src/epson_inkjet_printer_filter %{buildroot}%{_cupsserverbin}/filter
for file in AUTHORS COPYING COPYING.LIB COPYING.EPSON; do
    install -m 644 $file %{buildroot}%{_docdir}
done

# Regresar a la base y entrar a Source1 para documentos/librerías
cd ..
cd epson-inkjet-printer-201207w-1.0.1
install -m 644 Manual.txt README %{buildroot}%{_docdir}

# Bloque case eliminado: no es necesario, el siguiente bloque usa %_libdir
# case `uname -m` in
#     i?86) X86LIB="" ;;
#     *)      X86LIB=64 ;;
# esac

install -d %{buildroot}%{_datadir}/ppds
install -m 644 -t %{buildroot}%{_datadir}/ppds ppds/*

install -d %{buildroot}/usr/resource
install -m 644 -t %{buildroot}/usr/resource resource/*

install -d %{buildroot}/usr/watermark
install -m 644 -t %{buildroot}/usr/watermark watermark/*

# Usar %_libdir para compatibilidad x86_64/i686
install -d %{buildroot}%{_libdir}
for file in lib64/libEpson*.so*; do
    if [ -f "$file" ]; then
        install -m 644 "$file" %{buildroot}%{_libdir}/
    fi
done

# Eliminar macro obsoleta
# %create_opt_dirs 

%post
/sbin/ldconfig
# Eliminar macros obsoletas de CUPS

%postun
/sbin/ldconfig
# Eliminar macros obsoletas de CUPS

# Si el paquete se elimina (no se actualiza), reiniciar CUPS (o al menos intentarlo)
if [ $1 -eq 0 ]; then
    /usr/bin/systemctl restart cups.service 2>/dev/null || true
fi
# %end_not_on_rpm_update

%clean
cd %{filtername}-%{filterver}
make clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_cupsserverbin}/filter/epson_inkjet_printer_filter
%{_libdir}/libEpson*.so*
%{_datadir}/ppds/*
/usr/resource/*
/usr/watermark/*

%{_docdir}/AUTHORS
%{_docdir}/COPYING
%{_docdir}/COPYING.LIB
%{_docdir}/COPYING.EPSON
%{_docdir}/Manual.txt
%{_docdir}/README
