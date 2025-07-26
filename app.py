import yt_dlp
from flask import Flask, render_template, request, send_from_directory, flash, url_for

app = Flask(__name__)
app.secret_key = 'd6c5ace5338988db865fd67de7bb1ec3'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': 'downloads/%(title)s.%(ext)s',
                    'quiet': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info_dict)
                    mp3_filename = filename.rsplit('.', 1)[0] + '.mp3'
                return render_template('index.html', download_link=url_for('download_file', filename=os.path.basename(mp3_filename)))
            except Exception as e:
                flash(f"❌ Failed to download: {str(e)}", "error")
        else:
            flash("⚠️ Please enter a YouTube URL.", "warning")
    return render_template('index.html')

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory('downloads', filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
