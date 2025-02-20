import cv2
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# Encryption Function
def encrypt_image(image_path, secret_message, key):
    img = cv2.imread(image_path)
    if img is None or len(secret_message) + len(key) + 1 > img.size:
        messagebox.showerror("Error", "Invalid image or message too large.")
        return

    full_message = key + ':' + secret_message
    img[0, 0, 0] = len(full_message)

    for i, char in enumerate(full_message):
        img[(i + 1) // img.shape[1], (i + 1) % img.shape[1], 0] = ord(char)

    cv2.imwrite("encrypted_image.png", img)
    messagebox.showinfo("Success", "Encrypted image saved as 'encrypted_image.png'")

# Decryption Function
def decrypt_image(image_path):
    user_key = simpledialog.askstring("Input", "Enter Decryption Key:", show="*")
    if not user_key:
        return

    img = cv2.imread(image_path)
    length = img[0, 0, 0]
    full_message = ''.join(chr(img[(i + 1) // img.shape[1], (i + 1) % img.shape[1], 0]) for i in range(length))

    if ':' in full_message:
        stored_key, message = full_message.split(':', 1)
        if stored_key == user_key:
            messagebox.showinfo("Decryption Result", message.strip())
        else:
            messagebox.showerror("Error", "Incorrect key.")
    else:
        messagebox.showerror("Error", "Corrupted data or incorrect format.")

# File Selection
def select_image(action):
    path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if path:
        if action == "encrypt":
            user_key = key_entry.get()
            if user_key:
                encrypt_image(path, secret_entry.get(), user_key)
            else:
                messagebox.showerror("Error", "Please enter an encryption key.")
        elif action == "decrypt":
            decrypt_image(path)

# GUI Setup
root = tk.Tk()
root.title("Steganography Tool")
root.geometry("350x250")

# Widgets
tk.Label(root, text="Secret Message:").pack(pady=5)
secret_entry = tk.Entry(root, width=40)
secret_entry.pack(pady=5)

tk.Label(root, text="Encryption Key:").pack(pady=5)
key_entry = tk.Entry(root, width=40, show="*")
key_entry.pack(pady=5)

# Buttons
tk.Button(root, text="Encrypt", command=lambda: select_image("encrypt")).pack(pady=5)
tk.Button(root, text="Decrypt", command=lambda: select_image("decrypt")).pack(pady=5)

root.mainloop()
