import click
from RedisQ.scripts.DICOMpayload import run_worker as dicom_worker
from RedisQ.scripts.WSIpayload import run_worker as wsi_worker

@click.command()
@click.option('--worker', '-w', default='dicom', help="options: dicom, wsi")
@click.option('--num', '-n', default=1, help="options: int num")
@click.option('--host', '-h', default='127.0.0.1', help="options: server host")
@click.option('--port', '-p', default='6389', help="options: server port")
def cli(worker, num, host, port):
    if worker == 'dicom':
        dicom_worker(host, port)
    elif worker == 'wsi':
        wsi_worker(host, port)
