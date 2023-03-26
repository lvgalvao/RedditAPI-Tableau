import pandas as pd
import datetime as dt

class RedditDataProcessor:
    def __init__(self):
        self.posts_df = None
        self.comments_df = None
        self.comments_posts_df = None

    def load_data(self, posts_path, comments_path):
        self.posts_df = pd.read_parquet(f'../RedditTableau/raw/{posts_path}_posts.parquet.gzip')
        self.comments_df = pd.read_parquet(f'../RedditTableau/raw/{comments_path}_comments.parquet.gzip')

    def process_data(self):
        self.posts_df['created_date'] = self.posts_df['created_utc'].apply(lambda x: dt.datetime.fromtimestamp(x))
        self.posts_df['created_year'] = self.posts_df['created_date'].dt.year

        # Merge posts with their comments
        self.comments_posts_df = self.posts_df.merge(self.comments_df, on='post_id', how='left')

        # Remove rows with missing comments
        self.comments_posts_df = self.comments_posts_df[~self.comments_posts_df['comment'].isnull()]

    def save_data(self, posts_output_path, comments_output_path):
        self.posts_df.to_csv(f'gold/{posts_output_path}_posts.csv', header=True, index=False)
        self.comments_posts_df.to_csv(f'gold/{comments_output_path}_posts_plus_comments.csv', header=True, index=False)

