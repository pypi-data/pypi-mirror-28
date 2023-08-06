import sys
sys.path.append('../../')
from RedisQ.Base.Qlist import LQ, LD, HJ, HS, LF
from RedisQ.Base.tools import fetch_job
from redis import Redis
from RedisQ.Base.Qjob import BaseJob
from RedisQ.scripts.DICOMpayload import DICOMJob
import time


def run_test(host='127.0.0.1', port='6389', num=1):
    conn = Redis(host=host, port=port)
    hs = HS(connection=conn)
    ld = LD(connection=conn, job_hash=HJ)
    lq = LQ(connection=conn, job_hash=HJ)
    lf = LF(connection=conn, job_hash=HJ)

    for i, job in enumerate(lq):
        print(job.id)
        print(conn.hget('job_hash', job.id))
        job = fetch_job(conn, job.id)
        print(job)
        lq.pop()

    for _ in range(num):
        job = DICOMJob()
        job.content.api = 'http://{host}/api/v1/'.format(host=host)
        lq = LQ(connection=conn, job_hash=HJ)
        lq.queue(job)

    while True:

        print('queue work {}'.format(lq.len()))
        print('working workers {}'.format(hs.get_member()))
        print('done work {}'.format(ld.len()))
        print('failed work {}'.format(lf.len()))
        print('=================')
        time.sleep(5)
if __name__ == '__main__':
    run_test()
