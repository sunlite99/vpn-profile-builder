#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 21:17:52 2019

@author: Justin Coffman
"""

import plistlib
import defs
import uuid


def getcipher(msg):
    print()
    n = 0

    for key, value in defs.CIPHERS.items():
        n += 1
        safe = (" (UNSAFE)", "")[value]
        print("{0}: {1}{2}".format(n, key, safe))

    while True:
        try:
            return list(defs.CIPHERS)[
                int(input("Select " + msg + " encryption algorithm: ")) - 1
            ]
            break
        except ValueError:
            print("Invalid selection.")


def getdigest(msg):
    print()
    n = 0

    for key, value in defs.DIGESTS.items():
        n += 1
        safe = (" (UNSAFE)", "")[value]
        print("{0}: {1}{2}".format(n, key, safe))

    while True:
        try:
            return list(defs.DIGESTS)[
                int(input("Select " + msg + " digest algorithm: ")) - 1
            ]
            break
        except ValueError:
            print("Invalid selection.")


def getdh(msg):
    print()
    n = 0

    for key, _ in defs.DH_GROUPS.items():
        n += 1
        safe = (" (UNSAFE)", "")[defs.SAFE_DH_GROUPS[key]]
        print("{0}: {1}{2}".format(n, key, safe))

    while True:
        try:
            return defs.DH_GROUPS[
                list(defs.DH_GROUPS)[int(input("Select " + msg + " DH group: ")) - 1]
            ]
            break
        except ValueError:
            print("Invalid selection.")


def getalgos(phase):
    msg = ("IKEv2 Phase 1 (IKE SA)", "IKEv2 Phase 2 (Child SA)")[phase - 1]

    return getcipher(msg), getdigest(msg), getdh(msg)


def genuuid():
    return str(uuid.uuid4()).upper()


try:
    plDisplayName = input("Profile Display Name: ")

    if not plDisplayName:
        raise ValueError("Display name is required!")

    plVPNName = input("VPN Display Name [" + plDisplayName + "]: ") or plDisplayName
    plRemoteHost = input("Server IP or FQDN: ")

    if not plRemoteHost:
        raise ValueError("Remote host is required!")

    plRemoteID = input("Remote ID [" + plRemoteHost + "]: ") or plRemoteHost
    plLocalID = input("Local ID []: ") or None

    plIKEP1EA, plIKEP1IA, plIKEP1DH = getalgos(1)
    plIKEP2EA, plIKEP2IA, plIKEP2DH = getalgos(2)

    if input("Connect on demand (y/N)? ").lower().strip()[:1] == "y":
        plOnDemand = True
    else:
        plOnDemand = False

    if plOnDemand:
        if (
            input("Connect on while on cellular network (y/N)? ").lower().strip()[:1]
            == "y"
        ):
            plODCellular = True
        else:
            plODCellular = False

        if (
            input("Connect on while on wireless network (y/N)? ").lower().strip()[:1]
            == "y"
        ):
            plODWifi = True
        else:
            plODWifi = False

        if plODWifi:
            if (
                input("Whitelist any wireless networks (y/N)? ").lower().strip()[:1]
                == "y"
            ):
                plODWifiWL = list(
                    map(
                        str.strip,
                        input(
                            "Enter wireless networks to whitelist (comma-delimited): "
                        ).split(","),
                    )
                )
            else:
                plODWifiWL = None

        if (not plODCellular) and (not plODWifi):
            print("On-Demand was selected, but no networks were activated.")
            print("On-Demand will be disabled in this profile.")
            plOnDemand = False

    plUUID = genuuid()
    plContentUUID = genuuid()

    pl = {
        "PayloadContent": [
            {
                "IKEv2": {
                    "AuthenticationMethod": "None",
                    "IKESecurityAssociationParameters": {
                        "EncryptionAlgorithm": plIKEP1EA,
                        "IntegrityAlgorithm": plIKEP1IA,
                        "DiffieHellmanGroup": plIKEP1DH,
                    },
                    "ChildSecurityAssociationParameters": {
                        "EncryptionAlgorithm": plIKEP2EA,
                        "IntegrityAlgorithm": plIKEP2IA,
                        "DiffieHellmanGroup": plIKEP2DH,
                    },
                    "DisableRedirect": 1,
                    "EnablePFS": True,
                    "ServerCertificateIssuerCommonName": plRemoteHost,
                    "RemoteAddress": plRemoteHost,
                    "RemoteIdentifier": plRemoteID,
                    "ExtendedAuthEnabled": 1,
                },
                "IPv4": {"OverridePrimary": 1},
                "PayloadDescription": "Configures VPN settings",
                "PayloadDisplayName": "VPN",
                "PayloadIdentifier": "com.apple.vpn.managed." + plContentUUID,
                "PayloadType": "com.apple.vpn.managed",
                "PayloadUUID": plContentUUID,
                "PayloadVersion": 1,
                "UserDefinedName": plVPNName,
                "VPNType": "IKEv2",
            }
        ],
        "PayloadDisplayName": plDisplayName,
        "PayloadIdentifier": "donut.local." + plUUID,
        "PayloadType": "Configuration",
        "PayloadUUID": plUUID,
        "PayloadVersion": 1,
    }

    if plOnDemand:
        pl["PayloadContent"][0]["IKEv2"]["OnDemandEnabled"] = 1
        pl["PayloadContent"][0]["IKEv2"]["OnDemandRules"] = list()

        if plODWifi:
            if plODWifiWL:
                pl["PayloadContent"][0]["IKEv2"]["OnDemandRules"].append(
                    {
                        "Action": "Disconnect",
                        "InterfaceTypeMatch": "WiFi",
                        "SSIDMatch": plODWifiWL,
                    }
                )

            pl["PayloadContent"][0]["IKEv2"]["OnDemandRules"].append(
                {
                    "Action": "Connect",
                    "InterfaceTypeMatch": "WiFi",
                    "URLStringProbe": "http://captive.apple.com/hotspot-detect.html",
                }
            )

        if plODCellular:
            pl["PayloadContent"][0]["IKEv2"]["OnDemandRules"].append(
                {
                    "Action": "Connect",
                    "InterfaceTypeMatch": "Cellular",
                    "URLStringProbe": "http://captive.apple.com/hotspot-detect.html",
                }
            )

    with open(plRemoteHost.replace(".", "_") + ".mobileconfig", "wb") as fp:
        plistlib.dump(pl, fp)

    fp.close()

    print("Profile written to {0}.mobileconfig".format(plRemoteHost.replace(".", "_")))

except ValueError as err:
    print(err)

except Exception as err:
    print(err)
