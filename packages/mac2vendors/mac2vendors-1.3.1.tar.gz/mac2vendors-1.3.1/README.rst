mac2vendors
===========

Convert mac addresses to vendor information/ names !

Installation
------------

``pip install mac2vendors``

Usage
-----

::

    mtv --help

    usage: mtv [-h] {mac} ...

    positional arguments:
      {mac}  [command] help
        mac        Translates the mac address to a vendor mapping.

    optional arguments:
      -h, --help   show this help message and exit

Raw Usage
---------

Use from code
~~~~~~~~~~~~~

::

    from mac2vendors import get_mac_vendor
    vendor_list = get_vendor(mac_address="00:00:00")
    print(vendor_list)
    [['00:00:00', '00:00:00', 'Officially Xerox, but 0:0:0:0:0:0 is more common']]
