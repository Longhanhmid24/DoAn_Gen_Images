import pandas as pd
import os
import shutil

# ==========================================
# CẤU HÌNH ĐƯỜNG DẪN (Nhớ giữ chữ 'r' ở đầu)
# ==========================================

# 1. File CSV chứa caption của bạn
csv_path = r"C:\Users\Administrator\Desktop\New folder\dataset\train\captions_ready_to_train.csv"

# 2. Thư mục GỐC chứa 8000 ảnh (Script CHỈ ĐỌC ảnh từ đây, tuyệt đối không sửa/xóa)
original_image_dir = r"C:\Users\Administrator\Desktop\New folder\dataset\train\images"

# 3. Thư mục MỚI (Script sẽ tự tạo thư mục này, copy ảnh qua và xuất file .txt ra đây)
output_dir = r"C:\Users\Administrator\Desktop\New folder\dataset\train\images_ready_for_train"

# ==========================================
# XỬ LÝ DỮ LIỆU
# ==========================================

def main():
    print("Đang kiểm tra dữ liệu...")
    
    if not os.path.exists(csv_path):
        print(f"LỖI: Không tìm thấy file CSV tại: {csv_path}")
        return
    if not os.path.exists(original_image_dir):
        print(f"LỖI: Không tìm thấy thư mục ảnh gốc tại: {original_image_dir}")
        return

    # Tạo thư mục đầu ra mới tinh (nếu chưa có)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Đã tạo/tìm thấy thư mục đầu ra an toàn tại: {output_dir}")

    print("Đang đọc file CSV và gom các caption...")
    df = pd.read_csv(csv_path)
    # Gom caption như cũ
    df_grouped = df.groupby('image')['caption'].apply(lambda x: ', '.join(x.dropna().astype(str))).reset_index()

    count_success = 0
    count_missing = 0
    total_files = len(df_grouped)
    
    print(f"Bắt đầu quá trình COPY và TẠO TEXT cho {total_files} file...")

    for index, row in df_grouped.iterrows():
        image_filename = str(row['image']).strip()
        caption_text = str(row['caption']).strip()

        # Đường dẫn ảnh gốc (để copy)
        src_image_path = os.path.join(original_image_dir, image_filename)
        
        # Đường dẫn ảnh đích và file txt (ở thư mục mới)
        dst_image_path = os.path.join(output_dir, image_filename)
        base_name, _ = os.path.splitext(image_filename)
        txt_filepath = os.path.join(output_dir, f"{base_name}.txt")

        # Kiểm tra xem ảnh gốc có tồn tại không
        if os.path.exists(src_image_path):
            # 1. COPY ảnh từ thư mục gốc sang thư mục mới
            if not os.path.exists(dst_image_path): # Tránh copy đè nếu chạy lại code
                shutil.copy2(src_image_path, dst_image_path)
            
            # 2. TẠO file .txt ở thư mục mới
            with open(txt_filepath, "w", encoding="utf-8") as f:
                f.write(caption_text)
                
            count_success += 1
        else:
            count_missing += 1

        if (index + 1) % 500 == 0:
            print(f"  -> Đã xử lý {index + 1}/{total_files} file...")

    print("\n" + "="*50)
    print("HOÀN TẤT QUÁ TRÌNH TRÍCH XUẤT AN TOÀN!")
    print(f"Đã copy và tạo text thành công: {count_success} file.")
    if count_missing > 0:
        print(f"Có {count_missing} ảnh có tên trong CSV nhưng không tìm thấy trong thư mục gốc.")
    print(f"Dữ liệu để mang đi train đã sẵn sàng tại: {output_dir}")
    print("="*50)

if __name__ == "__main__":
    main()