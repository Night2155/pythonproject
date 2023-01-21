import requests
import json
import yt_dlp
from Video_data_txt_to_csv import read_all_file

def Download_video(Result, Video_Num, Video_Type):
    path = f'G:/audio_save/{Video_Type}/'   # 存放檔案路徑 範例 : 主目錄:/資料夾1/資料夾2/{Video_Type}
                                            # {Video_Type} 不用動 這是MP4或WAV 所以不用更動
    if Video_Type == "wav":
        for i in range(Video_Num):
            youtube_url = "https://www.youtube.com/watch?v=" + Result["Video_ID (" + str(i + 1) + ")"] + "&ab_channel=" + \
                      Result["Channel_ID (" + str(i + 1) + ")"]

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{path}%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192'
                }],
                'postprocessor_args': [
                    '-ar', '16000'
                ],
                'prefer_ffmpeg': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(youtube_url, download=True)

    if Video_Type == "mp4":
        for i in range(Video_Num):
            youtube_url = "https://www.youtube.com/watch?v=" + Result["Video_ID (" + str(i + 1) + ")"] + "&ab_channel=" + \
                          Result["Channel_ID (" + str(i + 1) + ")"]
            ydl_opts1 = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
                'outtmpl': f'{path}%(title)s.%(ext)s',
                'prefer_ffmpeg': True,
                'ffmpeg_location': 'C:\\Users\\09765\\anaconda3\\envs\\pythonProject\\Scripts'  # 這裡要改 你的ffmpeg.exe的位置
            }
            with yt_dlp.YoutubeDL(ydl_opts1) as ydl:
                ydl.extract_info(youtube_url, download=True)


def Search_Video_Id(YT_Data_API, Video_Num, SearchKeyword, Video_Type):  # 搜尋頁面的影片標題、影片ID、頻道ID
    Search_path = "https://www.googleapis.com/youtube/v3/search?part=snippet&q=" + SearchKeyword + \
                  "&key=" + YT_Data_API + "&type=video&maxResults=" + str(Video_Num)

    video_info = {}  # 存放資訊到字典
    res = requests.get(url=Search_path)
    data_json = json.loads(res.text)
    # 這裡改成你的路徑
    f = open("G:/audio_save/" + SearchKeyword + "_Search" + Video_Type + ".json", "w", encoding='UTF-8')
    f.write(res.text)
    f.close()

    for i in range(Video_Num):
        video_info["Video_Title (" + str(i + 1) + ")"] = data_json['items'][i]['snippet']['title']
        print("第" + str(i + 1) + "部影片標題 :" + data_json['items'][i]['snippet']['title'])

        video_info["Video_ID (" + str(i + 1) + ")"] = data_json['items'][i]['id']['videoId']
        print("第" + str(i + 1) + "部影片 ID :" + data_json['items'][i]['id']['videoId'])

        video_info["Channel_ID (" + str(i + 1) + ")"] = data_json['items'][i]['snippet']['channelId']
        print("第" + str(i + 1) + "部頻道 ID :" + data_json['items'][i]['snippet']['channelId'])

    return video_info  # 回傳字典


def Write_Video_Info(Result, Video_Num, SearchKeyword, Video_Type):  # 寫入TXT
    f = open("G:/audio_save/" + SearchKeyword + "_Search"+Video_Type+".txt", "w", encoding='UTF-8')
    for i in range(Video_Num):
        f.write("Title : " + Result["Video_Title (" + str(i + 1) + ")"] + "\n")
        f.write("VideoID : " + Result["Video_ID (" + str(i + 1) + ")"] + "\n")
        f.write("ChannelID : " + Result["Channel_ID (" + str(i + 1) + ")"] + "\n\n")
    f.close()
    return 0


if __name__ == '__main__':
    print("請輸入關鍵字 : ")
    SearchKeyword = input()  # 搜尋關鍵字
    print("請輸入搜尋影片數量 : ")
    Video_Num = input()  # 影片數量
    Video_Type = 'mp4'  # 檔案類型
    Video_Type2 = 'wav'
    file_path = "G:/audio_save/" # 文字檔存放處
    YT_Data_API = 'AIzaSyAu5spE0yqJOO4fyUcM6MEwWzS2mbazlSA'  # Youtube_Data_API
    SearchVideo_Path = ('https://www.youtube.com/results?search_query=' + SearchKeyword)  # 搜尋頁面連結

    Result = Search_Video_Id(YT_Data_API, int(Video_Num), SearchKeyword, Video_Type)  # 抓取搜尋頁面資料
    Write_Video_Info(Result, int(Video_Num), SearchKeyword, Video_Type)  # 寫入txt檔
    # Download_video(Result, int(Video_Num), Video_Type)  # 下載函式 for MP4
    # Download_video(Result, int(Video_Num), Video_Type2)  # 下載函式 for WAV
    read_all_file(file_path)








