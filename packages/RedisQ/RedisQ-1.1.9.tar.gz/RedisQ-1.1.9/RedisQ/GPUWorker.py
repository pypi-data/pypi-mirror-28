from RedisQ.Base.Qlist import LW, LQ
from RedisQ.Base.Qjob import PredictionJob, PredictionContent
from RedisQ.BaseWorker import BaseWorker
import time
import requests
#import GPUtil as gpu

headers = {'Authorization':'Basic YWRtaW46YWRtaW4xMjM0NTY='}


class GPUWorker(BaseWorker):
    """docstring for WSIWorker"""

    def management(self, payload, config):
        # TODO get system info and decide need to work
        if self.working_list.len() > 0:
            job = self.working_list.get(0)
        else:
            job = self.queue_list.pop_to(self.working_list)
        if not job:
            raise Exception('can not get a job instance')

#        gpus = gpu.getGPUs()
#        availability = gpu.getAvailability(gpus, maxLoad=self.config.gpu_load,
 #                                                maxMemory=self.config.gpu_memory)
        availability = True
        if availability:
            data = {
                'job_id':str(job.id),
                'accession_id':str(job.content.accession_id),
                'status':'running',
                'start_time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
            response = requests.put('{api}/{tasks}/{job_id}/?format={format}'
                    .format(tasks='tasks',
                            job_id=job.id,
                            format='json',
                            api='http://127.0.0.1/api/v1'),headers=headers,json=data)
            if response.status_code != 200:
                raise Exception(response.url, response.content)
            payload(job, config)
        else:
            self.working_list.re_queue(self.queue_list)

