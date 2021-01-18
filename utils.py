import numpy as np
from skimage.io import imsave
from scipy.ndimage import distance_transform_edt


def invert(array_in):
    return ~array_in


def create_CSV(dir: str, name: str, firstLine: list, secondLine: list, delimiter: str, list: list):
    """
    Creates a CSV File with the given delimiter in a given directory (dir). The first line is meant to consist of the
    names of the dimensions, e.g. "X" or "Y". The second line should be the window_size. :type
    secondLine: list :type list: list :type delimiter: str :type firstLine: list :type name: str :type dir: str
    """
    import csv
    import os
    name = name + ".csv"
    directory = os.path.join(dir, name)

    with open(directory, 'w') as myfile:
        csv_writer = csv.writer(myfile, delimiter=delimiter, lineterminator='\n')
        csv_writer.writerow(firstLine)
        csv_writer.writerow(secondLine)
        for element in list:
            csv_writer.writerow(element)
    return directory


def create_distanceMap(array_input):
    """
    Returns the distance map of a binary image.
    :type array_input: ndarray

    Example:
    from skimage.io import imsave
    import os
    from tifffile.tifffile import askopenfilename
    from AskOpenDirectory import askopendirectory

    savedir = askopendirectory()
    filename = "test"

    imsave(os.path.join(savedir, filename + ".tif"), np.uint8(create_distanceMap(imread(askopenfilename()))))
    """

    """Check the binary image"""
    numberOfValues = np.unique(array_input, return_counts=True)

    if numberOfValues[1][0] > numberOfValues[1][1]:
        pass
    else:
        array_input = invert(array_input)

    """Get the distance map of the binary image"""
    array_dist = distance_transform_edt(array_input)

    return array_dist


def create_Folder(directory: str, folderName: str):
    """ Creates folder in a given directory.
    :type folderName: str
    :type directory: str
    """
    import os, errno

    directoryCreate = os.path.join(directory, folderName)

    try:
        os.makedirs(directoryCreate)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return directoryCreate


def create_outline(array_input):
    """
    Creates the outline of a binary image.
    :type array_input: ndarray

    Example:
    from skimage.io import imsave
    import os
    from tifffile.tifffile import askopenfilename
    from skimage.io import imread
    from AskOpenDirectory import askopendirectory

    savedir = askopendirectory()
    filename = "test"
    imsave(os.path.join(savedir, filename + "_outline" + ".tif"), create_outline(imread(askopenfilename())))
    """
    import numpy as np
    from skimage.segmentation import find_boundaries

    """Check the binary image"""
    numberOfValues = np.unique(array_input, return_counts=True)

    if numberOfValues[1][1] > numberOfValues[1][0]:
        pass
    else:
        array_input = invert(array_input)

    """Get the outline/contour of the binary image"""
    array_input = find_boundaries(array_input, mode='inner', connectivity=2, background=255).astype(np.uint8)
    array_input[array_input == 0] = 255
    array_input[array_input == 1] = 0

    return array_input


def masking(array_input_cell, array_input_mask):
    """
    Uses a binary image as mask and applies it to the an image.
    :type array_input_mask: ndarray
    :type array_input_cell: ndarray

    Example:
    from tkinter.filedialog import askopenfilename
    from utils import askopendirectory
    from skimage.io import imsave, imread
    import os

    open_dir_cell = imread(askopenfilename(title="Select Cell"))
    open_dir_ring = imread(askopenfilename(title="Select Ring"))

    save_dir = askopendirectory()
    name = "Test.tif"

    new_array = masking(open_dir_cell, open_dir_ring)
    imsave(os.path.join(save_dir, name), new_array)
    """
    import numpy as np

    """Changing the values to 0 and 1 to create the mask"""
    array_input_mask[array_input_mask == 0] = 0
    array_input_mask[array_input_mask == 255] = 1

    """Masking"""
    mask = np.ma.masked_array(array_input_cell, mask=array_input_mask)
    mask[mask.mask == True] = 255

    return mask


def threshold_distancemap(array_input, width):
    """Thresholds a distance map and thereby creates a mask.
    Returns the thresholded distance map.
    :type width: int
    :type array_input: bytearray
    """

    array_input[array_input > width] = 0
    array_input[array_input > 0] = 1
    array_input[array_input == 0] = 255
    array_input[array_input == 1] = 0
    return array_input


def save_windows(csv_list, array_input, window_shape, save_dir, name, format):
    """
    Saves the created windows from the create_windows function. Takes the csv_list with the coords and an ndarray as
    input. Counting starts at 1 and 4 digits are set. Can be changed in the code. Format should be .tif,
    however .hdf5 is planned. :type format: str :type name: str :type save_dir: str :type window_shape: tuple :type
    array_input: ndarray :type csv_list: list

    Example:
    from tkinter.filedialog import askopenfilename
    from skimage.io import imsave
    from utils import askopendirectory
    from skimage.io import imsave, imread
    from Read_CSV import csv_reading, csv_read_window_size

    delimiter = ';'
    csv_list = csv_reading(
        askopenfilename(title="Select .csv file!", filetypes=(("csv files", "*.csv"), ("all files", "*.*"))), delimiter,
        SkipLines=2)
    array_input = imread(askopenfilename(title="Select Cell", filetypes=(("tif files", "*.tif"), ("all files", "*.*"))))
    window_shape = csv_read_window_size(csv_list, delimiter, SkipLines=1)

    save_dir = askopendirectory()
    name = "stack05_window_"
    format = ".tif"

    save_windows(csv_list, array_input, window_shape, save_dir, name, format)
    """
    import os

    count = 1
    digits = 4

    if len(window_shape) == 2:

        n = window_shape[0]
        m = window_shape[1]

        for y, x in csv_list:
            count_length = len(str(count))
            zeros = (digits - count_length) * str(0)

            array = array_input[y:y + n, x:x + m]
            imsave(os.path.join(save_dir, name + zeros + str(count) + format), array)
            count += 1

    if len(window_shape) == 3:
        k = window_shape[0]
        n = window_shape[1]
        m = window_shape[2]

        for z, y, x in csv_list:
            count_length = len(str(count))
            zeros = (digits - count_length) * str(0)

            array = array_input[z:z + k, y:y + n, x:x + m]
            imsave(os.path.join(save_dir, name + zeros + str(count) + format), array)
            count += 1


def csv_reading(csv_file, delimiter, SkipLines):
    """
    Reads a csv file with the given delimiter. The parameter defines how many lines should be skipped. Returns a list with coordinates.
    :type dim: int
    :type delimiter: str
    :type csv_file: str
    """
    import csv

    list_values = []

    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)

        for i in range(SkipLines):
            next(csv_reader)

        for line in csv_reader:
            TupleList = [int(line[i]) for i in range(0, len(line))]
            list_values.append(tuple(TupleList))

    return list_values


def csv_read_window_size(csv_file, delimiter, SkipLines):
    """
    Same as csv_reading but reads only one specific line. This specific line is meant to be the information for the
    window size. :type SkipLines: int :type delimiter: str :type csv_file: str

    Example:
    from tkinter.filedialog import askopenfilename
    open_dir = askopenfilename()
    list = csv_reading(open_dir, delimiter=';', SkipLines=2)
    print(list)
    print(len(list))
    print("")
    open_dir = askopenfilename()
    text = csv_read_window_size(open_dir, delimiter=';', SkipLines=1)
    print(tuple(text))
    """
    import csv

    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)

        for i in range(SkipLines):
            next(csv_reader)

        line = list(csv_reader)
        text = line[0]

        for i in range(0, len(text)):
            text[i] = int(text[i])

    return text


def recreate_Image(array_reference, csv_list, window_shape, path_windows):
    """
    Recreates the image from a folder with single windows and a list of their offset coordinates.
    :type path_windows: string
    :type window_shape: tuple
    :type csv_list: list
    :type array_reference: ndarray

    Example:

    from tkinter.filedialog import askopenfilename
    import os
    import numpy as np
    from skimage.io import imsave, imread
    from utils import askopendirectory
    from utils import csv_reading, csv_read_window_size

    csv_file = askopenfilename(title="Select .csv file!", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    array_input = imread(
        askopenfilename(title="Select Image for reference", filetypes=(("tif files", "*.tif"), ("all files", "*.*"))))
    path_windows = askopendirectory()
    delimiter = ';'
    csv_list = csv_reading(csv_file, delimiter, 2)
    window_size = csv_read_window_size(csv_file, delimiter, 1)

    new_array = recreate_Image(array_input, csv_list, window_size, path_windows)
    name = "test.tif"
    imsave(os.path.join(askopendirectory(), name), np.uint8(new_array))
    """

    """Import libraries"""
    from skimage.io import imread
    import numpy as np
    import os

    """Create a dummy array with the same size as the input array"""
    array_dummy = np.zeros_like(array_reference)

    """Load the arrays of a given folder and save them in a list"""
    list_image_names = []
    list_image_windows = []

    for name in os.listdir(path_windows):
        name_path = os.path.join(path_windows, name)
        list_image_names.append(name_path)

    list_image_names.sort()

    for element in list_image_names:
        array_input = imread(element)
        list_image_windows.append(array_input)

    if len(window_shape) == 2:
        n = int(window_shape[0])
        m = int(window_shape[1])
    elif len(window_shape) == 3:
        pass
        # TODO Add if len(window_shape == 3)

    """Creating the wighted mask"""
    count = 0

    for y, x in csv_list:
        slice = np.ones_like(list_image_windows[count])
        array_dummy[y:y + n, x:x + m] += slice
        count += 1

    """Changing the data type of the mask to float"""
    array_dummy = array_dummy.astype(float)

    """Changing all zeros to NaN as the reciprocal value of 0 is undefined"""
    array_dummy[array_dummy == 0] = np.nan

    """Getting the reciprocal array"""
    array_dummy = np.reciprocal(array_dummy)

    """Multiply the windows with the weighted values"""
    count = 0

    new_slices = []

    for y, x in csv_list:
        slice = list_image_windows[count].astype(float)
        slice *= array_dummy[y:y + n, x:x + m]
        new_slices.append(slice)
        count += 1

    array_dummy = np.zeros_like(array_reference).astype(float)

    count = 0

    """Recreating the image, based on the windows"""
    for y, x in csv_list:
        slice = new_slices[count]
        array_dummy[y:y + n, x:x + m] += slice
        count += 1

    return array_dummy
