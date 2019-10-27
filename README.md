# GreenEye
interview project

first download ground_truth, img, prediction files from https://drive.google.com/drive/folders/10fw953SEmkaUEkG0yj78mr7m9gSoOBm_
to the same dir as GreenEye.py.

when running the program 500 images will be open, each photo is combined from 3 images:
- left: original photo,
- middle: ground truth photo(with blue rectangles represting the grount truth bounding boxes),
- right: prediction and ground truth photo(yellow rectangles represting the prediction bounding boxes).

in addiotion, the precision will be print to screen.

calculate precision:
@ground_truth_amount is the total amount of bounding boxes in the files inside ground_truth folder.
@true_positive is the amount of bounding boxes from the prediction that where also in the relavant json in ground truth file.
@false_positive is the amount of bounding boxes from the prediction that where false - not in ground truth.
@precision = @true_positive devide by sum(@true_positive,@false_positive). 


the precision in this data set is: 0.7750696378830083.

