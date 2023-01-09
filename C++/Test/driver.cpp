#include "test.hpp"

Pix* image_factory(const char* source) {
    Pix *image,*image1,*image2;
    image = pixRead(source);
    //image = pixScale(image,0.8,0.8);
    //printf("%i\n",image->d);
    image = pixConvertRGBToGray(image,0.3,0.3,0.4);

    //pixDestroy(&image1);
    //pixDestroy(&image2);
    return image;
}

hideit::profile profile_factory() {
    hideit::profile profile;
    profile.regex_ban("[0-9]+");
    return profile;
}

class PARAMS {
public:
    static Pix* image;
    static hideit::driver driver;
    static hideit::profile profile;
};

Pix* PARAMS::image = image_factory("Test/Resources/Test-Image2.png");
hideit::driver PARAMS::driver = hideit::driver();
hideit::profile PARAMS::profile = profile_factory();

void test_search() {
    PARAMS::driver.search(PARAMS::profile,PARAMS::image);
}

int main() {
    TEST(test_search)
}