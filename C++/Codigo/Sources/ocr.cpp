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
        Pix *image = pixRead("/home/leo/Desktop/PAE/HideIT/C++/Test/Test-Image2.png");
//      Pix *image2 = pixConvertRGBToGray(image,0.3,0.3,0.4);
        Pix *image2 = pixScale(image,0.8,0.8);//hacer un scaling aplica grayscale al mismo tiempo.
        TessApi->SetImage(image2);
        TessApi->Recognize(0);
//         auto it = TessApi->getIterator();
        //se puede obtener un bounding box a partir del iterador
//         std::cout << TessApi->GetUTF8Text();
        
 
        pixDestroy(&image);
        pixDestroy(&image2);
    
    }

}
