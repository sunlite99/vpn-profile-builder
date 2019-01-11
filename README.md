# vpn-profile-builder
Python 3 utility to generate iOS IKEv2 VPN configuration profiles.

# Current Features
- Generates .mobileconfig file for loading onto iOS devices
- VPN Types: IKEv2
- Authentication Methods: Username/Password
- Supports all cryptographic algorithms and DH groups specified in iOS documentation
- Supports connect-on-demand for cellular and wireless networks with SSID whitelisting

# TO DO
- [ ] Comment my code. I know...
- [ ] Add other VPN types
  - [ ] Cisco IPsec (IKEv1)
  - [ ] L2TP
- [ ] Certificate authentication
- [ ] Menu?

# Notes

- PPTP is not happening. Ever. Don't even ask. It's horrendously insecure, and if you're still using it, you have bigger problems.
