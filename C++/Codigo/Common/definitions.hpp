#pragma once
#include <stdio.h>
#include <stdlib.h>

#define UNIMPLEMENTED fprintf(stderr,"%s:%d: %s is not implemented.\n", __FILE__, __LINE__, __PRETTY_FUNCTION__);