#!/usr/bin/python
import os
import json
from PIL import Image, ImageDraw


# returns list of images, each image is a copy of an image from @images with the
# polygons from the relevant polygons from @polygons
# param @color is the color of the new polygons
# param @width is the width of the outline of the new polygons.
def add_polygons(images, polygons, color, width):
    new_images = []
    for img, poly in zip(images, polygons):
        img2 = img.copy()
        draw = ImageDraw.Draw(img2)
        circles = poly['circle']
        triangles = poly['triangle']
        for circle in circles:
            draw.rectangle(list(tuple(c) for c in circle), outline=color, width=width)
        for triangle in triangles:
            draw.rectangle(list(tuple(t) for t in triangle), outline=color, width=width)
        new_images.append(img2)
    return new_images


# returns list of open images files from path @path
def load_images(path):
    images_list = os.listdir(path)
    images_list.sort()
    loaded_images = []
    for img_name in images_list:
        if img_name[36] == ".":  # checks that an image is not copy (e.g with (1).jpg at the end)
            img = Image.open(path + img_name).convert('RGBA')
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), img_name)
            loaded_images.append(img)

    return loaded_images


# returns list of coordinates read from json files in @path
def load_polygons(path):
    json_list = os.listdir(path)
    json_list.sort()
    loaded_polygons = []
    for j in json_list:
        if j[36] == ".":   # checks that an image is not copy (e.g with (1).jpg at the end)
            with open(path + j) as p:
                js = json.load(p)
                loaded_polygons.append(js)
    return loaded_polygons


# returns list of images, each image combined from 3 images, each on from the same index in @l1, @l2, @l3.
# the image size is 2100X512
def combine_images(l1, l2, l3):
    combined_images = []

    for i in range(0, min(len(l1), len(l2), len(l3))):
        # the size of 1 image is 700*512, so the big image need to contain 3 images - 2100 * 512
        new_im = Image.new('RGB', (700*3, 512))

        x_offset = 0
        # left most is the original photo
        new_im.paste(l1[i], (x_offset, 0))
        x_offset += 700
        # middle one is the ground truth image:
        new_im.paste(l2[i], (x_offset, 0))
        x_offset += 700
        # right photo is the image with both ground truth and prediction
        new_im.paste(l3[i], (x_offset, 0))

        combined_images.append(new_im)
    return combined_images


# calculate precision:
# @true_positive is the amount of bounding boxes from the prediction that where true(also in ground truth file)
# @false_positive is the amount of bounding boxes from the prediction that where false - not in ground truth
# @precision = @true_positive / (@true_positive + @false_positive).
def calculate_precision(ground_truth, prediction):

    true_positive = 0
    false_positive = 0

    # iterate on each polygon from the prediction and check if it in the ground truth
    for i in range(0, len(ground_truth)):            # for each image
        for key in prediction[i]:              # for each key (triangles and circles)
            for c in prediction[i][key]:    # for each polygon
                if c in ground_truth_polygons[i][key]:
                    true_positive += 1
                else:
                    false_positive += 1

    return true_positive / (true_positive + false_positive)


# ....paths.....
original_path = "img/"
ground_truth_path = "ground_truth/"
prediction_path = "prediction/"

# load the original images to array:
orig_imgs = load_images(original_path)

# create the ground truth images:
ground_truth_polygons = load_polygons(ground_truth_path)
ground_truth_images = add_polygons(orig_imgs, ground_truth_polygons, 'blue', 3)


# create images with ground truth and prediction:
prediction_polygons = load_polygons(prediction_path)
both_images = add_polygons(ground_truth_images, prediction_polygons, 'yellow', 2)

# merge 3 lists of images to list of big image contain the relevant image from each list
combined = combine_images(orig_imgs, ground_truth_images, both_images)

# calculate the precision:
precision = calculate_precision(ground_truth_polygons, prediction_polygons)

# print precision to screen
print("precision is: " + str(precision))

# create new directory 'combined' to save the new images there
try:
    if not os.path.exists('./combined/'):
        os.makedirs('./combined/')
except OSError:
    print('Error: Creating directory. ' + "combined")

# save and show images:
for x in range(0, len(combined)):
    combined[x].save('combined/' + str(x) + '.jpg')
    # combined[x].show()

