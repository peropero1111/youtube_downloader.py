import sys
import os
import keyboard

try:
    import yt_dlp
except ImportError:
    print("오류: yt-dlp 라이브러리를 찾을 수 없습니다.", file=sys.stderr)
    print("터미널(cmd)에서 'pip install yt-dlp' 명령어로 먼저 설치해주세요.", file=sys.stderr)
    input("엔터 키를 눌러 프로그램을 종료하세요.")
    sys.exit(1)

def request_exit():
    print("\n미쿠다요")
    try:
        
        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN and event.name == 'y':
            print("프로그램을 종료합니다.")
            keyboard.unhook_all() 
            os._exit(0) 
        else:
            print("종료를 취소했습니다.")
    except Exception as e:
        print(f"키 입력 처리 중 오류 발생: {e}")

def download_channel_content(channel_url):
    """
    지정된 Youtube 채널의 모든 동영상과 숏츠를 다운로드함.
    성공 시 True, 실패 시 False를 반환.
    """
    try:

        print("채널 정보를 가져오는 중...")
        with yt_dlp.YoutubeDL({'quiet': True, 'ignoreerrors': True}) as ydl:
            info_dict = ydl.extract_info(channel_url, download=False)
            if not info_dict:
                print("오류: 채널 정보를 가져올 수 없거나 유효하지 않은 URL입니다. URL을 확인해주세요.", file=sys.stderr)
                return False

        uploader = info_dict.get('uploader', 'Unknown_Channel')
        output_template = os.path.join(uploader, '%(title)s [%(id)s].%(ext)s')
        output_path = os.path.abspath(uploader)

        ydl_opts = {
            'ignoreerrors': True,
            'download_archive': 'downloaded.txt',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output_template,
            'writethumbnail': True,
            'addmetadata': True,
            'progress_hooks': [print_progress],
            'extractor_args': {'youtube': {'client': 'mweb'}},
            'match_filter': "availability?!='subscriber_only' & availability?!='premium_only'",
        }

        print("--------------------------------------------------")
        print(f"다운로드를 시작합니다: {channel_url}")
        print("멤버십 전용 동영상은 자동으로 제외됩니다.")
        print(f"저장 폴더: {output_path}")
        print("이 작업은 채널의 동영상 수에 따라 매우 오래 걸릴 수 있습니다.")
        print("취소하려면 Ctrl+C를 누르세요.")
        print("--------------------------------------------------")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([channel_url])

        print("\n--------------------------------------------------")
        print("다운로드가 완료되었습니다!")
        print(f"파일은 다음 경로에 저장되었습니다: {output_path}")
        print("다운로드된 동영상 목록은 downloaded.txt 파일에서 확인할 수 있습니다.")
        print("--------------------------------------------------")
        return True

    except Exception as e:
        print(f"\n오류가 발생했습니다: {e}", file=sys.stderr)
        return False
    except KeyboardInterrupt:
        print("\n\n사용자에 의해 프로그램이 중단되었습니다.")
        sys.exit(0)

def print_progress(d):
    if d['status'] == 'downloading':
        progress_bar = d.get('_percent_str', 'N/A').strip()
        total_bytes = d.get('total_bytes_str', 'N/A').strip()
        speed = d.get('speed_str', 'N/A').strip()
        eta = d.get('eta_str', 'N/A').strip()
        filename = os.path.basename(d.get('filename', 'N/A'))
        
        sys.stdout.write(f"\r[다운로드 중] {filename} | {progress_bar} of {total_bytes} at {speed} (ETA: {eta})")
        sys.stdout.flush()
    elif d['status'] == 'finished':
        sys.stdout.write("\n")
        sys.stdout.flush()

if __name__ == "__main__":
    keyboard.add_hotkey('ctrl+m', request_exit)

    print("다운로드할 YouTube 채널의 전체 URL을 입력하세요.")
    channel_url_input = input("URL: ").strip()

    if not channel_url_input:
        print("URL이 입력되지 않았습니다.", file=sys.stderr)
    else:
        download_channel_content(channel_url_input)

    print("\n엔터 키를 눌러 프로그램을 종료하세요.")
    input()

    keyboard.unhook_all()
    
    
    """
    특정 영상만 선택 해서 주소 입력시 그 영상만 다운되는 기능 추가 하기
    """
