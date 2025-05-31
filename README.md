# Background text
## Опис

**Background text** — is a desktop application in Python with a graphical interface that allows you to create beautifully designed notes or pages with text overlaid on a selected background image. You can customize the font, indentation, line spacing, and font size, and immediately view the result in a preview window.


## Main features

- Enter any text for the summary.
- Select a background image (JPEG, PNG).
- Select a font (TTF, OTF).
- Adjust the indents, font size, line spacing.
- Automatically move words across the width of the page.
- Preview the result before saving.
- Automatic pagination if the text does not fit.
- Ability to save pages as images (output_pages/output_page_N.jpg).
- Support for the Ukrainian interface language.


## Installation.

1. Install Python 3.6+.
2. Install the necessary libraries:
   ```
   pip install pillow
   ```
3. Save the file `Background text.py` to the desired directory.

## Start

Use the command:
```
python Background text.py
```

## Usage.

1. Enter your text in the large text box.
2. Specify the margins, font size, and line spacing (the default values are set to the standard values).
3. Choose a background image and font.
4. Preview the result on the right side of the window.
5. Click Generate to generate the pages and automatically open the directory with the results.


## Dependencies

- Python (3.6+)
- pillow (PIL)
- tkinter

## Known limitations

- Only JPG and PNG image formats and TTF/OTF fonts are supported.
- The interface is adapted for large screens (optimally FullHD).
