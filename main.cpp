#include <iostream>

#include "tmp.hpp"

using namespace std;

int main() {
    // var declaration
    unsigned int n;

    cout << "Hello world!" << endl;
    cout << "Enter a number to calculate the nth fib: ";
    cin >> n;
    cout << endl;
    fb(n);
    return 0;
}

