import os
import re

def update_slide(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add responsive.css link if not present
    if 'responsive.css' not in content:
        # Find the position to insert the responsive.css link
        head_end = content.find('</head>')
        if head_end != -1:
            # Find the navigation.css link
            nav_css_pos = content.find('navigation.css')
            if nav_css_pos != -1:
                # Find the end of the navigation.css link tag
                link_end = content.find('>', nav_css_pos) + 1
                # Insert responsive.css link after navigation.css
                content = content[:link_end] + '\n    <link rel="stylesheet" href="responsive.css">' + content[link_end:]

    # Add fullscreen button if not present
    if 'fullscreen-button' not in content:
        # Find the navigation container
        nav_container_pos = content.find('<div class="navigation-container">')
        if nav_container_pos != -1:
            # Insert fullscreen button before navigation container
            fullscreen_button = '''    <!-- Fullscreen Button -->
    <button class="fullscreen-button" onclick="toggleFullscreen()" id="fullscreenButton">
        <i class="fas fa-expand"></i>
    </button>

    '''
            content = content[:nav_container_pos] + fullscreen_button + content[nav_container_pos:]

    # Update slide class to ensure responsive behavior
    content = content.replace(
        'width: 1280px;\n            min-height: 720px;',
        'width: 100%;\n            min-height: 100vh;'
    )

    content = content.replace(
        'width: 1280px;\n    min-height: 720px;',
        'width: 100%;\n    min-height: 100vh;'
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
