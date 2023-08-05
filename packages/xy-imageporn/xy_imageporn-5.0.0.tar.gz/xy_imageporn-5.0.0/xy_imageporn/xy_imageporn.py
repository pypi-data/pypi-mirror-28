from qcloud_image import Client
from qcloud_image import CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers

appid = '1251185167'
secret_id = 'AKIDiFYdT5XeaIl04utt2waz87sOfiY9ucV9'
secret_key = 'XrwmMgkY6OQFvMYVEixxiDSRAdqnUw84'
bucket = 'ocr'
client = Client(appid, secret_id, secret_key, bucket)
client.use_http()
client.set_timeout(30)
'''
    {'result_list': [{'code': 0, 'message': 'success', 'filename': './king.jpg', 'data': {'result': 0, 'forbid_status': 0, 'confidence': 3.755, 'hot_score': 11.973, 'normal_score': 88.027, 'porn_score': 0.0}}], 'httpcode': 200}
'''
def porn_info(filename=''):
    if filename == '':
        return -1
    info = client.porn_detect(CIFiles([filename,]))
    # print(info['result_list'])
    res = info['result_list'][0]
    if res['code'] == 0:
        del res['data']['forbid_status']
        return res['data']
    else:
        return -1

def main():
    print(porn_info('king.jpg'))

if __name__ == '__main__':
    main()
