from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess
import os

app = Flask(__name__)
app.secret_key = 'd6c5ace5338988db865fd67de7bb1ec3'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            try:
                command = f'yt-dlp -f bestaudio -x --audio-format mp3 "{url}"'
                subprocess.run(command, shell=True, check=True)
                flash("✅ Download successful! Check your files.", "success")
            except subprocess.CalledProcessError:
                flash("❌ Failed to download. Please check the URL.", "error")
        else:
            flash("⚠️ Please enter a YouTube URL.", "warning")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)