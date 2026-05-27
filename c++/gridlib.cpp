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

string displayStr(vector<vector<string> > displayArray) {
    string displayString = "";
    int height = displayArray.size();
    int width = displayArray[0].size();

    for (int i = 0; i < width; i++) {
        for (int j = 0; j < height; j++) {
            displayString += displayArray[i][j] + " ";
        }
        displayString += "\n";
    }
    
    return displayString;
}