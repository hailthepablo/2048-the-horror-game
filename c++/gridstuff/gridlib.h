#ifndef GRIDLIB_H
#define GRIDLIB_H

#include <iostream>
#include <sstream>
#include <array>
#include <vector>
using namespace std;

string pointStr(array<int, 2> point);

template <typename T>
string str(T var) {
    stringstream tempStream;
    string ret;
    tempStream << var;
    getline(tempStream,ret);
    return ret;
}

template <typename T, int width, int height>
array< array< T, width >, height > generateArray(T defaultSpace) {
    array< array< T, width >, height > arr;
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            arr[i][j] = defaultSpace;
        }
    }
    return arr;
}

template<size_t width, size_t height>
string displayStr(array< array< string, height >, width > displayArray) {
    string displayString = "";

    for (int i = 0; i < width; i++) {
        for (int j = 0; j < height; j++) {
            displayString += displayArray[i][j] + " ";
        }
        displayString += "\n";
    }
    
    return displayString;
}

template <typename T = int, size_t width = 4, size_t height = 4>
class Grid {
    public:
        array<int, 2> _origin;
        int _slot0;
        int _slot1;
        int _xDir;
        int _yDir;
        int _height;
        int _width;
        array< array< T, width >, height > _gridArray;

        Grid(array< array< T, width >, height > gridArray, array<int, 2> origin = {0,0}, string order = "yx", string xDir = "right", string yDir = "down") {
            _origin = origin;
            _gridArray = gridArray;

            _height = height;
            _width = width;
            
            if (order == "yx") {
                _slot0 = 0;
                _slot1 = 1;
            } else if (order == "xy") {
                _slot1 = 0;
                _slot0 = 1;
            }

            if (xDir == "right") {
                _xDir = 1;
            } else if (xDir == "left") {
                _xDir = -1;
            }

            if (yDir == "down") {
                _yDir = 1;
            } else if (yDir == "up") {
                _yDir = -1;
            } 
        }

        array<int, 2> getPos(array<int, 2> indexes) {
            if (_slot0 == 0) {
                return {_yDir*(indexes[0]-_origin[0]),_xDir*(indexes[1]-_origin[1])};
            } else if (_slot0 == 1) {
                return {_xDir*(indexes[1]-_origin[1]),_yDir*(indexes[0]-_origin[0])};
            } else {
                exit(0);
            }
        }

        T getElem(array<int, 2> pos) {
            int rowNum = _yDir*pos[_slot0]+_origin[0];
            int columnNum = _xDir*pos[_slot1]+_origin[1];
            if ((0 <= rowNum) && (rowNum <= _height-1) && (0 <= columnNum) && (columnNum <= _width-1)) {
                return _gridArray[rowNum][columnNum];
            } else {
                return NULL;
            }
        }

        void setElem(array<int, 2> pos,  T elem) {
            int rowNum = _yDir*pos[_slot0]+_origin[0];
            int columnNum = _xDir*pos[_slot1]+_origin[1];
            if ((0 <= rowNum) && (rowNum <= _height-1) && (0 <= columnNum) && (columnNum <= _width-1)) {
                _gridArray[_yDir*pos[_slot0]+_origin[0]][_xDir*pos[_slot1]+_origin[1]] = elem;
            }
        }

        void displayPositions() {
            for (int i = 0; i < _height; i++) {
                for (int j = 0; j < _width; j++) {
                    cout << pointStr(getPos({i,j})) << " ";
                }
                cout << "\n";
            }
        }

        array< array< string, height >, width > getDisplayArray(string align) { 
            vector<int> maxList = {};
            int curMax;

            for (int i = 0; i < _width; i++) {
                curMax = 0;
                for (int j = 0; j < _width; j++) {
                    if (str(_gridArray[j][i]).size() > curMax) {
                        curMax = str(_gridArray[j][i]).size();
                    }
                }
                maxList.push_back(curMax);
            }
            
            array< array< string, height >, width > displayArray = generateArray<string,width,height>(string("."));
            string spaces;

            for (int i = 0; i < _width; i++) {
                for (int j = 0; j < _height; j++) {
                    for (int k = 0; k < maxList[i]-str(_gridArray[j][i]).size(); k++) {
                        spaces += " ";
                    }
                    if (align == "left") {
                        displayArray[j][i] = str(_gridArray[j][i]) + spaces;
                    } else if (align == "right") {
                        displayArray[j][i] = spaces + str(_gridArray[j][i]);
                    }
                }
            }
            
            return displayArray;
        }
};

#endif