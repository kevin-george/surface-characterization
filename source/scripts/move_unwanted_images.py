import os, subprocess

images = [os.path.join(root, name) for root, dirs, files in os.walk("./")
            for name in files if name.endswith((".png"))]

for name in images:
    cmd = "file " + name
    p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
    exif = p.stdout.read()[:-1].decode("UTF-8")
    dimensions = exif.split(",")[1]
    if dimensions != " 200 x 200":
        print("File -> " + name + " Dimensions -> " + dimensions)
        p1 =  subprocess.call(("mv", name, "./smaller_images/"))
