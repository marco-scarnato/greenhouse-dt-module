FROM python:3.12

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Copy the TensorFlow model directory (adjust if it's outside the root)
# This step is not needed if the model is already inside the project folder
# Otherwise, you can add:
# COPY path/to/cnn_no_aug /app/cnn_no_aug

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run your app
CMD ["python", "-u", "main.py"]
