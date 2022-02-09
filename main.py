import extract_data
import get_vid_links
import download_vids
import backup_data
import helpers
import get_frames


def main():
    backup_data.main(do_backup=True)  # if true does a backup
    extract_data.main()
    get_vid_links.main(check_all=False)  # if ture it checks all links that are either empty or not up yet, if false
    # checks only empty links
    download_vids.main()
    helpers.update_vid_length()
    get_frames.main()


if __name__ == '__main__':
    main()
