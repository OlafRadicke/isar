"isar" is a front end for KVM Libvirt.

    AUTHORS
Moldau  code is developed by:

"Olaf Radicke! <briefkasten@olaf-radicke.de>

    VERSION

Beta

    INSTALL

1. make
2. make install
3. start wieth command 'isar'.
4. ignore error window, with data base error (in first start).
5. init the database over window menu "file"->"Create Database".
6. Configure contact typ over window menu "file"->"Settings".

    install mail reminder:
Edit the file /src/cron/isar-cron.sh and configure this as cron job.


    UNINSTALL

make uninstall

    LICENSE:

GPL3


    DEPENDENCY

- Python
- PyQt4
- SQLite3
- doxygen
- kvm
- virsh
- virt-clone
- virt-install
- virt-view


    TODO

- List sort