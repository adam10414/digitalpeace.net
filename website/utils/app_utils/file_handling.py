import os
import time


def no_duplicate_files(file_name, os_path):
    """
    file_name = str, os_path = str

    This function will determine whether a given file name
    and the resulting path exists already.
    If it does, it will append a (slightly) modified timestamp 
    at the end of the file to ensure uniqueness.
    It will then return the modified file name.
    """

    #TODO:
    #Find a faster way of doing this.

    #Checking to see if the file name exists already, and if so, append a number to the end of the filename.
    while os.path.exists(f'{os_path}{file_name}'):

        #Temporarily removing the file extension, and inserting the timestamp.
        file_extension = file_name[file_name.find('.'):]
        file_name = file_name[:file_name.find('.')]

        time_stamp = str(time.time())
        time_stamp = time_stamp.replace(".", "")

        file_name += str(time_stamp)

        #Adding the file extension back to the image.
        file_name += file_extension

        #TODO:
        #Currently this counter will append numbers to the end of the file name like this:
        #test.jpg
        #test2.jpg
        #test23.jpg
        #test.234.jpg
        #etc...

        #While totally unimportant, but a nice to have:
        #Find a way to increment the filename by 1, rather than just appending a number to the end of the filename.

    return file_name
