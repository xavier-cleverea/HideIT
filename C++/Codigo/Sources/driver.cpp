#pragma once
#include <regex>

namespace hideit {

    driver::driver() {
        UNIMPLEMENTED
    }
    driver::~driver() {
        UNIMPLEMENTED
    }
    std::vector<quad> driver::search(hideit::profile profile, Pix* img) {
        std::vector<quad> quads;
        BOXA* boxes = ocr.get_components();

        for (int i = 0; i < boxes->n; i++) {
            BOX* box = boxaGetBox(boxes, i, L_CLONE);
            char* text = ocr.get_text(box->x, box->y, box->w, box->h);
            auto matchs = match(profile,text);
            float l_char = ((float) box->w)/strlen(text);
            for(auto& match : matchs) {
                quads.push_back({
                    box->x+match.w*l_char,
                    box->y,
                    box->x+match.h*l_char,
                    box->y+box->h,
                });

            }
            boxDestroy(&box);
        }
        return quads;
    }
    std::vector<quad> driver::search(hideit::profile profile, hideit::image img) {
        UNIMPLEMENTED
        return std::vector<quad>();
    }

    std::vector<point> driver::match(hideit::profile profile, const char* text) {
        std::string string(text);
        std::smatch result;
        std::vector<point> points;

        for(auto& regex : profile.regexs) {
            std::regex_search(string, result, regex);
            for (unsigned i=0; i<result.size(); ++i) {
                unsigned int pos = result.position(i);
                points.push_back({pos,pos+result[i].length()});
            }
        }

        return points;
    }


}
