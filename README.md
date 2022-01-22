# Context-Switching-Simmulator
## Mô phỏng quá trình context switch cùng với bộ lập lịch Round Robin.
### Mục đích:
* Mô phỏng quá trình context switch khi có I/O request hoặc hết time quantum.
* Mô phỏng thuật toán lập lịch Round Robin.
* Mô phỏng quán lý tiến trình với các hàng đợi đơn giản.

### Cách dùng:
* Để bắt đầu chương trình: 'python3 main.py'
* Khởi tạo các giá trị cho trình mô phỏng: 'boot [time quantum]'
* Tạo tiến trình để đưa vào hệ thống: 'create [path code] [arrival time]'
* Để bắt đầu mô phỏng quá trình chạy: 'run'

### Lưu ý để mô phỏng tín hiệu IO:
* Dùng file io.txt làm nơi chứa tín hiệu phản hồi IO
* Nhập "respone" vào file io.txt để tượng trưng cho tín hiệu IO đến.
