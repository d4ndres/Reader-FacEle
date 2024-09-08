import base64
import cv2


def encode_image_fromPath(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
def encode_image(image):
  retval, buffer = cv2.imencode('.jpg', image)
  return base64.b64encode(buffer).decode('utf-8')


def OCR( client, img ):
  base64_image = encode_image(img)
  

  response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text", 
          "text": "Return the text from the image. Only return the text, not more."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
  max_tokens=300,)

  return response.choices[0].message.content

  # print(response.choices[0].message.content)

  # # write the response to a file
  # with open('table_data.json', 'w') as f:
  #   f.write(json.dumps(response.choices[0].message.content, indent=4))
  
  # print("Table data saved to table_data.json")

