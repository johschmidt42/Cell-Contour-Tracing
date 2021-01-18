import numpy as np


def create_windows(array_input, window_shape, step):
    """
    Creates windows in an array in a given shape (window_shape). The Overlap is defined by the parameter step.
    Returns a list of the offset points of the created windows that pass the threshold (Checkbox or Slice).
    In this function the step_size equals the checkbox_size.
    :type step: tuple or int
    :type window_shape: tuple or int
    :type array_input: ndarray
    """
    from utils import invert
    import numpy as np
    from skimage.util import view_as_windows

    """Check the binary image"""
    numberOfValues = np.unique(array_input, return_counts=True)

    if numberOfValues[1][1] > numberOfValues[1][0]:
        pass
    else:
        array_input = invert(array_input)

    """changes the values to 0 and 1 instead of 0 and 255"""
    array_input[array_input == 0] = 1
    array_input[array_input == 255] = 0

    listCoordinates = []

    new_array = view_as_windows(array_input, window_shape, step=step)

    """Check the dimensions of the array"""
    if array_input.ndim == 2:

        n = window_shape[0]
        m = window_shape[1]

        if type(step) == tuple:
            stepY = step[0]
            stepX = step[1]
        if type(step) == int:
            stepX = step
            stepY = step

        """Iterating over the windows of new_array"""
        for y in range(new_array.shape[0]):
            for x in range(new_array.shape[1]):
                window = new_array[y, x]

                """Creating the central slice of the window"""
                OffSetSliceY = np.uint8((n - stepY) / 2)
                OffSetSliceX = np.uint8((m - stepX) / 2)
                SliceOfWindow = window[OffSetSliceY:OffSetSliceY + stepY, OffSetSliceX:OffSetSliceX + stepX]

                """Threshold"""
                sumSlice = np.sum(SliceOfWindow, axis=(0, 1))
                if sumSlice >= min(SliceOfWindow.shape[0], SliceOfWindow.shape[1]):
                    listCoordinates.append((y * stepY, x * stepX))

    if array_input.ndim == 3:

        k = window_shape[0]
        n = window_shape[1]
        m = window_shape[2]

        if type(step) == tuple:
            stepZ = step[0]
            stepY = step[1]
            stepX = step[2]
        if type(step) == int:
            stepZ = step
            stepX = step
            stepY = step

        """Iterating over the windows of new_array"""
        for z in range(new_array.shape[0]):
            for y in range(new_array.shape[1]):
                for x in range(new_array.shape[2]):
                    window = new_array[z, y, x]

                    """Creating the central slice of the window"""
                    OffSetSliceZ = np.uint8((k - stepZ) / 2)
                    OffSetSliceY = np.uint8((n - stepY) / 2)
                    OffSetSliceX = np.uint8((m - stepX) / 2)
                    SliceOfWindow = window[OffSetSliceZ:OffSetSliceZ + stepZ, OffSetSliceY:OffSetSliceY + stepY,
                                    OffSetSliceX:OffSetSliceX + stepX]

                    """Threshold"""
                    sumSlice = np.sum(SliceOfWindow, axis=(0, 1, 2))
                    if sumSlice >= min(SliceOfWindow.shape[0], SliceOfWindow.shape[1], SliceOfWindow.shape[2]):
                        listCoordinates.append((z * stepZ, y * stepY, x * stepX))

        """Changing the values back to 0 and 255"""
        array_input[array_input == 0] = 255
        array_input[array_input == 1] = 0

    return listCoordinates


def create_windows_slice(array_input, window_shape, step, checkbox_shape):
    """
    Same as create_windows function, but the checkbox_shape does not depend on the step_size.
    :type checkbox_shape: tuple
    :type step: tuple or int
    :type window_shape: tuple or int
    :type array_input: ndarray
    """
    from utils import invert
    import numpy as np
    from skimage.util import view_as_windows

    """Check the binary image"""
    numberOfValues = np.unique(array_input, return_counts=True)

    if numberOfValues[1][1] > numberOfValues[1][0]:
        pass
    else:
        array_input = invert(array_input)

    """changes the values to 0 and 1 instead of 0 and 255"""
    array_input[array_input == 0] = 1
    array_input[array_input == 255] = 0

    listCoordinates = []

    new_array = view_as_windows(array_input, window_shape, step=step)

    """Check the dimensions of the array"""
    if array_input.ndim == 2:

        n = window_shape[0]
        m = window_shape[1]

        if type(step) == tuple:
            stepY = step[0]
            stepX = step[1]
        if type(step) == int:
            stepX = step
            stepY = step

        """Iterating over the windows of new_array"""
        for y in range(new_array.shape[0]):
            for x in range(new_array.shape[1]):
                window = new_array[y, x]

                """Creating the central slice of the window"""
                OffSetSliceY = np.uint8((n - checkbox_shape[0]) / 2)
                OffSetSliceX = np.uint8((m - checkbox_shape[1]) / 2)
                SliceOfWindow = window[OffSetSliceY:OffSetSliceY + checkbox_shape[0],
                                OffSetSliceX:OffSetSliceX + checkbox_shape[1]]

                """Threshold"""
                sumSlice = np.sum(SliceOfWindow, axis=(0, 1))
                if sumSlice >= min(SliceOfWindow.shape[0], SliceOfWindow.shape[1]):
                    listCoordinates.append((y * stepY, x * stepX))

    if array_input.ndim == 3:

        k = window_shape[0]
        n = window_shape[1]
        m = window_shape[2]

        if type(step) == tuple:
            stepZ = step[0]
            stepY = step[1]
            stepX = step[2]
        if type(step) == int:
            stepZ = step
            stepX = step
            stepY = step

        """Iterating over the windows of new_array"""
        for z in range(new_array.shape[0]):
            for y in range(new_array.shape[1]):
                for x in range(new_array.shape[2]):
                    window = new_array[z, y, x]

                    """Creating the central slice of the window"""
                    OffSetSliceZ = np.uint8((k - checkbox_shape[0]) / 2)
                    OffSetSliceY = np.uint8((n - checkbox_shape[1]) / 2)
                    OffSetSliceX = np.uint8((m - checkbox_shape[2]) / 2)
                    SliceOfWindow = window[OffSetSliceZ:OffSetSliceZ + checkbox_shape[0],
                                    OffSetSliceY:OffSetSliceY + checkbox_shape[1],
                                    OffSetSliceX:OffSetSliceX + checkbox_shape[2]]

                    """Threshold"""
                    sumSlice = np.sum(SliceOfWindow, axis=(0, 1, 2))
                    if sumSlice >= min(SliceOfWindow.shape[0], SliceOfWindow.shape[1], SliceOfWindow.shape[2]):
                        listCoordinates.append((z * stepZ, y * stepY, x * stepX))

    """Changing the values back to 0 and 255"""
    array_input[array_input == 0] = 255
    array_input[array_input == 1] = 0

    return listCoordinates


def create_windows_slice_nth(array_input, window_shape, step, checkbox_shape, nth):
    """
    Same as create_windows function, but the checkbox_shape does not depend on the step_size.
    :type checkbox_shape: tuple
    :type step: tuple or int
    :type window_shape: tuple or int
    :type array_input: ndarray
    """
    from utils import invert
    import numpy as np
    from skimage.util import view_as_windows

    """Check the binary image"""
    numberOfValues = np.unique(array_input, return_counts=True)

    if numberOfValues[1][1] > numberOfValues[1][0]:
        pass
    else:
        array_input = invert(array_input)

    """changes the values to 0 and 1 instead of 0 and 255"""
    array_input[array_input == 0] = 1
    array_input[array_input == 255] = 0

    listCoordinates = []

    new_array = view_as_windows(array_input, window_shape, step=step)

    """Check the dimensions of the array"""
    if array_input.ndim == 2:

        n = window_shape[0]
        m = window_shape[1]

        if type(step) == tuple:
            stepY = step[0]
            stepX = step[1]
        if type(step) == int:
            stepX = step
            stepY = step

        """Iterating over the windows of new_array"""
        for y in range(0, new_array.shape[0], nth):
            for x in range(0, new_array.shape[1], nth):
                window = new_array[y, x]

                """Creating the central slice of the window"""
                OffSetSliceY = np.uint8((n - checkbox_shape[0]) / 2)
                OffSetSliceX = np.uint8((m - checkbox_shape[1]) / 2)
                SliceOfWindow = window[OffSetSliceY:OffSetSliceY + checkbox_shape[0],
                                OffSetSliceX:OffSetSliceX + checkbox_shape[1]]

                """Threshold"""
                sumSlice = np.sum(SliceOfWindow, axis=(0, 1))
                if sumSlice >= min(SliceOfWindow.shape[0], SliceOfWindow.shape[1]):
                    listCoordinates.append((y * stepY, x * stepX))

    if array_input.ndim == 3:

        k = window_shape[0]
        n = window_shape[1]
        m = window_shape[2]

        if type(step) == tuple:
            stepZ = step[0]
            stepY = step[1]
            stepX = step[2]
        if type(step) == int:
            stepZ = step
            stepX = step
            stepY = step

        """Iterating over the windows of new_array"""
        for z in range(0, new_array.shape[0], nth):
            for y in range(0, new_array.shape[1], nth):
                for x in range(0, new_array.shape[2], nth):
                    window = new_array[z, y, x]

                    """Creating the central slice of the window"""
                    OffSetSliceZ = np.uint8((k - checkbox_shape[0]) / 2)
                    OffSetSliceY = np.uint8((n - checkbox_shape[1]) / 2)
                    OffSetSliceX = np.uint8((m - checkbox_shape[2]) / 2)
                    SliceOfWindow = window[OffSetSliceZ:OffSetSliceZ + checkbox_shape[0],
                                    OffSetSliceY:OffSetSliceY + checkbox_shape[1],
                                    OffSetSliceX:OffSetSliceX + checkbox_shape[2]]

                    """Threshold"""
                    sumSlice = np.sum(SliceOfWindow, axis=(0, 1, 2))
                    if sumSlice >= min(SliceOfWindow.shape[0], SliceOfWindow.shape[1], SliceOfWindow.shape[2]):
                        listCoordinates.append((z * stepZ, y * stepY, x * stepX))

    """Changing the values back to 0 and 255"""
    array_input[array_input == 0] = 255
    array_input[array_input == 1] = 0

    return listCoordinates


def draw_windows(coords, array_input, window_shape, value):
    """
    Visualize the created windows of the create_windows functions by drawing the lines.
    :type value: int
    :type window_shape: tuple
    :type array_input: ndarray
    :type coords: list

    Example:

    from tkinter.filedialog import askopenfilename
    from utils import askopendirectory
    from utils import csv_read_window_size, csv_reading
    from skimage.io import imread, imsave
    import os

    csv_file = askopenfilename(title="Select .csv file!", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    delimiter = ';'
    window_shape = csv_read_window_size(csv_file, delimiter, SkipLines=1)
    image_file = askopenfilename(title="Select Image", filetypes=(("tif files", "*.tif"), ("all files", "*.*")))
    csv_list = csv_reading(csv_file, delimiter, SkipLines=2)
    save_dir = askopendirectory()
    name = "test"
    format = ".tif"
    color = 30
    array_input = imread(image_file)

    new_array = draw_windows(csv_list, array_input, window_shape, color)
    imsave(os.path.join(save_dir, name + format), new_array)
    """

    dummy_array = np.copy(array_input)

    """Checking the dimension of the coordinates"""
    if len(window_shape) == 2:

        n = window_shape[0]
        m = window_shape[1]

        for y, x in coords:
            dummy_array[y:y + n, x] = value
            dummy_array[y, x:x + m] = value
            dummy_array[y:y + n, x + m - 1] = value
            dummy_array[y + n - 1, x:x + m] = value

    if len(window_shape) == 3:

        k = window_shape[0]
        n = window_shape[1]
        m = window_shape[2]

        for z, y, x in coords:
            dummy_array[z, y:y + n, x] = value
            dummy_array[z, y, x:x + m] = value

            dummy_array[z, y:y + n, x + m - 1] = value
            dummy_array[z, y + n - 1, x:x + m] = value

            dummy_array[z:z + k, y, x] = value
            dummy_array[z:z + k, y + n - 1, x] = value
            dummy_array[z:z + k, y, x + m - 1] = value
            dummy_array[z:z + k, y + n - 1, x + m - 1] = value

            dummy_array[z + k - 1, y:y + n, x] = value
            dummy_array[z + k - 1, y, x:x + m] = value

            dummy_array[z + k - 1, y:y + n, x + m - 1] = value
            dummy_array[z + k - 1, y + n - 1, x:x + m] = value

    return dummy_array


if __name__ == "__main__":
    from skimage.io import imread
    import pathlib
    import numpy as np


    def show_img(*arrays: np.ndarray,
                 cmap: str = 'gray'
                 ) -> None:
        import matplotlib.pyplot as plt
        for array in arrays:
            if isinstance(array, np.ndarray):
                plt.imshow(array, cmap=cmap)
                plt.show()


    img = imread(pathlib.Path(pathlib.Path.cwd() / 'images' / 'outline.png'))
    step = (10, 10)
    checkbox = (20, 20)
    window = (50, 50)
    list = create_windows_slice(img, window, step, checkbox)
    output = draw_windows(list, img, window, value=125)
    show_img(img, output)
