#pragma once
#include <vector>

namespace hideit {

    class window 
    {

    public:
        window();
        ~window();
        void open();
        void close();

        void blur(std::vector<unsigned int[2]>&); 
    };

}

#include "../Sources/window.cpp"