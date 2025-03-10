from flask import Flask, request, render_template, redirect, url_for
import os
import json
import pickle

app = Flask(__name__)

CONFIG_DIR = 'configs'

def load_channels():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    channels = [f.replace('.json', '') for f in os.listdir(CONFIG_DIR) if f.endswith('.json')]
    return channels

def load_channel_config(channel_name):
    with open(os.path.join(CONFIG_DIR, f'{channel_name}.json'), 'r') as file:
        return json.load(file)

def save_channel_config(channel_name, config):
    with open(os.path.join(CONFIG_DIR, f'{channel_name}.json'), 'w') as file:
        json.dump(config, file, indent=4)

def save_cookies(channel_name, platform, cookies):
    cookies_file = os.path.join(CONFIG_DIR, f'{channel_name}_{platform}_cookies.pkl')
    with open(cookies_file, 'wb') as file:
        pickle.dump(cookies, file)

@app.route('/')
def index():
    channels = load_channels()
    return render_template('index.html', channels=channels)

@app.route('/add_channel', methods=['GET', 'POST'])
def add_channel():
    if request.method == 'POST':
        channel_name = request.form['channel_name']
        config = {
            'channel_name': channel_name,
            'photo': request.form.get('photo', 'default_photo.png'),
            'linked_accounts': []
        }
        save_channel_config(channel_name, config)
        return redirect(url_for('channel_home', channel_name=channel_name))
    return render_template('add_channel.html')

@app.route('/channel/<channel_name>')
def channel_home(channel_name):
    config = load_channel_config(channel_name)
    return render_template('channel_home.html', channel_name=channel_name, config=config)

@app.route('/channel/<channel_name>/add_linked_account', methods=['GET', 'POST'])
def add_linked_account(channel_name):
    if request.method == 'POST':
        platform = request.form['platform']
        username = request.form['username']
        password = request.form['password']
        config = load_channel_config(channel_name)
        config['linked_accounts'].append({
            'platform': platform,
            'username': username,
            'password': password
        })
        save_channel_config(channel_name, config)
        
        # Simulate cookie generation and saving
        cookies = {'dummy_cookie': 'value'}
        save_cookies(channel_name, platform, cookies)
        
        return render_template('cookies_generated.html', channel_name=channel_name)
    return render_template('add_linked_account.html', channel_name=channel_name)

@app.route('/channel/<channel_name>/upload', methods=['POST'])
def upload_video(channel_name):
    video_path = request.form['video_path']
    description = request.form['description']
    config = load_channel_config(channel_name)
    # Here you can call the upload functions for each linked account
    return redirect(url_for('channel_home', channel_name=channel_name))

if __name__ == "__main__":
    app.run(debug=True)
