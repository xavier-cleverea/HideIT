#pragma once
#include <vector>

namespace hideit {

    class driver 
    {
        hideit::ocr ocr;
        std::vector<point> match(hideit::profile, const char*);
    public:
        driver();
        ~driver();

        std::vector<coords> search(hideit::profile p, tesseract::ResultIterator* it);
        std::vector<quad> search(hideit::profile, Pix*);
        std::vector<quad> search(hideit::profile, hideit::image);

    };

}

#include "../Sources/driver.cpp"
