#pragma once

namespace hideit {

    driver::driver() {
    }
    driver::~driver() {
    }
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
