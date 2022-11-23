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
    void* ocr::get_text_boxes(unsigned char* img) {
        
        return nullptr;
    }
    void ocr::test() {
        Pix *image = pixRead("/home/leo/Desktop/PAE/HideIT/C++/Test/Test-Image3.png");
        TessApi->SetImage(image);
        std::cout << TessApi->GetUTF8Text();
        
 
        pixDestroy(&image);
    }

}
