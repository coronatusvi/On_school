#include <iostream>
#include <cstring>
#include <cctype>

using namespace std;

void trim(char str[]) {
    int n = strlen(str);
    int i = 0;
    while (i < n && isspace(str[i])) {
        i++;
    }

    int j = n - 1;
    while (j >= 0 && isspace(str[j])) {
        j--;
    }

    if (i > j) {
        str[0] = '\0';
    } else {
        for (int k = i; k <= j; k++) {
            str[k - i] = str[k];
        }
        str[j - i + 1] = '\0';
    }
}

void remove ExtraSpaces(char str[]){

    int n = strlen(str);
    int i = 0;
    while (i < n && isspace(str[i])) {
        i++;
    }

    int j = n - 1;
    while (j >= 0 && isspace(str[j])) {
        j--;
    }

    if (i > j) {
        str[0] = '\0';
    } else {
        int k = 0;
        for (int l = i; l <= j; l++) {
            if (isspace(str[l])) {
                if (isspace(str[l - 1])) {
                    continue;
                }
            }
            str[k++] = str[l];
        }
        str[k] = '\0';
    }
}

void capitalizeWords(char str[]) {
    int n = strlen(str);
    bool new_word = true;

    for (int i = 0; i < n; i++) {
        if (new_word && isalpha(str[i])) {
            str[i] = toupper(str[i]);
            new_word = false;
        } else if (isspace(str[i])) {
            new_word = true;
        }
    }
}

int main () {
    char name[100];

    cout << "Nhap mot xau: ";
    cin.getline(name, 100);

    cout << "Sau khi bo dau cach o hai cau:\n";
    trim(name);
    cout << name << endl;

    cout << "Sau khi loai bo dau cach giua cac tu:\n";
    removeExtraSpaces(name);
    cout << name << endl;

    cout << "Sau khi viet hoa chu cai dau cua moi tu:\n";
    capitalizeWords(name);
    cout << name << endl;

    return 0;
}