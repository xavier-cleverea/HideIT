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
    void* ocr::get_text_boxes(unsigned char* imagedata, int width, int height, int bytes_per_pixel, int bytes_per_line) {
        TessApi->SetImage(imagedata, width, height, bytes_per_pixel, bytes_per_line);
        TessApi->Recognize(0);
        return nullptr;
    }
    void* ocr::get_text_boxes(Pix* img) {
        TessApi->SetImage(img);
        TessApi->Recognize(0);
        return nullptr;
    }

}
