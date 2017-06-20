
# Description
The jython files rely on environment variables to be present.
They are meant to be run on the Dmgr for the Connections Cell.  
These can be set using your Operating System's command line (eg. export VAR=value on Linux).

## 043.GETAPPLICATIONSECURITY.py
```
export APPSECURITYOUTFILE=/tmp/roles
cd <dmgr_profile_root>/bin
./wsadmin.sh -lang jython -f <path-to-file>/043.GETAPPLICATIONSECURITY.py
```
## 044.SETAPPLICATIONSECURITY.py
```
export APPLICATIONSECURITYINPUTFILE=/tmp/modified-roles.txt
cd <dmgr_profile_root>/bin
./wsadmin.sh -lang jython -f <path-to-file>/044.SETAPPLICATIONSECURITY.py
```
