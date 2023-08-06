# Junc (Short for Junction)
## SSH to servers easily
Now you don't have to remember usernames and IPs, and no more aliases for each of your machines.
# Usage
## See the help page
```sh
$ junc --help
Usage:
    junc connect <name>
    junc list
    junc add (<name> <username> <ip>) [<location>]
    junc remove <name>
...
```
## Add a server
```
$ junc add [server_name] [username] [ip] [location (optional)]
OR
$ junc add
Name: [type-it-here]
Username: [type it here]
IP: [type it here]
Location: [type it here]
```
## List servers
```
--------------------------------------------------------------
$ junc list
+---------+----------------------+-------------+
| Name    | Address              | Location    |
+---------+----------------------+-------------+
| server1 | pi@192.168.0.115     | Server Room |
| server2 | pi@192.168.0.134     | Kitchen     |
| ec2     | ubuntu@145.555.55.57 | Oregon?     |
+---------+----------------------+-------------+
```
## Connect to a server
```
$ junc connect [server_name]
Connecting...
```
## Backup your servers
```
$ junc backup
Backing up to /Users/you/.junc.json.bak
Done
```
## Restore the backup
```
$ junc restore
This will overwrite your current /Users/llamicron/.junc.json
Are you sure? (y/n) y
Restoring to /Users/llamicron/.junc.json
Done
```

# Tricks
## Upload your server list to `haste`
you need the `haste` gem installed.
```
$ gem install haste
$ junc list --json | haste
```

## Custom backup location
```
$ junc backup /your/custom/location
```

