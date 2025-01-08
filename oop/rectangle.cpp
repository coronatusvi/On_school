#include <iostream>
#include <math.h>

class Rectangle {
private:
    double w;
    double l;

public: 
    void setW(double);
    void setL(double);

    double getW();
    double getL();
    double getArea();
};

void Rectangle::setW(double x) {
    w = x;
}

void Rectangle::setL(double x) {
    l = x;
}

double Rectangle::getW() {
    return w;
}

double Rectangle::getL() {
    return l;
}

double Rectangle::getArea() {
    return l*w;
}

int main () {
    Rectangle abc;

    abc.setW(10);
    abc.setL(3);
    std::cout << abc.getArea();
}