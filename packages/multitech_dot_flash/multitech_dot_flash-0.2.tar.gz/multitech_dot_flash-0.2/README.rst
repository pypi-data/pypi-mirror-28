===========================
xDot and mDot flash utility
===========================

ARM Mbed Multitech xDot and mDot flash utility to be used within ARM Mbed projects.

Features
--------

- Create a virtualenv with Mbed toolchain
- Deploy Mbed, installing the required Mbed libs
- Compile with ARM Compiler 5
- Flash the binary to your xDot or mDot devices

Install it globally
-------------------

``sudo pip install multitech_dot_flash``

How to use it
-------------

Compile and flash an xdot

``flashit -t=xdot``

Flash previous build, already compiled for an mdot

``flashit -t=mdot -p``
