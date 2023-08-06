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

## baby steps
### creating users
When you run **cryptopass** in the console:

```
Cryptopass - version 0.0.9
OK database file: ./database/users_db.dat

> cryptopass user:
```
```
	 User "ElonM" has not been found!
	 Do you want create new user? [y/n]: 
```
Cryptopass user is your *session name*. You will access to database for that session. You can have a lot of users. Database for users will be checked to know if the username exist, if not you will can create new one.

```
	 Creating new user...
	 if database left clear, it will be: ./database/pass_db.dat

database = 
notes = examples
	 done!
```
The _database_ is requested here is the filename for the encrypted database which will store your information. This database can be shared by users (different session names), and a user can save information (entries) below different _cryptopass passwords_ (passwords to decrypt entries).

### login
If your username is already load, you will see:

```
OK database file: ./database/pass_db.dat

> enter crypto command (press h for help):
```

   
Time for **crypto command**. That's the way you have to put cryptopass in action.
If you press h for help:

```
	 crypto commands: 

	 all: 	show all valid entries for user/password.
	 All: 	show all valid entries for user/password. (detailed)
	 all: 	show all valid entries HINTS for user/password.
	 dbg: 	execute debug script (just for developing).
	 end: 	exit cryptopass application.
	 h: 	help please!
	 np: 	New password entry.
	 p: 	Get a password for a given label.
	 p?: 	Get a password for a given label. Copied to clipboard only.
	 time: 	Calculate encryptio-decryption performance.
	 wd: 	Print path of working directory.
```
### new entry
Lot of interesting things to do, but I just want to store my firs password. To do that, type _np_ and press enter:

```
	 New password entry: 

label = 
```
Next steps **cryptopass** ask for fields' information. You can save only what you want (there are not mandatory fields).
```
label = gmail
user = ElonM1971
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
> enter crypto command (press h for help): p
	 get the password for a label: 

@ElonM> label: gmail
@ElonM> password: 
                  password            date_time
ElonM#0  univ3rs3Conqu3r0r  2018-02-06-20:16:57
	 password copied to clipboard!
```
The extra functionality is that the password is automatically copied to the clipboard.

If you don't want that cryptopass print your **hyper secret gmail password** use _p?_ command instead of _p_.

### exit
To exit of cryptopass just enter the _end_ command, so:

```
> enter crypto command (press h for help): end
	 chau
```








