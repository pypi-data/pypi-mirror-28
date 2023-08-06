# Sacrina Python SDK

## System Requirements

Sacrina Python SDK runs on Linux OS and Python 3.

## Installation

### Use pip

Run the following command to install:

    pip install sacrina
    
### Use git

Clone the repo:

    git clone https://github.com/sacrina/sacrina-python.git

Go into the sacrina-python folder, install the requirements using pip and install using setup.py:

    pip install -r requirements.txt
    python setup.py install

## Configuration

Register for Sacrina account at https://sacrina.com and get your key. Then use:

    import sacrinasdk
    sacrinasdk = new sacrinasdk()
    sacrinasdk.add_key('[your API key]')

## Usage

### Add dataset

You can add dataset as a list as:

    lis = ['data 1', 'data 2', 'data 3',..]
    sacrinasdk.add_dataset(list)
    
Or you can add data one by one as:

    sacrinasdk.add_data('Data 1')

### Upload dataset

Upload your dataset to Sacrina using:

    sacrinasdk.upload_dataset()
    
### Select an existing dataset

You can select an exisiting dataset using the id parameter:

    sacrinasdk.select_dataset([dataset_id])

### Create model

To create a new model using your added dataset, use the following:

    sacrinasdk.create_model()

### Select model

To select an existing model using its id, use the following:

    sacrinasdk.select_model([model_id])

### Train model

To start your model training, use the following:

    sacrinasdk.train_model()

### Check model status

To check the status of training, use the following:

    sacrinasdk.check_model_status()

### Create project

To create a new project, use the following:

    sacrinasdk.create_project(gen, sector_min, sector_max)

### Select project

To select an existing project using its id, use the following:

    sacrinasdk.select_project(project_id)

### Execute project

To execute the selected project, use the following:

    sacrinasdk.execute_project()

### Check project status

To check the project status, use the following:

    sacrinasdk.check_project_status()

### Download results

To download the results of the selected project, use the following:

    sacrinasdk.download_results()
