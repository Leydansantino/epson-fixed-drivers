# epson-fixed-drivers
Fixed PPD drivers for L110-L210-L300-L350-L355-L550-L555 series. Optimized for Fedora, Bazzite, and Atomic Linux systems.

Download the original drivers the source code:
L110/L210/L300/L350/L355/L550/L555

https://download-center.epson.com/search/

Select the indicated options

This will take you to the downloads page:

Source Code
Epson Inkjet Printer Driver (ESC/P) for Linux	1.0.1	2025-09-30	2.16 MB
CLICK IN --» PROCEED TO DOWNLOAD

You should receive the source code with this filename:
`epson-inkjet-printer-201207w-1.0.1-1.src.rpm`

###PREPARATION: Extract Source and Install Tools1. **Install rpmdev tools:**

```sudo dnf install rpmdevtools```




2. **Prepare the RPM build environment:** (This creates `~/rpmbuild/SPECS`, `~/rpmbuild/SOURCES`, etc.)
   
```rpmdev-setuptree```




4. **Extract the contents of the `.src.rpm`:** (Assuming the `.src.rpm` is in `~/Downloads`)

```cd ~/Downloads```
```rpm -i epson-inkjet-printer-201207w-1.0.1-1.src.rpm```




*This extracts the `.spec` file to `~/rpmbuild/SPECS/` and the original source tarball (`.tar.gz`) to `~/rpmbuild/SOURCES/`.*

###STEP 1: Modify the SPEC File1. **Open the spec file for editing:**

```nano ~/rpmbuild/SPECS/epson-inkjet-printer-201207w.spec```




2. Delete all code and **paste the modified code** (which includes the necessary dependency fixes).
3. Save and exit: `CTRL+O`, `ENTER`, `CTRL+X`

###STEP 2: Install Build DependenciesYou need development tools and libraries for the binary to compile correctly:


```sudo dnf install @development-tools cups-devel ghostscript libtool libjpeg-devel libtiff-devel```



###STEP 3: Build the Final RPM PackageExecute the compilation command:


```rpmbuild -ba ~/rpmbuild/SPECS/epson-inkjet-printer-201207w.spec```



Locate the Final RPM:
The finished installation package (`.rpm`) will be placed in the RPMS subdirectory for your architecture:
`~/rpmbuild/RPMS/x86_64/epson-inkjet-printer-201207w-1.0.1-1.rpm`

###STEP 4: Install the Driver and Restart CUPSInstall the final driver package:


```sudo dnf install ~/rpmbuild/RPMS/x86_64/epson-inkjet-printer-201207w-1.0.1-1.rpm```



Restart the CUPS Service:


```sudo systemctl restart cups```



###STEP 5: Test the PrinterConnect the printer using the **USB cable** and wait for it to configure automatically. Press the "Print Test Page" button to verify that everything was successful.

Enjoy!
