import sys
sys.path.append('../../')
from RedisQ.Base.Qlist import LQ,LD,HJ,HS
from RedisQ.Base.tools import fetch_job
from redis import Redis
from RedisQ.Base.Qjob import BaseJob
from RedisQ.scripts.WSIpayload import WSIJob
import time
conn = Redis(host='192.168.1.122', port='6389')
hs = HS(connection=conn)
ld = LD(connection=conn, job_hash = HJ)
lq = LQ(connection=conn, job_hash = HJ)


# for i, job in enumerate(lq):
#     print(job.id)
#     print(conn.hget('job_hash', job.id))
#     job = fetch_job(conn, job.id)
#     print(job)
#     lq.pop()

for _ in range(20):
    job = WSIJob()
    lq = LQ(connection = conn, job_hash = HJ)
    lq.queue(job)

while True:

    print('queue work {}'.format(lq.len()))
    print('done work {}'.format(ld.len()))
    print('=================')
    time.sleep(5)
