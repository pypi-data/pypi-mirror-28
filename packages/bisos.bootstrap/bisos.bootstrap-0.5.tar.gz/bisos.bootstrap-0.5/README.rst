=======================
bisos.bootstrap Scripts
=======================

.. contents::
   :depth: 3
..

Overview
========

Bash scripts (Interactive Command Modules – ICM) for bootstrapping BISOS
(ByStar Internet Services OS) software profiles on a virgin Linux
distro. Or for creating fully automated KVM guests that are ByStar
Platforms.

Running **bx2Genesis.sh** will go through a complete ByStar Platform
installation on the local host.

Running **bxBootstrapGuest.sh** will create a fully automated KVM Guest
ByStar Platform.

Support
=======

| For support, criticism, comments and questions; please contact the
  author/maintainer
| `Mohsen Banan <http://mohsen.1.banan.byname.net>`__ at:
  http://mohsen.1.banan.byname.net/contact

Documentation
=============

Part of ByStar Digital Ecosystem http://www.by-star.net.

This module’s primary documentation is in
http://www.by-star.net/PLPC/180047

Installation
============

::

    sudo pip install bisos.bootstrap

Usage
=====

::

    /usr/local/bin/bx2Genesis.sh
    /usr/local/bin/bxBootstrapGuest.sh

On a virgin BxP-Distro, run “sudo /usr/local/bin/bx2Genesis.sh” and you
will end up with a Generic BISOS Platform. Which you can then apply to a
desired bxpCharacter.

On any Linux machine that has kvm in its distro, run
/usr/local/bin/bxBootstrapGuest.sh and you will end up with a guest at
the specified desired level (as ByStar Platforms).
