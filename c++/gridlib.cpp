#include <iostream>
#include <sstream>
#include <array>
#include <vector>
#include "gridlib.h"
using namespace std;

string pointStr(array<int, 2> point) {
    stringstream tempStream;
    string ret;
    tempStream << "(" << point[0] << ", " << point[1] << ")";
    getline(tempStream,ret);
    return ret;
}