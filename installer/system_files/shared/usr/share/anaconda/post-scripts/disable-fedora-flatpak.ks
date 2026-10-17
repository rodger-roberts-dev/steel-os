# Based on Bazzite (github.com/ublue-os/bazzite), Apache-2.0. Modified for Steel OS by Steel & Code (STEEL-35).
%post --erroronfail --log=/tmp/anacoda_custom_logs/disable-fedora-flatpak.log
systemctl disable flatpak-add-fedora-repos.service || :
%end
