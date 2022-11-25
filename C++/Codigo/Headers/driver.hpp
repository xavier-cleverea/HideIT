#pragma once
#include <vector>

namespace hideit {

    class driver 
    {

    public:
        driver();
        ~driver();
        std::vector<coords> search(hideit::profile p, tesseract::ResultIterator* it);
    };

}

#include "../Sources/driver.cpp"
