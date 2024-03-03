from openai import OpenAI



class OpenAIWallpaperGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def generate_wallpaper(self, description, resolution):
        """
        Generates a wallpaper image based on the given description using OpenAI's API.

        :param resolution: Set the resolution for the generated image
        :param description: A string containing the description or keywords for the wallpaper.
        :return: The URL of the generated wallpaper image, or None if the API call fails.
        """
        try:
            response = self.client.images.generate(prompt=description,
            n=1,
            size=resolution)
            # Check if the response contains the generated images information
            if response.data:
                # Extracting the URL of the first generated image
                image_url = response.data[0].url
                return image_url
            else:
                print("No image was generated.")
                return None
        except Exception as e:  # Catching a general exception from the OpenAI library
            print(f"An error occurred while generating the wallpaper: {e}")
            return None
