from qcloud_image import Client
from qcloud_image import CIUrl, CIFile, CIBuffer, CIUrls, CIFiles, CIBuffers

appid = '1251185167'
secret_id = 'AKIDiFYdT5XeaIl04utt2waz87sOfiY9ucV9'
secret_key = 'XrwmMgkY6OQFvMYVEixxiDSRAdqnUw84'
bucket = 'ocr'
client = Client(appid, secret_id, secret_key, bucket)
client.use_http()
client.set_timeout(30)

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
    return res['age']

def gender(filename=''):
    res = face_info(filename)
    return res['gender']

def beauty(filename=''):
    res = face_info(filename)
    return res['beauty']

def glass(filename=''):
    res = face_info(filename)
    return res['glass']

# 名片识别
# print (client.namecard_detect(CIFiles(['./1.jpg'])))
# print (client.face_detect(CIFile('./pengyuyan.jpg')))
# 人脸识别 'age': 23, 'gender': 99, 'glass': False, 'expression': 20, 'glasses': 0, 'mask': 0, 'hat': 0, 'beauty': 88,
# print (client.face_detect(CIFile('./pengyuyan.jpg')))
# {'code': 0, 'message': 'OK', 'data': {'session_id': '', 'image_height': 1728, 'image_width': 1152, 'face': [{'face_id': '2388370616815203618', 'x': 524, 'y': 303, 'height': 273.0, 'width': 273.0, 'pitch': 7, 'roll': -10, 'yaw': 10, 'age': 23, 'gender': 99, 'glass': False, 'expression': 20, 'glasses': 0, 'mask': 0, 'hat': 0, 'beauty': 88, 'face_shape': {'face_profile': [{'x': 536, 'y': 351}, {'x': 530, 'y': 378}, {'x': 525, 'y': 405}, {'x': 523, 'y': 432}, {'x': 525, 'y': 460}, {'x': 532, 'y': 486}, {'x': 544, 'y': 511}, {'x': 560, 'y': 532}, {'x': 579, 'y': 551}, {'x': 602, 'y': 565}, {'x': 628, 'y': 571}, {'x': 652, 'y': 568}, {'x': 672, 'y': 556}, {'x': 692, 'y': 542}, {'x': 710, 'y': 527}, {'x': 726, 'y': 510}, {'x': 740, 'y': 490}, {'x': 752, 'y': 470}, {'x': 762, 'y': 448}, {'x': 769, 'y': 425}, {'x': 774, 'y': 405}], 'left_eye': [{'x': 594, 'y': 367}, {'x': 603, 'y': 375}, {'x': 614, 'y': 381}, {'x': 627, 'y': 383}, {'x': 639, 'y': 384}, {'x': 633, 'y': 372}, {'x': 621, 'y': 364}, {'x': 607, 'y': 363}], 'right_eye': [{'x': 745, 'y': 395}, {'x': 735, 'y': 402}, {'x': 723, 'y': 404}, {'x': 711, 'y': 401}, {'x': 701, 'y': 395}, {'x': 710, 'y': 386}, {'x': 723, 'y': 383}, {'x': 735, 'y': 387}], 'left_eyebrow': [{'x': 576, 'y': 339}, {'x': 598, 'y': 340}, {'x': 621, 'y': 344}, {'x': 642, 'y': 352}, {'x': 664, 'y': 359}, {'x': 650, 'y': 337}, {'x': 624, 'y': 325}, {'x': 598, 'y': 322}], 'right_eyebrow': [{'x': 772, 'y': 372}, {'x': 753, 'y': 370}, {'x': 734, 'y': 368}, {'x': 714, 'y': 368}, {'x': 695, 'y': 367}, {'x': 712, 'y': 352}, {'x': 736, 'y': 349}, {'x': 760, 'y': 351}], 'mouth': [{'x': 597, 'y': 498}, {'x': 605, 'y': 513}, {'x': 618, 'y': 524}, {'x': 634, 'y': 529}, {'x': 650, 'y': 529}, {'x': 665, 'y': 522}, {'x': 679, 'y': 513}, {'x': 665, 'y': 504}, {'x': 651, 'y': 496}, {'x': 639, 'y': 497}, {'x': 628, 'y': 492}, {'x': 612, 'y': 494}, {'x': 609, 'y': 506}, {'x': 622, 'y': 513}, {'x': 636, 'y': 518}, {'x': 650, 'y': 517}, {'x': 665, 'y': 516}, {'x': 666, 'y': 509}, {'x': 652, 'y': 506}, {'x': 638, 'y': 503}, {'x': 628, 'y': 498}, {'x': 614, 'y': 497}], 'nose': [{'x': 665, 'y': 451}, {'x': 673, 'y': 390}, {'x': 661, 'y': 404}, {'x': 650, 'y': 418}, {'x': 638, 'y': 432}, {'x': 622, 'y': 448}, {'x': 640, 'y': 463}, {'x': 657, 'y': 471}, {'x': 674, 'y': 469}, {'x': 690, 'y': 462}, {'x': 685, 'y': 443}, {'x': 681, 'y': 425}, {'x': 677, 'y': 407}]}}]}, 'httpcode': 200}
# print (client.face_compare(CIFile('./king.jpg'),CIFile('./king1.jpg') ))
# {'code': 0, 'message': 'OK', 'data': {'session_id': '', 'similarity': 64.0}, 'httpcode': 200}
# 人脸比对
# print (client.face_compare(CIFile('./king.jpg'),CIFile('./king1.jpg') ))
# print (client.face_compare(CIFile('./king.jpg'),CIFile('./pengyuyan.jpg') ))
# print (client.face_compare(CIFile('./king1.jpg'),CIFile('./pengyuyan.jpg') ))
# {'code': 0, 'message': 'success', 'tags': [{'tag_name': '海报', 'tag_confidence': 14}, {'tag_name': '独照', 'tag_confidence': 12}, {'tag_name': '男孩', 'tag_confidence': 58}], 'httpcode': 200}
# print (client.tag_detect(CIFile('./pengyuyan.jpg')))
# {'code': 0, 'message': 'success', 'tags': [{'tag_name': '宠物', 'tag_confidence': 25}, {'tag_name': '狗', 'tag_confidence': 72}], 'httpcode': 200}
# 图像标签识别
# print (client.tag_detect(CIFile('./6.jpeg')))
# 身份证正面识别
# print (client.idcard_detect(CIFiles(['./card.jpg']), 0))

# print (client.face_idcardcompare('320523197309040018', '邓欲国', CIFile('./card.jpg')))
