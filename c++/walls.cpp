#include <array>
#include "walls.h"
using namespace std;

Walls::Walls(bool rot0, bool rot1, bool rot2, bool rot3) {
    _wallArray = {rot0, rot1, rot2, rot3};
}
        
array<bool, 4> Walls::directionCorrect(int rot) {
    return {_wallArray[rot % 4], _wallArray[(rot+1) % 4], _wallArray[(rot+2) % 4], _wallArray[(rot+3) % 4]};
}