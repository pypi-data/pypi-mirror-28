# Junc (Short for Junction)
## SSH to servers easily
Now you don't have to remember usernames and IPs, and no more aliases for each of your machines.
## Usage
```bash
$ junc --help
# Usage:
#     junc connect <name>
#     junc list
#     junc add (<name> <username> <ip>) [<location>]
#     junc remove <name>
# ...

$ junc add [server_name] [username] [ip] [location (optional)]

$ junc list
# +---------+----------------------+-------------+
# | Name    | Address              | Location    |
# +---------+----------------------+-------------+
# | server1 | pi@192.168.0.115     | Server Room |
# | server2 | pi@192.168.0.134     | Kitchen     |
# | ec2     | ubuntu@145.555.55.57 | Oregon?     |
# +---------+----------------------+-------------+

$ junc connect [server_name]
Connecting...
```

