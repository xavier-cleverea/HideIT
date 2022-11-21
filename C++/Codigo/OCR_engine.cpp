#include"OCR_engine.h"

OCR_engine::OCR_engine(std::string idioma) {
    //constructora
    api = new tesseract::TessBaseAPI();
    if(api->Init(NULL,idioma)) {
        std::cout << "No se ha podido inicializar Tesseract" << std::endl;
    }
}

OCR_engine::test() {
    Pix *imagen = pixRead("./imagen.png");
    api->SetImage(image);
    outText = api->GetUTF8Text();
    std::cout << outText << std::endl;
    pixDestroy(&image);
}
