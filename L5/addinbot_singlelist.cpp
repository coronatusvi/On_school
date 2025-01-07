#include <iostream>
using namespace std;

struct Node {
    int data;
    Node* next;
};

void push(Node*& bott, int new_data) {
    Node* new_node = new Node();
    new_node->data = new_data;
    new_node->next = nullptr;
    
    if (bott == nullptr) {
        bott = new_node;
    } else {
        Node* temp = bott;
        while (temp->next != nullptr) {
            temp = temp->next;
        }
        temp->next = new_node;
    }
};

void printList(Node* node) {
    while (node != nullptr) {
        cout << node->data << " ";
        node = node->next;
    }
    cout << endl;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    Node* bott = nullptr;

    int n;
    cin >> n; 
    
    for (int i = 0; i < n; ++i) {
        int a;
        cin >> a; 
        push(bott, a); 
    }

    printList(bott); 

    return 0;
}