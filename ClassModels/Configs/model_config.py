import os


class ModelConfig:
    def __init__(self, model_path, enable_edgetpu=False, num_threads=1, conf_thresh=0.5, max_results=3):
        self.model_path = model_path
        assert os.path.exists(model_path), 'model path not found !'
        self.enable_edgetpu = enable_edgetpu
        self.num_threads = num_threads
        self.conf_thresh = conf_thresh
        self.max_results = max_results

    def __str__(self):
        return f"ModelConfig(model_path={self.model_path}, enable_edgetpu={self.enable_edgetpu}, num_threads={self.num_threads}, conf_thresh={self.conf_thresh}, max_results={self.max_results})"

    def to_dict(self):
        return vars(self)