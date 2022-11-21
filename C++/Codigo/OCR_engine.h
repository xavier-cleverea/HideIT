#pragma once

#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include "tessbaseapi.h"
class OCR_engine {
    
private:
    tesseract::TessBaseAPI *api;
public:
    
    void test();
    
}
