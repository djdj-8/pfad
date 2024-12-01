from flask import Flask, render_template, request, send_file, send_from_directory
from diffusers import AutoPipelineForImage2Image, LCMScheduler, AutoencoderTiny
import torch
from PIL import Image
import io
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# 初始化模型
pipe = AutoPipelineForImage2Image.from_pretrained("lykon/dreamshaper-8-lcm", torch_dtype=torch.float16)
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe.vae = AutoencoderTiny.from_pretrained("madebyollin/taesd").to(device="mps", dtype=torch.float16)

# 加载 LoRA 权重
lora_weights_path = "8bit.safetensors"
if not os.path.exists(lora_weights_path):
    print(f"LoRA weights file does not exist at: {lora_weights_path}")
else:
    print("LoRA weights file found.")
    try:
        pipe.load_lora_weights(lora_weights_path, "pixel")
        print("LoRA weights loaded successfully.")
    except Exception as e:
        print(f"Error loading LoRA weights: {e}")

pipe.set_adapters(["pixel"], adapter_weights=[1])
print("Adapters set successfully.")
pipe.to("mps")
pipe.unet.to(memory_format=torch.channels_last)

# 设置生成参数
prompt = "flat, pixar, 2d, character, design, concept, art, illustration, drawing, painting, digital"
negative_prompt = "realistic, portrait, photography, photo, human, face, people"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image_route():
    file = request.files['image']
    if file:
        try:
            # 将图像转换为PIL格式
            image = Image.open(io.BytesIO(file.read()))

            # 调整图像尺寸以匹配模型期望的尺寸
            image = image.resize((64, 64))

            # 生成像素风格的图片
            generator = torch.manual_seed(0)
            output_image = pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                image=image,
                num_inference_steps=8,
                generator=generator,
                strength=0.7,
                guidance_scale=1.2
            ).images[0]

            # 将生成的图像转换为字节流
            buffered = io.BytesIO()
            output_image.save(buffered, format="PNG")
            buffered.seek(0)

            # 发送给客户端
            return send_file(io.BytesIO(buffered.getvalue()), mimetype='image/png', as_attachment=True, download_name='pixar_style_output.png')
        except Exception as e:
            print(f"Error processing image: {e}")
            return str(e), 500
    return "Error: No image provided", 400

@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)