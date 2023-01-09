namespace hideit {
    struct point {
        const unsigned short w;
        const unsigned short h;

        point(int width,int height) : w(width), h(height) {}
    };

    struct quad {
        const point p1;
        const point p2;

        quad(point p1, point p2) : p1(p1), p2(p2) {}
        quad(int w1,int h1,int w2, int h2) : p1({w1,h2}), p2({w2,h2}) {}

    };

    struct image
    {
        const int width, height, bpp, bpl;
        unsigned char* data;

        image(unsigned char* data, int width, int height, int bpp, int bpl) 
            : data(data), width(width), height(height), bpp(bpp), bpl(bpl) {}   
    };
    
}