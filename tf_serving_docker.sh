docker run -t --rm -p 8501:8501 \
    -v "/Users/bharathkkb/Documents/cs161/ASL-detector/asl_classifier_model:/models/asl_classifier_model" \
    -e MODEL_NAME=asl_classifier_model \
    tensorflow/serving
