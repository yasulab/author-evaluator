#!/bin/sh
if [ $# -eq 3 ]
then
    printf "Getting recent tweets by %s... " $1
    python ./simple-tag-getter/tag-getter.py http://twitter.com/$1 span class=entry-content > tweets-by-$1.txt
    printf "Done.\n"
    
    printf "Translating the tweets into English... "
    python ./ja2en/api-translator.py tweets-by-$1.txt ja2en > tweets-by-$1_en.txt
    printf "Done.\n"
    
    printf "Getting %s's %s list... " $2 $3
    python ./simple-tag-getter/tag-getter.py http://twitter.com/$2/$3 span class=entry-content > $2-$3-list.txt
    printf "Done.\n"
    
    printf "Translating the tweets into English... "
    python ./ja2en/api-translator.py $2-$3-list.txt ja2en > $2-$3-list_en.txt
    printf "Done.\n"
    
    printf "Generating the interesting tweet ranking for %s... \n\n" $1
    sleep 5
    python scoring-tweets.py tweets-by-$1_en.txt $2-$3-list_en.txt
    printf "Done.\n"
else
    echo "Usage: main.sh TWITTER_ACCOUNT LIST_OWNER LIST_NAME"
    echo "Ex 1.: main.sh billgates  yasulab watch"
    echo "Ex 2.: main.sh yasulab yasulab watch"
fi
