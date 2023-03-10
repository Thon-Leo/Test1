#include <iostream>

#include "tmp.hpp"

using namespace std;

void fb(unsigned int n) {
    cout << fb_helper(n) << endl;
}

int fb_helper(unsigned int n) {
    if (n == 0 || n == 1) return 1;
    if (n == 2) return 2;
    return fb_helper(n-1) + fb_helper(n-2);
}