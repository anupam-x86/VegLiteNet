from pathlib import Path
from PIL import Image,UnidentifiedImageError
import hashlib
from collections import Counter

class DatasetInspector:

    def __init__(self, dataset_root):
        self.dataset_root = Path(dataset_root)
        if not self.dataset_root.exists():
            raise FileNotFoundError(f"Dataset directory does not exist: {self.dataset_root}")
        if not self.dataset_root.is_dir():
            raise NotADirectoryError(f"Dataset path is not a directory: {self.dataset_root}")
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

    def _verify_image(self, file_path):
        """Check whether an image file passes Pillow's integrity verification."""
        try:
            with Image.open(file_path) as image:
                image.verify()
            with Image.open(file_path) as image:
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

    def _calculate_image_hash(self,file_path):
        with open(file_path,"rb") as image:
            file_hash = hashlib.sha256(image.read()).hexdigest()
        return file_hash

    def find_duplicate_images(self):
        image_hashes = {}

        if not self.dataset_structure:
            self._build_dataset_structure()

        for dataset_splits in self.dataset_structure.values():
            for class_directories in dataset_splits.values():
                for class_directory in sorted(class_directories):
                    for file_path in sorted(class_directory.iterdir()):
                        if file_path.is_file() and file_path.suffix.lower() in self.image_extensions and self._verify_image(file_path):
                            file_hash = self._calculate_image_hash(file_path)
                            image_hashes.setdefault(file_hash,[]).append(str(file_path))

        duplicate_image_hashes = {
            file_hash: file_paths
            for file_hash, file_paths in image_hashes.items()
            if len(file_paths) > 1
        }
        return duplicate_image_hashes

    def _get_image_properties(self,file_path):
        with Image.open(file_path) as image:
            image_properties = {
                "size": image.size,
                "format": image.format,
                "mode": image.mode,
            } 
        return image_properties

    def analyze_images_properties(self):
        sizes = []
        formats = []
        modes = []
        if not self.dataset_structure:
            self._build_dataset_structure()

        for dataset_splits in self.dataset_structure.values():
            for class_directories in dataset_splits.values():
                for class_directory in sorted(class_directories):
                    for file_path in sorted(class_directory.iterdir()):
                        if file_path.is_file() and file_path.suffix.lower() in self.image_extensions and self._verify_image(file_path):
                            properties = self._get_image_properties(file_path)
                            sizes.append(properties['size'])
                            formats.append(properties['format'])
                            modes.append(properties['mode'])

        size_counts = Counter(sizes)  
        format_counts = Counter(formats)  
        mode_counts = Counter(modes)  
        return {"sizes": size_counts, "formats": format_counts, "modes": mode_counts}

    def dataset_statistics(self):
        """Return image counts for every dataset split and class."""

        statistics = {
            "datasets": {},
            "total_valid_images": 0,
            "total_corrupted_images": 0
        }
        self._build_dataset_structure()
        
        if not self.dataset_structure:
            return {}

        for dataset_name, dataset_splits in self.dataset_structure.items():

            statistics["datasets"].setdefault(dataset_name,{})
            
            statistics["datasets"][dataset_name]["total_valid_images"] = 0
            statistics["datasets"][dataset_name]["total_corrupted_images"] = 0

            for split_name, class_directories in dataset_splits.items():

                split_valid_images = 0
                split_corrupted_images = 0
                statistics["datasets"][dataset_name].setdefault(split_name,{"classes": {}})

                for class_directory in class_directories:

                    valid_image_count,corrupted_images = self._count_images(class_directory)

                    split_valid_images += valid_image_count
                    split_corrupted_images += len(corrupted_images)

                    statistics["datasets"][dataset_name][split_name]["classes"][class_directory.name] = {
                            "valid_images_count": valid_image_count,
                            "corrupted_images_count": len(corrupted_images),
                            "corrupted_images": corrupted_images
                        }

                statistics["datasets"][dataset_name][split_name]["split_valid"] = split_valid_images
                statistics["datasets"][dataset_name][split_name]["split_invalid"] = split_corrupted_images

                statistics["datasets"][dataset_name]["total_valid_images"] += split_valid_images
                statistics["datasets"][dataset_name]["total_corrupted_images"] += split_corrupted_images

                statistics["total_valid_images"] += split_valid_images
                statistics["total_corrupted_images"] += split_corrupted_images
        return statistics
