# GreenEye
Interview Project

When running the program 500 images will open; each photo is combined from 3 images:
- left: original photo,
- middle: ground truth photo (with blue rectangles representing the grount truth bounding boxes),
- right: prediction and ground truth photo (yellow rectangles representing the prediction bounding boxes).
The new images will be saved in the combined directory.

In addition, the precision will be printed to the screen.

Calculate precision:
@ground_truth_amount is the total amount of bounding boxes in the files inside ground_truth folder.
@true_positive is the amount of bounding boxes from the prediction that where also in the relavant json in ground truth file.
@false_positive is the amount of bounding boxes from the prediction that where false - not in ground truth.
@precision = @true_positive devide by sum(@true_positive,@false_positive). 


The precision in this data set is: 0.7745378807602187.

