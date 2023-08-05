#
# This file is part of pysnmp-apps software.
#
# Copyright (c) 2005-2018, Ilya Etingof <etingof@gmail.com>
# License: http://snmplabs.com/pysnmp/license.html
#
from pysnmp import error


class SnmpApplicationError(error.PySnmpError):
    pass
