# Data Generator with Real Twitter Data
This directory containes a data generator that connects to the live Twitter stream, collects tweets and saves them to a file as described in the coding challenge directions.  

In order to use it, you will need to have a Twitter account, then obtain Twitter OAuth credentials from [apps.twitter.com](http://apps.twitter.com) as described [here](https://www.youtube.com/watch?v=j8KqeBGlWec&index=38&list=PLAwxTw4SYaPnWVpbkeoLu7WwI0JIiuXhT).  Then place these credentials in a file named '.twitter', matching the JSON format of the included '.twitter-example'. This '.twitter' file must be placed in the same directory as the 'tweet-cleaner.py' script.

To begin collecting data, simply 'cd' to the directory containing the 'data-gen' directory from the Terminal, and run the command 'python data-gen/get-tweets.py'.  This will begin collecting data and storing it in a newly created file named 'tweets.txt'.
