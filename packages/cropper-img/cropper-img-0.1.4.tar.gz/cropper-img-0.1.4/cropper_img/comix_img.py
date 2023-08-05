from PIL import Image
import argparse
import os

class Main:
    def start(self):
        parser = argparse.ArgumentParser(description="Cropper image on parts")
        parser.add_argument('-no', '--name_open', type=str, required=False, default='com.jpg', help="path to open image")
        parser.add_argument('-m', '--margin', type=int, default=5, help="margin crop image")
        parser.add_argument('-p', '--part', type=int, default=9, help="parts crop image")
        parser.add_argument('-c', '--color', default='#fff', required=False, help="color fon image")
        parser.add_argument('-n', '--name', default='comix_new.jpg', help="name image")
        parser.add_argument('-o', '--output', type=str, required=False, default='', help="save in your path")
        args = parser.parse_args()

        #params create img
        margin = args.margin
        count_drop_img = args.part
        color_fon = args.color
        name_img = args.name
        path_open = args.name_open
        drop_img = Image.open(path_open)
        path_out = args.output

        size_img = list(drop_img.size)
        delta_marg = (count_drop_img * (margin * 2))-(margin * round(count_drop_img + 1))
        width_fon = size_img[0] + delta_marg
        height_fon = size_img[1] + delta_marg
        fon = Image.new('RGB', (width_fon, height_fon), color_fon)
        width_crop = round(size_img[0]/count_drop_img)
        height_crop = round(size_img[1]/count_drop_img)
        counts = lines = 0
        delta = round(margin)
        area = area_paste = [width_crop * counts, height_crop * lines, width_crop, height_crop]
        for i in range(0, count_drop_img * count_drop_img):
            count = drop_img.crop(area)
            fon.paste(count, area_paste)
            counts += 1
            if counts%count_drop_img == 0:
                counts = 0
                lines += 1
            delta_x = (delta * counts)
            delta_y = (delta * lines)
            width_map = width_crop * counts
            height_map = height_crop * lines
            area = [width_map, height_map, width_crop * (counts + 1), height_crop * (lines + 1)]
            area_paste = [width_map + delta_x, height_map + delta_y, (width_crop * (counts + 1)) + delta_x, (height_crop * (lines + 1)) + delta_y]
        if args.output:
            full_path = path_out + name_img
            if not os.path.exists(full_path):
                fon.save(full_path)
        else:
            fon.save(name_img)

if __name__== '__main__':
    Main().start()

def start():
    Main().start()