#include <iostream>

using namespace std;

class phanSo
{
private:
    int tuSo;
    int mauSo;

public:
    phanSo(int tuSo, int mauSo)
    {
        this->tuSo = tuSo;
        this->mauSo = mauSo;
    };
    int getTuSo()
    {
        return tuSo;
    }
    int getMauSo()
    {
        return mauSo;
    }
    string toString()
    {
        return to_string(tuSo) + "/" + to_string(mauSo);
    }
    phanSo Cong(phanSo ps)
    {
        int mau = mauSo * ps.getMauSo();
        int tu = tuSo * ps.getMauSo() + ps.getTuSo() * mauSo;
        return phanSo(tu, mau);
    };
    phanSo operator+(phanSo ps)
    {
        return Cong(ps);
    }
    phanSo operator-(phanSo ps);
    phanSo operator*(phanSo ps);
    phanSo operator/(phanSo ps);
};
int main()
{
    phanSo ps1(1, 2);
    phanSo ps2(2, 5);

    cout << ps1.Cong(ps2).toString() << endl;
    cout << (ps1 - ps2).toString() << endl;

    return 0;
}