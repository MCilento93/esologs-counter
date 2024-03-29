#  ESOlogs-counter
This project aims to develop a software infrastructure to handle the *history of esologs* (retrieved by [esologs.com](https://www.esologs.com)) in a Elder Scrolls Online guild/community. In less words, its main purpose is to **account for every user the number of trials closed succesfully**. In this way, guild masters may have an useful tool to organize guild roles and check unactive users.

The project is supposed to be implemented only for a *local guild*: large scale deployments are not planned yet. If you want to use this software for your guilds, clone the project and autenticate to your google sheet as reported [here](https://docs.gspread.org/en/latest/oauth2.html) following 'Service Account' procedure.

Its raw architecture is herebelow sketched:
* Routines that scrape strings in order to find **valid esologs.com urls**
* Google sheet database via [gspread](https://docs.gspread.org/en/latest/index.html) to store the output of the scrape
* A discord bot that constantly keeps an eye on the eso-logs discord chat for new logs to scrape

## Vocabulary
With reference to the game:
| <!-- -->     	| <!-- -->                                                                                                             	|
|--------------	|----------------------------------------------------------------------------------------------------------------------	|
| Zone         	| trial zone as reported on the game map                                                                               	|
| Fight        	| every pull classified according to esologs.com. Type 'trash' is neglected, type 'boss' is taken for further analysis 	|
| Trial closed 	| a Fight with `last_pull_kill=True` (final boss defeated)                                                             	|

With reference to esologs.com:
| <!-- --> 	| <!-- -->                                                                                               	|
|----------	|--------------------------------------------------------------------------------------------------------	|
| Friendly 	| either human or not human appearing in the log. Anonimous Friendly are neglected for further processes 	|
| Owner    	| the account name of the one that loaded the log on esologs.com                                         	|
| code     	| the alphanumerical end section of the esolog url and unique identifier                                 	|

With reference to this project:
| <!-- -->      	| <!-- -->                                                                                                            	|
|---------------	|---------------------------------------------------------------------------------------------------------------------	|
| Attendee      	| each human friendly appearing in the log. For being considered attendee, the trial has not to be necessarly closed. 	|
| Winner        	| An attendee that closed a trial                                                                                     	|
| Success rate  	| % of logs in which an attendee has closed with success at least a trial                            	|
| Rank database 	| a big table of the database containing the number of attendances for every trial analyzed in the processed logs     	|
| Log database  	| a big table containing information on all logs analyzed or not yet                                                 	|

## Commands
### Software
* To **analyze and calculate the logs** from a file containing valid esologs urls (without any query to databases):
```
:: If a txt holds the link, run in the project folder
python main.py analyze_logs_from_file txt/local.txt
```
* To scrape a local file, collect and **send valid esologs urls** to the log-database:
```
:: If a txt holds the link, run in the project folder
python main.py load_logs_from_file txt/local.txt
```
* To **update the rank-database** with the calculation of logs stored on the logs-database:
```
:: Run in the project folder
python main.py process_logs
```
* To **run discord bot** whose task is to listen in a given chat:
```
:: Run in the project folder
python main.py discord
```

### Tips on the software usage
It is highly recommended to store the console output when dealing with many historical logs. Check the log files as well.
```
python main.py analyze_logs_from_file txt/local.txt > txt/output.txt
python main.py load_logs_from_file txt/local.txt > txt/output.txt
python main.py process_logs > txt/output.txt
python main.py discord > txt/output.txt
```
Console output can be really helpful when dealing with high number of logs, since google API has limited number of requests (60 requests/min) and the process may take a while.

## Google sheet
The database is hosted on a google sheet (spreadsheet). Only one copy of the spreadsheet is valid and contains the updated database.
The software works only on two worksheet, respectively named **logs** and **rank**. One can add worksheets to the spreadsheet using different names, without affecting at all the computation.<br>
<br>With regards to the **logs** database:
* One must not change name of the header (i.e. first row with the title of the different columns)
* One must not change the order of columns
* One must not leave holes in both 1st column/row of the spreadsheet
* Only the logs marked as 'N' in the *processed* column will be calculated (when proper command is invoked). You can change the value to something else in order to store the logs without add their attendances in the current version of the rank database. The *processed* will be marked 'Y' if log outcomes have been added to rank database
* The *status* column will report the number of trials closed (if any)<br>
* It is not recommended to delete the *attendees* column (it will not be updated after the loading of new logs)

<br>With regards to the **rank** database:
* One must not change name of the header (i.e. first row with the title of the different columns)
* One must not leave holes in both 1st column/row of the spreadsheet
* It is recommended to highlight the columns containing formulas (i.e. column based on editable equations on their cells), to avoid confusion with columns where the software actually reads/writes. A good practice can be to mark borders only of editable columns
* One can add columns wherever and even change their order
* The blank row can be deleted if not necessary
* You can reset the worksheet deleting all the columns written by the software and invoking again the process procedure only on desired logs (i.e. those whose processed status is set to 'N')

## Discord
* **/help**: gather general information on the bot usage
* **/show_rank**: show the rank of the guild, sorted by number of attendances
* **/process_logs**: process the unprocessed logs in the database (i.e. **only** those marked as 'N' in *processed* column). This will invoke an irreversible calculation. Be careful when using. For this reason, this command can be invoked only by developer and guild master.

## License
This repository is licensed under [MIT License](LICENSE) (c) 2024 GitHub, Inc.