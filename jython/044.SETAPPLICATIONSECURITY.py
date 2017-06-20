#
#    Set application security roles on connections apps
#    
#    
#
#    2012-08-09    Tom Bosmans (tom.bosmans@be.ibm.com)
#    2012-08-13     Tom Bosmans - updated all admin roles to include connections, and all widget-admin roles
#    The option takes these parms;
#    2013-05-28     Tom Bosmans - made the script generic, using a properties file
#    2014-03-27    Tom Bosmans - fixed 2 errors : (1)multiple users where not added correctly, (2)syntax error in if/else statement
#    2015-08-25		Tom Bosmans - fix to allow email addresses as usernames	
#    2016-11-15	Tom Bosmans - fix to allow points and = signs as usernames and role names 
#    
#    ./wsadmin.sh -lang jython -username -password -f //setApplicationSecurity2.py //appsecurity.txt
#    
#    Role name - "role"
#    Everyone - yes/no
#    All Authenticated - yes/no
#    Mapped users - "user1|user2"
#    ( one/more users separated with a '|'
#    Mapped groups - "group1|group2"
#    ( one/more groups separated with a '|'
#    AllAuthenticated in trusted realms    - yes/no
#    MappedUserAccessIDs
#    MappedGroupAccessIds

#Use this script to map users to any Registry Services-specific roles
#AdminApp.edit(AppName, '[-MapRolesToUsers [[Role Everyone AllAuthenticated MappedUsers MappedGroups AllAuthenticatedInTrustedRealms MappedUsersAccessIDs MappedGroupsAccessIDs]]]')
#AdminConfig.save()

print "*******************"
import sys
import java.lang.System as system
import os
# This line controls whether the updateAccessIDs is executed.  This requires the users and groups to exist in the directory!
# use 1 or 0 (yes/no)
doUpdateAccessIDs = 0
aclfilename=os.environ['APPLICATIONSECURITYINPUTFILE']
if aclfilename == "":
    raise Exception("YOU MUST PROVIDE THE FULL FILEPATH TO THE ACL FILE through the environment variable APPLICATIONSECURITYINPUTFILE")
    sys.exit


#aclfilename =  sys.argv[0]
print "Using "+aclfilename
if not os.path.exists( aclfilename ):
    raise Exception(aclfilename + " does not exist.  Exiting.")
    sys.exit

lineSeparator = system.getProperty('line.separator')

accesscontrolfile = open( aclfilename , 'r')
accesscontrolfile.seek(0)
#Empty dictionary
aclDict = {}
#Empty dictionary to contain the commands
commandDict = {}

for aclline in accesscontrolfile.readlines():
    if aclline.startswith("#"):
        #comments - skip
        print aclline.rstrip()
    elif aclline.strip() == "":
        #SKIP empty lines        
        print ""
    else:
        print aclline.rstrip()
        aclentry = aclline.rstrip().split("=")
	tempAclEntry = aclentry.pop(0)
	#thingieList = aclentry.pop(0)  # pop removes first item and returns that item
	#print "Thingielist // "+ "".join(aclentry) 	
        if len(aclDict) < 1:
            #print "new dictionary"
            #aclDict[tempAclEntry] = aclentry[1].rstrip()
	    aclDict[tempAclEntry] = "=".join(aclentry)
        else:
	    #thingieList = aclentry.remove(aclentry[0])
            if  aclDict.has_key(tempAclEntry):
                existingValue = aclDict[tempAclEntry]
                #print "existing " + existingValue
                #aclDict[aclentry[0]] = existingValue  + ";" + aclentry[1]
                aclDict[tempAclEntry] = existingValue  + ";" + "=".join(aclentry)
            else:
                aclDict[tempAclEntry] = "=".join(aclentry)  

accesscontrolfile.close()
#now everything is loaded in a dictionary

#print "dictionary:"
#print "***********"
#for v in aclDict.keys():
#    print v + " : " + aclDict.get(v,"Not found")

# Loop the dictionary
for v in aclDict.keys():
    splitV = v.rstrip().split(";")
    # splitV now contains an array, with the first the appname+role and the second value, the individual values to set
    # we'd need to build the command
    appName = splitV[0].split(".")[0]
#    appRole = splitV[0].split(".")[1]
    rolesList = splitV[0].split(".") 
    if len(rolesList) > 1:
	x = 1
	appRole = ""
	while (x < len(rolesList)):
		if appRole == "":
			appRole = rolesList[x]
		else:
			appRole = appRole+"."+rolesList[x]
		print appRole 
		x = x+1
    else:
	appRole = rolesList[1]
    groups = ""
    users = ""
    allAuth = "no"
    everyone = "no"
    print "*******************************************"
    print "AppName: " + appName + " Role: " + appRole
    print "*******************************************"
    for entry in aclDict.get(v,"Not found").split(";"):
        splitEntry = entry.split(".")
        if splitEntry[0] == "group":
	    c1 = 2
            tmpGroup = splitEntry[1]	
            print "group - " + "".join(splitEntry)
            while c1 < len(splitEntry):
		tmpGroup = tmpGroup + "." + splitEntry[c1]
		c1=c1+1
            print "group - " + tmpGroup
            if groups == "":
                groups = tmpGroup
            else:
                groups = groups+"|"+tmpGroup
        elif splitEntry[0] == "user":
            c1 = 2
            tmpUser = splitEntry[1]
            while c1 < len(splitEntry):
                tmpUser = tmpUser + "." +  splitEntry[c1]
                c1 = c1+1
            print "user - " + tmpUser
            if users == "":
                users =  tmpUser
            else:
                users = users+"|"+ tmpUser
        elif splitEntry[0] == "special":
            #print "special - " + splitEntry[1]
            if splitEntry[1] == "AllAuthenticated":
                allAuth = "yes"
            if splitEntry[1] == "Everyone":
                 everyone = "yes"
        else:
            print "*************"
            print " WARNING : UNKNOWN TYPE " + splitEntry[0] + " , Please check your syntax"
            print "*************"

    #command = '[-MapRolesToUsers [[ "' + appRole + '" ' + everyone + ' '+ allAuth +' "' + users + '" "'+groups+'" "" "" "" ]]]'
    #command = '[ "' + appRole + '" ' + everyone + ' '+ allAuth +' "' + users + '" "'+groups+'" "" "" "" ]'
    command = '[ "' + appRole +'" ' + everyone + ' '+ allAuth +' "' + users + '" "'+groups+'" "" "" "" ]'
    
    #print command
    #AdminApp.edit(appName,command)

    # note that this next line will cause errors if the users do not exist !!!!!
    #if doUpdateAccessIDs:
    #    print AdminApp.updateAccessIDs(appName, 0)
    #    AdminConfig.save()
    #print "*******************************************"
    if len(commandDict) < 1:
            #print "new dictionary"
            commandDict[appName] = command
    else:
        if  commandDict.has_key(appName):
          existingValue = commandDict[appName]
          #print "existing " + existingValue
          commandDict[appName] = existingValue + " " + command
        else:
          commandDict[appName] = command

print "Command List:"
print "*********************************************"

for v in commandDict.keys():
    printMyLine= "AdminApp.edit('" + v + "','[-MapRolesToUsers [" +  commandDict.get(v,
"Not found") + "]]')" 
    print printMyLine 

print "*********************************************"
print "*********************************************"

for v in commandDict.keys():
    printMyLine= "AdminApp.edit('" + v + "','[-MapRolesToUsers [" +  commandDict.get(v,
"Not found") + "]]')" 
    exec(printMyLine)    

#EXECUTING
# Save
print "*********************************************"
print "Saving ...."
AdminConfig.save()

print "*********************************************"

AdminNodeManagement.syncActiveNodes()
print '******* DONE *********'

