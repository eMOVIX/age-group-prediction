# age-group-prediction
Age Group Prediction for Catalan Twitter users based on their following list.


Source TSV file ("ca_twitterStatus.tsv"): https://figshare.com/s/d53c14092b5603e7f091

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

Catalan Users ("ca_users.csv"): https://figshare.com/s/d8dc6bed26fc5f0d34d0
