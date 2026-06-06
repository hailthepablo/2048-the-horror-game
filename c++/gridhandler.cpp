#include <iostream>
#include <array>
#include "gridlib.h"
#include "handyfuncs.h"
using namespace std;

template <size_t width, size_t height>
bool push(Grid<int, width, height>& numGrid, array<int, 2> pos, int rot) {
    array<int, 2> pushDir = vectorize(rot);
    array<int, 2> curSpace = pos;
    array<int, 2> newPos;
    int amount = 0;
    int prevNum = 0;
    int curNum;

    while (true) {
        curNum = numGrid.getElem(curSpace);

        if ((amount != 0) && (prevNum == curNum || curNum == 0)) {
            break;
        }

        // Implement wall detection logic

        amount++;
        curSpace = addVec2(curSpace, pushDir);
        prevNum = curNum;
    }

    for (int i = 0; i < amount; i++) {
        curSpace = addVec2(curSpace, negVec2(pushDir));
        newPos = addVec2(curSpace, pushDir);
        numGrid.setElem(newPos, numGrid.getElem(curSpace)+numGrid.getElem(newPos));
        numGrid.setElem(curSpace,0);
    }

    return true;
}

int main() {
    Grid<int,4,4> g(generateArray<int,4,4>(0),{3,0},"xy","right","up");
    g.setElem({0,1},2);
    g.setElem({0,2},4);
    g.setElem({0,3},4);
    cout << displayStr(g.getDisplayArray("left"));
    cout << "\n";
    push(g,{0,0},1);
    cout << displayStr(g.getDisplayArray("left"));
}