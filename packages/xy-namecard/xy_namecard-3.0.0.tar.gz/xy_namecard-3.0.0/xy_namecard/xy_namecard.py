from qcloud_image import Client
from qcloud_image import CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers

appid = '1251185167'
secret_id = 'AKIDiFYdT5XeaIl04utt2waz87sOfiY9ucV9'
secret_key = 'XrwmMgkY6OQFvMYVEixxiDSRAdqnUw84'
bucket = 'ocr'
client = Client(appid, secret_id, secret_key, bucket)
client.use_http()
client.set_timeout(30)

'''返回名片信息'''
def namecard_info(filename=''):
    if filename == '':
        return -1
    info = client.namecard_detect(CIFiles([filename]))
    res = info['result_list'][0]
    if res['code'] == 0:
        return res['data']
    else:
        return -1
