import pyautogui
import tkinter as tk
from PIL import ImageGrab, Image, ImageTk, ImageDraw

def spotlight_cursor():
    # Code to spotlight the cursor with normal brightness within the circle
    screen_width, screen_height = pyautogui.size()
    root = tk.Tk()
    root.attributes("-fullscreen", True)  # Create a fullscreen window
    root.attributes("-alpha", 0.9)  # Set the transparency (0.0 = fully transparent, 1.0 = fully opaque)

    canvas = tk.Canvas(root, bg="black", width=screen_width, height=screen_height)
    canvas.pack(fill=tk.BOTH, expand=True)

    radius = 75

    def draw_circle_around_cursor():
        x, y = pyautogui.position()

        # Capture screen area around the cursor
        x1, y1, x2, y2 = x - radius, y - radius, x + radius, y + radius
        screen = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        # Create a circular mask
        mask = Image.new("L", (2 * radius, 2 * radius), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 2 * radius, 2 * radius), fill=255)

        # Apply the circular mask to the captured screen
        cursor_area = Image.composite(screen, Image.new("RGBA", screen.size, (0, 0, 0, 0)), mask)

        # Create a new canvas image
        canvas.delete("circle")
        img = ImageTk.PhotoImage(cursor_area)
        canvas.create_image(x, y, image=img, tags="circle", anchor=tk.CENTER)
        canvas.image = img  # Store a reference to avoid garbage collection

        root.after(50, draw_circle_around_cursor)  # Refresh circle position every 50 ms

    draw_circle_around_cursor()

    root.after(100, lambda: root.attributes("-topmost", 1))  # Set the window to be always on top after 100 ms

    # Bind the 'Escape' key to close the overlay
    root.bind("<Escape>", lambda event: root.destroy())

    root.mainloop()

spotlight_cursor()
