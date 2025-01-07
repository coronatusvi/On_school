#include <iostream>
#include <cstring>
#include <cctype>
#include <algorithm>
using namespace std;

struct CharCount {
    char character;
    int count;
};

bool compareCharCounts(const CharCount& a, const CharCount& b) {
    return a.count > b.count;
}

int main() {
    char str[200];
    cout << "Moi ban nhap mot xau:\n";
    cin.getline(str, 200);

    int counts[26] = {0}; // Mảng đếm tần suất các chữ cái
    for (int i = 0; str[i] != '\0'; i++) {
        if (isalpha(str[i])) {
            counts[tolower(str[i]) - 'a']++; // Chuyển về chữ thường và đếm
        }
    }

    CharCount charCounts[26];
    int countIndex = 0;

    for(int i = 0; i < 26; i++){
        if(counts[i] > 0){
            charCounts[countIndex].character = 'a' + i;
            charCounts[countIndex].count = counts[i];
            countIndex++;
        }
    }

    sort(charCounts, charCounts + countIndex, compareCharCounts);


    cout << "\nTan suat cua cac ky tu:\n";
    for (int i = 0; i < countIndex; i++) {
        cout << charCounts[i].character << ":" << charCounts[i].count << endl;
    }
    return 0;
}