#ifndef HANDYFUNCS_H
#define HANDYFUNCS_H

#include <array>
using namespace std;

array<int, 2> vectorize(int rot); // Turn rotation into directional vector
array<int, 2> addVec2(array<int, 2> lhs, array<int, 2> rhs); // Add two directional vectors
array<int, 2> negVec2(array<int, 2> vec); // Negate a directional vector

#endif