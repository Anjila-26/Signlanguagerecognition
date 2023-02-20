import string
import os
import matplotlib.pyplot as plt

def display_images(image_paths):
    """
    Displays all images_paths in the list
    :param image_paths: List of image path of the words
    """
    fig, axes = plt.subplots(1, len(image_paths), figsize=(20, 10))
    for i, path in enumerate(image_paths):
        image = plt.imread(path)
        axes[i].imshow(image)
        axes[i].axis('off')
    plt.tight_layout()
    plt.show()

def text_to_image_paths(transcribed_words,sign_language_paths):
    """
    Converts the transcribed words to image paths
    :param transcribed_words: List of words
    :param sign_language_paths: Dictionary of letters(keys) and image paths of corresponding letterss
    :return: List of image paths
    """
    sign_language_translated = []
    for word in transcribed_words:
        image_paths = []
        for letters in word:
            letters_path = sign_language_paths[letters]
            image_paths.append(letters_path)
        sign_language_translated.append(image_paths)
    return sign_language_translated

def text_to_sign_language(transcribed_text):
    """
    Transforms and Displays text to image of sign language
    :param transcribed_text: String
    """
    directory = 'loginpage/static/loginpage/hand'
    file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    alphabet = list(string.ascii_lowercase)
    sign_language_paths = dict(zip(alphabet, file_paths))
    transcribed_words = transcribed_text.split()
    image_paths = text_to_image_paths(transcribed_words,sign_language_paths)
    i = 0
    
    for word in image_paths:
        i += 1
        print(transcribed_words[0])
        display_images(word)

def run():
    """
    Runs the Audio to SignLanguage translator Program
    :return:
    """
    transcribed_text = input("Input the text: ")
    transcribed_text.lower()
    text_to_sign_language(transcribed_text)
