import praw
import pandas as pd
import os

from config import client_id, client_secret, user_agent

# Initialize the PRAW Reddit API Wrapper
class RedditAPI():

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://localhost:8080",
            user_agent=user_agent
            )


    def fetch_data(self, subreddit_name, post_limit=10):
        subreddit = self.reddit.subreddit(subreddit_name)
        return [submission for submission in subreddit.top(time_filter="all", limit=post_limit)]

    def get_posts(self, message):
        self.subreddit_name = message.strip().lower()
        try:
            posts = self.fetch_data(self.subreddit_name)
            # response = f"Here are the top {len(posts)} posts from r/{subreddit_name}:\n"
            posts_list = []
            for idx, post in enumerate(posts):
                posts_list.append({'post_id': post.id,
                                'subreddit':str(post.subreddit),
                                'created_utc': post.created_utc,
                                'selftext': post.selftext,
                                'post_url': post.url,
                                'post_title': post.title,
                                'score':post.score,
                                'num_comments': post.num_comments,
                                'upvote_ratio': post.upvote_ratio
                                })
            posts_df = pd.DataFrame(posts_list)
        except Exception as e:
            return f"Sorry, I couldn't fetch data from r/{self.subreddit_name}. Please try another subreddit."
        
        target_directory = '../RedditTableau/raw'
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        posts_df.to_parquet(f'{target_directory}/{self.subreddit_name}_posts.parquet.gzip', compression='gzip')
        return posts_df
    
    def get_comments(self, posts_df):
        comments_list = []
        for post_id in posts_df['post_id']:
            submission = self.reddit.submission(post_id)
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                comments_list.append({'post_id': post_id, 'comment': comment.body})
        
        target_directory = '../RedditTableau/raw'
        comments_df = pd.DataFrame(comments_list)
        comments_df.to_parquet(f'{target_directory}/{self.subreddit_name}_comments.parquet.gzip', compression='gzip')
        return comments_df
    
if __name__ == "__main__":
    chatbot = RedditAPI()

    while True:
        message = input("Enter the name of the subreddit you'd like to fetch data from (type 'exit' to quit): ")
        if message.lower() == "exit":
            break
        response = chatbot.chatbot_response(message)
        print(response)