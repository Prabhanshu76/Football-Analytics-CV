from flask import Flask, render_template, Response, request
from common_imports import cv2
from detection_utility import detections2boxes, match_detections_with_tracks
from config import *


app = Flask(__name__)


def generate_frames():
    global team1_passes, team2_passes, team1_possession_percentage, team2_possession_percentage
    possession_team=""

    player_in_possession_detection = None
    player_in_possession_track_id = None
    while True:
        success, frame = cap.read()

        if not success:
            break


        results = model(frame, size=1280)
        detections = Detection.from_results(
            pred=results.pred[0].cpu().numpy(),
            names=model.names)

        ball_detections = filter_detections_by_class(detections=detections, class_name="ball")
        referee_detections = filter_detections_by_class(detections=detections, class_name="referee")
        goalkeeper_detections = filter_detections_by_class(detections=detections, class_name="goalkeeper")
        player_detections = filter_detections_by_class(detections=detections, class_name="player")
        print(len(player_detections))

        annotated_image = frame.copy()
        player_classifications = []
        
        
        player_in_possession_detection = None

        print(possession_team)
        player_goalkeeper_detections = player_detections + goalkeeper_detections
        tracked_detections = player_detections + goalkeeper_detections + referee_detections  
        
        if len(detections2boxes(detections=tracked_detections)):
            tracks = byte_tracker.update(
                output_results=detections2boxes(detections=tracked_detections),
                img_info=frame.shape,
                img_size=frame.shape
            )

            if len(tracks):
                tracked_detections = match_detections_with_tracks(detections=tracked_detections, tracks=tracks)

                tracked_referee_detections = filter_detections_by_class(detections=tracked_detections, class_name="referee")
                tracked_goalkeeper_detections = filter_detections_by_class(detections=tracked_detections, class_name="goalkeeper")
                tracked_player_detections = filter_detections_by_class(detections=tracked_detections, class_name="player")

                for player_detection in tracked_player_detections:
                    rect = player_detection.rect
                    x, y, width, height = int(rect.x), int(rect.y), int(rect.width), int(rect.height)
                    player_image = frame[y:y+height, x:x+width] 
                    jersey_color = jersey_classifier.classify_player_jersey(player_image)
                    player_classifications.append(jersey_color)
                    if len(ball_detections) != 1:
                        player_in_possession_detection = None
                        player_in_possession_track_id = None
                    elif player_detection.rect.pad(PLAYER_IN_POSSESSION_PROXIMITY).contains_point(point=ball_detections[0].rect.center):
                        possession_team=jersey_color
                        player_in_possession_detection = player_detection
                        player_in_possession_track_id = player_detection.tracker_id 

                annotated_image = base_annotator.annotate(
                    image=annotated_image,
                    detections=tracked_detections)

                annotated_image = player_goalkeeper_text_annotator.annotate(
                    image=annotated_image,
                    detections=tracked_goalkeeper_detections + tracked_player_detections,
                    jersey_colors=player_classifications)

                annotated_image = ball_marker_annotator.annotate(
                    image=annotated_image,
                    detections=ball_detections)

                annotated_image = player_marker_annotator.annotate(
                    image=annotated_image,
                    detections=[player_in_possession_detection] if player_in_possession_detection else [])

                print(possession_team)
                print("Player in Possession Track ID:", player_in_possession_track_id) 

            pass_tracker.update_pass(possession_team, player_in_possession_track_id)
            team1_passes, team2_passes = pass_tracker.get_passes()
            possession_calculator.update_possession(possession_team)
            current_frame = 1 + possession_calculator.team1_possession + possession_calculator.team2_possession
            team1_possession_percentage, team2_possession_percentage = possession_calculator.get_possession_stats(current_frame)

            print("Team 1 Passes:", team1_passes)
            print("Team 2 Passes:", team2_passes)


            print(f"Frame {current_frame}:")
            print("Team 1 Possession Percentage: {:.2f}%".format(team1_possession_percentage))
            print("Team 2 Possession Percentage: {:.2f}%".format(team2_possession_percentage))

        annotated_image = cv2.resize(annotated_image, (640, 480))
        ret, buffer = cv2.imencode('.jpg', annotated_image)
        frameA = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frameA + b'\r\n') 



@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    # Save the uploaded file to a folder (you need to create the 'uploads' folder in your project directory)
    file.save('static/uploads/' + file.filename)

    # return 'File uploaded successfully'
    return render_template('displayvideo.html', filename=file.filename) 


@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/process_video', methods=['POST'])
def process_video():
    return render_template('display_final.html')

@app.route('/data')
def data():
    global team1_passes, team2_passes, team1_possession_percentage, team2_possession_percentage
    return {
        'team1_passes': team1_passes,
        'team2_passes': team2_passes,
        'team1_possession_percentage': team1_possession_percentage,
        'team2_possession_percentage': team2_possession_percentage
    }


if __name__ == '__main__':
    app.run(debug=True)
#detection(WEIGHTS_PATH, model, SOURCE_VIDEO_PATH, TARGET_VIDEO_PATH, color_list, boundaries)