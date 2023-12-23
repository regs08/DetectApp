import time


class FPSUtility:
    def __init__(self, avg_frame_count=5):
        self.avg_frame_count = avg_frame_count
        self.frame_counter = 0
        self.start_time = time.time()
        self.fps = 0

    def update(self):
        """Update the frame counter and recalculate FPS."""
        self.frame_counter += 1
        if self.frame_counter % self.avg_frame_count == 0:
            end_time = time.time()
            self.fps = self.avg_frame_count / (end_time - self.start_time)
            self.start_time = end_time

    def get_fps(self):
        return self.fps
