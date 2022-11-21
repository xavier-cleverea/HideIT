#pragma once

namespace hideit {

    class ocr 
    {

    public:
        ocr();
        ~ocr();
        void* get_text_boxes(unsigned char*);
    };

}

#include "../Sources/ocr.cpp"