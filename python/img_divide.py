from PIL import Image
import os

def image_crop(infilename, save_path):
    img = Image.open(infilename)
    (img_w, img_h) = img.size
    print(img.size)
    
    # Crop size
    grid_w = 100
    grid_h = 100
    range_w = img_w // grid_w
    range_h = img_h // grid_h
    print(range_w, range_h)
    
    i = 0 
    
    for w in range(range_w):
        for h in range(range_h):
            bbox = (h * grid_w, w * grid_h, (h + 1) * grid_w, (w + 1) * grid_h)
            print(h * grid_w, w * grid_h, (h + 1) * grid_w, (w + 1) * grid_h)
            
            crop_img = img.crop(bbox)
            
            fname = "{}.jpg".format("{0:05d}".format(i))
            savename = save_path + fname
            crop_img.save(savename)
            print('save file ' + savename + '.....')
            i += 1
            
if __name__ == '__main__':
    input_image_path = "C:/kkt/2024_07_ColonyCounter/Colony_Image/50.Streptococcus agalactiae.jpg"
    output_save_path = "C:/kkt/2024_07_ColonyCounter/Resize_Img/re.50.Streptococcus agalactiae/" 
    os.makedirs(output_save_path, exist_ok=True) 
    image_crop(input_image_path, output_save_path)