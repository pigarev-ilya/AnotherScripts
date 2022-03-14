import requests
import time
from tqdm import tqdm
import json


class YaUploaderPhotoVk:
    def __init__(self, id_vk, token_ya, name_folder):
        self.id = id_vk
        self.token_ya = token_ya
        self.headers = {'Content-type': 'application/json',
                        'Authorization': 'OAuth {}'.format(self.token_ya)}
        self.name_folder = name_folder
        self.report = {self.id: []}

    def get_photo(self):
        request_settings = {
            'user_id': self.id,
            'v': '5.131',
            'album_id': 'profile',
            'count': '5',
            'rev': '1',
            'extended': '1',
            'access_token': ''
        }
        url = 'https://api.vk.com/method/photos.get?'
        response_ph = requests.get(url, params=request_settings).json()
        print(response_ph)
        create_folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params_create_folder = {'path': self.name_folder}
        requests.put(create_folder_url, headers=self.headers, params=params_create_folder)
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        if len(response_ph['response']['items']) < int(request_settings['count']) + 1:
            progress_list = [x for x in range(1, len(response_ph['response']['items']) + 1)]
        else:
            progress_list = [x for x in range(1, int(request_settings['count']) + 1)]

        for index_photo in tqdm(progress_list):
            file_name = str(response_ph['response']['items'][index_photo - 1]['likes']['count'])
            file_url = response_ph['response']['items'][index_photo - 1]['sizes'][-1]['url']
            file_size = response_ph['response']['items'][index_photo - 1]['sizes'][-1]['type']
            params_upload_ph = {'path': self.name_folder + '/' + file_name,
                                'url': file_url}
            requests.post(url=upload_url, headers=self.headers, params=params_upload_ph)
            time.sleep(1)
            self.report[self.id].append({'file' + str(index_photo) + '-name': file_name + '.jpg',
                                         'size': file_size})
        return json.dumps(self.report, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    uploader = YaUploaderPhotoVk(552934290, 'YANDEX TOKEN', 'VK photo')
    a = uploader.get_photo()
    print(a)
