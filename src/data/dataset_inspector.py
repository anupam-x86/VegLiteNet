from pathlib import Path
from PIL import Image,UnidentifiedImageError

class DatasetInspector:

    def __init__(self, dataset_root):
        self.dataset_root = Path(dataset_root)
        self.dataset_structure = {}
        self.split_names = ["train", "val", "test"]
        self.image_extensions = {".jpg", ".jpeg", ".png", ".bmp"}

    def _find_dataset_splits(self):
        """Find all available dataset splits."""

        split_directories = []

        for dataset_directory in sorted(self.dataset_root.iterdir()):
            if dataset_directory.is_dir():
                for split_name in self.split_names:
                    split_directory = dataset_directory / split_name

                    if split_directory.is_dir():
                        split_directories.append(split_directory)

        return split_directories


    def _build_dataset_structure(self):
        """Organize dataset directories by dataset and split."""

        self.dataset_structure.clear()
        split_directories = self._find_dataset_splits()

        for split_directory in split_directories:
            dataset_name = split_directory.parent.name
            split_name = split_directory.name

            class_directories = [
                class_directory
                for class_directory in sorted(split_directory.iterdir())
                if class_directory.is_dir()
            ]

            self.dataset_structure.setdefault(dataset_name, {})
            self.dataset_structure[dataset_name][split_name] = class_directories

    def _verify_image(self, image_path):
        """Check whether an image file passes Pillow's integrity verification."""
        try:
            with Image.open(image_path) as image:
                image.verify()
            with Image.open(image_path) as image:
                image.load()
            return True
        except (IOError, SyntaxError, UnidentifiedImageError):
            return False
    
    def _count_images(self, class_directory):
        """Count valid images and identify corrupted files."""
        valid_image_count = 0
        corrupted_image_files = []

        for file_path in sorted(class_directory.iterdir()):

            if file_path.is_file() and file_path.suffix.lower() in self.image_extensions:

                if self._verify_image(file_path):
                    valid_image_count += 1
                else:
                    corrupted_image_files.append(file_path)

        return valid_image_count, corrupted_image_files

    def _display_dataset_statistics(self):
        """Display image counts for every dataset split and class."""


        for dataset_name, dataset_splits in self.dataset_structure.items():
            
            total_valid_images = 0
            total_corrupted_images = 0
        
            all_corrupted_images = []

            print(f"Dataset: {dataset_name}")
            print(f"Number of splits: {len(dataset_splits)}")

            for split_name, class_directories in dataset_splits.items():

                print(f"\nSplit: {split_name}")
                print(f"Number of classes: {len(class_directories)}")

                split_valid_images = 0
                split_corrupted_images = 0
                            
                for class_directory in class_directories:

                    valid_image_count,corrupted_images = self._count_images(class_directory)
                    
                    split_valid_images += valid_image_count
                    split_corrupted_images += len(corrupted_images)

                    all_corrupted_images.extend(corrupted_images)
                    print(f"Class: {class_directory.name}: \n Valid = {valid_image_count}, \n Corrupted = {len(corrupted_images)}\n")

                total_valid_images += split_valid_images
                total_corrupted_images += split_corrupted_images

                print(f"Total Valid images in {split_name}: {split_valid_images}")
                print(f"Total Corrupted images in {split_name}: {split_corrupted_images}\n")
            
            if all_corrupted_images:
                print("Corrupted files:\n")
                for file_path in all_corrupted_images:
                    print(file_path)
            else:
                print("No corrupted images found.\n")

            print(f"Total Valid images in {dataset_name}: {total_valid_images}")
            print(f"Total Corrupted images in {dataset_name}: {total_corrupted_images}\n")

            print("-" * 50)


    def inspect_dataset(self):
        """Run the complete dataset inspection pipeline."""

        self._build_dataset_structure()
        self._display_dataset_statistics()
