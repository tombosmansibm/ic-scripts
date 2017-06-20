#
#    Get current application security roles on connections apps
#    
#    
#
#    2014-12-09    Tom Bosmans (tom.bosmans@be.ibm.com)
#    
import java.lang.System as system
import time
import os

lineSeparator = system.getProperty('line.separator')
#appName="Activities"

#afilename = "/tmp/security"+time.strftime("%Y%m%d_%H%M%S")+".txt"
afilename = os.environ['APPSECURITYOUTFILE']
if afilename == "":
	afilename = "/tmp/security"
if afilename == None:
	afilename = "/tmp/security"
afilename = afilename+time.strftime("%Y%m%d_%H%M%S")+".txt"
accesscontrolfile = open( afilename , 'w')

apps = AdminApp.list()
appsList = apps.split( lineSeparator )
for appName in appsList:
	outputApp = AdminApp.view(appName, "-MapRolesToUsers")
	outputApp = outputApp.split(lineSeparator)

	#	accesscontrolfile = open( "/tmp/activities.txt" , 'w')
	accesscontrolfile.write("# "+appName.upper()+lineSeparator)
	for aline in outputApp:
		# locate all role entries and store them in a list or something
		if aline.startswith("Role"):
			# stay in the role
			# clear the aclDict value
			currentRoleName=aline.split(":")
			accesscontrolfile.write("# "+currentRoleName[1]+lineSeparator)
			currentRoleName=appName+"."+currentRoleName[1].strip()
		if aline.startswith("Everyone"):
			roleEnabled=aline.split(":")
			if roleEnabled[1].strip() == "Yes":
				accesscontrolfile.write(currentRoleName+"=special.Everyone"+lineSeparator)
		if aline.startswith("All authenticated"):
			roleEnabled=aline.split(":")
			if roleEnabled[1].strip() == "Yes":
				accesscontrolfile.write(currentRoleName+"=special.AllAuthenticated"+lineSeparator)
		if aline.startswith("Mapped users:"):
			roleEnabled=aline.split(":")
			if roleEnabled[1].strip() == "":
				print "no users for role " + currentRoleName
			else:
				userList=roleEnabled[1].strip()
				userList=userList.split("|")
				for users in userList:
					accesscontrolfile.write(currentRoleName+"=user."+users+lineSeparator)
		if aline.startswith("Mapped groups:"):
			roleEnabled=aline.split(":")
			if roleEnabled[1].strip() == "":
				#print "no groups for role " + currentRoleName
				print ""
			else:
				userList=roleEnabled[1].strip().split("|")
				for users in userList:
					accesscontrolfile.write(currentRoleName+"=group."+users+lineSeparator)
	accesscontrolfile.flush()

print " Results stored in : " + afilename 

accesscontrolfile.close()


