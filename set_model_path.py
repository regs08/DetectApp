import os

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
default_model_path = os.path.join(current_dir, 'saved_models', 'grape_trunk_detect_ssd.tflite')
model_path = os.getenv('MODEL_PATH', 'default_model_path')

