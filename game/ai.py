import math


class EnemyAI:

    CHASE = "CHASE"
    ATTACK = "ATTACK"
    RETREAT = "RETREAT"

    def __init__(self):

        self.state = self.CHASE

        self.prediction_time = 15

        self.reaction_timer = 0

        self.difficulty = 1

        # Adaptive values
        self.aggression = 1.0

        self.aim_accuracy = 0.70

        self.strafe_speed = 1.0

    # =====================================================
    # DIFFICULTY
    # =====================================================

    def update_difficulty(self, score):

        if score < 100:

            self.difficulty = 1

            self.prediction_time = 12

            self.aggression = 1.0

            self.aim_accuracy = 0.70

            self.strafe_speed = 1.0

        elif score < 250:

            self.difficulty = 2

            self.prediction_time = 16

            self.aggression = 1.15

            self.aim_accuracy = 0.78

            self.strafe_speed = 1.15

        elif score < 500:

            self.difficulty = 3

            self.prediction_time = 20

            self.aggression = 1.30

            self.aim_accuracy = 0.86

            self.strafe_speed = 1.30

        else:

            self.difficulty = 4

            self.prediction_time = 24

            self.aggression = 1.45

            self.aim_accuracy = 0.93

            self.strafe_speed = 1.45

    # =====================================================
    # PREDICT PLAYER
    # =====================================================

    def predict_position(
        self,
        x,
        y,
        velocity_x,
        velocity_y
    ):

        predicted_x = (
            x
            + velocity_x
            * self.prediction_time
        )

        predicted_y = (
            y
            + velocity_y
            * self.prediction_time
        )

        return (
            predicted_x,
            predicted_y
        )

    # =====================================================
    # DISTANCE
    # =====================================================

    def get_distance(
        self,
        enemy_x,
        enemy_y,
        player_x,
        player_y
    ):

        dx = player_x - enemy_x
        dy = player_y - enemy_y

        return math.sqrt(
            dx * dx +
            dy * dy
        )

    # =====================================================
    # STATE DECISION
    # =====================================================

    def decide_state(
        self,
        enemy_x,
        enemy_y,
        player_x,
        player_y
    ):

        distance = self.get_distance(
            enemy_x,
            enemy_y,
            player_x,
            player_y
        )

        # Far away
        if distance > 400:

            self.state = self.CHASE

        # Medium range
        elif distance > 150:

            self.state = self.ATTACK

        # Very close
        else:

            self.state = self.RETREAT

        return self.state

    # =====================================================
    # PLAYER SHOOT REACTION
    # =====================================================

    def player_shot_reaction(self):

        self.reaction_timer = (
            20 + self.difficulty * 5
        )

        self.state = self.RETREAT

    # =====================================================
    # REACTION UPDATE
    # =====================================================

    def update_reaction(self):

        if self.reaction_timer > 0:

            self.reaction_timer -= 1

        return (
            self.reaction_timer > 0
        )

    # =====================================================
    # SHOOT DECISION
    # =====================================================

    def should_shoot(
        self,
        distance
    ):

        if self.reaction_timer > 0:

            return False

        if self.state == self.ATTACK:

            return distance < 600

        if self.state == self.RETREAT:

            return distance < 420

        return False

    # =====================================================
    # STRAFE TIMING
    # =====================================================

    def get_strafe_time(self):

        if self.difficulty == 1:
            return 80

        if self.difficulty == 2:
            return 65

        if self.difficulty == 3:
            return 50

        return 38

    # =====================================================
    # DIRECTION CHANGE
    # =====================================================

    def get_direction_change_time(self):

        if self.difficulty == 1:
            return 120

        if self.difficulty == 2:
            return 95

        if self.difficulty == 3:
            return 70

        return 50