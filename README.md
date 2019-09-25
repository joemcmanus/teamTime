# teamTime
----

Team Time is a tool to aid solve the problem of keeping track of time of a globably distributed team. 

You will need to put the name of your teammates in staff.csv using the format name, timezone, city . 

Questions/Feedback/Feature Requests? Please let me know. 

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


To create a map run ./teamTime.py --map 

![alt_tag](https://github.com/joemcmanus/teamTime/blob/master/map.png)


      
