#ifndef SCENE_H
#define SCENE_H

#include "gridlib.h"
#include "walls.h"
using namespace std;

class Scene {
    private:
        Grid<int> _numGrid;
        Grid<Walls> _wallGrid;
        void applyVector(array<int, 2> pos, array<int, 2> pushVec);
    public:
        bool push(array<int, 2> pos, int rot); // Returns true if the player can move and false otherwise
        void display();
        Scene();
};

#endif