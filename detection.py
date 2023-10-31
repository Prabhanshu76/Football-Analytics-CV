from IPython.display import display, clear_output
import PIL.Image
from common_imports import io, os, tqdm, cv2, torch, BYTETracker, np

from video_writer import VideoConfig, get_video_writer, generate_frames
from geometry_utilities import BaseAnnotator, Color, Detection, filter_detections_by_class
from colors import *
from text_annotator import TextAnnotator
from possession_maker import MarkerAnntator
from byte_tracker_args import BYTETrackerArgs
from player_in_possession import get_player_in_possession
from detection_utility import detections2boxes, match_detections_with_tracks
from jersey_classifier import PlayerJerseyClassifier
from possession_calc import *


def detection(WEIGHTS_PATH, model, SOURCE_VIDEO_PATH, TARGET_VIDEO_PATH, color_list, boundaries):

    fcount=0

    # initiate video writer
    video_config = VideoConfig(
        fps=30,
        width=1920,
        height=1080)
    video_writer = get_video_writer(
        target_video_path=TARGET_VIDEO_PATH,
        video_config=video_config)

    # get fresh video frame generator
    frame_iterator = iter(generate_frames(video_file=SOURCE_VIDEO_PATH))

    # initiate annotators
    base_annotator = BaseAnnotator(
        colors=[
            BALL_COLOR,
            PLAYER_COLOR,
            PLAYER_COLOR_BLUE,
            PLAYER_COLOR_WHITE,
            REFEREE_COLOR
        ],
        thickness=THICKNESS)

    player_goalkeeper_text_annotator = TextAnnotator(
        PLAYER_COLOR, PLAYER_COLOR_BLUE,PLAYER_COLOR_WHITE, text_color=Color(255, 255, 255), text_thickness=2)
    #referee_text_annotator = TextAnnotator(
    #    REFEREE_COLOR, text_color=Color(0, 0, 0), text_thickness=2)

    ball_marker_annotator = MarkerAnntator(
        color=BALL_MARKER_FILL_COLOR)
    player_in_possession_marker_annotator = MarkerAnntator(
        color=PLAYER_MARKER_FILL_COLOR)
    player_marker_annotator = MarkerAnntator(color=PLAYER_MARKER_FILL_COLOR)


    # initiate tracker
    byte_tracker = BYTETracker(BYTETrackerArgs())

    jersey_classifier = PlayerJerseyClassifier(color_list,boundaries)

    ############################################################################
    # Initialize possession variables
    #team1_possession = 0
    #team2_possession = 0

    #possession_team1_frames = 0
    #possession_team2_frames = 0

    #current_possessing_team = None
    #consecutive_frames_in_possession = 0
    #consecutive_possession_threshold = 3  # Change this threshold as needed

    # Create an instance of PossessionCalculator
    #possession_calculator = PossessionCalculator(consecutive_threshold=3)
    possession_calculator = PossessionCalculator()
    possession_team=""

    # Loop over frames
    for frame in tqdm(frame_iterator, total=1001):
        # Run detector
        results = model(frame, size=1280)
        detections = Detection.from_results(
            pred=results.pred[0].cpu().numpy(),
            names=model.names)

        # Filter detections by class
        ball_detections = filter_detections_by_class(detections=detections, class_name="ball")
        referee_detections = filter_detections_by_class(detections=detections, class_name="referee")
        goalkeeper_detections = filter_detections_by_class(detections=detections, class_name="goalkeeper")
        player_detections = filter_detections_by_class(detections=detections, class_name="player")
        print(len(player_detections))

        annotated_image = frame.copy()

        # Create a list to store the classifications of player jerseys
        player_classifications = []
        
        
        player_in_possession_detection = None
        # Classify player jerseys and store the result in player_classifications
        for player_detection in player_detections:
            rect = player_detection.rect
            x, y, width, height = int(rect.x), int(rect.y), int(rect.width), int(rect.height)
            player_image = frame[y:y+height, x:x+width]  # Crop player image
            jersey_color = jersey_classifier.classify_player_jersey(player_image)
            player_classifications.append(jersey_color)
            
            if len(ball_detections) != 1:
                player_in_possession_detection = None
            elif player_detection.rect.pad(PLAYER_IN_POSSESSION_PROXIMITY).contains_point(point=ball_detections[0].rect.center):
                possession_team=jersey_color
                player_in_possession_detection = player_detection

        print(possession_team)

        player_goalkeeper_detections = player_detections + goalkeeper_detections
        tracked_detections = player_detections + goalkeeper_detections + referee_detections

        # calculate player in possession
        #player_in_possession_detection = get_player_in_possession(
            #player_detections=player_goalkeeper_detections,
            #ball_detections=ball_detections,
            #proximity=PLAYER_IN_POSSESSION_PROXIMITY)

            ######combine player in possession detection and jersey detection in above for loop, so when the player is in possesion, jersey color will be save for that frame.
        possession_calculator.update_possession(possession_team)
        #if len(ball_detections) == 1:
            #possession_calculator.update_possession(possession_team)
            #  if possession_team == current_possessing_team:
            #     consecutive_frames_in_possession += 1
            #  else:
            #     consecutive_frames_in_possession = 1
            #     current_possessing_team = possession_team

            #  # Check if the team has possession for more than the threshold frames
            #  if consecutive_frames_in_possession >= consecutive_possession_threshold:
            #     if possession_team == 'Team 1':
            #         team1_possession += 1
            #     elif possession_team == 'Team 2':
            #         team2_possession += 1

        
        current_frame = 1 + possession_calculator.team1_possession + possession_calculator.team2_possession

        # Get possession statistics for the current frame
        team1_percentage, team2_percentage = possession_calculator.get_possession_stats(current_frame)

        # Print the possession percentages for the current frame
        print(f"Frame {current_frame}:")
        print("Team 1 Possession Percentage: {:.2f}%".format(team1_percentage))
        print("Team 2 Possession Percentage: {:.2f}%".format(team2_percentage))
        
        
        if len(detections2boxes(detections=tracked_detections)):
            # trackcol
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

                # Annotate video frame
                annotated_image = base_annotator.annotate(
                    image=annotated_image,
                    detections=tracked_detections)

                annotated_image = player_goalkeeper_text_annotator.annotate(
                    image=annotated_image,
                    detections=tracked_goalkeeper_detections + tracked_player_detections,
                    jersey_colors=player_classifications)  # Pass the jersey colors

                #annotated_image = referee_text_annotator.annotate(
                    #image=annotated_image,
                    #detections=tracked_referee_detections)

                annotated_image = ball_marker_annotator.annotate(
                    image=annotated_image,
                    detections=ball_detections)

                annotated_image = player_marker_annotator.annotate(
                    image=annotated_image,
                    detections=[player_in_possession_detection] if player_in_possession_detection else [])

        # save video frame
        #video_writer.write(annotated_image)

    # Close output video
    #video_writer.release()


        cv2.imshow("Annotated Video", annotated_image)

        # Press 'q' to quit the video display
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    total_frames = 1250  # class to auto cal total frames

    team1_percentage, team2_percentage = possession_calculator.get_possession_stats(total_frames)
    total_percentage = team1_percentage + team2_percentage
    normalized_team1_percentage = (team1_percentage / total_percentage) * 100
    normalized_team2_percentage = (team2_percentage / total_percentage) * 100

    # Print the normalized possession percentages
    print("Normalized Team 1 Possession Percentage: {:.2f}%".format(normalized_team1_percentage))
    print("Normalized Team 2 Possession Percentage: {:.2f}%".format(normalized_team2_percentage))

    # close output video
    cv2.destroyAllWindows()
    video_writer.release()