# naver-real-estate

## Brief Description
This repository is to get information from the Naver Real Estate website based on each identification number of housing complexes.

## Background
The information on the website is easy to use as it allows a map-based user interface. However, when user wants to check lots of data for multiple housing complexes, especially when you want to find a sudden, quickly-disappearing property--that is usually the cheapest one, the website does not offer much of convenience to users. There comes this set of codes to quickly sweep through the lists of complexes to find the ones that meet user's condition.

## Organization
1. functions.py: contains most of the functions
2. telegram.py: functions to send a message to the IDs of your choice through your telegram bot
3. watch_list.py: a collection (lists) of complexes that you would want to sweep through
4. naver_re_scrape.py: the main file to run all the codes

## Preparation
1. Create config.py within the folder
    -> Set up a Telegram bot (there are plenty of tutorials for this.) Put tokens and chat id information in config.py
2. Complexes of your interest
    -> Put complex information in the watch_list.py; you can find this information in the development mode within your browser in the website
3. Set options
    -> naver_re_scrape.py accepts conditions (parameters) of your taste

Now run the program.

This is still a work in progress.

## Reference
<https://github.com/inasie/inasie.github.io/blob/master/_posts/2018-11-24-%EB%84%A4%EC%9D%B4%EB%B2%84-%EB%B6%80%EB%8F%99%EC%82%B0-%ED%81%AC%EB%A1%A4%EB%A7%81.md>
