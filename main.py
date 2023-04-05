import os 
import PIL.Image
from datetime import datetime

folder_to_sort = input("Chemin du dossier à trier : ")
destination = input("Chemin du dossier de destination (defaut : dans le même dossier):")

valid_images = [".jpg",".png",".jpeg"]

def get_all_images(folder=None,images = []):
    """
    Get all images in a folder and subfolder
    """
    for file in os.listdir(folder):
        file = os.path.join(folder,file)
        if any(file.endswith(ext) for ext in valid_images):
            images.append(file)
        if os.path.isdir(file):
            get_all_images(file,images)
    return images

def get_exif_data(image):
    image_file = PIL.Image.open(image)
    print(image_file.__dict__)
    exit()
    image_file.verify()
    return image_file._getexif()

all_images = get_all_images(folder_to_sort)
len_images = len(all_images)


if all_images:
    try:
        os.mkdir(destination)
    except:
        pass

images_copies = 0
for img in all_images:
    data = get_exif_data(img)  
    try:
        date = data[36867]
        if not date:
            print(f"Date pas trouvée pour {img}")
            continue

        date = datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
        month = date.strftime("%B")
        year = date.strftime("%Y")
        try:
            os.mkdir(f"{destination}/{year}")
        except:
            pass
        
        try:
            os.mkdir(f"{destination}/{year}/{month}")
        except:
            pass

        os.system(f"cp {img} {destination}/{year}/{month}")
        images_copies += 1

    except Exception as E:
        continue
    

print(f"{images_copies} images copiées sur {len_images}")