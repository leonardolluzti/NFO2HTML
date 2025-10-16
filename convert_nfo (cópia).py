import xml.etree.ElementTree as ET
import os

def convert_nfo_to_html(nfo_filepath, output_filepath):
    """
    Converts a tvshow.nfo file into an HTML5 file.

    Args:
        nfo_filepath (str): The path to the tvshow.nfo file.
        output_filepath (str): The desired path for the output HTML file.
    """
    try:
        tree = ET.parse(nfo_filepath)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing NFO file: {e}")
        return
    except FileNotFoundError:
        print(f"Error: NFO file not found at '{nfo_filepath}'")
        return

    # Extracting common TV show details
    title = root.findtext('title', 'Unknown Title')
    originaltitle = root.findtext('originaltitle', 'Unknown originaltitle')
    plot = root.findtext('plot', 'No plot available.')
    premiered = root.findtext('premiered', 'N/A')
    mpaa = root.findtext('mpaa', 'Not Rated')
    studio_elements = root.findall('studio')
    studios = [studio.text for studio in studio_elements if studio.text]
    genre_elements = root.findall('genre')
    genres = [genre.text for genre in genre_elements if genre.text]
    tag_elements = root.findall('tag')
    tags = [tag.text for tag in tag_elements if tag.text]

    # Extracting actors
    actors = []
    for actor_elem in root.findall('actor'):
        name = actor_elem.findtext('name')
        role = actor_elem.findtext('role')
        thumb = actor_elem.findtext('thumb')
        if name:
            actors.append({'name': name, 'role': role, 'thumb': thumb})

    # --- HTML Generation ---
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - TV Show Details</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{title}</h1>
        <p class="originaltitle">Título Original: {originaltitle}</p>
        <p class="premiered">Premiered: {premiered}</p>
    </header>

    <main>
        <section class="folder">
            <img src="./folder.jpg" align="left">
        </section>
        <section class="overview">            
            <h2>Sinopse:</h2>
            <p>{plot}</p>
            <p><strong>Clasificação:</strong> {mpaa}</p>
            <p><strong>Estudios:</strong> {', '.join(studios) if studios else 'N/A'}</p>
            <p><strong>Gêneros:</strong> {', '.join(genres) if genres else 'N/A'}</p>
            <p><strong>Tags:</strong> {', '.join(tags) if tags else 'N/A'}</p>
        </section>
"""
    if actors:
        html_content += """
        <section class="cast">
            <h2>Elenco:</h2>
            <div class="actor-list">
        """
        for actor in actors:
            actor_image = f'<img src="{actor["thumb"]}" alt="{actor["name"]}" onerror="this.onerror=null;this.src=\'https://via.placeholder.com/50\';">' if actor["thumb"] else ''
            html_content += f"""
                <div class="actor">
                    {actor_image}
                    <p><strong>{actor['name']}</strong> as {actor['role']}</p>
                </div>
            """
        html_content += """
            </div>
        </section>
        """ 

    html_content += """
    </main>

    <footer>
        <p>&copy; 2025 TV Show Converter. Data parsed from NFO file.</p>
    </footer>
</body>
</html>
"""

    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Successfully converted '{nfo_filepath}' to '{output_filepath}'")
    except IOError as e:
        print(f"Error writing HTML file: {e}")

if __name__ == "__main__":
    # Create the dummy NFO file in the current directory
    nfo_filename = "tvshow.nfo"
    
    # Define input and output paths
    input_nfo_file = nfo_filename
    output_html_file = "tvshow_details.html"

    convert_nfo_to_html(input_nfo_file, output_html_file)

    # Clean up the dummy NFO file
    # os.remove(nfo_filename)