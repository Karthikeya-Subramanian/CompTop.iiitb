from PIL import Image, ExifTags
import os

def resize_images(input_folder, output_folder, max_size=(300, 300), output_format="JPEG"):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through each file in the input folder
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.jpg")

        try:
            # Open the image file
            with Image.open(input_path) as img:
                # Correct the orientation
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(img._getexif().items())

                if exif[orientation] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    img = img.rotate(90, expand=True)

                # Calculate the new size while maintaining the aspect ratio
                img.thumbnail(max_size)

                # Save the resized image to the output folder in JPEG format without rotation
                img.save(output_path, output_format, exif=b"")
                print(f"Resized {filename} successfully.")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    # Set your input and output directories
    input_directory = "images"
    output_directory = "output_images"

    # Set the maximum size (width, height) in pixels
    max_size = (1000, 700)

    # Call the function to resize images
    resize_images(input_directory, output_directory, max_size)
