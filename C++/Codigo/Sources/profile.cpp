namespace hideit {

    profile::profile() {
        UNIMPLEMENTED
    }
    profile::~profile() {
        UNIMPLEMENTED
    }
    void profile::word_ban(std::string word) {
        UNIMPLEMENTED
    }
    void profile::regex_ban(std::string regex) {
        regexs.push_back(std::regex(regex));
    }

}
