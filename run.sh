#!/bin/bash

# Place the folder location of the Clueless repo
clueloc="/Users/austinbrown/Documents/Foundations_of_Software_Engineering/Clue/"

start=1

# Number of clients to connect
clientNumber=3

echo "Starting CLUELESS..."

osascript -e 'tell app "Terminal"
    do script "'$clueloc'runServer.sh '$clueloc'"
end tell'

for (( index=$start; index<=$clientNumber; index++ ))
do
    osascript -e 'tell app "Terminal"
        do script "'$clueloc'runClient.sh '$index' '$clueloc'"
    end tell'
done

echo "Game Started..."