import sys
sys.path.append('../../')
from RedisQ.GPUWorker import GPUWorker
from redis import Redis
from RedisQ.Base.Qjob import BaseJob
from RedisQ.Base.Qlist import LQ, LW, LD, HS, HJ
# from WSI.algorithm.code import *
from pyseri.serializer import serializer
import requests
import os
import json
import csv


class WSIPredictionContent(object):
    # those data is used for testing
    api = 'http://192.168.1.122:8000/api/v1/'
    patient = 'patients/'
    patient_id = '1'
    case = 'cases/'
    case_id = '2351cb63-ea0a-4f40-8fed-5a82761adb7e'
    accession = 'accessions/'
    accession_id = '1'
    image = 'images/'
    image_id = '1'
    cad = 'cads/'


class WSIJob(BaseJob):

    content = WSIPredictionContent()


class WSIConfig(object):

    gpu_load = 0.3
    gpu_memory = 0.3
    docker_path = './test'
    docker_image_tag = 'test_work'
    res_base = 'WSI/res'
    des_base = 'workout/WSI/des'

    @property
    def gpu_fraction(self):
        return (self.gpu_memory + self.gpu_load) * 0.5


def payload(job, config):
    print('playload running...')
    # get job
    content = job.content
    # get api information
    print('get resource info')
    response = requests.get(content.api + content.image + content.image_id + '/')
    if response.status_code != 200:
        raise Exception("can't get resource information")
    raw_uri = response.json().get('raw_file_path', None)
    filename = raw_uri.split('/')[-1]
    res = '{base}/{filename}'.format(
        base=config.res_base,
        filename=filename
    )
    # download the rawfile if there is not be 
    if not os.path.isfile(res):
        print('download raw file')
        response = requests.get(raw_uri)
        if response.status_code != 200:
            raise Exception("can't download raw files")
        with open(res, 'wb+') as f:
            f.write(response.content)
    
    des = '{base}/{filename}/'.format(
        base=config.des_base,
        filename=filename.split('.')[0]
    )
    # make destenation path if there not be
    if not os.path.isdir(des):
        os.mkdir(des)
 
    # run algorithm if there is not result
    files = os.listdir(des)
    if not files:
        print('prediction...')
        try:
            predict_one_wsi(res, des)
        except Exception as e:
            print(e)

    metadata = job.create_metadata()
    for file_name in files:
        if file_name.endswith('png') or file_name.endswith('jpg') or file_name.endswith('jpeg'):
            metadata.images.append(file_name)
        if file_name.endswith('csv'):
            with open('{des}/{file_name}'.format(des=des,file_name=file_name), 'r') as f:
                reader = csv.reader(f)
                rows = []
                for row in reader:
                    rows.append(row)
                for row in zip(*rows):
                    key = row[0]
                    values = row[1]
                    metadata.features[key] = values
    if not os.path.isfile('{des}/metadata.json'.format(des=des)):
        print('write metadata')
        with open('{des}/metadata.json'.format(des=des), 'w+') as f:
            j = serializer.dump(metadata)
            f.write(json.dumps(j))
    print('payload done')
    print('polling...')


def run_worker(host, port):
    conn = Redis(host=host, port=port)
    config = WSIConfig()
    worker = GPUWorker(connection=conn, config=config, job_hash=HJ, sign_hash=HS,
                       queue_list=LQ, working_list=LW, done_list=LD)
    print('polling...')
    worker.polling(config=config, payload=payload)

if __name__ == '__main__':
    while True:
        try:
            run_worker(host='192.168.1.122', port='6389')
        except KeyboardInterrupt as e:
            break
