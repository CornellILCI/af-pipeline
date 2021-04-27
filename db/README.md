### Liquibase Setup

1. Clone the af-db repository to your home directory.  
`git clone https://bitbucket.org/ebsproject/breeding-analytics-db.git`  
2. Add the repository to your terminal PATH   
	* Enter the repository's folder  
		`cd /home/<username>/af-db/build/liquibase/bin/`  
	* Type `pwd`, then press `Enter` to see your current working directory  
		`pwd`
	* Copy it then add it to your PATH  
		`export PATH=$PATH:/home/<username>/af-db/build/liquibase/bin/`  
	* The command above only updates your path temporarily. Use the command below to permanently change your PATH even after terminating the current session.  
		`source ~/.profile or source ~/.bashrc`  
    * For Mac users, you can conveniently set the PATH using the terminal in Default mode. To update the PATH, you can run...  
		`sudo nano /etc/paths`  
		then append the path to the end of the file.  
		```...
		/path/to/af-db```  
		Hit Ctrl + X, then Y for yes, to save the file and restart your Terminal.  
		Note: Make sure to start a new terminal session for the changes to take effect.
		
3. Run the command below to test liquibase.  
	`liquibase --version`  
	You should see the following output.  
```
		Starting Liquibase at Wed, 15 Apr 2020 23:28:39 PST (version 3.8.6 #49 built at Fri Feb 07 05:16:10 UTC 2020)  
		Liquibase Version: 3.8.6  
		Liquibase Community 3.8.6 by Datical  
		Running Java under /Library/Java/JavaVirtualMachines/jdk-13.0.1.jdk/Contents/Home (Version 13.0.1)
```  
### Template Database Setup
1. Create `aftemplatedb` database in your local.
2. Configure liquibase-template.properties file  
```
		changeLogFile: changelogs/db-changelog-master.xml
		driver: org.postgresql.Driver
		url: jdbc:postgresql://localhost:5432/aftemplatedb
		username: postgres
		password: XXXX
		classpath: drivers/postgresql-42.2.10.jar
		contexts: schema, template
		labels: clean
```
3. Execute this command on your terminal to update your database.  
		`liquibase --defaultsFile=liquibase-template.properties update`
		
### Fixture Database Setup
1. Create `affixturedb` database in your local.  
2. Configure liquibase_fixture.properties file
```
		changeLogFile: changelogs/db-changelog-master.xml
		driver: org.postgresql.Driver
		url: jdbc:postgresql://localhost:5432/affixturedb
		username: postgres
		password: postgres
		classpath: drivers/postgresql-42.2.10.jar
		contexts: schema, template, fixture
		labels: clean, develop
```
3. Execute this command on your terminal to update your database.  
		`liquibase --defaultsFile=liquibase-fixture.properties update`
	
