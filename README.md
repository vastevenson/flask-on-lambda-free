# Flask on Lambda - Python 3.12 ARM64 Setup

This project demonstrates how to deploy a Flask application on AWS Lambda using Python 3.12 on ARM64 architecture with custom Lambda layers.

## Prerequisites

- macOS, Linux, or Windows with Python 3.12 support
- AWS CLI configured with appropriate permissions
- Basic knowledge of AWS Lambda and Python virtual environments

## Setup Instructions

### 1. Install Python 3.12

First, ensure you have Python 3.12 installed on your local machine:

**macOS (using Homebrew):**
```bash
brew install python@3.12
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip
```

**Windows:**
Download and install from [python.org](https://www.python.org/downloads/)

### 2. Create Virtual Environment

Create and activate a Python 3.12 virtual environment:

```bash
python3.12 -m venv lambda312
source lambda312/bin/activate  # On Windows: lambda312\Scripts\activate
```

Verify the Python version:
```bash
python --version  # Should output Python 3.12.x
```

### 3. Create Lambda Layers

#### Flask Layer

Create the Flask dependency layer:

```bash
mkdir -p flask-layer/python
pip install Flask -t flask-layer/python
cd flask-layer
zip -r ../flask-layer.zip python
cd ..
```

#### Lambda WSGI Layer

Create the lambda-wsgi dependency layer:

```bash
mkdir -p lambda_wsgi-layer/python
pip install lambda-wsgi -t lambda_wsgi-layer/python
cd lambda_wsgi-layer
zip -r ../lambda_wsgi-layer.zip python
cd ..
```

#### Serverless WSGI Layer

Create the serverless-wsgi dependency layer:

```bash
mkdir -p serverless-wsgi-layer/python
pip install serverless-wsgi -t serverless-wsgi-layer/python
cd serverless-wsgi-layer
zip -r ../serverless-wsgi-layer.zip python
cd ..
```

### 4. Upload Lambda Layers to AWS

Upload each layer to AWS Lambda, ensuring you specify:
- **Architecture**: ARM64
- **Runtime**: Python 3.12

You can upload via AWS Console or AWS CLI:

```bash
# Example AWS CLI commands (replace with your layer names and descriptions)
aws lambda publish-layer-version \
    --layer-name flask-layer \
    --description "Flask framework for Python 3.12 ARM64" \
    --zip-file fileb://flask-layer.zip \
    --compatible-architectures arm64 \
    --compatible-runtimes python3.12

aws lambda publish-layer-version \
    --layer-name lambda-wsgi-layer \
    --description "Lambda WSGI adapter for Python 3.12 ARM64" \
    --zip-file fileb://lambda_wsgi-layer.zip \
    --compatible-architectures arm64 \
    --compatible-runtimes python3.12

aws lambda publish-layer-version \
    --layer-name serverless-wsgi-layer \
    --description "Serverless WSGI for Python 3.12 ARM64" \
    --zip-file fileb://serverless-wsgi-layer.zip \
    --compatible-architectures arm64 \
    --compatible-runtimes python3.12
```

### 5. Deploy Your Lambda Function

1. Create a ZIP file containing your `lambda_function.py`
2. Upload to AWS Lambda
3. Attach the three layers you created
4. Set the runtime to Python 3.12
5. Set the architecture to ARM64

## Project Structure

```
flask-on-lambda-free/
├── lambda_function.py    # Main Lambda handler
├── README.md            # This file
├── flask-layer.zip      # Flask dependency layer
├── lambda_wsgi-layer.zip # Lambda WSGI layer
└── serverless-wsgi-layer.zip # Serverless WSGI layer
```

## Lambda Function Code

The main Lambda function (`lambda_function.py`) contains:

```python
from flask import Flask
from serverless_wsgi import handle_request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask + serverless-wsgi in a Lambda layer!"

def lambda_handler(event, context):
    return handle_request(app, event, context)
```

## Testing

After deployment, you can test your Lambda function through:
- AWS Lambda Console
- API Gateway (if configured)
- AWS CLI

## Troubleshooting

- **Architecture Mismatch**: Ensure all layers and the function use ARM64 architecture
- **Runtime Issues**: Verify Python 3.12 runtime is selected
- **Dependency Errors**: Check that all required packages are included in the layers
- **Memory/Timeout**: Adjust Lambda function configuration as needed

## Cleanup

To clean up local files after deployment:

```bash
rm -rf lambda312/ flask-layer/ lambda_wsgi-layer/ serverless-wsgi-layer/
rm *.zip
```

## License

This project is open source and available under the [MIT License](LICENSE). 