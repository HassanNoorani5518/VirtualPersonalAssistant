import fitness_core as fc
from fitness_core import argparse, np, cv2, sys, time, Image, common, make_interpreter, threading
from inference import Inference
from exercises import Exercises
from visualization import Visualization
import gemini as gemini

def main():
    fc.sense.clear()
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--model', required=True, help="Enter TPU or CPU")
    args = parser.parse_args()

    inactive_time_limit = 15 # Time in seconds to clear the display after inactivity
    tpu = None
    interpreter = None
    
    if args.model == 'TPU':
        tpu = True
        try:
            interpreter = make_interpreter('movenet_single_pose_thunder_ptq_edgetpu.tflite')
            interpreter.allocate_tensors()
        except ImportError:
            print("pycoral is not installed. Please install it to run on TPU.")
            sys.exit(1)
    elif args.model == 'CPU':
        tpu = False
        try:
            interpreter = tf.lite.Interpreter(model_path='movenet_single_pose_thunder.tflite')
            interpreter.allocate_tensors()
        except ImportError:
            print("TensorFlow is not installed. Please install it to run on CPU.")
            sys.exit(1)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    bicep_curl = Exercises.BicepCurl()
    squat = Exercises.Squat()
    exercises = {'Bicep Curls': bicep_curl, 'Squats': squat}
    current_exercise = 'Bicep Curls'
    
    last_activity_time = time.time()
    validation_passed = False
    shutdown = False

    def listen_for_command():
        nonlocal current_exercise, shutdown
        while not shutdown:
            prompt = gemini.capture_speech()
            ans = gemini.send_to_gemini(prompt)
            if str(ans).lower() == "curls":
                current_exercise = 'Bicep Curls'
                print(f"Switched to: {current_exercise}")
                fc.sense.clear()
            elif str(ans).lower() == "squats":
                current_exercise = 'Squats'
                print(f"Switched to: {current_exercise}")
                fc.sense.clear()
            elif str(ans).lower() == "reset":
                Exercises.reset_count(exercises[current_exercise])
                fc.sense.clear()
            elif str(ans).lower() == "quit":
                fc.sense.clear()
                fc.sense.show_message("Take care!! See you soon")
                shutdown = True
            else:
                pass
            time.sleep(0.1)
            
    def fitness_activate():
        nonlocal shutdown
        while not shutdown:
            activity_detected = False
            nonlocal current_exercise
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image")
                break

            if tpu:
                keypoints_with_scores = Inference.doInferenceTPU(frame, interpreter)
            else:
                keypoints_with_scores = Inference.doInferenceCPU(frame, interpreter)

            validation_passed = Exercises.validate_keypoints(keypoints_with_scores)
            if not validation_passed:
                #print("No person detected. Waiting for person to enter the frame.")
                time.sleep(0.1)
                continue
                       
            img = Image.fromarray(frame)
            img = Visualization.draw_landmarks_on_image(img, keypoints_with_scores, exercises)
            exercises[current_exercise].process(keypoints_with_scores)

            if time.time() - exercises[current_exercise].last_update_time <= inactive_time_limit:
                activity_detected = True

            Visualization.draw_counts(img, exercises)

            if activity_detected:
                last_activity_time = time.time()

            if time.time() - last_activity_time > inactive_time_limit:
                fc.sense.clear()
                for name, exercise in exercises.items():
                    if exercise.counter != 0:
                        if name == 'Bicep Curls':
                            Exercises.display_curl(exercise)
                        elif name == 'Squats':
                            Exercises.display_squat(exercise)
                    Exercises.reset_count(exercise)
                activity_detected = False

            if current_exercise == 'Bicep Curls':
                Visualization.update_curl_display(exercises['Bicep Curls'].counter)
            elif current_exercise == 'Squats':
                Visualization.update_squat_display(exercises['Squats'].counter)
            

            time.sleep(0.1)
            cv2.imshow("Landmark Visualization", np.array(img))
            if cv2.waitKey(1) & 0xFF == ord('q') or shutdown:
                fc.sense.clear()
                break
        
        cap.release()
        cv2.destroyAllWindows()

    thread = threading.Thread(target=listen_for_command)
    thread2 = threading.Thread(target=fitness_activate)
    
    thread.start()
    thread2.start()
    thread.join()
    thread2.join()

if __name__ == "__main__":
    main()
