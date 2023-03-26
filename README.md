# Reddit Data Pipeline and Visualization Project

This project is a data pipeline that fetches data from the Reddit API, performs data transformations, and generates CSV files for further analysis and visualization using Tableau. The pipeline is structured into three main Python files: `main.py`, `RedditGet.py`, and `RedditDataProcessor.py`.

## Architeture

![Pipeline](/assets/pipeline.png "Pipeline")


assets/pipeline.png

## Overview
- RedditGet.py: Fetches posts and comments data from a specified subreddit using the Reddit API (PRAW).
- RedditDataProcessor.py: Performs data transformations and preprocessing to make the data ready for analysis and visualization.
- main.py: Orchestrates the entire process by calling the appropriate functions from the other two files and handling user input.