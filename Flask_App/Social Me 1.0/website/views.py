from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, copy_current_request_context
from flask_login import login_required, current_user
import os, threading, time
import undetected_chromedriver as uc

from flask import  send_file

from werkzeug.utils import secure_filename
from flask import current_app

import json

from . import db
from .models import Account, Channel
from .cookie_extraction import login_to_instagram_and_save_cookies
from .cookie_extraction import login_to_tiktok_and_save_cookies
from .cookie_extraction import login_to_youtube_and_save_cookies
from .cookie_extraction import login_to_snapchat_and_save_cookies
from .cookie_extraction import login_to_x_and_save_cookies
from .cookie_extraction import login_to_linkedin_and_save_cookies

from .tiktok_upload import main as tiktok_upload
from .linkedin_upload import main as linkedin_upload
from .instagram_upload import main as instagram_upload
from .snapchat_upload_old import main as snapchat_upload
from .youtube_upload import main as youtube_upload
from .x_upload import main as x_upload

import yt_dlp
import re


from .srt import generate_srt
from.srdownload import download_media
from .sraudio import process_audio_file
channel_status_dict = {}

# 100 means sucessfuly upload
# 101 means unsucessful potentially fine upload
# 102 means unsucessful upload
# 103 means platform not selected

upload_status_dict = {}

process_status_dict = {}

views = Blueprint('views', __name__)

@views.route('/process_status/<user_id>')
def process_status(user_id):
    user_id = int(user_id)  # Convert channel_id to an integer
    if process_status_dict:
        status = process_status_dict.get(user_id)
    else:
        status = "nope"
    return jsonify({"status": status})

image_dict = {
    1: ("images/instagram.svg","instagram"),
    2: ("images/linkedin.svg", "linkedin"),
    3: ("images/snapchat.svg", "snapchat"),
    4: ("images/tiktok.svg", "tiktok"), 
    5: ("images/x.svg", "x"),
    6: ("images/youtube.svg", "youtube")
}

upload_functions = {
    1: instagram_upload,
    2: linkedin_upload,
    3: snapchat_upload,
    4: tiktok_upload,
    5: x_upload,
    6: youtube_upload
}

def download_file(file_path, custom_name=None):
    try:
        # Debugging: Log entry point
        print("Download function called")
        print(f"Original file path: {file_path}")
        print(f"Custom download name: {custom_name}")

        # Get base directory and adjust path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Base directory (current file's directory): {base_dir}")

        # Move up one level
        parent_dir = os.path.abspath(os.path.join(base_dir, os.pardir))
        print(f"Parent directory (one level up): {parent_dir}")

        # Adjust file path relative to parent directory
        adjusted_file_path = os.path.join(parent_dir, file_path)
        print(f"Adjusted file path: {adjusted_file_path}")

        # Check if the file exists at the adjusted path
        if not os.path.exists(adjusted_file_path):
            print(f"ERROR: File does not exist at {adjusted_file_path}")
            raise FileNotFoundError(f"File not found: {adjusted_file_path}")

        # Log before sending file
        print("File found. Preparing to send...")

        # Attempt to send the file
        return send_file(adjusted_file_path, as_attachment=True, download_name=custom_name)

    except FileNotFoundError as fnf_error:
        # Log specific error if file is missing
        print(f"FileNotFoundError: {fnf_error}")
        raise fnf_error

    except Exception as ex:
        # Log general errors
        print(f"ERROR: An unexpected error occurred: {ex}")

@views.route('/audioEnhance/<int:user>', methods=['POST'])
@login_required
def audioEnhance(user):
    file = request.files.get("audio")

    noise_reduction = float(request.form.get("noiseReduction", 0))
    silence_threshold = int(request.form.get("silenceThreshold", -40))
    min_silence_length = int(request.form.get("minSilenceLength", 500))
    padding = int(request.form.get("padding", 500))
    leeway = int(request.form.get("leeway", 150))
    
    process_status_dict[user] = "pending"
    
    if not (file and noise_reduction and silence_threshold and min_silence_length and padding and leeway):
        process_status_dict[user] = "complete"
        return
    
    # Process audio file
    settings = {
        "silence_thresh": silence_threshold,
        "min_silence_len": min_silence_length,
        "padding": padding,
        "leeway": leeway,
        "prop_decrease": noise_reduction
    }

    UPLOAD_FOLDER = "uploads\\audio"

    number = user
    filename = secure_filename(f"{((number ** 3) * 9999 + (number ** 2) - (42 * number) + 314159) % 100000000}")
    audio_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(audio_path)
    
    try: 
        output_path = process_audio_file(audio_path, settings)
    except Exception:
        process_status_dict[user] = "complete"
        return
    
    process_status_dict[user] = "complete"
    
    return download_file(output_path, "++" + file.filename)

@views.route('/getFromTube/<int:user>', methods=['POST'])
@login_required
def getFromTube(user):
    url = request.form.get("url")
    quality = request.form.get("format-id")
    download_type = request.form.get("download-type")

    process_status_dict[user] = "pending"


    print(url)

    print(quality)

    print(download_type)

    if not (url and quality and download_type):
        print("something aint here")
        process_status_dict[user] = "complete"
        return render_template("dashboard.html", user=current_user, image_dict=image_dict, pannel="download")
        
    what = {
        "Only Video":1,
        "Only Audio":2,
        "Merged Audio and Video":3
    }
    
    download_type=what[download_type]

    print(download_type)

    UPLOAD_FOLDER = "uploads\\tube"

    number = user
    filename = secure_filename(f"{((number ** 3) * 9999 + (number ** 2) - (42 * number) + 314159) % 100000000}")
    the_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, filename))

    print(the_path)
    try:
        output_path, ending = download_media(download_type, the_path, url, quality)
    except Exception:
        process_status_dict[user] = "complete"
        return
    
    print("func was good")
    process_status_dict[user] = "complete"
    print(output_path)

    return download_file(output_path, filename + ending)

@views.route('/captioning/<int:user>', methods=['GET', 'POST'])
@login_required
def captioning(user):
    print("captioning")
    if request.method == 'POST':
        audio_file = request.files.get("audio")
        caption_type = request.form.get('radio')
        caption_range = request.form.get('captionRange')  # Get the slider value
        print("captioning")

        process_status_dict[user] = "pending"
        if not audio_file or not caption_type or not caption_range:
            process_status_dict[user] = "complete"
            print("error")
            return 
        
        UPLOAD_FOLDER = "uploads\\captions"
        number = user
        filename = secure_filename(f"{((number ** 3) * 9999 + (number ** 2) - (42 * number) + 314159) % 100000000}")
        audio_path = os.path.join(UPLOAD_FOLDER, filename)
        audio_file.save(audio_path)

        try:
            output_path = generate_srt(audio_path, caption_type, caption_range)
        except Exception:
            process_status_dict[user] = "complete"
            print("exception")
            return
        
        process_status_dict[user] = "complete"

        base, ext = os.path.splitext(audio_file.filename)
        filename = filename + ".srt"
        print("yay")

        return download_file(output_path, filename)


@views.route('/')
def home():
    return render_template("home.html")

@views.route('/donate')
def donate():
    return redirect(url_for("views.home"))

@views.route('/upload')
@login_required
def upload():
    return render_template("dashboard.html", user=current_user, image_dict=image_dict, pannel="upload")

@views.route('/tabs/<string:tab>')
@login_required
def tabs(tab):
    return render_template("dashboard.html", user=current_user, image_dict=image_dict, pannel=tab)


@views.route('/upload/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        account_name = request.form.get('account-name')

        # Check if account name is empty
        if not account_name or len(account_name) < 2:
            flash("Invalid Name", category="error")
            return redirect(url_for('views.create'))

        new_account = Account(
            user_id=current_user.id,  # Ensure account is linked to user
            account_name=account_name,
        )
        db.session.add(new_account)
        db.session.commit()

        flash("", category="none")
        return redirect(url_for('views.upload'))

    return render_template("create.html")

@views.route('/caption')
def caption():
    return render_template("dashboard.html", user=current_user, image_dict=image_dict, pannel="caption")

@views.route('/audio')
def audio():
    return render_template("dashboard.html", user=current_user, image_dict=image_dict, pannel="audio")

@views.route('/download')
def download():
    return render_template("dashboard.html", user=current_user, image_dict=image_dict, pannel="download")

@views.route('/delete_account/<int:account_id>', methods=['POST'])
@login_required
def delete_account(account_id):
    account = Account.query.get(account_id)

    if not account or account.user_id != current_user.id:
        return redirect(url_for('views.home'))
    if account.user_id != current_user.id:
        return redirect(url_for('views.upload'))
    
    db.session.delete(account)
    db.session.commit()

    return redirect(url_for('views.upload'))

@views.route('/delete_channel/<int:channel_id>', methods=['POST'])
@login_required
def delete_channel(channel_id):
    channel = Channel.query.get(channel_id)

    account_id = channel.account_id
    
    db.session.delete(channel)
    db.session.commit()

    return redirect(url_for('views.view_channel', account_id=account_id, status=500))

@views.route('/edit_account/<int:account_id>', methods=['GET','POST'])
@login_required
def edit_account(account_id):

    account = Account.query.get(account_id)
    
    if request.method == "POST":
        
        account_name = request.form.get('account-name')

        if not account_name or len(account_name) < 2:
            flash('Invalid Name', category='error')
            return redirect(url_for('views.create_channel', account_id=account_id))
        
        account.account_name = account_name
        
        db.session.commit()

        flash("", "none")
        return redirect(url_for('views.upload'))
    
    if not account or account.user_id != current_user.id:
        return redirect(url_for('views.home'))
    if account.user_id != current_user.id:
        return redirect(url_for('views.upload'))

    return render_template("edit.html", name=account.account_name, account_id=account_id)

@views.route('/info')
def dashboard():
    # You can pass data to the template if needed
    return render_template('info.html')

@views.route('/view_channel/<int:account_id>/<int:status>', methods=['GET','POST'])
@login_required
def view_channel(account_id, status):

    account = Account.query.get(account_id)

    return render_template("upload.html",account=account, image_dict=image_dict, status=status)
 
@views.route('/channel_status/<channel_id>')
def channel_status(channel_id):
    channel_id = int(channel_id)  # Convert channel_id to an integer
    status = channel_status_dict.get(channel_id)
    return jsonify({"status": status})

@views.route('/upload_status/<account_id>')
def upload_status(account_id):
    account_id = int(account_id)  # Convert channel_id to an integer
    status = upload_status_dict.get(account_id)
    return jsonify({"status": status})


@views.route('/create_channel/<int:account_id>', methods=['GET', 'POST'])
@login_required
def create_channel(account_id):
    def generate_cookies(new_channel, platform, channel_username, channel_password, cookies_file, channel_name):

        """ Function to generate cookies in a separate thread """
        options = uc.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-popup-blocking")
        driver = uc.Chrome(options=options)
        #options.add_argument("--headless")  # Runs browser in headless mode (hidden)

        try:
            if int(platform) == 1:
                login_to_instagram_and_save_cookies(driver, channel_username, channel_password, cookies_file)
            elif int(platform) == 2:
                login_to_linkedin_and_save_cookies(driver, channel_username, channel_password, cookies_file)
            elif int(platform) == 3:
                login_to_snapchat_and_save_cookies(driver, channel_username, channel_password, cookies_file)
            elif int(platform) == 4:
                login_to_tiktok_and_save_cookies(driver, channel_username, channel_password, cookies_file)
            elif int(platform) == 5:
                login_to_x_and_save_cookies(driver, channel_username, channel_password, cookies_file)
            elif int(platform) == 6:
                login_to_youtube_and_save_cookies(driver, channel_username, channel_password, cookies_file, channel_name)

        except Exception as e:
            print(f"Error generating cookies: {e}")
            db.session.delete(new_channel)
            db.session.commit()
            channel_status_dict[new_channel.id] = "error"  # Update status to "error"
            

        finally:
            driver.quit()
            if channel_status_dict.get(new_channel.id) != "error":
                channel_status_dict[new_channel.id] = "complete"  # Update status to "complete" if no error
                time.sleep(3)
                channel_status_dict[new_channel.id] = "waiting"  # Update status to "complete" if no error


    if request.method == 'POST':
        platform = request.form.get('platform')
        channel_name = request.form.get('channel-name')
        channel_username = request.form.get('channel-username')
        channel_password = request.form.get('channel-password')

        if not platform or not channel_name or not channel_username or not channel_password:
            flash('Please complete full form', category='error')
            return redirect(url_for('views.create_channel', account_id=account_id))
                            
        if int(platform) not in image_dict:
            flash('Invalid platform selected', category='error')
            return redirect(url_for('views.create_channel', account_id=account_id))

        new_channel = Channel(
            uname = channel_username,
            pword = channel_password,
            channel_name=channel_name,
            platform_number=int(platform),
            account_id=account_id,
            channel_cookies=""
        )

        db.session.add(new_channel)
        db.session.commit()

        channel_status_dict[new_channel.id] = "pending"  # Initialize the status

        if not os.path.exists('cookies'):
            os.makedirs('cookies')

        cookies_file = os.path.join('cookies', f"{new_channel.id}_cookies.pkl")
        new_channel.channel_cookies = cookies_file
        db.session.commit()
        account = Account.query.get(account_id)

        @copy_current_request_context
        def generate_cookies_with_context():
            generate_cookies(new_channel, platform, channel_username, channel_password, cookies_file, channel_name)

        thread = threading.Thread(target=generate_cookies_with_context)
        thread.start()

        return render_template("loading.html", new_channel=new_channel, account_id=account_id)
    account = Account.query.get(account_id)
    return render_template("create_channel.html", account=account, image_dict=image_dict)

@views.route('channel/view')
@login_required
def view():
    return render_template("loading.html")

@views.route('/upload_videos/<int:account_id>', methods=["GET", "POST"])
@login_required
def upload_videos(account_id):
    UPLOAD_FOLDER = "uploads/exports"
    
    upload_status_dict[account_id] = "waiting"

    def upload_worker(video_path, title, description, tags, selected_platforms, account_id):
        """Uploads the video to selected platforms using a saved file path."""
        error = 0
        for platform_id in selected_platforms:
            if platform_id in upload_functions:
                channel = Channel.query.filter_by(account_id=account_id, platform_number=platform_id).first()
                if channel and channel.channel_cookies:
                    cookies_path = channel.channel_cookies
                    upload_function = upload_functions[platform_id]
                    print(upload_function)
                    # Open and read the video file inside the thread
                    print("we trying")
                    try:
                        print("trying")
                        with open(video_path, "rb") as video_file:
                            print("opened")
                            upload_function(
                                video_path=video_path, 
                                title=title, 
                                description=description, 
                                tags=tags, 
                                cookies_file=cookies_path, 
                                username=channel.uname, 
                                password=channel.pword, 
                                channel_name=channel.channel_name
                                )
                    except Exception as e:
                        print(f"except {e}")
                        error += 1
                        pass

        if error == 0:
            upload_status_dict[account_id] = "complete"
            time.sleep(3)
            upload_status_dict[account_id] = "waiting"

        else: 
            upload_status_dict[account_id] = "error"

    UPLOAD_FOLDER = "uploads/exports"

    """Handles video uploads and starts a background thread to process them."""
    upload_status_dict[account_id] = "pending"  # Initialize the status

    account = Account.query.get(account_id)
    if request.method == "POST":
        video_file = request.files.get("video")
        title = request.form.get("title", "My Video")
        description = request.form.get("description", "")
        tags = request.form.get("tags", "")
        selected_platforms_json = request.form.get("platforms", "[]")
        selected_platforms = json.loads(selected_platforms_json)
        print(selected_platforms)

        if not video_file:
            print("no video")
            return redirect(url_for('views.view_channel', account_id=account_id, status=101))

        if not selected_platforms:
            print("No plat")
            return redirect(url_for('views.view_channel', account_id=account_id, status=102))

        # Secure and save the file temporarily
        number = account_id
        filename = secure_filename(f"{((number ** 3) * 9999 + (number ** 2) - (42 * number) + 314159) % 100000000}")
        video_path = os.path.join(UPLOAD_FOLDER, filename + ".mp4")
        video_file.save(video_path)

        print("Video Saved")

        video_path = os.path.abspath(video_path)
        
        @copy_current_request_context
        def upload_worker_context():
            with current_app.app_context():
                try:
                    print("with context trying")
                    upload_worker(video_path, title, description, tags, selected_platforms, account_id)
                except Exception as e:
                    print(f"error of {e}")
                    upload_status_dict[account_id] = "error"
        print("threaad")
        # Start upload in a separate thread with Flask app context
        thread = threading.Thread(target=upload_worker_context)
        thread.start()

        print("get loading")
        return render_template("uploading.html", account_id=account_id)

    return redirect(url_for('views.view_channel', account_id=account_id, status=300))


@views.route('/get_formats/<path:url>', methods=['POST'])
def list_formats(url):
    formats_list = []
    seen_resolutions = set()
    
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])
            for fmt in formats:
                format_id = fmt.get('format_id', '')
                file_type = fmt.get('ext', '')
                resolution = fmt.get('format_note', '')
                
                # Check if the format is mp4 and the resolution is a number followed by 'p'
                if file_type == 'mp4' and re.match(r'^\d+p$', resolution):
                    if resolution not in seen_resolutions:
                        formats_list.append({
                            'id': format_id,
                            'format': f"{resolution}"
                        })
                        seen_resolutions.add(resolution)
                        
    except Exception as e:
        return jsonify([{}])
    
    print(formats_list)
    return jsonify(formats_list)
