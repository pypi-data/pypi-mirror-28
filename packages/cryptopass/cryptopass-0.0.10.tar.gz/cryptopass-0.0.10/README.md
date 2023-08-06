# cryptopass
Application to manage your passwords in a safe and a simple way.

## description
**cryptopass** store encrypted data entries in a (pandas) database. Each entry stores confidential information in the following fields:
* *cryptopass user*: is your username for cryptopass session. Example: ElonM
* *label*: is the name you wish for the entry. Example: gmail
* *user*: is the username for the login linked to the label. Example: ElonM1971
* *password*: is the password you want to store safely, secretly. Example: univ3rs3Conqu3r0r
* *url*: sometimes is useful to remember the url for login, don't you think? Example: www.gmail.com
* *date_time*: this is an automatic field that stores the time when you create the entry.
* *hint*: some clue to recover. It's more useful if you don't want to store password (not recommended).
* *notes*: be your self and write what you want. Please, be brief.

## instalation

Instalation through PIP:
```
pip install cryptopass
```

The dependecies (python modules) are:
* cryptography
* pandas
* pyperclip

In windows OS execute in command windows:
```
python -m pip install cryptopass
```

If you have Anaconda, **cryptopass** executable will be installed in _Scripts_ folder.


## baby steps
### creating users
When you run **cryptopass** in the console:

```
Cryptopass - version 0.0.10
OK database file: ./database/default.udb

	 Working directory: ./database/
> enter console command (press h for help):
```
A _console command_ is requested. By now, just enter **login** command.
```
> cryptopass user: 
```
Cryptopass user is your *session name*. You will access to database for that session. You can have a lot of users. 
Database for users will be checked to know if the username exist, if not you will can create new one.

We will start with _ElonM_:
```
	 User "ElonM" has not been found!
	 Do you want create new user? [y/n]: 
```
Of course, y (yes):

```
	 Creating new user...
	 if database left clear, it will be: <working dir>/default.pdb

database = 
notes = examples
	 done!
```
The _database_ is requested here is the filename for the encrypted database which will store your information. This database can be shared by users (different session names), and a user can save information (entries) below different _cryptopass passwords_ (passwords to decrypt entries).

### login
If your username is already load, you will see:

```
database does not exist! New database created: ./database/default.pdb

OK database file: ./database/default.pdb

@ElonM> enter crypto command (press h for help):
```

Note that the prompt is _@ElonM_ now, so you are logged.
   
Time for **crypto command**. That's the way you have to put cryptopass in action.
If you press h for help:

```
	 crypto commands: 

	 all: 	 show all valid entries for user/password.
	 All: 	 show all valid entries for user/password. (detailed)
	 all: 	 show all valid entries HINTS for user/password.
	 dbg: 	 execute debug script (just for developing).
	 end: 	 exit of cryptopass.
	 h: 	     help please!
	 logout: logout user session.
	 np: 	 New password entry.
	 p: 	     Get a password for a given label.
	 p?: 	 Get a password for a given label. Copied to clipboard only.
	 time: 	 Calculate encryptio-decryption performance.
	 wd: 	 Print path of working directory.
```
### new entry
Lot of interesting things to do, but I just want to store my firs password. 
To do that, type _np_ and press enter:

```
	 New password entry: 

label = 
```
Next steps **cryptopass** ask for fields' information. You can save only what you want (there are not mandatory fields).
```
label = gmail
user = ElonM1971
email = ElonM1971@gmail.com
password = univ3rs3Conqu3r0r
url = www.gmail.com
hint = no clues
notes = just testing!
@ElonM> password: 
```
Note the difference between _password_ and _@ElonM> password:_. The first password is just information (to be encrypted), but last password requested is the one used for encryption, so, all this entry's information is encrypted using _cryptopass user_ and this _last password_ (cryptopass password).

_Note: you can use several cryptopass passwords for different entries with same cryptopass username, but you won't can decrypt all at the same time._
Just type your **hyper secret cryptopass password** (SpaceZ, for example) and press enter (the password is not printed in console). Now your entry was stored in your pass database.

### reading entries
To read the entry that store your _gmail_ password and you have loaded using the password _SpaceZ_:

```
@ElonM> enter crypto command (press h for help): p
	 get the password for a label: 

@ElonM> label: gmail
@ElonM> password: 
              user           password            date_time
ElonM#0  ElonM1971  univ3rs3Conqu3r0r  2018-02-08-18:52:32
	 password copied to clipboard!
```
The extra functionality is that the password is automatically copied to the clipboard.

If you don't want that cryptopass print your **hyper secret gmail password** use _p?_ command instead of _p_.

### logout
To logout of your user session of cryptopass just enter the _logout_ command, so:
```
@ElonM> enter crypto command (press h for help): logout
	 logging out... bye ElonM
```

### exit
To exit of cryptopass just enter the _end_ command (you can do this logged in or not), so:
```
> enter console command (press h for help): end
	 chau
```


## Files
Cryptopass works using 3 files:
1. ./**cryptopass.json**
    Created in installation folder, and it is used for initialize cryptopass.
2. _working dir_/**default.udb**
    Created in the working directory you've defined (default is ./database/),
    and it is used to store user information. 
    You can change the file that cryptopass read to load user information. 
    You can use the name you want for this one.
3. _working dir_/**default.pdb**
    Created in the working directory you've defined (default is ./database/),
    and it is used to store encrypted information (entries). 
    You can change the file that cryptopass read to load encrypted information. 
    You can use the name you want for this one.
    
You can manage *.udb and *.pdb you want, but it's recommended that a pair udb and 
pdb file was stored in the same working directory. If you want to copy those to 
another computer, just carry both with you.

Several _cryptopass passwords_ can be used for each _cryptopass user_,
and several _cryptopass users_ can share the same udb and pdb files with no security issues.



