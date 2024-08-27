import fitness_core as fc
from fitness_core import np, ImageDraw, ImageFont


class Visualization:
    @staticmethod
    def draw_counts(img, exercise_counters):
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 40)
        for idx, (name, counter) in enumerate(exercise_counters.items()):
            draw.text((10, 50 + idx * 50), f'{name}: {counter.counter}', fill=(255, 255, 255), font=font)

    @staticmethod
    def draw_landmarks_on_image(img, keypoints_with_scores, exercises):
        draw = ImageDraw.Draw(img)
        width, height = img.size
        connections = [(5, 7), (7, 9), (11, 13)]
        for point1, point2 in connections:
            if keypoints_with_scores[point1][2] > fc.CONFIDENCE_THRESHOLD and keypoints_with_scores[point2][2] > fc.CONFIDENCE_THRESHOLD:
                draw.line(
                    [(keypoints_with_scores[point1][1] * width, keypoints_with_scores[point1][0] * height),
                     (keypoints_with_scores[point2][1] * width, keypoints_with_scores[point2][0] * height)],
                    fill=(0, 255, 0), width=2
                )
        for keypoint in keypoints_with_scores:
            y, x, score = keypoint
            if score > fc.CONFIDENCE_THRESHOLD:
                draw.ellipse(
                    [(x * width - 2, y * height - 2), (x * width + 2, y * height + 2)],
                    fill=(255, 0, 0)
                )
        for exercise in exercises.values():
            exercise.process(keypoints_with_scores)
        return img

    @staticmethod
    def update_curl_display(curl_count):
        total_leds = 64
        for i in range(min(curl_count, total_leds)):
            x = i % 8
            y = i // 8
            fc.sense.set_pixel(x, y, fc.green)

    @staticmethod
    def update_squat_display(squat_count):
        total_leds = 64
        for i in range(min(squat_count, total_leds)):
            x = 7 - (i % 8)
            y = 7 - (i // 8)
            fc.sense.set_pixel(x, y, fc.purple)
