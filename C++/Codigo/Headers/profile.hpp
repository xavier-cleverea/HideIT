#pragma once
#include <string>

namespace hideit {

    class profile 
    {

    public:
        profile();
        ~profile();

        std::string name;
        void word_ban(std::string);
        void regex_ban(std::string);
    };

}

#include "../Sources/profile.cpp"