Active Directory Simple Management Toolkit
==========================================


Author: Denis Khodus (aka "Reagent")

License: MIT 2.0

Description:
-----------

Simple Active Directory console-based management toolkit (CLI - command line interface)
which is designed to execute basic administration of MSAD like creating, modifying,
listing, deleting and searching users, groups, computers; printing and managing domain
tree structure and so on. The point of this toolkit creation was to give to system
administrators an ability to easily manage Samba4-based AD domains (when there is no
ability to use GUI MS management console and samba utilities (samba-tool, ldbsearch
and so on) are not comfortable to use.
    
This toolkit was written just because the author did not find any suitable CLI-based,
web-based or GUI-based product which can be comfortably used to administer an
Active Directory domains.

It is not supports multi-domain infrastructure (with domains with relationships with
each other) for now (but is planned to do). Also, support for some elements (like "contacts"
object types and, maybe, DNS records manipulations) is planned to be added later.


Installation:
-------------

Use pip (or pip3) to install this package using PyPI repository:
   

    pip install adsmt


Create a configuration file at "/etc/adsmt.conf". Fill it like example:

**/etc/adsmt**

    
    [mydomain1.lan]
    server=192.168.0.1

    
Where "mydomain.lan" - is the name of the first domain which you want to
administer, and "server" option specifies the IP or hostname of the domain
controller which you want to connect to. Only those two moments are required
to be set in the configuration file. Other options are optional.

Also, several domains may be defined just by adding sections with other
domain names. Example:
    

    [mydomain1.lan]
    server=192.168.1.1
    
    [mydomain2.com]
    server=10.1.76.1
    

Start "**adcli**" bash script which opens CLI for you.


Upgrading
---------

The new version is easy to install - just use pip for this purpose
too, as for installing, but add _-U_ option:


    pip install -U adsmt



Configuration file options:
---------------------------
 
        server=
            The IP address or hostname of the domain controller which will be used
            to administer the entire domain.
        server_port=
            The TCP port of the domain controller to use when connecting.
        use_ssl=
            "1" enables the usage of secure connection to the domain controoler
            (which is default), "0" disables it (not recommended)
        default_user_path=
            The filesystem-like path to the default container where new users about
            to be added to. For example:
            default_user_path=/Users
            or
            default_user_path=/Personnel/Staff
        default_group_path=
            The filesystem-like path to the default container where new groups about
            to be added to. For example:
            default_user_path=/Users
            or
            default_user_path=/Groups/Staff
        default_computer_path=
            The filesystem-like path to the default container where new computers about
            to be added to (means computers which creates by this CLI only). For example:
            default_user_path=/Computers
            or
            default_user_path=/Servers/Datacenter1
        username=
        password=
            The username and his/her password which can be set permanently and which can
            be used instead of querying each time CLI selects the domain. While it is
            really not recommended to fill those options up, it is possible, but it is
            good idea to strongly restrict access to the /etc/adsmt.conf file to running
            user only (maybe for 'root' only and run 'adcli' using 'sudo').


Example configuration file
--------------------------

This is an example configuration file for two abstract domains.


    [domain1.lan]
    server=192.168.1.1
    use_ssl=1
    default_user_path=/Personnel
    default_group_path=/Groups
    default_computer_path=/ExDomain
    
    [domain2.lan]
    server=192.168.10.1
    use_ssl=0
    

