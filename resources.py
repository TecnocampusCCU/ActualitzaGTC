# -*- coding: utf-8 -*-

# Resource object code
#
# Created by: The Resource Compiler for PyQt5 (Qt v5.15.2)
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore

qt_resource_data = b"\
\x00\x00\x01\x29\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x17\x00\x00\x00\x18\x08\x06\x00\x00\x00\x11\x7c\x66\x75\
\x00\x00\x00\x01\x73\x52\x47\x42\x00\xae\xce\x1c\xe9\x00\x00\x00\
\x04\x67\x41\x4d\x41\x00\x00\xb1\x8f\x0b\xfc\x61\x05\x00\x00\x00\
\x09\x70\x48\x59\x73\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7\x6f\
\xa8\x64\x00\x00\x00\xbe\x49\x44\x41\x54\x48\x4b\x63\x64\x20\x02\
\x38\x39\x39\xfd\x17\x13\x13\x63\x78\xf5\xea\x15\xc3\xbe\x7d\xfb\
\x88\xd2\x03\x02\x4c\x50\x9a\x26\x60\xd4\x70\xac\x80\xa6\x86\x13\
\x15\xf3\xff\xd7\x49\xfc\x87\x32\xc1\x80\x31\xe8\x05\x51\xfa\x08\
\x2a\x42\x37\x18\x06\x88\xb1\x80\xb6\xc1\x02\xca\x20\x50\x36\x56\
\xb0\x37\xe7\x1a\x94\x85\x0a\x9c\xa7\x68\x41\x59\xb8\x01\x63\x44\
\x44\x04\x5e\xc3\x97\x87\x1d\x80\xb2\x50\x41\xe4\x2a\x07\x28\x0b\
\x37\x20\xe8\x72\x10\x40\x77\x3d\x31\xae\x1e\x05\x38\x01\x3c\xad\
\xbe\x91\x51\xc1\x1a\xf6\x22\x4f\xee\x30\xe2\x93\x03\xd1\xe8\xf2\
\x30\x71\x8a\xd3\x39\x2e\x8b\x51\x00\x48\x11\x21\x85\xd8\xd4\xe0\
\xd3\x87\xd5\xe5\x30\x0d\xb8\x34\x11\x0b\xe8\x5f\xe4\xc2\x22\x84\
\x52\x80\x61\x38\xb9\xc1\x81\x2d\x28\x29\x0e\x16\x6a\xf9\x92\x44\
\xc0\xc0\x00\x00\x59\xab\x4d\xe0\xa0\xb5\x84\xb9\x00\x00\x00\x00\
\x49\x45\x4e\x44\xae\x42\x60\x82\
"

qt_resource_name = b"\
\x00\x07\
\x07\x3b\xe0\xb3\
\x00\x70\
\x00\x6c\x00\x75\x00\x67\x00\x69\x00\x6e\x00\x73\
\x00\x0d\
\x00\x17\x2d\x03\
\x00\x41\
\x00\x63\x00\x74\x00\x75\x00\x61\x00\x6c\x00\x69\x00\x74\x00\x7a\x00\x61\x00\x47\x00\x54\x00\x43\
\x00\x08\
\x0a\x61\x5a\xa7\
\x00\x69\
\x00\x63\x00\x6f\x00\x6e\x00\x2e\x00\x70\x00\x6e\x00\x67\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x14\x00\x02\x00\x00\x00\x01\x00\x00\x00\x03\
\x00\x00\x00\x34\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x14\x00\x02\x00\x00\x00\x01\x00\x00\x00\x03\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x34\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x8e\xe0\x7e\xa1\x65\
"

qt_version = [int(v) for v in QtCore.qVersion().split('.')]
if qt_version < [5, 8, 0]:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2

def qInitResources():
    QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
