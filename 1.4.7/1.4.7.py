import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw            

# Open the files in the same directory as the Python script
directory = os.path.dirname(os.path.abspath(__file__))  
logo_file = os.path.join(directory, 'student.jpg')


# Open, resize, and display earth
logo_img = PIL.Image.open('logo.png')
logo_small = logo_img.resize((89, 87)) #eye width and height measured in plt
logo_file = os.path.join(directory, 'logo.png')
logo_file.paste(logo_file, (1162, 966), mask=logo_small)

def frame(original_image, color, frame_width,):
    """ Frames the image with the specified color of a PIL.Image
    
    original_image must be a PIL.Image
    Returns a new PIL.Image with a frame, where
    0 < frame_width < 1
    is the corner radius as a portion of the shorter dimension of original_image
    """
    
    directory = os.path.dirname(os.path.abspath(__file__)) 
    
    #set the width of the frame
    width, height = original_image.size
    thickness = int(frame_width * min(width, height)) # thickness in pixels
    
    ###
    #create a mask
    ###
    
    #start with transparent mask
    r,g,b = color
    frame_mask = PIL.Image.new('RGBA', (width, height), (0,0,0,0))
    drawing_layer = PIL.ImageDraw.Draw(frame_mask)
    
    
    # Overwrite the RGBA values with A=255.
    # The 127 for RGB values was used merely for visualizing the mask
    
    # Draw two rectangles to fill interior with opaqueness
    drawing_layer.rectangle((0,0,width,thickness), fill=(r,g,b,255)) #top rectangle
    drawing_layer.rectangle((0,0,thickness,height), fill=(r,g,b,255))  
    drawing_layer.rectangle((0,height,width,height-thickness),fill=(r,g,b,255))
    drawing_layer.rectangle((width,0,width-thickness,height),fill=(r,g,b,255))                  
    # Uncomment the following line to show the mask
    # plt.imshow(rounded_mask)
    
    # Make the new image, starting with all transparent
    result = original_image.copy()
    result.paste(frame_mask, (0,0), mask=frame_mask)
    return result
    


    
def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def frame_all_images(directory=None, color=(0,0,0), frame_width=0.10):
    """ Saves a modfied version of each image in directory.
    
    Uses current directory if no directory is specified. 
    Places images in subdirectory 'modified', creating it if it does not exist.
    New image files are of type PNG and have transparent rounded corners.
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'modified')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    # Load all the images
    image_list, file_list = get_images(directory)  

    # Go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        print n
        filename, filetype = file_list[n].split('.')
        
        # Round the corners with default percent of radius
        new_image = frame(image_list[n],color,frame_width) 
        
        # Save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename) 