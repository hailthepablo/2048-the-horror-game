#include "handyfuncs.h"
#include <array>
using namespace std;

array<int, 2> vectorize(int rot) {
    switch (rot) {
    case 0:
        return {1,0};
        break;
    case 1:
        return {0,1};
        break;
    case 2:
        return {-1,0};
        break;
    case 3:
        return {0,-1};
        break;
    default:
        return {0,0};
        break;
    }
}

array<int, 2> addVec2(array<int, 2> lhs, array<int, 2> rhs) {
    return {lhs[0]+rhs[0], lhs[1]+rhs[1]};
}

array<int, 2> negVec2(array<int, 2> vec) {
    return {-vec[0],-vec[1]};
}