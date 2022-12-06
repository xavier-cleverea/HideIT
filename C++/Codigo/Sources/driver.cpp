#pragma once
#include <regex>

namespace hideit {

    driver::driver() {
     }
    driver::~driver() {
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

    
    std::vector<coords> driver::search(hideit::profile p, tesseract::ResultIterator* it) {
        
        tesseract::PageIteratorLevel level = tesseract::RIL_WORD;
        auto bbox_vec = std::vector<coords>();
        
        if(it != 0){
            while(it->Next(level)) {
                const char* word = it->GetUTF8Text(level);
                //falta implementar el condicional word_is_banned
                bool word_is_banned = true;
                if(word_is_banned) {
                    coords new_c;
                    it->BoundingBox(level, &(new_c.x1), &(new_c.y1), &(new_c.x2), &(new_c.y2));
                    bbox_vec.push_back(new_c);
                }
                delete[] word;
            }
        }
        return bbox_vec;

    }


}
