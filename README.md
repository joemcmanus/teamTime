# teamTime
----

teamTime is a tool to aid the problem of keeping track of time for a globally distributed team. 

You will need to put the name of your teammates in staff.csv using the format name, timezone, city. Take a look at https://raw.githubusercontent.com/joemcmanus/teamTime/master/example.csv

    Alice,US/Eastern,New York New York
    Bob,US/Central,Chicago Illinois
    Charlie,Africa/Abidjan, Abidjan
    Doug,America/Tijuana, Tijuana Mexico
    Ed,America/Winnipeg, Winnipeg
    Frank,Asia/Dubai,Dubai

Questions/Feedback/Feature Requests? Please let me know. 

#Installation 
----
The simplest way to install teamtime is to use the snap

    sudo snap install teamtime 

As a note if you are using the snap to avoid typing the path to the CSV file you might want to make an alias: 

    alias teamtime='teamtime --src=/home/foo/staff.csv'


Otherwise clone the repo and install the dependencies pandas, plotly, prettytable and geopy. 

# Usage 
----

    ./teamTime.py --help 
    usage: teamTime.py [-h] [--name NAME] [--src SRC] [--map]
    
    Time Table
    
    optional arguments:
      -h, --help   show this help message and exit
      --name NAME  Optional name to search for
      --src SRC    Optional src file, defaults to staff.csv
      --map        Draw map	

To simply print a table of your team run ./teamTime.py

    +---------+------------------+
    |  Person |    Local Time    |
    +---------+------------------+
    |  Alice  | 2019-09-25 12:16 |
    |   Bob   | 2019-09-25 11:16 |
    | Charlie | 2019-09-25 16:16 |
    |   Doug  | 2019-09-25 09:17 |
    |    Ed   | 2019-09-25 11:17 |
    |  Frank  | 2019-09-25 20:17 |
    |  now()  | 2019-09-25 10:16 |
    +---------+------------------+

To search for just Bob run ./teamTime.py --name=Bob

    +--------+------------------+
    | Person |    Local Time    |
    +--------+------------------+
    | Bob    | 2019-10-02 15:37 |
    +--------+------------------+

To create a map run ./teamTime.py --map 

![alt_tag](https://github.com/joemcmanus/teamTime/blob/master/map.png)


      
