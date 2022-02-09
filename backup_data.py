from get_vid_links import load_data
from os import path


def find_backup_index():
    index = 1
    while True:
        file_name = f'data\\backups\\past_meetings_data_backup{index}.txt'
        if path.exists(file_name) is False:
            return file_name
        index += 1


def save_data(data):
    file_path = find_backup_index()
    with open(file_path, 'w') as file:
        for meeting in data:
            line = '>'.join(meeting)
            if '\n' in line:
                file.write(line)
            else:
                file.write('>'.join(meeting) + "\n")


def main(do_backup):
    if do_backup is False:
        return
    data = load_data()
    save_data(data)
    print('Backup created')


if __name__ == '__main__':
    main(True)