# Steel OS (STEEL-35): mark a successful install so the live desktop can offer
# "Restart now" once the installer closes (see /usr/bin/steel-os-install-done).
%post --nochroot --log=/tmp/anacoda_custom_logs/steel-os-installed.log
touch /run/steel-os-installed
chmod 0644 /run/steel-os-installed
%end
