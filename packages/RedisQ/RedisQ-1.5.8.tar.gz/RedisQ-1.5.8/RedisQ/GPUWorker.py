from RedisQ.Base.Qlist import LW, LQ
from RedisQ.Base.Qjob import PredictionJob, PredictionContent
from RedisQ.BaseWorker import BaseWorker
import time
import requests
#import GPUtil as gpu


class GPUWorker(BaseWorker):
    """docstring for WSIWorker"""

    def management(self, payload, config):
        # TODO get system info and decide need to work
        if self.working_list.len() > 0:
            job = self.working_list.get(0)
        else:
            job = self.queue_list.pop_to(self.working_list)
        if not job:
            raise Exception('cant get job exception')

#        gpus = gpu.getGPUs()
#        availability = gpu.getAvailability(gpus, maxLoad=self.config.gpu_load,
 #                                                maxMemory=self.config.gpu_memory)
        availability = True
        if availability:
            response = requests.get('http://{api}/api/v1/{tasks}/{job_id}/?format={format}'
                                    .format(tasks='tasks',
                                            job_id=job.id,
                                            format='json',
                                            api=self.host), headers=self.headers)
            data = {}
            data.update(response.json())
            data.update({
                'status': 'running',
                'start_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            })
            response = requests.put('http://{api}/api/v1/{tasks}/{job_id}/?format={format}'
                                    .format(tasks='tasks',
                                            job_id=job.id,
                                            format='json',
                                            api=self.host), headers=self.headers, json=data)
            if response.status_code != 200:
                raise Exception(response.url, response.content)
            payload(job, config)
        else:
            self.working_list.re_queue(self.queue_list)
