Note: As of 10/13 I asked in the snapcraft forum to have the ownership of the snap changed to joesecurity . Thanks for checking roadmr.

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

# Installation
----

## Snap
To install teamTime as a snap, type:

    sudo snap install teamtime

## pip

To install teamTime with pip, type:

	pip install teamtime

## To install and run from source

Install the requirements:

	pip install -r requirements.txt
	python -m teamtime.teamtime

## Note

To avoid typing the path to the CSV file you might want to make an alias:

    alias teamtime='teamtime --src=/home/foo/staff.csv'


# Usage
----

    teamtime --help
    usage: teamtime [-h] [--name NAME] [--src SRC] [--map]

    Time Table

    optional arguments:
      -h, --help   show this help message and exit
      --name NAME  Optional name to search for
      --comp COMP  Compare times, use --name and --comp together
      --src SRC    Optional src file, defaults to staff.csv
      --map        Draw map	

To simply print a table of your team run `teamtime`

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

To search for just Bob run `teamtime --name=Bob`

    +--------+------------------+
    | Person |    Local Time    |
    +--------+------------------+
    | Bob    | 2019-10-02 15:37 |
    +--------+------------------+

To convert a local time to another time in a person's time zone use --comp. This helps when you are trying to figure out when to schedule a call.

    $ teamtime --name=andy --comp=15:00
    +--------+------------------+---------------------+
    | Person |    Their Time    |      Your Time      |
    +--------+------------------+---------------------+
    |  Andy  | 2019-10-18 07:30 | 2019-10-17 15:00:00 |
    +--------+------------------+---------------------+

To create a map run `teamtime --map`

![alt_tag](https://github.com/joemcmanus/teamTime/blob/master/map.png)
