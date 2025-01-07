#include <iostream>
using namespace std;

struct Node {
    int data;
    Node* next;
};

void push(Node*& head, int new_data) {
    Node* new_node = new Node();
    new_node->data = new_data;
    new_node->next = head;
    head = new_node;
}

void removeHead(Node*& head) {
    if (head != nullptr) {
        Node* temp = head;
        head = head->next;
        delete temp;
    }
}

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
    Node* head = nullptr;

    int n, m;
    cin >> n >> m; 
    
    for (int i = 0; i < n; ++i) {
        int a;
        cin >> a; 
        push(head, a); 
    }

    for (int i = 0; i < m; ++i) {
        removeHead(head);
    }

    printList(head); 

    return 0;
}