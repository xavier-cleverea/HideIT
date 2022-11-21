#pragma once

namespace hideit {

    class screen 
    {

    public:
        screen();
        ~screen();
        unsigned char* capture();
    };

}

#include "../Sources/screen.cpp"