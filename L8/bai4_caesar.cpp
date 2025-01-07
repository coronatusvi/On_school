#include <iostream>
#include <cstring>
#include <cctype>
using namespace std;

char caesarCipher(char ch, int k, bool encode) {
    if (isalpha(ch)) {
        char base = islower(ch) ? 'a' : 'A';
        if(encode){
             return base + (ch - base + k) % 26;
        } else {
            return base + (ch - base -k + 26) % 26;
        }
    }
    return ch;
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        cerr << "Cu phap: caesar (encoding/decoding) k \"xau\"\n";
        return -1;
    }
    
    bool encoding = true;
    if(strcmp(argv[1], "encoding") != 0)
        if(strcmp(argv[1], "decoding") == 0)
            encoding = false;
        else
            {
                cerr << "Cu phap: caesar (encoding/decoding) k \"xau\"\n";
                return -1;
            }

    int k = atoi(argv[2]);
    char *input = argv[3];

    for (int i = 0; input[i] != '\0'; i++) {
        cout << caesarCipher(input[i], k, encoding);
    }
    cout << endl;

    return 0;
}