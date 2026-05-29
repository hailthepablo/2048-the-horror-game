#include "scene.h"
#include "handyfuncs.h"
#include <iostream>
using namespace std;

void Scene::applyVector(array<int, 2> pos, array<int, 2> pushVec) {
    array<int, 2> newPos = addVec2(pos, pushVec);
    _numGrid.setElem(newPos, _numGrid.getElem(newPos) + _numGrid.getElem(pos));
    _numGrid.setElem(pos, 0);
}

Scene::Scene() {
    return;
}

bool Scene::push(array<int, 2> pos, int rot) {
    array<int, 2> pushDir = vectorize(rot);
    array<int, 2> curSpace = pos;

    int amount = 0;
    int prevNum = 0;
    int curNum;

    while (true) {
        curNum = _numGrid.getElem(curSpace);
        
        // if wall then stop and return false
        
        if (amount != 0 && prevNum == curNum)
        
        
        amount++;
        curSpace = addVec2(curSpace, pushDir);
        prevNum = curNum;

    }
}

void Scene::display() {
    displayStr(_numGrid.getDisplayArray("left"));
}