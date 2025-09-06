import os
import re

def update_slide(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add navigation.css link if not already present
    if '<link rel="stylesheet" href="navigation.css">' not in content:
        # Find the position to insert the navigation.css link
        head_end = content.find('</head>')
        if head_end != -1:
            # Find the last stylesheet link before </head>
            head_content = content[:head_end]
            last_link_pos = head_content.rfind('<link')
            if last_link_pos != -1:
                # Find the end of the last link tag
                link_end = content.find('>', last_link_pos) + 1
                # Insert navigation.css link after the last stylesheet
                content = content[:link_end] + '\n    <link rel="stylesheet" href="navigation.css">' + content[link_end:]
    
    # Update navigation buttons and script if already present
    if '<!-- Navigation Buttons -->' in content:
        # Replace existing navigation buttons
        navigation_pattern = r'<!-- Navigation Buttons -->.*?<!-- Navigation Buttons -->'
        new_navigation_html = '''<!-- Navigation Buttons -->
    <div class="navigation-container">
        <button class="nav-button prev-button" onclick="previousSlide()" id="prevButton">
            <i class="fas fa-arrow-left"></i>
        </button>
        <button class="nav-button next-button" onclick="nextSlide()" id="nextButton">
            <i class="fas fa-arrow-right"></i>
        </button>
    </div>'''
        content = re.sub(r'<!-- Navigation Buttons -->.*?</script>', new_navigation_html, content, flags=re.DOTALL)
    else:
        # Add navigation buttons and script if not already present
        body_end = content.rfind('</body>')
        if body_end != -1:
            # Find the last script tag before </body>
            body_content = content[:body_end]
            last_script_end = body_content.rfind('</script>')
            if last_script_end != -1:
                # Find the end of the last script tag
                script_end = content.find('>', last_script_end) + 1
                # Insert navigation buttons and script
                navigation_html = '''
    
    <!-- Navigation Buttons -->
    <div class="navigation-container">
        <button class="nav-button prev-button" onclick="previousSlide()" id="prevButton">
            <i class="fas fa-arrow-left"></i>
        </button>
        <button class="nav-button next-button" onclick="nextSlide()" id="nextButton">
            <i class="fas fa-arrow-right"></i>
        </button>
    </div>
    
    <script src="navigation.js"></script>
    <script>
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
                content = content[:script_end] + navigation_html + content[script_end:]
    
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
