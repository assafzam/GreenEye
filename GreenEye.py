#!/usr/bin/python
import glob
import os
import json
from PIL import Image, ImageDraw


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


# returns list of pairs, each pair is (Image file, image name) from path @p
def load_images(p):
    # return array of images
    images_list = os.listdir(p)
    images_list.sort()
    loaded_images = []
    for img_name in images_list:
        if img_name[36] == ".":
            img = Image.open(p + img_name).convert('RGBA')
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), img_name)
            loaded_images.append(img)

    return loaded_images


def load_polygons(path):
    json_list = os.listdir(path)
    json_list.sort()
    loaded_polygons = []
    for j in json_list:
        if j[36] == ".":
            with open(path + "/" + j) as p:
                js = json.load(p)
                loaded_polygons.append(js)
    return loaded_polygons


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


"""
calculate precision:
@ground_truth_amount is the total amount of positives
@true_positive is the amount of bounding boxes from the prediction that where true(also in ground truth file)
@false_positive is the amount of bounding boxes from the prediction that where false - not in ground truth
@precision = @true_positive / (@true_positive + @false_positive). 
"""
ground_truth_amount = 0
true_positive = 0
false_positive = 0

for i in range(0, len(ground_truth_polygons)):
    ground_truth_amount += len(ground_truth_polygons[i]['circle']) + len(ground_truth_polygons[i]['triangle'])
    for c in prediction_polygons[i]['circle']:
        if c in ground_truth_polygons[i]['circle']:
            true_positive += 1
        else:
            false_positive += 1

precision = true_positive/(true_positive+false_positive)

print("precision is:")
print(precision)
for x in range(0, len(combined)):
    combined[x].save(str(x) + ".jpg")
    combined[x].show()

