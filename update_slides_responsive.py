import os
import re

def update_slide(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add viewport meta tag if not present
    if 'width=device-width' not in content:
        head_end = content.find('</head>')
        if head_end != -1:
            meta_viewport = '    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">'
            head_start = content.rfind('<head>', 0, head_end)
            if head_start != -1:
                head_content = content[head_start:head_end]
                last_meta_pos = head_content.rfind('<meta')
                if last_meta_pos != -1:
                    # Find the end of the last meta tag
                    meta_end = content.find('>', head_start + last_meta_pos) + 1
                    content = content[:meta_end] + '\n' + meta_viewport + content[meta_end:]
    
    # Update the navigation script to ensure proper initialization
    navigation_script = '''    <script>
        // Disable previous button on first slide
        document.addEventListener('DOMContentLoaded', function() {
            const currentSlide = getCurrentSlideNumber();
            if (currentSlide === 1) {
                document.getElementById('prevButton').disabled = true;
            } else if (currentSlide === 19) {
                document.getElementById('nextButton').disabled = true;
            }
        });
    </script>'''
    
    # Replace the old navigation script with the new one
    content = re.sub(
        r'    <script>\s*// Disable previous button on first slide.*?</script>',
        navigation_script,
        content,
        flags=re.DOTALL
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # Get all slide files
    slide_files = [f for f in os.listdir('.') if f.startswith('slide') and f.endswith('.html')]
    
    # Update each slide
    for slide_file in slide_files:
        print(f"Updating {slide_file}...")
        update_slide(slide_file)
    
    print("All slides updated successfully!")

if __name__ == "__main__":
    main()
