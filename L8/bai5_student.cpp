#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

struct Date {
    int day;
    int month;
    int year;
};

struct Student {
    int id;
    string fullname;
    Date birthday;
    string yclass;
};

Student inputStudent() {
    Student student;

    cout << "Nhap ID sinh vien: ";
    cin >> student.id;
    cin.ignore();

    cout << "Nhap ho ten: ";
    getline(cin, student.fullname);

    cout << "Nhap ngay sinh (dd/mm/yyyy): ";
    cin >> student.birthday.day;
    cin.ignore();
    cin >> student.birthday.month;
    cin.ignore();
    cin >> student.birthday.year;
    cin.ignore();

    cout << "Nhap lop: ";
    getline(cin, student.yclass);

    return student;
}

void printStudent(const Student& student) {
    cout << "ID: " << student.id << endl;
    cout << "Ho ten: " << student.fullname << endl;
    cout << "Ngay sinh: " << student.birthday.day << "/" << student.birthday.month << "/" << student.birthday.year << endl;
    cout << "Lop: " << student.yclass << endl;
}

bool compareStudentsByName(const Student& a, const Student& b){
    size_t pos_a = a.fullname.find_last_of(' ');
    string last_name_a = (pos_a != string::npos) ? a.fullname.substr(pos_a + 1) : a.fullname;
    
    size_t pos_b = b.fullname.find_last_of(' ');
    string last_name_b = (pos_b != string::npos) ? b.fullname.substr(pos_b + 1) : b.fullname;

    if (last_name_a != last_name_b) {
        return last_name_a < last_name_b;
    }
    return a.fullname < b.fullname;
}

bool compareStudentsByClass(const Student& a, const Student& b){
    return a.yclass < b.yclass;
}

void selectionSort(vector<Student>& students, bool (*compareFunc)(const Student&, const Student&)) {
    int n = students.size();
    for (int i = 0; i < n - 1; i++) {
        int min_idx = i;
        for (int j = i + 1; j < n; j++) {
            if (compareFunc(students[j], students[min_idx]))
                min_idx = j;
        }
         if (min_idx != i)
            swap(students[i], students[min_idx]);
    }
}

int main() {
    vector<Student> students;
    int choice;

    do {
        cout << "\n--- MENU ---" << endl;
        cout << "1. Nhap sinh vien" << endl;
        cout << "2. Sap xep theo ho ten" << endl;
        cout << "3. Sap xep theo lop khoa hoc" << endl;
        cout << "4. Thoat" << endl;
        cout << "Nhap lua chon: ";
        cin >> choice;

        switch (choice) {
            case 1: {
                char continueInput;
                 do {
                    students.push_back(inputStudent());
                    cout << "Nhap tiep (y/n): ";
                    cin >> continueInput;
                    cin.ignore();
                } while(continueInput == 'y' || continueInput == 'Y');
                break;
            }
            case 2: {
                selectionSort(students, compareStudentsByName);
                cout << "Danh sach sinh vien sau khi sap xep theo ho ten:\n";
                for (const Student& student : students) {
                    printStudent(student);
                }
                break;
            }
            case 3: {
                selectionSort(students, compareStudentsByClass);
                cout << "Danh sach sinh vien sau khi sap xep theo lop hoc:\n";
                for (const Student& student : students) {
                    printStudent(student);
                }
                break;
            }
            case 4:
                cout << "Thoat chuong trinh.\n";
                break;
            default:
                cout << "Lua chon khong hop le.\n";
        }
    } while (choice != 4);

    return 0;
}