import os
# Todo get the model path set or configure it with mqtt


grape_model_file = 'grape_trunk_detect_ssd.tflite'
pretrained_coco_model_file = 'efficientdet_lite0.tflite'
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
default_model_path = os.path.join(current_dir, 'saved_models', grape_model_file)
model_path = default_model_path #os.getenv('MODEL_PATH', 'default_model_path')
