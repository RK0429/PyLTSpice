#!/usr/bin/env python
# coding=utf-8

# -------------------------------------------------------------------------------
#    ____        _   _____ ____        _
#   |  _ \ _   _| | |_   _/ ___| _ __ (_) ___ ___
#   | |_) | | | | |   | | \___ \| '_ \| |/ __/ _ \
#   |  __/| |_| | |___| |  ___) | |_) | | (_|  __/
#   |_|    \__, |_____|_| |____/| .__/|_|\___\___|
#          |___/                |_|
#
# Name:        raw_write.py
# Purpose:     Create RAW Files
#
# Author:      Nuno Brum (nuno.brum@gmail.com)
#
# Created:     16-10-2021
# Licence:     refer to the LICENSE file
# -------------------------------------------------------------------------------

"""
This module generates RAW Files from user data.
It can be used to combine RAW files generated by different Simulation Runs
"""
from kupicelib.raw.raw_write import RawWrite, Trace

# Re-export the classes
__all__ = ["RawWrite", "Trace"]
