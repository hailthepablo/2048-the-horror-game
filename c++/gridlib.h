#ifndef GRIDLIB_H
#define GRIDLIB_H

#include <iostream>
#include <sstream>
#include <array>
#include <vector>
using namespace std;

string pointStr(array<int, 2> point);
string displayStr(vector<vector<string> > displayArray);

template <typename T>
string str(T var) {
    stringstream tempStream;
    string ret;
    tempStream << var;
    getline(tempStream,ret);
    return ret;
}

template <typename T>
vector<vector<T> > generateArray(int numRows, int numCols, T defaultSpace) {
    vector<T> row = {};
    vector<vector<T> > fullArray = {};
    for (int i = 0; i < numCols; i++) {
        row.push_back(defaultSpace);
    }
    for (int i = 0; i < numRows; i++) {
        fullArray.push_back(row);
    }
    return fullArray;
}

template <typename T>
class Grid {
    public:
        array<int, 2> _origin;
        int _slot0;
        int _slot1;
        int _xDir;
        int _yDir;
        int _height;
        int _width;
        vector<vector<T> > _gridArray;

        Grid(vector<vector<T> > gridArray, array<int, 2> origin = {0,0}, string order = "yx", string xDir = "right", string yDir = "down") {
            _origin = origin;
            _gridArray = gridArray;

            _height = gridArray.size();
            _width = gridArray[0].size();
            
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
                cout << "ERROR: Slot indexes were not 0 or 1\n";
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

        vector<vector<string> > getDisplayArray(string align) { 
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
            
            vector<vector<string> > displayArray = generateArray(_height,_width,string("."));
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