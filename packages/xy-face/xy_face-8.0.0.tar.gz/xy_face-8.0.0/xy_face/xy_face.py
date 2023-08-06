from qcloud_image import Client
from qcloud_image import CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers

appid = '1251185167'
secret_id = 'AKIDiFYdT5XeaIl04utt2waz87sOfiY9ucV9'
secret_key = 'XrwmMgkY6OQFvMYVEixxiDSRAdqnUw84'
bucket = 'ocr'
client = Client(appid, secret_id, secret_key, bucket)
client.use_http()
client.set_timeout(30)

''' 返回人脸信息'''
def face_info(filename=''):
    if filename == '':
        return -1
    info = client.face_detect(CIFile(filename))

    if info['data']['face']:
        res = info['data']['face'][0]
        res_dict = {
        'age':res['age'],
        'gender':res['gender'],
        'beauty':res['beauty'],
        'glass':res['glass']
        }
        return res_dict
    else:
        return -1

def age(filename=''):
    res = face_info(filename)
    if res == -1:
        return -1
    return res['age']

def gender(filename=''):
    res = face_info(filename)
    if res == -1:
        return -1
    return res['gender']

def beauty(filename=''):
    res = face_info(filename)
    if res == -1:
        return -1
    return res['beauty']

def glass(filename=''):
    res = face_info(filename)
    if res == -1:
        return -1
    return res['glass']

'''人脸相似度对比，返回相似度'similarity': 77.0'''
def compare(filename1,filename2):
    if not filename1 or not filename2:
        return -1
    res = client.face_compare(CIFile(filename1),CIFile(filename2))
    if res['code'] != 0:
        return -1
    return res['data']['similarity']
