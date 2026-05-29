#ifndef WALLS_H
#define WALLS_H

#include <array>
using namespace std;

class Walls {
    private:
        array<bool, 4> _wallArray;
    public:
        Walls(bool rot0, bool rot1, bool rot2, bool rot3);
        array<bool, 4> directionCorrect(int rot);
};

#endif