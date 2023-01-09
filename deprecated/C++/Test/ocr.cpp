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
    static hideit::driver driver;
};

hideit::ocr PARAMS::ocr = hideit::ocr();
hideit::driver PARAMS::driver = hideit::driver();
Pix* PARAMS::image = image_factory("Test/Resources/Test-Image2.png");

void test_get_text_boxes() {
    tesseract::PageIteratorLevel level = tesseract::RIL_WORD;
    //el nivel define si se lee el texto letra por letra, palabra por palabra, linea por linea etc.

    auto it = PARAMS::ocr.get_text_boxes(PARAMS::image);
    if(it != 0){
        while(it->Next(level)) {
            const char* word = it->GetUTF8Text(level);
            float conf = it->Confidence(level);
            int x1, y1, x2, y2;
            it->BoundingBox(level, &x1, &y1, &x2, &y2);
//             printf("word: '%s';  \tconf: %.2f; BoundingBox: %d,%d,%d,%d;\n", word, conf, x1, y1, x2, y2);
            delete[] word;
        }
    }
}

MAIN_TEST(test_get_text_boxes)
