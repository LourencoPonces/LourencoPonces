import os
import sys
from PIL import Image, ImageDraw


def round_image(image_path: str, output_path: str, radius_percent: int = 50, is_circular: bool = True) -> None:
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size

    if is_circular:
        radius = min(width, height) // 2
    else:
        radius = min(width, height) * radius_percent // 100

    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)

    if is_circular:
        draw.ellipse((0, 0, width, height), fill=255)
    else:
        draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=255)

    rounded_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    rounded_img.paste(img, (0, 0), mask)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    rounded_img.save(output_path)
    print(f"✅ Created rounded image: {output_path}")


def process_single_image(image_path: str, output_dir: str = "images/logos") -> None:
    """Process a single image and create both circular and rounded versions."""
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found.")
        return
    
    # Get filename without extension
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filenames
    circular_output = os.path.join(output_dir, f"{base_name}_round.png")
    rounded_output = os.path.join(output_dir, f"{base_name}_rounded.png")
    
    print(f"🔄 Processing: {image_path}")
    print("=" * 50)
    
    # Create circular version
    round_image(image_path, circular_output, is_circular=True)
    
    # Create rounded rectangle version
    round_image(image_path, rounded_output, radius_percent=20, is_circular=False)
    
    print("=" * 50)
    print("🎉 Image rounding complete!\n")
    print("📁 Generated files:")
    print(f"   • {os.path.basename(circular_output)} (circular)")
    print(f"   • {os.path.basename(rounded_output)} (rounded)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python round_images.py <image_path>")
        print("Example: python round_images.py images/logos/aeon_logo.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    process_single_image(image_path)


