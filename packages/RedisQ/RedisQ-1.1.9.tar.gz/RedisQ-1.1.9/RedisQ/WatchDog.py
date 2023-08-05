
# Notifier example from tutorial
#
# See: http://github.com/seb-m/pyinotify/wiki/Tutorial
#
import pyinotify
import json
import functools
import requests
wm = pyinotify.WatchManager()  # Watch Manager
watch_dir_name = 'workout'
watch_dir = './{0}/'.format(watch_dir_name)


class EventHandler(pyinotify.ProcessEvent):

    def process_IN_CREATE(self, event):
        print("Create:{0}".format(event.pathname))
        base_path = '/'.join(event.pathname.split('/')[:-1])
        if event.name == 'metadata.json':
            # if metadata.json create
            with open(event.pathname, 'r') as f:
                _json = f.read()
                j = json.loads(_json)
                job = j.get('job', None)
                api = job['api']
                cad_api = api + job['cad']
                image_api = api + job['image']
                accession_id = job['accession_id']

                if not job:
                    raise Exception("no job content")

                features = j.get('features', None)
                images = j.get('images', None)
                if features:
                    # upload features
                    headers = {
                        "Authorization": "Basic YWRtaW46YWRtaW4xMjM0NTY="}
                    response = requests.post(cad_api, headers=headers, json={
                                             "accession_id": accession_id, "result": features})
                    print(response.content)
                    if response.status_code != 201:
                        raise Exception('upload err!')
                    cad_id = response.json().get('id', None)
                    if cad_id:
                        if images:
                            for image in images:
                                # upload images
                                headers = {
                                    "Authorization": "Basic YWRtaW46YWRtaW4xMjM0NTY="}
                                data = {'cad_id': cad_id}
                                files = [
                                    ('raw_file_path', (image, open(base_path + image, 'rb'), 'image/png'))]
                                response = requests.post(
                                    image_api, headers=headers, data=data, files=files)
                                print(response.content)
                                if response.status_code != 201:
                                    raise Exception('upload err!')

    def process_IN_DELETE(self, event):
        print("Removing:{0}".format(event.pathname))


def on_loop(notifier):
    """
    Dummy function called after each event loop, this method only
    ensures the child process eventually exits (after 5 iterations).
    """
    pass


handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(watch_dir, pyinotify.ALL_EVENTS, rec=True)
while True:
    try:
        notifier.loop()
    except KeyboardInterrupt as e:
        exit()
    else:
        print('something err re-loop ...')
        continue

# on_loop_func = functools.partial(on_loop)

# try:
#     notifier.loop(daemonize=True, callback=on_loop_func,
#                   pid_file='/tmp/pyinotify.pid', stdout='/tmp/pyinotify.log')
# except pyinotify.NotifierError as err:
#     print >> sys.stderr, err
