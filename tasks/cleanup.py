import os
from celery import shared_task

@shared_task
def cleanup_file(shared_dir, file_name):
    """특정 파일만 삭제하는 태스크"""
    try:
        file_path = os.path.join(shared_dir, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)  # 파일 삭제
            print(f"파일 삭제 완료: {file_path}")
        else:
            print(f"파일을 찾을 수 없음: {file_path}")
    except Exception as e:
        print(f"파일 삭제 실패: {e}")
        raise