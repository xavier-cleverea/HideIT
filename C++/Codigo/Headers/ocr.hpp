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
        void* get_text_boxes(unsigned char*,int,int,int,int);
        void* get_text_boxes(Pix*);
        char* get_text(int,int,int,int);
        BOXA* get_components();
    };

}

#include "../Sources/ocr.cpp"
