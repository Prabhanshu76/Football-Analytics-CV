class PassTracker:
    def __init__(self):
        self.possession_team = None
        self.last_possession_team = None
        self.last_team1_possession_track_id = None
        self.last_team2_possession_track_id = None
        self.team1_passes = 0
        self.team2_passes = 0

    def update_pass(self, possession_team, player_in_possession_track_id):
        if possession_team != self.last_possession_team:
            self.last_possession_team = possession_team

        if possession_team == 'Team 1':
            if (
                player_in_possession_track_id is not None
                and player_in_possession_track_id != self.last_team1_possession_track_id
                and self.last_possession_team == 'Team 1'
            ):
                self.team1_passes += 1
                self.last_team1_possession_track_id = player_in_possession_track_id

        elif possession_team == 'Team 2':
            if (
                player_in_possession_track_id is not None
                and player_in_possession_track_id != self.last_team2_possession_track_id
                and self.last_possession_team == 'Team 2'
            ):
                self.team2_passes += 1
                self.last_team2_possession_track_id = player_in_possession_track_id

    def get_passes(self):
        return self.team1_passes, self.team2_passes

    def reset(self):
        self.possession_team = None
        self.last_possession_team = None
        self.last_team1_possession_track_id = None
        self.last_team2_possession_track_id = None
        self.team1_passes = 0
        self.team2_passes = 0
