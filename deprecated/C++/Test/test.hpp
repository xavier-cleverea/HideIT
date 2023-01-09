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

#define CONCAT(a, b) CONCAT_INNER(a, b)
#define CONCAT_INNER(a, b) a ## b

#define MAIN_TEST(func) \
int main() { \
    TEST(func) \
}

#define TEST(func) TEST_(func, __COUNTER__)
#define TEST_(func, _count) \
int CONCAT(s_memory,_count) = get_memory(); \
auto CONCAT(s_time,_count) = std::chrono::high_resolution_clock::now(); \
func(); \
auto CONCAT(e_time,_count) = std::chrono::high_resolution_clock::now(); \
int CONCAT(e_memory,_count) = get_memory(); \
printf("%s leaks %iKB of memory.\n",#func,CONCAT(e_memory,_count)-CONCAT(s_memory,_count)); \
auto CONCAT(duration,_count) = std::chrono::duration_cast<std::chrono::milliseconds>(CONCAT(e_time,_count)-CONCAT(s_time,_count)); \
printf("%s executed in %li milliseconds.\n",#func,CONCAT(duration,_count).count()); \
