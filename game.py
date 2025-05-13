import tkinter as tk
import random
from collections import defaultdict



WIDTH = 400
HEIGHT = 600

# 動物とそのポイント設定
ANIMAL_POINTS = {
    "crab": 1,
    "crab": 2,
    "crab": 2,
    "crab": 3,
    "crab": 3,
    "crab": 1,
    "crab": 1
}
ANIMAL_LIST = list(ANIMAL_POINTS.keys())

class FirstPersonCatcher:
    def __init__(self, root):
        self.animal_images = {
            "crab": tk.PhotoImage(file="img/crab.png")
            # "fish": tk.PhotoImage(file="img/fish.jpg"),
            # "jellyfish": tk.PhotoImage(file="img/jellyfish.jpg"),
            # "seaweed": tk.PhotoImage(file="img/seaweed.jpg"),
            # "shrimp": tk.PhotoImage(file="img/shrimp.jpg"),
            # "squid": tk.PhotoImage(file="img/squid.jpg"),
            # "whale": tk.PhotoImage(file="img/whale.jpg"),
        }



        self.root = root
        self.root.title("一人称クリックアニマルキャッチャー")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.score = 0
        self.caught_animals = defaultdict(int)

        self.animal = self.spawn_animal()
        self.canvas.bind("<Button-1>", self.click_to_catch)

        self.score_text = self.canvas.create_text(10, 10, anchor="nw", fill="white", font=("Arial", 14), text="Score: 0")
        self.caught_text = self.canvas.create_text(WIDTH - 10, 10, anchor="ne", fill="white", font=("Arial", 12), text="")

        self.update()

    def spawn_animal(self):
        animal_type = random.choice(ANIMAL_LIST)
        from_left = random.choice([True, False])
        x = 0 if from_left else WIDTH
        direction = 1 if from_left else -1
        return {
            "x": x,
            "y": random.randint(150, HEIGHT - 100),
            "size": 30,
            "image": self.animal_images[animal_type],
            "type": animal_type,
            "id": None,
            "direction": direction
        }

    def update(self):
        if self.animal["id"]:
            self.canvas.delete(self.animal["id"])

        self.animal["x"] += self.animal["direction"] * 5
        ax = self.animal["x"]
        ay = self.animal["y"]
        self.animal["id"] = self.canvas.create_image(ax, ay, image=self.animal["image"])

        if ax < -50 or ax > WIDTH + 50:
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over", fill="red", font=("Arial", 24))
            return

        self.root.after(30, self.update)

    def click_to_catch(self, event):
        ax = self.animal["x"]
        ay = self.animal["y"]
        s = self.animal["size"]
        click_x = event.x
        click_y = event.y

        if abs(click_x - ax) < s and abs(click_y - ay) < s:
            animal_type = self.animal["type"]
            point = ANIMAL_POINTS[animal_type]
            self.canvas.delete(self.animal["id"])
            self.score += point
            self.caught_animals[animal_type] += 1

            self.canvas.itemconfigure(self.score_text, text=f"Score: {self.score}")
            self.update_caught_text()

            bonus_text = self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 30, text=f"+{point}", fill="yellow", font=("Arial", 24, "bold"))
            self.root.after(1000, lambda: self.canvas.delete(bonus_text))

            self.animal = self.spawn_animal()

    def update_caught_text(self):
        lines = ["Caught:"]
        for animal in ANIMAL_LIST:
            count = self.caught_animals[animal]
            if count > 0:
                lines.append(f"{animal} x {count}")
        text = "\n".join(lines)
        self.canvas.itemconfigure(self.caught_text, text=text)

# 実行
if __name__ == "__main__":
    root = tk.Tk()
    game = FirstPersonCatcher(root)
    root.mainloop()
