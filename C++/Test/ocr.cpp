#include "test.hpp"

Pix* image_factory(const char* source) {
    Pix *image,*image1,*image2;
    image = pixRead(source);
    printf("%i\n",image->d);
    //image = pixScale(image,0.8,0.8);
    //printf("%i\n",image->d);
    image = pixConvertRGBToGray(image,0.3,0.3,0.4);
    printf("%i\n",image->d);

    //pixDestroy(&image1);
    //pixDestroy(&image2);
    return image;
}

class PARAMS {
public:
    static Pix* image;
    static hideit::ocr ocr;
};

hideit::ocr PARAMS::ocr = hideit::ocr();
Pix* PARAMS::image = image_factory("Test/Resources/Test-Image2.png");

void test_get_text_boxes() {
    PARAMS::ocr.get_text_boxes(PARAMS::image);
}

MAIN_TEST(test_get_text_boxes)