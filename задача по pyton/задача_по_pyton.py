#Libraries for creating an application
import tkinter as tk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt

#Libraries for the Stable Diffusion neural network
import keras_cv
from tensorflow import keras

class TextToImage:
    def __init__(self):

        #Width and height image
        self.width = 512
        self.height = 512

        #Window settings
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Stable diffusion model
        self.model = keras_cv.models.StableDiffusion(img_width=self.width, img_height=self.height, jit_compile=True)

        #Creating an input field
        self.entry = tk.Entry(self.root, width=50, font=('Times New Roman', 20))
        self.entry.pack(pady=50)

        #Creating a button, witch generate image
        self.image_button = tk.Button(self.root, text="Execute", font=("Times New Roman", 15),background= "bisque", width=20, command=self.print_image)
        self.image_button.pack(pady=10)

        #Create a close button
        self.close_button = tk.Button(self.root, text="X", font=("Times New Roman", 13), background= "red", command=self.on_closing)
        self.close_button.place(relx=1, y=0, anchor="ne")

        #image settings
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

    #Close function
    def on_closing(self):
        self.root.destroy()
    
    def plot_images(self, images):
        plt.figure(figsize=(20, 20))
        for i in range(len(images)):
            ax = plt.subplot(1, len(images), i + 1)
            plt.imshow(images[i])
            plt.axis("off")

    def print_image(self):
        if self.entry.get().isalpha():
            images = self.model.text_to_image(self.entry.get(), batch_size=1, num_steps= 15, unconditional_guidance_scale = 7)
            self.plot_images(images)
            path = "img1.png"
            plt.savefig(path, bbox_inches='tight')
            image = Image.open(path)
            max_size = (self.width, self.height)
            image.thumbnail(max_size)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TextToImage()
    app.run()
