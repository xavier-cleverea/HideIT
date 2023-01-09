#pragma once
#include <string>
#include <vector>
#include <regex>

namespace hideit {

    class profile 
    {
        
    public:
        profile();
        ~profile();

        void word_ban(std::string);
        void regex_ban(std::string);
        
        std::string name;
        std::vector<std::regex> regexs;
    };

}

#include "../Sources/profile.cpp"