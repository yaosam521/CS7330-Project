# CS7330-Project

## Getting Started:
### Running the Virtual Environment
1. Type 'pip install virtualenv' to install virtualenvironment
2. Navigate to the directory in which you want to place your environment
3. DO NOT PUSH the venv into the github. Put it in a .gitignore.
4. To create a venv, type 'python -m venv name_of_venv'
5. to activate the venv, type 'name_of_venv\Scripts\activate.bat' for windows, and 'source name_of_venv/bin/activate' for MacOS
6. Once the venv is activated, you should notice that the terminal should have a ("name_of_venv") at the front of the terminal line.
7. While inside the venv, type 'python install -r requirements.txt' 

### Running the Web App
1. Make sure the virtual environment is running
2. Navigate into the folder containing the project (in this case, 'sports_gui')
3. Type into the command line 'python manage.py runserver'
4. If the compilation is successful, follow this link: http://127.0.0.1:8000

## How to Use the Web App
### Home Page:
The first page you should land on is the homepage. There should be a navbar at the top with links to pages such as "Leagues, Date, Queries" etc.

All fields are mandatory unless stated otherwise.

Navigate to whichever tab you would like to get started.

### League Page
This page creates new leagues. When creating an entirely new league, you must have created teams first before inserting them into the league, otherwise, the league cannot be created.

Scroll down on the page to insert teams. Here, you'll have to input fields such as name, field, state, etc. to create the team.

If there are teams that you know you want to insert into a league, go ahead and create the league. Each league will have a commissioner, and you will have to put the name of the commissioner and their SSN into the system. 

Notice that creating a league will initialize the first season. You have the option to either automatically insert games, manually insert them, or to not insert any games at all for that season. You also get to create the rule sfor the season, meaning how many points a win is, a loss is, and how many points a draw is. Note that win > draw > loss, otherwise the input will not be accepted.

Manually creating the teams will mean that you will have to insert the date and the field that each and every possible combination of game is played at.

### Date
Here, you can change the current date. Notice that this will affect how you put in game results, as you can only enter game results for that day only. Additionally, You cannot change the date to go backwards (despite what Tame Impala sings, while it may feel like you only go backwards, you can only go forwards).

### Season
Create a Season for a League. The league in question has to exist in the database, otherwise it will return that there is no such league. Additionally, the new season cannot be in conflict with a season that the league is playing already. You must also place the number of games per day and the maximum number of games total. Finally, there is the option that you can manually create the games in the season.

### Move Teams
On this page, you can change teams from league to league. The team must exist, and it must exist in the league that you indicate. The league you wish to move this team to must also exist as well.

### Games
You can insert games into a season. If at the beginning of the league creation you chose not to insert any games, here's your chance to do so! Just like on all the other pages, you can insert the games into whichever league you desire. You must also know when the start and end dates of the season you want to insert games into. Just like in both the season and league menus where you have to insert games, you once again have the option to insert games into the season automatically or maually.

### Queries
You have the option to submit several queries to the database. You can find information about:
1. Leagues
   1. For leagues, you can find general information about the leagues, or you can find the champion of the league
2. Teams
   1. You can also find general team info and also the records for that team
3. Games
   1. You can find games played between two teams, and it will return which league these games were played in, and the game, the game date, and the score
4. Seasons
   1. Find information about a season of a league. You must know the exact start and end date about the season, otherwise it won't find it
5. Ratings
   1. Here, you can find the ratings for a league. Again, you must know the exact start and end date of the season.


## Future Changes