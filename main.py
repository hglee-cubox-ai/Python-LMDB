from io import BytesIO
import os
from io import BytesIO

import lmdb
import cv2
from PIL import Image



if __name__ == '__main__':
    sample_names = os.listdir('samples')
    
    imgs = []
    for s_name in sample_names:
        img = Image.open(f'samples/{s_name}') 
        buffer = BytesIO()
        img.save(buffer, format='jpeg', quality=100)
        val = buffer.getvalue()
        
        imgs.append(val)
    
    ### Make LMDB ###
    with lmdb.open('./lmdb', map_size=1024**2, readahead=False) as env:
        total = 0
        for idx, img in enumerate(imgs):
            key = f'{idx}'.encode('utf-8')
            
            with env.begin(write=True) as txn:
                txn.put(key, img)
            
            total += 1
            
        with env.begin(write=True) as txn:
            txn.put('length'.encode('utf-8'), str(total).encode('utf-8')) 
    
    
    ### Load LMDB ###
    
    env = lmdb.open('./lmdb')
    
    with env.begin(write=False) as txn:
        img_bytes = txn.get('0'.encode('utf-8'))
        print(img_bytes[:10])
        
        length = txn.get('length'.encode('utf-8')).decode('utf-8')
        print(length)
    