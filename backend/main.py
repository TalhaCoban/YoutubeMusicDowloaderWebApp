import flask
from flask import request, jsonify, abort, Response
from pydantic import ValidationError
from video_handler import VideoHandler
from ydl_options import YDLOptions



app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route('/api', methods=['GET'])
def home():
    return jsonify({
        "title": "Welcome to Youtube Music Dowloader", 
        "message": "You can dowload mp3 files from Youtube by using its url"
    })


@app.route('/api/getvideoinfo/', methods=['POST'])
def getvideoinfo():
    data = request.json
    if not data or 'url' not in data:  # Check if 'url' is missing
        abort(400, description="The url parameter is required.")  # Return 400 Bad Request
        
    video_url = data['url']
    try:
        videohandler = VideoHandler(url=video_url)
        return videohandler.video.to_dict()
    
    except ValidationError as e:
        # Return 400 Bad Request with validation error details
        abort(400, description=f"Validation error: {e}")
    
    except Exception as e:
        abort(500, description=f"An error happend: {e}")


@app.route('/api/getvideoaudioformats/', methods=['POST'])
def getvideoaudioformats():
    data = request.json
    if not data or 'url' not in data:  # Check if 'url' is missing
        abort(400, description="The url parameter is required.")  # Return 400 Bad Request
        
    video_url = data['url']
    try:
        videohandler = VideoHandler(url=video_url)
        formats = videohandler.video.getAllAudioFormats()
        return [f.to_dict() for f in formats]
    
    except ValidationError as e:
        # Return 400 Bad Request with validation error details
        abort(400, description=f"Validation error: {e}")
    
    except Exception as e:
        abort(500, description=f"An error happend: {e}")


def turkish_to_english(title):
    turkish_karakterler = ['ç', 'ı', 'ğ', 'ş', 'ü', 'ö', 'Ç', 'İ', 'Ğ', 'Ş', 'Ü', 'Ö']
    english_karakterler = ['c', 'i', 'g', 's', 'u', 'o', 'C', 'I', 'G', 'S', 'U', 'O']
    for turkish, english in zip(turkish_karakterler, english_karakterler):
        title = title.replace(turkish, english)
    return title


@app.route('/api/downloadaudio/', methods=['POST'])
def downloadaudio():
    data = request.json
    if not data or 'url' not in data or "format_id" not in data:  # Check if 'url' and 'format_id' is missing
        abort(400, description="Missing or invalid parameter")  # Return 400 Bad Request
        
    video_url = data['url']
    audio_format_id = str(data['format_id'])
    title = data['title'] if 'title' in data else None

    try:
        videohandler = VideoHandler(url=video_url)
        ydlOptions = YDLOptions(videohandler.video)
        ydlOptions.setAudioFormat(audio_format_id)
        if title == None:
            title = videohandler.video.title
        ydlOptions.setTitle(title)
        ydl_opts_object = ydlOptions.getYDLOptionsObject()
        buffer = videohandler.getBufferAudio(ydlOptions)
        name = turkish_to_english(ydl_opts_object.outtmpl)
        return Response(
            buffer.read(),
            mimetype=f"audio/{ydlOptions.ext}",
            headers={
                "Content-Disposition": f"attachment; filename={name}"
            }
        )
    
    except ValidationError as e:
        # Return 400 Bad Request with validation error details
        abort(400, description=f"Validation error: {e}")
    
    except Exception as e:
        abort(500, description=f"An error happend: {e}")






if __name__ == "__main__":
    app.run()
    
    
    # video_url= "https://www.youtube.com/watch?v=To_gVXXIKlk&ab_channel=TaylanKayaMusic"
    # audio_format_id= "140"
    # title= "deneme"