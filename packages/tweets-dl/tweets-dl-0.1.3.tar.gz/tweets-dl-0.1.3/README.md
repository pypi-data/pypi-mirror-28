## tweets-dl

Python script to download tweets for a given twitter handle or multiple twitter handles. It returns the tweets in csv format.

### Installing

    pip install tweets-dl

### Running the Script

Run the following command in command line. Replace twitter_user_* by the official twitter handle of the user whose tweets need to be downloaded. You can specify any number of user names separated by space. If you do not specify a csv filename, the tweets will be saved in a file tweets.csv.


    tweets-dl filename.csv twitter_user_1 twitter_user_2

### Caveat

A word of caution if using the default key and secret; one might experience "rate limit exceeded" by Twitter upon simultaneous usage. In that case, get your consumer key and consumer secret from Twitter by following these steps:

    Go to https://apps.twitter.com/app/new
    Fill in the details of the application to connect with the API
    Click on Create your Twitter application
    Details of your new app will be shown along with your consumer key and consumer secret
    Save the key and secret.


### Running the script with your consumer key and secret

    tweets-dl --key <your_key_from_twitter> --secret <your_secret_from_twitter> filename.csv twitter_user_1 twitter_user_2 twitter_user_n

### Author

    Vaishali Garg

### License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Vaishali-Garg/tweet-downloader/blob/master/LICENSE) file for details
