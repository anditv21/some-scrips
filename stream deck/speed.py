from collections import Counter

def parse_speed_test_results(file_path):
    download_speeds = []
    upload_speeds = []
    servers = []

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if 'Server:' in line and 'Upload:' in line and 'Download:' in line:
                server_start = line.index('Server:') + len('Server: ')
                upload_start = line.index('Upload:')
                download_start = line.index('Download:')

                server_name = line[server_start:upload_start].strip()
                servers.append(server_name)

                upload_speed_str = line[upload_start + len('Upload:'):download_start].strip()
                upload_speed = float(upload_speed_str.replace('M', '').replace(',', '.'))

                download_speed_str = line[download_start + len('Download:'):].strip()
                if 'K' in download_speed_str:
                    download_speed = float(download_speed_str.replace('K', '').replace(',', '.')) / 1000
                else:
                    download_speed = float(download_speed_str.replace('M', '').replace(',', '.'))

                upload_speeds.append(upload_speed)
                download_speeds.append(download_speed)

    avg_download_speed = sum(download_speeds) / len(download_speeds)
    avg_upload_speed = sum(upload_speeds) / len(upload_speeds)
    most_common_server = Counter(servers).most_common(1)[0][0]

    return avg_download_speed, avg_upload_speed, most_common_server

file_path = 'speed.txt'
avg_download, avg_upload, most_used_server = parse_speed_test_results(file_path)

print(f"Average Download Speed: {avg_download:.2f} M")
print(f"Average Upload Speed: {avg_upload:.2f} M")
print(f"Most Used Server: {most_used_server}")
