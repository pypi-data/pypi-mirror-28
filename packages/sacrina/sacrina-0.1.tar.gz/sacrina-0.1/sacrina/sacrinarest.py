#!/usr/bin/python
import requests
import json

class sacrinarest:
    '''Use Sacrina API in python'''

    def __init__(self):
        self.key = None
        self.dataset = []
        self.headers = {}
        self.dataset_id = None
        self.model_id = None
        self.project_id = None
        self.results = []

    #add key
    def add_key(self,key):
        self.key = key
        self.headers = {
            "Accept": "application/json",
            "Api-Key": self.key,
        }
        
    #create dataset
    def add_data(self, input_string):
        if not isinstance(input_string, str):
            print("input_string paramter is not string, please check your input")
        else:
            self.dataset.append(input_string)

    def add_dataset(self, input_array):
        if not isinstance(input_array, list) or not all(isinstance(item, str) for item in input_array):
            print("input_array paramter is not an array of strings, please check your input")
        else:
            self.dataset.extend(input_array)

    #upload dataset to sacrina

    def upload_dataset(self):
        #create dataset
        url = 'https://sacrina.com/REST/learning/datasets/'
        params = {'title':'my-dataset','description':'asdasdasdasd'}
        response = requests.post(url, headers = self.headers, data = params, verify=False)
        if response.status_code != 201:
            return "error creating dataset"
        response_json = json.loads(response.text)
        self.dataset_id = response_json['id']
        #upload data to dataset
        url = 'https://sacrina.com/REST/learning/datas/'
        for item in self.dataset:
            params = {'title':'data1', 'dataset_id': 'https://sacrina.com/REST/learning/datasets/' + str(self.dataset_id) + '/', 'content': str(item) }
            response = requests.post(url, headers = self.headers, data = params, verify=False)
            if response.status_code != 201:
                return "error uploading data to dataset"
        return "Dataset upload completed"

        
    #add an existing dataset
    def select_dataset(self, dataset_id):
        self.dataset_id = dataset_id
        url = 'https://sacrina.com/REST/learning/datasets/' + str(self.dataset_id) + '/'
        response = requests.get(url, headers = self.headers, verify=False)
        if response.status_code != 200:
            return "error"
        else:
            return response.text

    #create a new model

    def create_model(self):
        url = 'https://sacrina.com/REST/learning/models/'
        params = {'title':'mymodel','datasets': 'https://sacrina.com/REST/learning/datasets/' + str(self.dataset_id) + '/'}
        response = requests.post(url, headers = self.headers, data = params, verify=False)
        if response.status_code != 201:
            return "error"
        else:
            response_json = json.loads(response.text)
            self.model_id = response_json['id']
            return response.text


    #add an old model
    def select_model(self, model_id):
        self.model_id = model_id
        url = 'https://sacrina.com/REST/learning/models/' + str(self.model_id) + '/'
        response = requests.get(url, headers = self.headers, verify=False)
        return response.text
        if response.status_code != 200:
            return "error"
        else:
            return response.text

    #train the model
    def train_model(self):
        url = 'https://sacrina.com/REST/learning/models/' + str(self.model_id) + '/?train'
        response = requests.get(url, headers = self.headers, verify=False)
        if response.status_code != 200:
            return "error"
        else:
            return response.text

    #check model training status
    def check_model_status(self):
        url = 'https://sacrina.com/REST/learning/models/' + str(self.model_id) + '/'
        response = requests.get(url, headers = self.headers, verify=False)
        if response.status_code != 200:
            return "error"
        else:
            response_json = json.loads(response.text)
            status = response_json['status']
            return status

    #create a project with the model
    def create_project(self,gen, sector_min, sector_max):
        url = 'https://sacrina.com/REST/production/projects/'
        params = {'name':'myproject','model': 'https://sacrina.com/REST/learning/models/' + str(self.model_id) + '/', 'gen': gen, 'sector_min': sector_min, 'sector_max': sector_max }
        response = requests.post(url, headers = self.headers, data = params, verify=False)
        if response.status_code != 201:
            return "error"
        else:
            response_json = json.loads(response.text) 
            self.project_id = response_json['id']
            return response.text
    #add an existing project
    def select_project(self, project_id):
        self.project_id = project_id
        url = 'https://sacrina.com/REST/production/projects/' + str(self.project_id) + '/'
        response = requests.get(url, headers = self.headers, verify=False)
        return response.text
        if response.status_code != 200:
            return "error"
        else:
            return response.text

    #execute the project
    def execute_project(self):
        url = 'https://sacrina.com/REST/production/projects/' + + str(self.project_id) + '/?execute'
        response = requests.get(url, headers = self.headers, verify=False)
        if response.status_code != 200:
            return "error"
        else:
            return response.text

    #check project status
    def check_project_status(self):
        url = 'https://sacrina.com/REST/production/projects/' + str(self.project_id) + '/'
        response = requests.get(url, headers = self.headers, verify=False)
        if response.status_code != 200:
            return "error"
        else:
            return response.text

    #download results
    def download_results(self):
        url = 'https://sacrina.com/REST/production/results/?project_id=' + str(self.project_id)
        response = requests.get(url, headers = self.headers, verify=False)
        if response.status_code != 200:
            return "error"
        else:
            response_json = json.loads(response.text)
            for item in response_json:
                item = dict(item)
                self.results.append(item["content"])
            return self.results

        
