# age-group-prediction
Age Group Prediction for Catalan Twitter users based on their following list.

## Prerequisites

 - Python 2.7
 - git
 - pip
 - virtualenv

## Installation

    git clone https://github.com/eMOVIX/age-group-prediction.git
    cd age-group-prediction
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Configuration

Add your database configuration to the configuration file:

    vim config.json

## Step 0

Filter the "ca_twitterStatus" collection:

```
db.ca_twitterStatus.find({"language_detections.language": "ca", "language_detections.isReliable": true}, {_id: 0, id: 1, created_at: 1, timestamp_ms: 1, text: 1, "coordinates.0": 1, "coordinates.1": 1, "place.full_name": 1, "place.name": 1, "user.id": 1, "user.lang":1, "user.screen_name": 1, "user.friends_count": 1, "user.followers_count": 1, "user.location": 1, "user.source": 1})
```

## Step 1

Source TSV file ("ca_twitterStatus.tsv"): https://figshare.com/s/d53c14092b5603e7f091


## Step 2

R Script (generated with Exploratory):

```
# Set libPaths.
.libPaths("/Users/jordi/.exploratory/R/3.3")

# Load required packages.
library(lubridate)
library(tidyr)
library(urltools)
library(stringr)
library(readr)
library(broom)
library(RcppRoll)
library(tibble)
library(dplyr)
library(exploratory)

# Data Analysis Steps
read_delim("/Users/jordi/ca_twitterStatus.tsv" , "\t", quote = "\"", skip = 0 , col_names = TRUE , na = c("","NA"), n_max=-1 , locale=locale(encoding = "UTF-8", decimal_mark = ".") , progress = FALSE) %>%
  exploratory::clean_data_frame() %>%
  filter(user.lang == "ca") %>%
  distinct(user.screen_name) %>%
  arrange(user.screen_name)
```

## Step 3

Catalan Users ("ca_users.csv"): https://figshare.com/s/d8dc6bed26fc5f0d34d0

## Step 4

Fet followers/ids for each user.

## Step 5

Get the most common ids (500?)

## Step 6

Get the full information for each of the most common Twitter accounts.

## Step 7

Classify each account into one or more groups: Sports, Politics, Music, Media, 
