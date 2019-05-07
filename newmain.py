import argparse

ealgos = {
    'DES': {'secure': False},
    '3DES': {'secure': False},
    'AES-128': {'secure': True},
    'AES-256': {'secure': True},
    'AES-128-GCM': {'secure': True},
    'AES-256-GCM': {'secure': True}
}

aalgos = {
    'SHA1-96': {'secure': False},
    'SHA1-160': {'secure': False},
    'SHA2-256': {'secure': True},
    'SHA2-384': {'secure': True},
    'SHA2-512': {'secure': True}        
}

pfsgroups = {
    'None': {'secure': False, 'desc': 'Disable PFS'},
    '1': {'secure': False, 'desc': 'MODP768'},
    '2': {'secure': False, 'desc': 'MODP1024'},
    '5': {'secure': False, 'desc': 'MODP1536'},
    '14': {'secure': True, 'desc': 'MODP2048'},
    '15': {'secure': True, 'desc': 'MODP3072'},
    '16': {'secure': True, 'desc': 'MODP4096'},
    '17': {'secure': True, 'desc': 'MODP6144'},
    '18': {'secure': True, 'desc': 'MODP8192'},
    '19': {'secure': True, 'desc': 'ECP256'},
    '20': {'secure': True, 'desc': 'ECP384'},
    '21': {'secure': True, 'desc': 'ECP521'}
}

pfshelpstr = "{:<8} {:<13} {:<10}".format('PFS ID', 'PFS Group', 'Secure?') + '\n'
pfshelpstr += ("-" * 30) + '\n'
for pfsid, v in pfsgroups.items():
    pfsname = v['desc']
    if v['secure']:
        pfssec = "Yes"
    else:
        pfssec = "No"
    pfshelpstr += "{:<8} {:<13} {:<10}".format(pfsid, pfsname, pfssec) + '\n'

pfshelpstr = pfshelpstr.rstrip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates a .mobileconfig VPN profile for iOS devices.",
        epilog=f"""
Acceptable EALGO values:
    DES*
    3DES*
    AES-128
    AES-256
    AES-128-GCM
    AES-256-GCM

Acceptable AALGO values:
    SHA1-96*
    SHA1-160*
    SHA2-256
    SHA2-384
    SHA2-512

Acceptable PFSID values:

{pfshelpstr}
    
* Indicates selections that are considered insecure.""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--name",
        help="VPN name"
    )

    parser.add_argument(
        "--profile",
        help="profile name"
    )

    parser.add_argument(
        "--org",
        help="organization name"
    )

    parser.add_argument(
        "--host",
        metavar="IP/FQDN",
        help="VPN server IP or FQDN"
    )

    parser.add_argument(
        "--remote",
        help="remote ID"
    )

    parser.add_argument(
        "--local",
        help="local ID"
    )

    parser.add_argument(
        "--p1e",
        metavar="EALGO",
        help="phase 1 encryption algorithm",
        choices=ealgos
    )

    parser.add_argument(
        "--p1a",
        metavar="AALGO",
        help="phase 1 authentication algorithm",
        choices=aalgos
    )

    parser.add_argument(
        "--p1pfs",
        metavar="PFSID",
        help="phase 1 PFS group ID",
        choices=pfsgroups
    )

    parser.add_argument(
        "--p2e",
        metavar="EALGO",
        help="phase 2 encryption algorithm",
        choices=ealgos
    )

    parser.add_argument(
        "--p2a",
        metavar="AALGO",
        help="phase 2 authentication algorithm",
        choices=aalgos
    )

    parser.add_argument(
        "--p2pfs",
        metavar="PFSID",
        help="phase 2 PFS group ID",
        choices=pfsgroups
    )

    args = parser.parse_args()
    print(args)