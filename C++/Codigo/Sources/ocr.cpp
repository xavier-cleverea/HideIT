namespace hideit {

    ocr::ocr() {
        TessApi = new tesseract::TessBaseAPI();
        if (TessApi->Init(NULL, "eng")) {
            fprintf(stderr, "Could not initialize tesseract.\n");
            exit(1);
        }
    }
    ocr::~ocr() {
        TessApi->End();
        delete(TessApi);
    }
    tesseract::ResultIterator* ocr::get_text_boxes(unsigned char* imagedata, int width, int height, int bytes_per_pixel, int bytes_per_line) {
        TessApi->SetImage(imagedata, width, height, bytes_per_pixel, bytes_per_line);
        TessApi->GetBoxText();
        TessApi->Recognize(0);
        return TessApi->GetIterator();
    }
    tesseract::ResultIterator* ocr::get_text_boxes(Pix* img) {
        TessApi->SetImage(img);
        TessApi->Recognize(0);
        return TessApi->GetIterator();
    }

    BOXA* get_components() {
        TessApi->GetComponentImages();

        return nullptr;
    }


}
