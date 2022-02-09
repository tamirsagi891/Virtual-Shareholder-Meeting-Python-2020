#######################################################################################################################
# constants for extract_data

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
          'October', 'November', 'December']

MONTHS_TICKER = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

#######################################################################################################################
# constants for get_vid_link

# selenium chrome driver location and site url (also used for extract_data)
PATH = "chromedriver.exe"
URL = 'https://central.virtualshareholdermeeting.com/vsm/home'
G_DRIVE_PATH = 'G:\\My Drive\\VSM\\Videos\\'

# data array cell content
COMP_NAME = 0
MEETING_DATE = 1
MEETING_LINK = 2
COMP_TICKER = 3
VIDEO_STATUS = 4
VIDEO_LINK = 5
VIDEO_LENGTH = 6
NUMBER_OF_SLIDES = 7

NEED_TO_CHECK = ['EMPTY', 'EMPTY\n', 'NOT UP YET']

# register form x_paths and data
FIRST_NAME_XPATH = '//*[@id="root"]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[' \
                   '2]/div/div/div/div[1]/div/label/div/div/input '
LAST_NAME_XPATH = '//*[@id="root"]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[' \
                  '2]/div/div/div/div[2]/div/label/div/div/input '
EMAIL_XPATH = '//*[@id="root"]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[' \
              '3]/div/label/div/div/input '
REGISTER_BUTTON_XPATH = '//*[@id="root"]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[' \
                        '2]/div/button '

FIRST_NAME = 'Hebrew'
LAST_NAME = 'University'
EMAIL = 'filler@gmail.com'

FORM_NOT_FILLED = -1

# web page elements to choose action
REGISTRATION_XPATH = '//*[@id="root"]/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/h1'
MEETING_CONCLUDED_XPATH = '//*[@id="WaitingRoomDescription"]'
MEETING_CONCLUDED_TEXT = 'Thank you for joining. The meeting has now concluded.'
MEETING_NOT_UPLOADED_YET_TEXT = 'A replay may be available within 24 hours'
BROKEN_LINK_XPATH = '//*[@id="root"]/div/div[1]/div/div/div[1]/div[2]/div/div/div/div/div[1]/div/h2'
BROKEN_LINK_TEXT = 'Oops! Something went wrong.'
VID_MP4_XPATH = '//*[@id="root"]/div/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div/div[1]/div/div/video/source'
# elem.get_attribute('src') is the link to the vid
VID_BLOB_XPATH = '//*[@id="headerWelcomeTextContainer"]/div[2]/img'

XPATH_DICT = {REGISTRATION_XPATH: 1, MEETING_CONCLUDED_XPATH: 2, BROKEN_LINK_XPATH: 3,
              VID_MP4_XPATH: 4, VID_BLOB_XPATH: 5}
ACTION_DICT = {1: 'FILL FORM', 2: 'MEETING CONCLUDED', 3: 'BROKEN LINK', 4: 'MP4',
               5: 'VIDEO EXISTS', 6: 'PROBLEMATIC LINK'}

#######################################################################################################################

# constants for download_videos

CHUNK_SIZE = 256

#######################################################################################################################

# constants for get frames

BAD_FRAMES = ['data\\black_frames\\frame{}.jpg'.format(i) for i in range(6)]
