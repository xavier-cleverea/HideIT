#pragma once
#include <vector>

namespace hideit {

    class driver 
    {

    public:
        driver();
        ~driver();
        std::vector<unsigned int[2]> search(hideit::profile, void*);
    };

}

#include "../Sources/driver.cpp"