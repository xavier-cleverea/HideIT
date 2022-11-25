#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <iostream> 
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>

#define UNIMPLEMENTED fprintf(stderr,"%s:%d: %s is not implemented.\n", __FILE__, __LINE__, __PRETTY_FUNCTION__);


struct coords {
    int x1, y1, x2, y2;
};
