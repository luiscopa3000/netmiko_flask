# network_template.py

template = """
Value Vlan (\d+)
Value Mac_Address (\S+)
Value Type (\S+)
Value Ports (\S+)

Start
  ^\s*${Vlan}\s+${Mac_Address}\s+${Type}\s+${Ports} -> Record
"""
