#include "../Codigo/Headers/hideit.hpp"

#include <chrono>
#include <cstring>
#include <sys/types.h>
#include <sys/sysinfo.h>

int parseLine(char* line){
    int i = strlen(line);
    const char* p = line;
    while (*p <'0' || *p > '9') p++;
    line[i-3] = '\0';
    i = atoi(p);
    return i;
}

int get_memory(){
    FILE* file = fopen("/proc/self/status", "r");
    int result = -1;
    char line[128];
    while (fgets(line, 128, file) != NULL){
        if (strncmp(line, "VmRSS:", 6) == 0){
            result = parseLine(line);
            break;
        }
    }
    fclose(file);
    return result;
}

#define TEST(func) \
int main() { \
    int s_memory = get_memory(); \
    auto s_time = std::chrono::high_resolution_clock::now(); \
    func(); \
    auto e_time = std::chrono::high_resolution_clock::now(); \
    int e_memory = get_memory(); \
    printf("%s leaks %iKB of memory.",#func,s_memory-e_memory); \
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(e_time-s_time); \
    printf("%s executed in %i milliseconds.\n",#func,duration.count()); \
}
