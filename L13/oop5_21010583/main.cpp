#include <iostream>
#include "myLine.cpp"
#include <iomanip>

using namespace std;

int main()
{
    MyLine line1(1, 2, 4, 6);
    cout << "Line 1: " << line1.toString() << endl;

    cout << "Length of line 1: " << fixed << setprecision(4) << line1.getLength() << endl;
    cout << "Gradient of line 1: " << fixed << setprecision(4) << line1.getGradient() << endl;
    cout << "Begin X of line 1: " << line1.getBeginX() << endl;
    cout << "Begin Y of line 1: " << line1.getBeginY() << endl;
    cout << "End X of line 1: " << line1.getEndX() << endl;
    cout << "End Y of line 1: " << line1.getEndY() << endl;

    MyPoint start(0, 0);
    MyPoint end(5, 5);

    MyLine line2(start, end);

    cout << "Line 2: " << line2.toString() << endl;
    int *beginXY = line2.getBeginXY();
    cout << "Begin XY of line 2: " << beginXY[0] << ", " << beginXY[1] << endl;

    line2.setBeginXY(1, 1);
    cout << "Line 2 After updating Begin: " << line2.toString() << endl;
    int *endXY = line2.getEndXY();
    cout << "End XY of line 2: " << endXY[0] << ", " << endXY[1] << endl;
    line2.setEndXY(6, 6);
    cout << "Line 2 After updating End: " << line2.toString() << endl;

    return 0;
}           