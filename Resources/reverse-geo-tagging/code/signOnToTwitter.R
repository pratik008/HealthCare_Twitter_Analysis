#
# sign on to Twitter with R
# see the setup instructions in "Instructions for r.pdf"
#

library("httr")
library(twitteR)
API_Key=" "
API_Secret=" "
accessToken=" "
accessSecret=" "

setup_twitter_oauth(API_Key, API_Secret, accessToken, accessSecret)

rm(API_Key,API_Secret,accessToken,accessSecret) # don't leave them in the workspace

## example of searching for tweets online
#
# tweets <- searchTwitter('#beer', n=50)
# head(tweets)
#