#  Copyright (c) 2008 Red Hat, Inc.

#  There is no URL or upstream source entry as this package constitutes
#  upstream for itself.

Summary: Infiniband/iWARP Kernel Module Initializer
Name: rdma
Version: 4.1
Release: 1%{?dist}
License: GPLv2+
Group: System Environment/Base
Source0: rdma.conf
Source1: rdma.sriov-vfs
Source2: rdma.mlx4.conf
Source3: rdma.udev-ipoib-naming.rules
Source4: rdma.mlx4.user.modprobe
Source5: rdma.ifup-ib
Source6: rdma.ifdown-ib
Source7: rdma.service
Source8: rdma.modules-setup.sh
Source9: rdma.udev-rules
Source10: rdma.mlx4.sys.modprobe
Source11: rdma.cxgb3.sys.modprobe
Source12: rdma.cxgb4.sys.modprobe
Source13: rdma.kernel-init
Source14: rdma.sriov-init
Source15: rdma.fixup-mtrr.awk
Source16: rdma.mlx4-setup.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: systemd-units
Requires: udev >= 095, systemd-units, dracut
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Conflicts: initscripts <= 9.49.16-1, libmlx4 <= 1.0.6-2, libcxgb3 <= 1.3.1-6, libcxgb4 <= 1.3.5-1
%global dracutlibdir %{_prefix}/lib/dracut
%global sysmodprobedir %{_prefix}/lib/modprobe.d

%description 
User space initialization scripts for the kernel InfiniBand/iWARP drivers

%prep

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/modprobe.d
install -d %{buildroot}%{_sysconfdir}/udev/rules.d
install -d %{buildroot}%{_sysconfdir}/sysconfig/network-scripts
install -d %{buildroot}%{_libexecdir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_udevrulesdir}
install -d %{buildroot}%{dracutlibdir}/modules.d/05rdma
install -d %{buildroot}%{sysmodprobedir}

# Stuff to go into the base package
install -m 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/sriov-vfs
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/mlx4.conf
install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/udev/rules.d/70-persistent-ipoib.rules
install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/modprobe.d/mlx4.conf
install -m 0755 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-ib
install -m 0755 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifdown-ib
install -m 0644 %{SOURCE7} %{buildroot}%{_unitdir}/rdma.service
install -m 0755 %{SOURCE8} %{buildroot}%{dracutlibdir}/modules.d/05rdma/module-setup.sh
install -m 0644 %{SOURCE9} %{buildroot}%{_udevrulesdir}/98-rdma.rules
install -m 0644 %{SOURCE10} %{buildroot}%{sysmodprobedir}/libmlx4.conf
install -m 0644 %{SOURCE11} %{buildroot}%{sysmodprobedir}/cxgb3.conf
install -m 0644 %{SOURCE12} %{buildroot}%{sysmodprobedir}/cxgb4.conf
install -m 0755 %{SOURCE13} %{buildroot}%{_libexecdir}/rdma-init-kernel
install -m 0755 %{SOURCE14} %{buildroot}%{_libexecdir}/rdma-set-sriov-vf
install -m 0644 %{SOURCE15} %{buildroot}%{_libexecdir}/rdma-fixup-mtrr.awk
install -m 0755 %{SOURCE16} %{buildroot}%{_libexecdir}/mlx4-setup.sh

%clean
rm -rf %{buildroot}

%post
%systemd_post rdma.service

%preun
%systemd_preun rdma.service

%postun
%systemd_postun

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/udev/rules.d/*
%config(noreplace) %{_sysconfdir}/modprobe.d/mlx4.conf
%{_sysconfdir}/sysconfig/network-scripts/*
%{_unitdir}/%{name}.service
%dir %{dracutlibdir}/modules.d/05rdma
%{dracutlibdir}/modules.d/05rdma/module-setup.sh
%{_udevrulesdir}/*
%{sysmodprobedir}/libmlx4.conf
%{sysmodprobedir}/cxgb3.conf
%{sysmodprobedir}/cxgb4.conf
%{_libexecdir}/rdma-init-kernel
%{_libexecdir}/rdma-set-sriov-vf
%{_libexecdir}/rdma-fixup-mtrr.awk
%{_libexecdir}/mlx4-setup.sh

%changelog
* Wed Jun 24 2015 Honggang Li <honli@redhat.com> - 7.2_4.1_rc6-1
- Update version to match kernel submission
- Fix two documentation issues
- Related: bz1227995

* Mon Jun 22 2015 Michal Schmidt <mschmidt@redhat.com> - 7.2_3.17-2
- udev rules: Defer setting of node description to rdma-ndd if it is
  installed.
- Related: bz1169968

* Fri Jun 05 2015 Doug Ledford <dledford@redhat.com> - 7.2_3.17-1
- Rebuilding for 7.2
- Resolves: bz1227995

* Mon Feb 02 2015 Doug Ledford <dledford@redhat.com> - 7.1_3.17-6
- The system libmlx4.conf file had the name of the config script
  backwards and on systems with ethernet devices in ib/eth mode,
  the eth port was not getting set properly
- Related: bz1164618

* Thu Jan 08 2015 Doug Ledford <dledford@redhat.com> - 7.1_3.17-5
- Bump and rebuild to eliminate an rpm version compare issue on alternate
  arches that don't use the .el7 dist tag
- Related: bz1164618

* Tue Dec 23 2014 Doug Ledford <dledford@redhat.com> - 7.1_3.17-4
- Move init of all RDMA related kernel modules from various user space
  driver libraries (libmlx4, libcxgb3, libcxgb4, etc.) to rdma
  package and make those packages require rdma package.  This excludes
  libipathverbs since the modprobe files are provided by upstream.
- Resolves: bz1164618

* Fri Dec 05 2014 Doug Ledford <dledford@redhat.com> - 7.1_3.17-3
- Fixes for module load problems at startup
- Resolves: bz1158000

* Wed Nov 26 2014 Doug Ledford <dledford@redhat.com> - 7.1_3.17-2
- Fixes to the SRIOV setup code
- Related: bz1094538

* Mon Oct 06 2014 Doug Ledford <dledford@redhat.com> - 7.1_3.17-1
- Update version to match kernel submission
- Fix for usnic_verbs instead of enic in udev rules file
- Add support for setting the GUIDs and MACs of SRIOV vfs
- Resolves: bz1094538

* Wed Apr 02 2014 Doug Ledford <dledford@redhat.com> - 7.0_3.13_rc8-3
- Use is_available_wait from new initscripts so we wait for link to
  come up.  These keeps high speed devices from failing to start
  because their link is slow to initialize.
- Related: bz1078915

* Fri Feb 28 2014 Doug Ledford <dledford@redhat.com> - 7.0_3.13_rc8-2
- Add a dracut module so the rdma stack can be brought up in
  by the initramfs
- Related: bz1064316

* Thu Jan 23 2014 Doug Ledford <dledford@redhat.com> - 7.0_3.13_rc8-1
- Fix numbering (3.10 versus 3.13)
- Related: bz1056145

* Wed Jan 22 2014 Doug Ledford <dledford@redhat.com> - 7.0_3.10_rc8-1
- Update Requires to systemd-units instead of just systemd
- Reset numbering back to what it is supposed to be, but change the
  format to mass rebuilds don't cause a problem in the future
- Related: bz1018658, bz1056145

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 7.0-4
- Mass rebuild 2013-12-27

* Tue Nov 26 2013 Doug Ledford <dledford@redhat.com> - 7.0-3.10.3
- Actually use the udev rules macro to keep rpmdiff happy
- Related: bz1012796

* Tue Nov 26 2013 Doug Ledford <dledford@redhat.com> - 7.0-3.10.2
- Add a comment to the udev rules file for IPoIB renaming
- Move rdma commands to libexecdir.  They aren't intended to be run
  manually by humans and this avoids the errors about man pages
  not being present
- Move udev rules to /usr/lib/udev
- Resolves: bz1012796

* Tue Nov 26 2013 Doug Ledford <dledford@redhat.com> - 7.0-3.10.1
- Update numbering scheme.  Version now corresponds to the version of
  rhel it is built under, release is a dual component number that
  gives the upstream kernel version of the InfiniBand stack used
  in our current release (aka, the 3.10 above) followed by our
  own release number (aka .1).
- Make rds loading conditional on the rds module existing (it has
  been disabled in some kernels)
- Update udev rule script and rdma-kernel-init scripts to offload
  node description setting to udev, and make it more reliable
- Resolves: bz1018658

* Thu Aug 08 2013 Doug Ledford <dledford@redhat.com> - 2.0-13
- Fix bug in ifdown-ib script

* Tue Jul 30 2013 Doug Ledford <dledford@redhat.com> - 2.0-12
- Change VLAN/PKEY in ifup/ifdown scripts.  Overloading VLAN was
  causing problems

* Thu May 23 2013 Doug Ledford <dledford@redhat.com> - 2.0-11
- Oops, didn't update ifdown-ib to match latest ifup-ib

* Thu May 23 2013 Doug Ledford <dledford@redhat.com> - 2.0-10
- More fixups for ifup-ib and P_Key support
- Move persistent-ipoib.rules to 70 instead of 60 to match prior
  persistent-net.rules file numbering

* Wed May 22 2013 Doug Ledford <dledford@redhat.com> - 2.0-9
- Add support for P_Key interfaces (IPoIB version of VLANs)
- Add sample 60-persistent-ipoib.rules file

* Mon Mar 25 2013 Doug Ledford <dledford@redhat.com> - 2.0-8
- Drop the sysv package
- Add the SRPT module to the conf file and startup script
- Add support for the new ocrdma driver from Emulex

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 05 2012 Doug Ledford <dledford@redhat.com> - 2.0-6
- Add some proper systemd scriptlets
- Resolves: bz820154, bz816073, bz816389

* Tue Nov 27 2012 Doug Ledford <dledford@redhat.com> - 2.0-5
- Oops, we really do need that install section in our service file, so
  put it back

* Tue Nov 27 2012 Doug Ledford <dledford@redhat.com> - 2.0-4
- Don't add an Install section to our service file, that way we aren't
  started unless our hardware is detected

* Mon Nov 26 2012 Doug Ledford <dledford@redhat.com> - 2.0-3
- Minor corrections to systemd service file

* Mon Nov 26 2012 Doug Ledford <dledford@redhat.com> - 2.0-2
- Minor whitespace cleanups
- Correct the usage of MTRR_SCRIPT in rdma-init-kernel
- Remove no longer relevant sections of config related to NFSoRDMA
  (now handled by nfs-utils-rdma)

* Mon Nov 26 2012 Doug Ledford <dledford@redhat.com> - 2.0-1
- Update version to reflect addition of systemd support

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Doug Ledford <dledford@redhat.com> - 1.0-11
- Remove udev rules file, recent kernels create the proper devices without
  need of the file
- Remove the nfs-rdma init script so it can be taken over by the nfs-utils
  package
- Fix up some LSB header bogons in the init script (will convert to
  systemd after this is tested and working and move sysv init script
  to a sub-package)
- Add ifdown-ib and update ifup-ib so we have more of the same capabilities
  on IPoIB interfaces that RHEL has

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 02 2010 Doug Ledford <dledford@redhat.com> - 1.0-8
- Update udev rules syntax to eliminate warnings emitted via syslog (bz603264)
- Add new init script for starting/stopping nfs over rdma support
- Require that the nfs-rdma service be down before stopping the rdma
  service (bz613437)
- Change ifup-ib to properly account for the fact that the [ test program
  does not process tests in order and fail immediately on first failing
  test, resulting in error messages due to unquoted environment variables
  that don't need quoting in the second test due to the fact that the
  first test guarantees they exist.  Or that's how things should be, but
  they aren't, so rewrite tests to accommodate this fact. (bz612284)
- Use ip instead of ifconfig as ifconfig knows it doesn't handle infinband
  hardware addresses properly (even though we don't care, we aren't using
  it for that) and prints out copious warning messages (bz613086)
  
* Thu Feb 25 2010 Doug Ledford <dledford@redhat.com> - 1.0-7
- Minor tweak to rdma.init to silence udev warnings (bz567981)

* Tue Dec 01 2009 Doug Ledford <dledford@redhat.com> - 1.0-6
- Tweak init script for LSB compliance
- Tweak ifup-ib script to work properly with bonded slaves that need their
  MTU set
- Tweak ifup-ib script to properly change connected mode either on or off
  instead of only setting it on but not turning it off if the setting changes

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 09 2008 Doug Ledford <dledford@redhat.com> - 1.0-3
- Add the ifup-ib script so we support connected mode on ib interfaces

* Mon Jun 09 2008 Doug Ledford <dledford@redhat.com> - 1.0-2
- Attempt to use --subsystem-match=infiniband in the rdma init script use
  of udevtrigger so we don't trigger the whole system
- Add a requirement to stop opensm to the init script

* Sun Jun 08 2008 Doug Ledford <dledford@redhat.com> - 1.0-1
- Create an initial package for Fedora review

