# Hello World!
## Date: 2021-Feb-11
This is the 'dev' journal, where I plaster my thoughts regarding
'babelfish' project.

## Todo List:
1. Publish current code base to 'babelDev' branch. 
2. Comment on the code. 

## Code comments :boom:

Adding new module called babeldb that will replace and deprecate most
lines of code in babelconfy. No need of storing password in cfg-file, if
the same can be accomplished by db module in a database.

## Needs to be done :cold_sweat:
* Response-parser from client i.e. get translation out of json-object. 
* Create validation of username and password. Maybe use a namedtuple
	from 'collections' :thinking:. 
* DB schema for language codes. 

## If I have time :hourglass: 
* BabelDB._width_calculator : needs to be rewritten, since column width
	is not constant resulting in on even lines :scream:!Code will be
	changed to be more dynamic by: get longest word (in characters) for
	each column and then add spacer. 

#### thanks for the read.


# No parsing today :flushed:
## Date: 2021-Feb-12

## Todo List
* json to sql schema this is needed for languages registry. 
* Need to work on a better parser for language codes. Too many
	for-loops, too costly and ugly :see_no_evil: 
* Documentation of code base needs to go up!
* Test implementation needs be more prioritized. Always try to keep your
	technical debt low. 

## What was accomplished :metal:
* Crushed a :bug: in class BabelBD.db_connect property, 
	code base failed at lines 75 - 77 because table was missing.
* Added a new module called 'babellancode.py', this will be dependent on
	classes BabelClient.api_get_response and whatever I call the table
	creation method in class BabelDB.method for language code.

## Unforeseen event :bomb:!
* Pycharm virtual environment stopped working after updating macports.
	Haven't figured out why, yet! 

#### thanks for the read!

# All your builds :hammer: are belong to us! 
### Date: 2021-02-15
Hello again,
I need to confess that I have not code today on the project
:astonished:. The reason new IKEA furniture needs to be assembled.

#### thanks for the read and cya again on 19-feb.

# Guess who back!:grimacing:
### 2021-March-01 
Hello Babeler,
Latest confession, I've been parsing strings and making life difficult,
also crushed some bugs.

## What was accomplished :star: !
1. Assembled a ton of Ikea furniture, also snapped a bolt in half something
   about me and concrete don't get all long :grin:!

2. Created a parser for language registry that converts a encoded utf8
   response to Json object. 

3. Created mockdata method for dev reasons in babeldb.py

4. 'Finished' pptable method or at least now column width is constant as
   it should.

5. Learned more about defaultdict from collections module.

6. BabelFiler class got two new static methods called 'create_json'and 'read_json' (see babelfiler.py)

## What could be improved :see_no_evil: .
* The parser converter in babellangcode.py it's far from optimal a
	double nested for-loop is never a good answer or memory efficient.
	Need to see if there's an algorithm for parsing. Or something in the
	itertools module that could do this smarter. 

* The BabelDB.pptable is not optimal right now, SQL-querry does a fetchall (yet
	another snail), which will kill memory if the db becomes
	big. The code there is not scalable, but I think we can fix this
	with OFFSET and little math, question the internet about it. 

## What's in the pipeline :wrench: .
* Convert Json-object to SQL, either by generator or go the easy route
	of adding a new dependency with Pandas.

* Create db.get_value or db.get_cells, a getter method.
* Create db.update or db.setcell, a setter method.

* Creating a user login data validator and hasher. I will use 're'
	module to do a re.fullmatch for input of user and hashed data from
	db. 

* Plan for CLI, this is the tricky part need to visualize the
	interaction, before coding that part. 

#### thanks for the read!

# Two for one!:grimacing:
### 2021-March-07 
Hello again, 
the week has been kind of rough.. but some bugs were found and killed
(hopefully!).

I decided to create my own json to sql route, this might give some
valuable insights. 

## What was accomplished :star: !
1. BabelLangCode class had a minor update to the lang_columns
   property, the idea was to have an easy why to get all the unique
   columns found in the Json object. So to make sure of that I used a
   set data structure which by default removes duplicates.

2. BabelLangCode._str_parser was updated to catch a very special case.
   Line that contain an extra colon mid sentence. 

3. New methods added to BabelDB: json\_to\_tuples conversion from Json object to 
tuple so insertion of data with SQLite3 is working, create\_langcode\_table 
creates schema for langcode table, jsondata\_filtered filters with the Type 
field set to 'language'.

## What could be improved :see_no_evil: .
* Need to get more coding in my life.
* Need to add Kanban board (trello, or other system).
* Need to ask the python-community about repeating yourself, when
	dealing with creation of table to uphold parameterization and avoid
	sql injections. 
* Need to test more!


## What's in the pipeline :wrench: .
* Continue with BabelDB todo list: get data, update value, delete value
	and lastly rollback.
* Code for password hasher
* Ask the community about do not repeat issue. 
#### thanks for the read!

# Added some 'hash':es to my code:grimacing:
### 2021-March-09 
## General Rambles of Mad hErmit.
Hello Again, 
Code is funny sometimes, you get the sense that a problem is rather easy
until you actually try it out. This happened with my hash function for
passwords, it was alienating and a bit daunting.

First mistake was to pick good hash algorithm, apparently there's not
only md5, sha256 and other letters scrabbled with digits. Turns out that
the combination letters and digits had a purpose and the wrongly applied
function could lead to an insecure mess.

So surfed the web for an answer and found the argon2 module and hashlib.blake2b 
function.

Hypothesis: if hashing once is secure, hashing twice with different
algorithm should be better?

Interaction:
User types passwords -> hashed in blake2b with salt of n=16 bytes ->
hashed_result is then hashed again with argon2.

Salt was created with the secretes.token_bytes function.

Database will contain both salt, argon2 hashed password. 

## Why hash twice? 
First round hashing is to create a bit more entropy for bad passwords.
Second round hashing is to create cost and security. Argon2 hashing was
intended to be a bit costly for force brute attacks. Also, it was
designed for the purpose of hashing passwords. 

## BTW
Added a Kanban board to the project [link](https://trello.com/b/HcC44A6F/babelfish)

## What was accomplished :star: !
* New module called babeluser with class UserData.
* Minor fixes of hint typing and under and over indention code.
* One, sick Kanban board.
* Gain new respect for cryptography, (I thought a knew something.)

## What could be improved :see_no_evil: .
* Validation model of user, it's half baked at the minute. 
* General Documentation of classes.
* Test coverage. 

## What's in the pipeline :hammer:?
* User Validation model.
* (Maybe) an encryption of the other data in db like email, username
	etc..
* Think about command line interface.
* Design UnitTest or add pytest to project.
#### thanks for the read!

# Spring Break/Clean Code 
### 2021-March-25 
## A tangled mess, simplified :raise_hands:!
Hello there, 
Ohh.. mee I've been working with something behind the curtain for some
time now, hence my hiatus in git commits and blog post updates.


## What was accomplished :star: !
* New UML model for the project.
* A new branch in git titled DevRefactor
* A simplification of project scope that removed the necessity of
	hashing and storing user information.

## What could be improved :see_no_evil: .
* Over design is not good design, think simple and have a user centric
	view about the project.
* General Documentation of classes.
* Test coverage. 

## What's in the pipeline :hammer:?
* Refactor the whole code base to reflect the new UML model.
* Update UML if needed.
* Think about command line interface.
* Design UnitTest or add pytest to project.

## BTW
Added the new UML model of the project here in card '# New UML Model for Project' -> [link](https://trello.com/b/HcC44A6F/babelfish)

#### thanks for the read!

