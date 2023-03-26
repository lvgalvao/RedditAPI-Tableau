from RedditGet import RedditAPI
from RedditDataProcessor import RedditDataProcessor

response = RedditAPI()
processor = RedditDataProcessor()

if __name__ == "__main__":
    while True:
        subreddit = input("Enter the name of the subreddit you'd like to fetch data from (type 'exit' to quit): ")
        if subreddit.lower() == "exit":
            break
        posts = response.get_posts(subreddit)
        comments = response.get_comments(posts)
        processor.load_data(subreddit, subreddit)
        processor.process_data()
        processor.save_data(subreddit, subreddit)
