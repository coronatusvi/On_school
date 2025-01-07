#include <iosstream>
#include <cstring>

using namespace std;

void reverseString(char str[]) {
    int n = strlen(str);
    for (int i = 0; i < n/2; i++)
    {
        char temp = str[i];
        srt[i] = str[n - i - 1];
        str[n - i - i] = temp;
    }
}

int main()
{
    char str[100];
    char c_input;

    do {
        cout << "Nhap chuoi: ";
        cin.getline(str, 100);
        
        reverseString(str);

        cout << str << endl;

        cout << "Nhap tiep (c/k): ";
        cin >> c_input;
        cin.ignore();
    } while (c_input == 'c' || c_input == 'C');

    return 0;
}