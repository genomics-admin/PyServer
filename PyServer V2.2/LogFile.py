#!/usr/bin/python
import os,sys


def filelog(fileName,IP,TS,searchString):
          lines="\n-----------\nRequested by : "+str(IP)+"\nTimeStamp : "+str(TS)+"\nSearch Value: "+searchString+"\n-----------\n"
          #---If file dont exist
          if os.path.isfile(fileName):
                    try:
                              f = open(fileName, "a+")
                              try:
                                        count = int(f.readlines()[-1])+1 # Read the count from the file
                                        print 'count'+str(count)
                                        f.writelines(lines+str(count)) # Write a sequence of strings to a file
                              finally:
                                        f.close()
                    except IOError:
                              print "Error Creating File"
                              return 0
                    
                    return count
          #---If file Exists
          else:
                    try:
                              f = open(fileName, "a+")
                              try:
                                        f.writelines(lines) # Write a sequence of strings to a file
                                        f.writelines('1') # Write a string to a file
                              finally:
                                        f.close()
                    except IOError:
                              print "Error Creating File"
                              return 0
                    
                    return 1

#homeDIR=str(os.path.dirname(os.path.realpath(sys.argv[0])))+'\\'
#filecount=filelog(homeDIR+"TestLog.txt","127.0.0.1","2015/03/24 09:12:33","stpuxa01,stpuxa05")
#print filecount
