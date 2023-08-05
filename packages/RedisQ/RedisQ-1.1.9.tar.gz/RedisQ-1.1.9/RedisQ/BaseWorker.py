import uuid
import os
import time
import requests
pid_file = 'worker.pid'

headers = {'Authorization':'Basic YWRtaW46YWRtaW4xMjM0NTY='}


class BaseWorker(object):
    """docstring for BaseWorker"""
    conn = None
    config = None
    queue_list = None
    working_list = None
    done_list = None
    sign_hash = None
    job_hash = None
    id = None

    def __init__(self, connection=None, config=None, job_hash=None, sign_hash=None, queue_list=None, working_list=None, done_list=None):
        if connection:
            self.conn = connection
            self.job_hash = job_hash
            self.id = uuid.uuid1()
            self.queue_list = queue_list(
                connection=self.conn, job_hash=job_hash)
            self.working_list = working_list(
                connection=self.conn, job_hash=job_hash, list_name='work_list_{}'.format(self.id))
            self.sign_hash = sign_hash(self.conn)
            self.sign_hash.sign_in(self, self.working_list)
            self.done_list = done_list(connection=self.conn, job_hash=job_hash)
        if config:
            self.config = config
        if os.path.isfile(pid_file):
            # 宣告前任死亡,继承前任的工作
            with open(pid_file, 'r') as f:
                id = f.read()
                dead_working_list = working_list(
                    connection=self.conn, job_hash=self.job_hash, list_name='work_list_{}'.format(id))
                dead_working_list.id = id
                for job in dead_working_list:
                    print('find a dead job')
                    self.working_list.queue(job)
                    print(self.working_list.len())
                self.sign_hash.sign_out(dead_working_list)

        with open(pid_file, 'w+') as f:
            f.write(str(self.id))

    def polling(self, payload=None, config=None):
            # with daemon.DaemonContext():
            while True:
                try:
                    if self.working_list.len() > 0 or self.queue_list.len() > 0:
                        self.management(payload, config)
                        job = self.working_list.pop_to(self.done_list)
                        data = {
                            'job_id':str(job.id),
                            'accession_id':str(job.content.accession_id),
                            'status':'finished',
                            'end_time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        }
                        response = requests.put('{api}/{tasks}/{job_id}/?format={format}'
                                .format(tasks='tasks',
                                        job_id=job.id,
                                        format='json',
                                        api='http://127.0.0.1/api/v1'),headers=headers,json=data)
                        if response.status_code != 200:
                            raise Exception(response.url, response.content)
                except KeyboardInterrupt as e:
                    os.remove(pid_file)
                    self.sign_hash.sign_out(self)
                    raise e
                else:
                    continue

    def management(self, payload, config):
        raise NotImplementedError('management should implement')
