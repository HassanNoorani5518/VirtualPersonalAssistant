import fitness_core as fc
from fitness_core import np, time
class Exercises:
    class Exercise:
        def __init__(self):
            self.counter = 0
            self.state = 'down'
            self.last_update_time = time.time()
            self.previous_counter = 0

    class BicepCurl(Exercise):
        def __init__(self):
            super().__init__()
            self.checkpoints_passed_up = [False, False]
            self.checkpoints_passed_down = [False, False]
        
       
            
        def calculate_distance(self, p1, p2):
            return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        
        def counter_updated(self):
            return self.counter > self.previous_counter

        def process(self, keypoints):
            left_shoulder, left_elbow, left_wrist = keypoints[5], keypoints[7], keypoints[9]
            right_shoulder, right_elbow, right_wrist = keypoints[6], keypoints[8], keypoints[10]
            
            if not hasattr(self, 'left_state'):
                self.left_state = 'down'
                self.left_checkpoints_passed_up = [False, False]
                self.left_checkpoints_passed_down = [False, False]
            
            if not hasattr(self, 'right_state'):
                self.right_state = 'down'
                self.right_checkpoints_passed_up = [False, False]
                self.right_checkpoints_passed_down = [False, False]

            self.process_arm(
                shoulder=left_shoulder, 
                elbow=left_elbow, 
                wrist=left_wrist, 
                arm_state='left_state', 
                checkpoints_passed_up='left_checkpoints_passed_up', 
                checkpoints_passed_down='left_checkpoints_passed_down'
            )

            self.process_arm(
                shoulder=right_shoulder, 
                elbow=right_elbow, 
                wrist=right_wrist, 
                arm_state='right_state', 
                checkpoints_passed_up='right_checkpoints_passed_up', 
                checkpoints_passed_down='right_checkpoints_passed_down'
            )

        def process_arm(self, shoulder, elbow, wrist, arm_state, checkpoints_passed_up, checkpoints_passed_down):
            full_arm_distance = self.calculate_distance(shoulder, elbow) + self.calculate_distance(elbow, wrist)
            shortest_distance = self.calculate_distance(shoulder, wrist)

            if getattr(self, arm_state) == 'down':
                if shortest_distance < 0.5 * full_arm_distance:
                    getattr(self, checkpoints_passed_up)[0] = True
                if getattr(self, checkpoints_passed_up)[0] and shortest_distance < 0.6 * full_arm_distance:
                    getattr(self, checkpoints_passed_up)[1] = True

                if getattr(self, checkpoints_passed_up)[0] and getattr(self, checkpoints_passed_up)[1]:
                    setattr(self, arm_state, 'up')
                    setattr(self, checkpoints_passed_down, [False, False])

            elif getattr(self, arm_state) == 'up':
                if shortest_distance > 0.5 * full_arm_distance:
                    getattr(self, checkpoints_passed_down)[0] = True
                if getattr(self, checkpoints_passed_down)[0] and shortest_distance > 0.75 * full_arm_distance:
                    getattr(self, checkpoints_passed_down)[1] = True

                if getattr(self, checkpoints_passed_down)[0] and getattr(self, checkpoints_passed_down)[1]:
                    self.counter += 1
                    setattr(self, arm_state, 'down')
                    setattr(self, checkpoints_passed_up, [False, False])

                if self.counter_updated():
                    self.last_update_time = time.time()
                self.previous_counter = self.counter

    class Squat(Exercise):
        def process(self, keypoints):
            left_hip, left_knee = keypoints[11], keypoints[13]
            right_hip, right_knee = keypoints[12], keypoints[14]

            if (self.state == 'up' and left_hip[0] > left_knee[0]) and (self.state == 'up' and right_hip[0] > right_knee[0]):
                self.state = 'down'
            elif (self.state == 'down' and left_hip[0] <= left_knee[0]) and (self.state == 'down' and right_hip[0] <= right_knee[0]):
                self.counter += 1
                self.state = 'up'

    @staticmethod
    def validate_keypoints(keypoints):
        valid_keypoints = sum(1 for keypoint in keypoints if keypoint[2] > fc.CONFIDENCE_THRESHOLD)
        return valid_keypoints >= fc._NUM_KEYPOINTS // 2

    @staticmethod
    def check_gesture_to_switch_exercise(keypoints, radius=0.05):
        left_wrist = keypoints[9]
        right_wrist = keypoints[10]
        distance = np.sqrt((left_wrist[0] - right_wrist[0]) ** 2 + (left_wrist[1] - right_wrist[1]) ** 2)
        return distance < radius

    @staticmethod
    def display_curl(exercise):
        if exercise.counter > 8:
            fc.sense.show_message(f"WOW!! YOU DID {exercise.counter} CURLS.")
        else:
            fc.sense.show_message(f"YOU DID {exercise.counter} CURLS.")

    @staticmethod
    def display_squat(exercise):
        if exercise.counter > 8:
            fc.fc.sense.show_message(f"WOW!! YOU DID {exercise.counter} SQUATS.")
        else:
            fc.sense.show_message(f"YOU DID {exercise.counter} SQUATS.")
    
    def reset_count(exercise):
            exercise.counter = 0
