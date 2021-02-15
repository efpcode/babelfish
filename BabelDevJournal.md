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
:astonished:. The reason new IKEA furniture needs to assembled.

#### thanks for the read and cya again on 19-feb.



