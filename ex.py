search_text_start = "geometry"
search_text_end = "</geometry>"
file_path = "kinematic_mockup2.dae"
result = [] # 결과를 저장할 리스트

# 결과를 저장할 딕셔너리 초기화
result_dict = {}

end=[]
end_search_start_text = "library_visual_scenes"
end_search_end_text = "/library_visual_scenes"

with open(file_path, "r") as f:
    # 파일의 모든 라인을 읽어서 순회하면서 시작 텍스트가 있는지 확인합니다.
    for line in f:
        if end_search_start_text in line:
            # 시작 텍스트가 있으면 라인을 결과 리스트에 추가합니다.
            end.append(line)
            # 끝 텍스트가 나올 때까지 결과 리스트에 라인을 추가합니다.
            for line in f:
                end.append(line)
                if end_search_end_text in line:
                    break

end_len = len(end)

start=[]
start.append('<?xml version="1.0" encoding="utf-8"?>\n')
start.append('<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">')
start.append('<library_geometries>')

with open(file_path, "r") as f:
    current_key = None
    current_result = []
    
    # 파일의 모든 라인을 읽어서 순회하면서 시작 텍스트가 있는지 확인합니다.
    for line in f:
        if search_text_start in line:
            # 이전 결과가 있는 경우, 딕셔너리에 저장합니다.
            if current_key is not None:
                current_result.append('</library_geometries>\n')
                for n in range(0, end_len - 1):
                    current_result.append(f"{end[n]}")
                result_dict[current_key] = current_result
            
            # 새로운 파일명으로 저장하기 위해 시작 텍스트 다음 문자열을 가져옵니다.
            
            current_key = line.split("geometry")[1].strip() + ".dae"
            # 새로운 결과를 저장하기 위해 리스트를 초기화합니다.
            current_result = [f"{start[0]}\n", f"{start[1]}\n", f"{start[2]}", line]
            # 끝 텍스트가 나올 때까지 결과 리스트에 라인을 추가합니다.
            for line in f:
                current_result.append(line)
                if search_text_end in line:
                    break
    
    # 마지막 결과가 있으면, 딕셔너리에 저장합니다.
    if current_key is not None:
        current_result.append(f"\n{search_text_end}\n")
        result_dict[current_key] = current_result

# 결과를 파일로 저장합니다.
for key, result in result_dict.items():
    with open(key, "w") as f_out:
        f_out.writelines(result)
        