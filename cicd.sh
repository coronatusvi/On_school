#!/bin/bash

# Kiểm tra xem có truyền vào tên tệp không
if [ -z "$1" ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

# Lấy tên tệp từ tham số đầu vào
filename=$1

# Biên dịch tệp C++
gcc -fopenmp "$filename" -o output

# Kiểm tra xem biên dịch có thành công không
if [ $? -eq 0 ]; then
    # Chạy tệp thực thi và sau đó xóa nó
    ./output
    rm output
else
    echo "Compilation failed."
    exit 1
fi

// Run terminal "chomd +x runCICDopenmp.sh"
// Run file "./runCICDopenmp.sh <filename>.cpp"