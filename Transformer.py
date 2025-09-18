from PIL import Image
import os

def enlarge_image(input_path, output_path, target_size=(1024*2, 1024*2)):
    # 원본 이미지 열기
    original_image = Image.open(input_path)
    
    # 원본 이미지의 크기 얻기
    original_width, original_height = original_image.size
    print(f"Original size: {original_width}x{original_height}")
    
    # 확대 배율 계산
    scale_factor = target_size[1] // original_width
    
    # 확대 이미지 생성
    enlarged_image = original_image.resize((original_width * scale_factor, original_height * scale_factor), Image.NEAREST)
    
    # 최종 이미지 크기 출력
    enlarged_width, enlarged_height = enlarged_image.size
    print(f"Enlarged size: {enlarged_width}x{enlarged_height}")
    
    # 이미지 저장
    enlarged_image.save(output_path, format='PNG')
    print(f"Image saved to {output_path}")


files = os.listdir(os.getcwd())
if '.DS_Store' in files:
    files.remove('.DS_Store')
files.remove('Transformer.py')
for i in files:
    enlarge_image(os.getcwd()+'/'+i,os.getcwd()+'/'+i)