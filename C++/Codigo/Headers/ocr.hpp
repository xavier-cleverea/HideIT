#pragma once

namespace hideit {

    class ocr 
    {
    private:
        char *lang;
        tesseract::TessBaseAPI *TessApi;
    public:
        ocr();
        ~ocr();
        void test();
        void* get_text_boxes(unsigned char*);
    };

}

#include "../Sources/ocr.cpp"
