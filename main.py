#! /bin/python

# import required modules
from pandas import DataFrame
from datetime import datetime as dt
from sys import argv
from subprocess import check_output as run

# get the processes
txt = run('ps aux' , shell=True).decode()[:-1]

# some cleaning
rows = txt.split("\n")
for i in range(len(rows)):
    rows[i] = rows[i].split(maxsplit=10)

# create and clean the dataframe
df = DataFrame(rows[1:],columns=rows[0])
df["RSS"] = (df["RSS"].astype('float') / 1000).round(0)
df.columns = ["User" , "PID" , "%CPU" , "%RAM" , "VSZ" , "RAM(MB)" , "tty" , "Status" , "Start" , "Time" , "Command"]
df.index = df["PID"]
df.drop("PID" , axis=1 , inplace=True)

# save to csv
time = str(dt.now())
time = time[:time.find(".")].replace(" " , "_")
df.to_csv(f'/opt/process_sorter/{time}.csv')

if len(argv) > 1:
    # get parameters
    print("How many of the first rows do you want?")
    n = int(input())
    print('''How do you want to sort the columns?
        RAM(1) or CPU(2)?''')
    by = int(input())
    by = ["%RAM" , "%CPU"][by-1]

    # sort and print
    sorted = df.sort_values(by=by , ascending=False).head(n)
    print(sorted)
