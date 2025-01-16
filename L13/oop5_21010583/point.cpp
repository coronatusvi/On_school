#pragma once
#include <iostream>
using namespace std;
class MyPoint
{
private:
    int x;
    int y;

public:
    MyPoint(int x, int y);
    int getX() const;
    void setX(int x);
    int getY() const;
    void setY(int y);
};

MyPoint::MyPoint(int x, int y)
{
    this->x = x;
    this->y = y;
}

int MyPoint::getX() const
{
    return x;
}

void MyPoint::setX(int x)
{
    this->x = x;
}

int MyPoint::getY() const
{
    return y;
}

void MyPoint::setY(int y)
{
    this->y = y;
}