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
* DB schema for language code. 

## If I have time :hourglass: 
* BabelDB._width_calculator : needs to be rewritten, since column width
	is not constant resulting in on even lines :screams:!Code will be
	changed to be more dynamic by: get longest word (in characters) for
	each column and then add spacer. 

#### thanks for the read.
