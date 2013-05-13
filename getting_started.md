Getting started with github
===========================

Forking the project
--------------------------------------------------

Assuming that you now have a github account, have access to a terminal window, and have git installed on your system (see https://class.coursera.org/datasci-001/wiki/view?page=GithubInstructions if not)

* Go to https://github.com/pratik008/HealthCare_Twitter_Analysis
* Click on the "Fork" button, at the top right of the screen. This will create a copy of the project attached to your account. That means that you can make as many changes as you want without any fear to mess up with the official/trusted repository. 
* Go to your github user page (click on your user icon) and select the HealthCare project from the repository list. For instance, my fork lives at: https://github.com/widged/HealthCare_Twitter_Analysis
Copy the github url to your clipboard. It shows in the text input box at the top of the page.  For mine, it is https://github.com/widged/HealthCare_Twitter_Analysis.git. Make sure you have selected the http option and that the url shows as https / read+write access (it should by default if you are logged in into your account).
* Go to your terminal window. Type 

```shell
git clone https://github.com/{your_github_id}/HealthCare_Twitter_Analysis.git
```

* Now, you should have a folder named "HealthCare_Twitter_Analysis" on your computer. Go to it, try and execute Tweepy.py (python Tweetpy.py). Install the tweepy library if not available yet (https://github.com/tweepy/tweepy/blob/master/INSTALL).  

Pulling in changes made to the official version
--------------------------------------------------

* To keep it in sync with the official projects, you have to add the official repository as a remote

```shell
git remote add pratik https://github.com/pratik008/HealthCare_Twitter_Analysis
```

Then at any time you will be able to run to pull in the changes not present in your local repository.

```shell
git fetch pratik
```

(it will do its best to "merge" the changes made in Patrik version into your current local version). The different between fetch and pull is explained there: http://stackoverflow.com/questions/292357/whats-the-difference-between-git-pull-and-git-fetch

Working on the code, locally
-------------------------------

Git can be used to keep track of the changes made to your file locally as well as remotely. If you end up making any change to the code files, it is good pratices to regularly commit (backup) the changes that you  have made. 

* Make a change to any file. For instance type "touch test.txt"
* Commit your changes, locally. 

```shell
git add .
git commit -a -m "comments describing your changes"
```

Making your changes public
--------------------------

* If you wish to share with the team, push your changes to github, so that they will be visible to others.

```shell
git push origin master
```

Contributing your changes to the official project
--------------------------------------------------

* If you think the official version is likely to benefit from your changes, submit a pull request. Don't worry too much about this for now. That can wait. Getting familiar with 1-8 is more important. If you are curious, you can find information there: https://help.github.com/articles/using-pull-requests


Resources
==========

See https://help.github.com/articles/fork-a-repo for step by step information of the forking process

Final Note
==========

That sounds like a lot of information, a lot of new things to absorb. Sure it is. But by experience, it doesn't take long to get a handle on this. The most difficult step is to find the courage to give it a shot. 

It really is a worthwhile investment. If you hope to one day get a job as part of a team involved in programming, then that's a must have skill. But even for your personal projects, source control makes a huge difference. Less stress. 