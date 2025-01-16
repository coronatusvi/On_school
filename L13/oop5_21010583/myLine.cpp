#pragma once
#include <iostream>
#include <cmath>
#include "point.cpp"
#include <sstream>
using namespace std;
class MyLine
{
private:
    MyPoint begin;
    MyPoint end;

public:
    MyLine(int x1, int y1, int x2, int y2);
    MyLine(MyPoint begin, MyPoint end);
    MyPoint getBegin() const;
    void setBegin(MyPoint begin);
    MyPoint getEnd() const;
    void setEnd(MyPoint end);
    int getBeginX() const;
    void setBeginX(int x);
    int getBeginY() const;
    void setBeginY(int y);
    int getEndX() const;
    void setEndX(int x);
    int getEndY() const;
    void setEndY(int y);
    int *getBeginXY() const;
    void setBeginXY(int x, int y);
    int *getEndXY() const;
    void setEndXY(int x, int y);

    double getLength() const;
    double getGradient() const;
    string toString() const;
};
MyLine::MyLine(int x1, int y1, int x2, int y2) : begin(x1, y1), end(x2, y2) {}
MyLine::MyLine(MyPoint begin, MyPoint end) : begin(begin), end(end) {}
MyPoint MyLine::getBegin() const { return begin; }
void MyLine::setBegin(MyPoint begin) { this->begin = begin; }
MyPoint MyLine::getEnd() const { return end; }
void MyLine::setEnd(MyPoint end) { this->end = end; }
int MyLine::getBeginX() const { return begin.getX(); }
void MyLine::setBeginX(int x) { begin.setX(x); }
int MyLine::getBeginY() const { return begin.getY(); }
void MyLine::setBeginY(int y) { begin.setY(y); }
int MyLine::getEndX() const { return end.getX(); }
void MyLine::setEndX(int x) { end.setX(x); }
int MyLine::getEndY() const { return end.getY(); }
void MyLine::setEndY(int y) { end.setY(y); }
int *MyLine::getBeginXY() const
{
    static int arr[2];
    arr[0] = begin.getX();
    arr[1] = begin.getY();
    return arr;
}
void MyLine::setBeginXY(int x, int y)
{
    begin.setX(x);
    begin.setY(y);
}
int *MyLine::getEndXY() const
{
    static int arr[2];
    arr[0] = end.getX();
    arr[1] = end.getY();
    return arr;
}
void MyLine::setEndXY(int x, int y)
{
    end.setX(x);
    end.setY(y);
}
double MyLine::getLength() const
{
    int xDiff = end.getX() - begin.getX();
    int yDiff = end.getY() - begin.getY();
    return sqrt(xDiff * xDiff + yDiff * yDiff);
}
double MyLine::getGradient() const
{
    int xDiff = end.getX() - begin.getX();
    int yDiff = end.getY() - begin.getY();
    return atan2(yDiff, xDiff);
}
string MyLine::toString() const
{
    stringstream ss;
    ss << "MyLine[begin=(" << begin.getX() << "," << begin.getY() << "),end=(" << end.getX() << "," << end.getY() << ")]";
    return ss.str();
}