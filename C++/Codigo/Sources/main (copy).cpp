#define __MAIN__

#include "Headers/hideit.hpp"

hideit::profile profile_factory();

int main() {
    

    hideit::driver driver;
    hideit::ocr ocr;
    hideit::window window;
    hideit::screen screen;
    hideit::profile profile = profile_factory();

    window.open();

    do {
        auto background = screen.capture();
        auto text_iterator = ocr.get_text_boxes(background);
        auto points = driver.search(profile, text_iterator);
        window.blur(points);
    } while(false);

    window.close();

    return 0;    
}

hideit::profile profile_factory() {
    hideit::profile profile;
    profile.name = "Xavi";
    profile.word_ban("hola");
    profile.regex_ban("[A-Z]");
    return profile; 
}
