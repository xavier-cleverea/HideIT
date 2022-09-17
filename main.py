from hideit import *
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ba','--blur-all', action='store_true', default=False, help='Blur all text in the image')
    parser.add_argument('-bd','--blur-digits', action='store_true', default=False, help='Blur all digits in image')
    parser.add_argument('-bw','--blur-words', nargs='+', default=[],help='blur especific words')
    parser.add_argument('-i','--images', nargs='+', help='name of images')

    parser.add_argument('-d','--directory', nargs='?',default='resources/', help='name of the directory of images')
    parser.add_argument('-s','--store', nargs='?', default='out/',help='name of the directory to store images')
    args = parser.parse_args()

    print(vars(args))

    for images in args.images:
        img = ImageProcessor(images,args.directory)
        if args.blur_all:
            img.blur_all_text()
        else:
            if args.blur_digits:
                img.blur_if_regex(r'[0-9.,](.|,[0-9]+)?')
            for word in args.blur_words:
                img.blur_if_contains(word)
        img.save()
    
if __name__ == '__main__':
    main()
