class PossessionCalculator:
    def __init__(self, consecutive_threshold=3):
        self.consecutive_threshold = consecutive_threshold
        self.current_possessing_team = None
        self.consecutive_frames_in_possession = 0
        self.team1_possession = 0
        self.team2_possession = 0

    def update_possession(self, possession_team):
        if possession_team == self.current_possessing_team:
            self.consecutive_frames_in_possession += 1
        else:
            self.consecutive_frames_in_possession = 1
            self.current_possessing_team = possession_team

        if self.consecutive_frames_in_possession >= self.consecutive_threshold:
            if possession_team == 'Team 1':
                self.team1_possession += 1
            elif possession_team == 'Team 2':
                self.team2_possession += 1

    def get_possession_stats(self, total_frames):
        team1_percentage = (self.team1_possession / total_frames) * 100
        team2_percentage = (self.team2_possession / total_frames) * 100
        return team1_percentage, team2_percentage
