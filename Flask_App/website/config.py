import json
import os

class Config:
    CONFIG_DIR = 'configs'
    
    @staticmethod
    def load_channel_config(channel_name):
        with open(os.path.join(Config.CONFIG_DIR, f'{channel_name}.json'), 'r') as file:
            return json.load(file)
    
    @staticmethod
    def save_channel_config(channel_name, config):
        with open(os.path.join(Config.CONFIG_DIR, f'{channel_name}.json'), 'w') as file:
            json.dump(config, file, indent=4)

    video_path = "Your video path"
    description_file_path = "Your file descript path, txt btw"

    instagram_cookies_file = "instagram_cookies.pkl"
    tiktok_cookies_file = "tiktok_cookies.pkl"
    youtube_cookies_file = "youtube_cookies.pkl"
    
    x_cookies_file = "x_cookies.pkl"
    linkedin_cookies_file = "linkedin_cookies.pkl"

    youtube_account_name = "Clips Master"

    snapchat_username = "ur_snap_username"
    snapchat_password = "ur_snap_password"
    instagram_username = "ur_insta_username"
    instagram_password = "ur_insta_username"
    tiktok_username = "ur_tiktok_username"
    tiktok_password = "ur_tiktok_username"
    youtube_email = "gostrika11@gmail.com"
    youtube_password = "God1salwaysfirst"

    x_email = "ur_x_email"
    x_password = "ur_x_password"
    linkedin_email = "ur_linkedin_email"
    linkedin_password = "ur_linkedin_email"
