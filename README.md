# Image Annotation Tool

A clean, user-friendly OpenCV-based annotation tool for creating bounding box annotations for object detection datasets.

## Features

- **Interactive Bounding Box Creation**: Click two points to create precise bounding boxes
- **Real-time Visual Feedback**: See annotations as you create them with blue rectangle overlays
- **Batch Processing**: Automatically processes all `.bmp` images in a directory
- **Flexible Navigation**: Skip images, clear annotations, or quit at any time
- **Clean Output Format**: Generates standardized annotation files compatible with object detection frameworks
- **Error Handling**: Robust validation and clear error messages
- **Progress Tracking**: Visual progress indicators and detailed console feedback

## Requirements

- Python 3.6+
- OpenCV (`cv2`)
- Standard library modules: `sys`, `glob`, `os`, `typing`, `dataclasses`

## Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/opencv-annotation-tool.git
cd opencv-annotation-tool
```

2. Install OpenCV:
```bash
pip install opencv-python
```

## Usage

### Basic Usage
```bash
python annotation.py /path/to/images/ output.txt
```

### Arguments
- `path/to/images/`: Directory containing `.bmp` images to annotate
- `output.txt`: Output file where annotations will be saved

### Controls
- **Left Click**: Select bounding box corners (two clicks create one box)
- **'n' Key**: Save current annotations and move to next image
- **'c' Key**: Clear all annotations for the current image
- **'q' Key**: Save current annotations and quit the program

### Workflow
1. Run the program with your image directory and desired output file
2. For each image:
   - Click on the top-left corner of the object you want to annotate
   - Click on the bottom-right corner to complete the bounding box
   - Repeat for multiple objects in the same image
   - Press 'n' to save and move to the next image, or 'c' to clear and start over
3. Press 'q' to quit and save all annotations

## Output Format

The tool generates annotations in the following format:
```
image_path object_count x1 y1 width1 height1 x2 y2 width2 height2 ...
```

### Example Output
```
/path/to/images/0001.bmp 2 23 64 42 38 98 103 56 74 
/path/to/images/0002.bmp 1 15 25 80 60 
```

This means:
- `0001.bmp` has 2 objects:
  - Object 1: top-left at (23, 64), dimensions 42×38 pixels
  - Object 2: top-left at (98, 103), dimensions 56×74 pixels
- `0002.bmp` has 1 object:
  - Object 1: top-left at (15, 25), dimensions 80×60 pixels

## Code Structure

The refactored codebase follows object-oriented principles with clear separation of concerns:

### Classes

- **`BoundingBox`**: Data class representing a single bounding box annotation
- **`ImageAnnotator`**: Handles image display, mouse interactions, and annotation management
- **`AnnotationSession`**: Manages the overall annotation workflow across multiple images

### Key Methods

- `load_image()`: Loads and prepares images for annotation
- `mouse_callback()`: Processes mouse clicks for bounding box creation
- `reset_annotations()`: Clears all annotations for the current image
- `run()`: Main session loop handling user input and file processing

## File Support

Currently supports `.bmp` image files. The code can be easily extended to support additional formats by modifying the file pattern in the `_load_image_files()` method.

## Error Handling

The tool includes comprehensive error handling for:
- Invalid command line arguments
- Non-existent file paths
- Image loading failures
- Empty directories

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Potential Enhancements
- Support for additional image formats (JPG, PNG, etc.)
- Undo/redo functionality
- Different annotation shapes (circles, polygons)
- Export to popular dataset formats (YOLO, COCO, Pascal VOC)
- GUI improvements with tkinter or Qt

## License

This project is open source and available under the MIT License.

## Changelog

### v2.0 (Current)
- Complete code refactoring with object-oriented design
- Improved error handling and user feedback
- Better code documentation and type hints
- Enhanced visual feedback with thicker borders
- Progress tracking and detailed console output

### v1.0 (Original)
- Basic annotation functionality
- Simple procedural code structure
