#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 21:39:34 2019

@author: jcoffman

CIPHERS and DIGESTS are dicts containing a key that is used as the programmatic
    reference, display value, and plist value, and a value that is a boolean
    indicating whether that option is cryptographically safe.

DH_GROUPS is a dict containing a key that is used as the programmatic reference
    and display value, and a value that is the matching DH group number used
    within the plist payload.

SAFE_DH_GROUPS is a dict containing a key that matches the DH_GROUPS keys and
    a value that is a boolean indicating whether that option is
    cryptographically safe.
"""

CIPHERS = {
    "DES": False,
    "3DES": False,
    "AES-128": True,
    "AES-256": True,
    "AES-128-GCM": True,
    "AES-256-GCM": True,
}

DIGESTS = {
    "SHA1-96": False,
    "SHA1-160": False,
    "SHA2-256": True,
    "SHA2-384": True,
    "SHA2-512": True,
}

DH_GROUPS = {
    "MODP768": 1,
    "MODP1024": 2,
    "MODP1536": 5,
    "MODP2048": 14,
    "MODP3072": 15,
    "MODP4096": 16,
    "MODP6144": 17,
    "MODP8192": 18,
    "ECP256": 19,
    "ECP384": 20,
    "ECP521": 21,
}

SAFE_DH_GROUPS = {
    "MODP768": False,
    "MODP1024": False,
    "MODP1536": False,
    "MODP2048": True,
    "MODP3072": True,
    "MODP4096": True,
    "MODP6144": True,
    "MODP8192": True,
    "ECP256": True,
    "ECP384": True,
    "ECP521": True,
}
