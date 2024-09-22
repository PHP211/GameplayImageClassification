import pyautogui
import time
from pynput import keyboard
import threading

# Biến toàn cục để điều khiển việc dừng chương trình
running = True

# Hàm chụp màn hình
def take_screenshot(filename):
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)

# Hàm xử lý khi có phím được bấm
def on_press(key):
    global running
    try:
        key_str = str(key.char)  # Lấy ký tự của phím thường
    except AttributeError:
        key_str = str(key)  # Lấy ký tự của các phím đặc biệt

    # Nếu nhấn ESC, dừng chương trình
    if key == keyboard.Key.esc:
        print("Thoát chương trình...")
        running = False  # Dừng vòng lặp auto_screenshot
        return False  # Thoát listener

    # Chụp màn hình khi có phím bấm
    timestamp = time.strftime("%Y%m%d-%H%M%S")  # Lấy timestamp để làm tên file
    filename = f"{timestamp}_{key_str}.png"  # Tên file là timestamp + tên phím
    take_screenshot(filename)
    print(f"Chụp màn hình và lưu với tên: {filename}")
    
    # Thêm khoảng delay sau khi chụp khi có phím bấm
    time.sleep(0.5)  # Delay 0.5 giây (500ms) sau khi chụp

# Hàm tự động chụp màn hình mỗi giây
def auto_screenshot():
    global running
    while running:
        timestamp = time.strftime("%Y%m%d-%H%M%S")  # Lấy timestamp để làm tên file
        filename = f"{timestamp}_auto.png"  # Tên file tự động chụp
        take_screenshot(filename)
        print(f"Tự động chụp màn hình và lưu với tên: {filename}")
        time.sleep(2)  # Chờ 1 giây trước khi chụp lần tiếp theo

# Khởi động listener để nghe các phím bấm
def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    # Yêu cầu người dùng nhập để bắt đầu chương trình
    start_input = input("Nhập 'start' để bắt đầu chương trình chụp màn hình: ").lower()

    if start_input == 'start':
        print("Chương trình bắt đầu!")

        # Tạo thread cho việc chụp màn hình tự động
        auto_screenshot_thread = threading.Thread(target=auto_screenshot)
        auto_screenshot_thread.daemon = True  # Để thread tự động dừng khi chương trình kết thúc
        auto_screenshot_thread.start()

        # Khởi động listener để nghe các phím bấm
        start_listener()

        # Sau khi listener kết thúc, dừng chương trình
        auto_screenshot_thread.join()
    else:
        print("Chương trình đã hủy.")
