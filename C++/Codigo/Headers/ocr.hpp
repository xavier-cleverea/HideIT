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

        char* get_text(int,int,int,int);
        BOXA* get_components();

        tesseract::ResultIterator* get_text_boxes(unsigned char*,int,int,int,int);
        tesseract::ResultIterator* get_text_boxes(Pix*);

    };

}

#include "../Sources/ocr.cpp"
