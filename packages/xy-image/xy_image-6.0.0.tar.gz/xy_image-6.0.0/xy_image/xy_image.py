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
    图像标签识别{'code': 0, 'message': 'success', 'tags': [{'tag_name': '宠物', 'tag_confidence': 25}, {'tag_name': '狗', 'tag_confidence': 72}], 'httpcode': 200}
'''
def image_info(filename=''):
    if filename == '':
        return -1
    info = client.tag_detect(CIFile(filename))
    if info['code'] == 0:
        return info['tags']
    else:
        return -1
