from flask import Flask,render_template,Response,request,jsonify,send_from_directory
from camera import VideoCamera
from translation_service import translate_text
from tts_service import text_to_speech
import os
import time 

app=Flask(__name__)
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
CACHE_DIR=os.path.join(BASE_DIR,'static','4_cache')
if not os.path.exists(CACHE_DIR):
   os.makedirs(CACHE_DIR)

camera=VideoCamera()
translation_cache={}

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(CACHE_DIR,filename)

def gen(camera):
   while True:
      frame,text=camera.get_frame()
      if frame:
         yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')
      else:
         time.sleep(0.1)

@app.route('/video_feed')
def video_feed():
   return Response(gen(camera),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_status')
def get_status():
   return jsonify({
      'text':camera.current_prediction,
      'is_recording':camera.is_recording
   })

@app.route('/add_gesture',methods=['POST'])
def add_gesture():
   label=request.json.get('label')
   if not label:
      return jsonify({'status':'error','message':'No label provided'}) 
   camera.start_recording(label)
   return jsonify({'status':'success','message':f'Recording started for {label}'})

@app.route('/process_audio',methods=['POST'])
def process_audio():
   data=request.json
   text=data.get('text')
   target_lang=data.get('language')
   cache_key=f"{text}_{target_lang}"
   if cache_key in translation_cache:
      translated_text=translation_cache[cache_key]
   else:
        translated_text=translate_text(text,target_lang)
        translation_cache[cache_key]=translated_text
   audio_url=text_to_speech(translated_text,target_lang)
   return jsonify({
        'translated_text':translated_text,
        'audio_url':audio_url
   })

@app.route('/reset_model',methods=['POST'])
def reset_model():
    camera.manager.reset_data()
    return jsonify({'status':'success'})

if __name__=='__main__':
   app.run(debug=True)