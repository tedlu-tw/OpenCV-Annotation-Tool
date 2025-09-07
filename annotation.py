import cv2
import sys
import glob
import os
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class BoundingBox:
    """Represents a bounding box annotation."""
    x: int
    y: int
    width: int
    height: int
    
    def __str__(self) -> str:
        return f"{self.x} {self.y} {self.width} {self.height}"


class ImageAnnotator:
    """Main class for handling image annotation functionality."""
    
    def __init__(self, debug: bool = True):
        self.debug = debug
        self.current_frame = None
        self.original_frame = None
        self.annotations: List[BoundingBox] = []
        self.click_count = 0
        self.start_point: Optional[Tuple[int, int]] = None
        self.window_name = "Image Annotator"
        
    def mouse_callback(self, event: int, x: int, y: int, flags: int, param) -> None:
        """Handle mouse events for drawing bounding boxes."""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.click_count += 1
            
            if self.click_count % 2 == 1:
                # First click - record starting point
                self.start_point = (x, y)
                if self.debug:
                    print(f"Started box at ({x}, {y})")
            else:
                # Second click - complete the bounding box
                if self.start_point is not None:
                    self._create_bounding_box(self.start_point, (x, y))
                    self.start_point = None
    
    def _create_bounding_box(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        """Create a bounding box from two points and add it to annotations."""
        x1, y1 = start
        x2, y2 = end
        
        # Calculate top-left corner and dimensions
        top_left_x = min(x1, x2)
        top_left_y = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        # Create and store the bounding box
        bbox = BoundingBox(top_left_x, top_left_y, width, height)
        self.annotations.append(bbox)
        
        if self.debug:
            print(f"Added bounding box: {bbox}")
        
        # Draw the rectangle on the image
        self._draw_rectangle(bbox)
        self._update_display()
    
    def _draw_rectangle(self, bbox: BoundingBox) -> None:
        """Draw a rectangle on the current frame."""
        cv2.rectangle(
            self.current_frame,
            (bbox.x, bbox.y),
            (bbox.x + bbox.width, bbox.y + bbox.height),
            (255, 0, 0),  # Blue color
            2  # Thickness
        )
    
    def _draw_all_rectangles(self) -> None:
        """Redraw all bounding boxes on the current frame."""
        for bbox in self.annotations:
            self._draw_rectangle(bbox)
    
    def _update_display(self) -> None:
        """Update the display window."""
        cv2.imshow(self.window_name, self.current_frame)
    
    def load_image(self, image_path: str) -> bool:
        """Load an image for annotation."""
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"Error: Could not load image {image_path}")
            return False
        
        self.original_frame = frame.copy()
        self.current_frame = frame.copy()
        self.annotations.clear()
        self.click_count = 0
        self.start_point = None
        
        if self.debug:
            print(f"Loaded image: {image_path}")
        
        return True
    
    def reset_annotations(self) -> None:
        """Clear all annotations and restore original image."""
        self.annotations.clear()
        self.click_count = 0
        self.start_point = None
        if self.original_frame is not None:
            self.current_frame = self.original_frame.copy()
            self._update_display()
        
        if self.debug:
            print("Cleared all annotations")
    
    def get_annotation_count(self) -> int:
        """Get the number of annotations."""
        return len(self.annotations)
    
    def get_annotations_string(self) -> str:
        """Get annotations as a formatted string."""
        return " ".join(str(bbox) + " " for bbox in self.annotations)


class AnnotationSession:
    """Manages the annotation session for multiple images."""
    
    def __init__(self, image_path: str, output_file: str, debug: bool = True):
        self.image_path = image_path
        self.output_file = output_file
        self.debug = debug
        self.annotator = ImageAnnotator(debug)
        self.image_files = []
        
    def _load_image_files(self) -> bool:
        """Load list of image files from the specified path."""
        pattern = os.path.join(self.image_path, "*.bmp")
        self.image_files = glob.glob(pattern)
        
        if not self.image_files:
            print(f"No .bmp files found in {self.image_path}")
            return False
        
        if self.debug:
            print(f"Found {len(self.image_files)} images:")
            for img in self.image_files:
                print(f"  - {img}")
        
        return True
    
    def _setup_window(self) -> None:
        """Set up the OpenCV window and mouse callback."""
        cv2.namedWindow(self.annotator.window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(self.annotator.window_name, self.annotator.mouse_callback)
    
    def _print_instructions(self) -> None:
        """Print usage instructions."""
        print("\n" + "="*50)
        print("IMAGE ANNOTATION TOOL")
        print("="*50)
        print("Instructions:")
        print("- Click two points to create a bounding box")
        print("- Press 'c' to clear all annotations for current image")
        print("- Press 'n' to save and move to next image")
        print("- Press 'q' to quit and save")
        print("="*50 + "\n")
    
    def run(self) -> None:
        """Run the annotation session."""
        if not self._load_image_files():
            return
        
        self._setup_window()
        
        if self.debug:
            self._print_instructions()
        
        with open(self.output_file, "w") as output:
            for i, image_file in enumerate(self.image_files):
                if not self.annotator.load_image(image_file):
                    continue
                
                print(f"\nAnnotating image {i+1}/{len(self.image_files)}: {os.path.basename(image_file)}")
                self.annotator._update_display()
                
                # Wait for user input
                while True:
                    key = cv2.waitKey(0) & 0xFF
                    
                    if key == ord('q'):
                        # Quit - save current annotations if any
                        self._save_annotations(output, image_file)
                        print("Quitting...")
                        return
                    elif key == ord('n'):
                        # Next image - save current annotations
                        self._save_annotations(output, image_file)
                        break
                    elif key == ord('c'):
                        # Clear annotations
                        self.annotator.reset_annotations()
        
        cv2.destroyAllWindows()
        print(f"\nAnnotations saved to: {self.output_file}")
    
    def _save_annotations(self, output_file, image_file: str) -> None:
        """Save annotations for the current image."""
        annotation_count = self.annotator.get_annotation_count()
        if annotation_count > 0:
            line = f"{image_file} {annotation_count} {self.annotator.get_annotations_string()}\n"
            output_file.write(line)
            
            if self.debug:
                print(f"Saved {annotation_count} annotations for {os.path.basename(image_file)}")
        else:
            if self.debug:
                print(f"No annotations to save for {os.path.basename(image_file)}")


def main():
    """Main function to handle command line arguments and start the session."""
    if len(sys.argv) != 3:
        print("Usage: python annotation.py /path/to/images output_filename.txt")
        print("\nDescription:")
        print("  This tool allows you to annotate images by drawing bounding boxes.")
        print("  It processes all .bmp files in the specified directory.")
        sys.exit(1)
    
    image_path = sys.argv[1]
    output_file = sys.argv[2]
    
    # Validate input path
    if not os.path.exists(image_path):
        print(f"Error: Path '{image_path}' does not exist.")
        sys.exit(1)
    
    if not os.path.isdir(image_path):
        print(f"Error: '{image_path}' is not a directory.")
        sys.exit(1)
    
    # Create and run annotation session
    session = AnnotationSession(image_path, output_file, debug=True)
    session.run()


if __name__ == "__main__":
    main()
