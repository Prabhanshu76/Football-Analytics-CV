# Football-Analytics-CV
Our project is dedicated to revolutionizing real-time soccer match analysis by leveraging cutting-edge technologies such as YOLOv5 and ByteTracker. We have successfully implemented a range of features that enhance soccer video analysis through precise player identification, accurate ball tracking, and the identification of crucial in-game events.

## YOLOv5 Integration
With the integration of YOLOv5, we've achieved remarkable accuracy and speed in player and ball detection within live match footage. YOLOv5 has proven to be an invaluable asset, allowing us to reliably spot players and the soccer ball even in fast-paced game scenarios.

## ByteTracker Tracking System
In tandem with YOLOv5, we've incorporated ByteTracker, a sophisticated tracking system. ByteTracker's efficiency ensures seamless and continuous tracking of players and the ball across frames, providing a reliable way to monitor their movements throughout the game.

## Implemented Features
Our project boasts a comprehensive set of features, enhancing soccer match analysis:

- **Player and Ball Detection:**
  - Leveraging YOLOv5, our system accurately identifies and tracks players and the soccer ball in real-time.

- **Player in Possession Detection:**
  - The system intelligently identifies the player currently in possession of the ball during the match.

- **Team Identification/Classification:**
  - Our system classifies and identifies teams based on jersey colors, contributing to comprehensive team analysis.

- **Team Possession Count:**
  - We provide insights into team possession counts, helping teams understand and analyze their control over the ball during the game.

- **Team Pass Count:**
  - The system counts and analyzes the passes made by each team, offering a valuable metric for assessing teamwork and strategic plays.

## Project Goals
Our overarching goal is to provide coaches and analysts with a tool that offers deep insights into team strategies and player performances. By enabling comprehensive soccer analytics, we aim to support smarter decision-making in coaching and enhance overall performance analysis. Our ultimate objective is to contribute to the advancement of soccer analysis methods, offering teams valuable insights to refine their strategies and tactics.

## Demo Video
[![Football Analytics Demo]([link_to_thumbnail_image](https://drive.google.com/file/d/1gbQy6c6K2Q7uZMs1uUytLeKsPthnDOle/view?usp=sharing))]([link_to_demo_video](https://drive.google.com/file/d/1rV_ib7MFLPu8kYvxj0eibML2f3NSCfm5/view?usp=drive_link))
---

## Project Setup
To get started with our project, follow these steps:

1. **Download and Copy ByteTrack Folder:** [Custom ByteTrack Folder](https://drive.google.com/file/d/12Yzo3-L2uiR4ivmQkLLFM501_4nXU_ue/view?usp=sharing)
   - Copy this custom ByteTrack folder to your project directory.

2. **Download Model:**
   - Download the model from this [link](https://drive.google.com/file/d/1_3nIEdVzW3674-lumMaU0OY7nhKTwdSL/view?usp=sharing)
   - Edit `config.ini` to set the correct path for the downloaded model.

3. **Setup:**
   - Run `setup.py` to ensure all dependencies are installed.

4. **Launch:**
   - Run `app.py` to start the application.
  
After launching, open the following URL in your web browser: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

#### Configuring Jersey Color Ranges

Open the `config.ini` file and navigate to the `[Boundaries_HSV]` section. Adjust the HSV parameters for each team to match the specific colors of their jerseys:

```ini
[Boundaries_HSV]
team1_h_min = ...
team1_s_min = ...
team1_v_min = ...
team1_h_max = ...
team1_s_max = ...
team1_v_max = ...

team2_h_min = ...
team2_s_min = ...
team2_v_min = ...
team2_h_max = ...
team2_s_max = ...
team2_v_max = ...
